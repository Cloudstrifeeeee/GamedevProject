import random # we import random so we can roll dice, pick random enemies, and generate random numbers throughout the game

# these are shortcuts for terminal color codes so we don't have to type the long escape codes every time
# \033[ is the start of an ANSI escape code, the number picks the color, m ends it
R, G, Y, C, W = "\033[31m", "\033[32m", "\033[33m", "\033[36m", "\033[37m"
B, RESET = "\033[1m", "\033[0m" # B makes text bold, RESET turns all formatting off

# prints the game title using box-drawing characters to make it look fancy in the terminal
print(f"{R}{B}╔══════════════════════════════════════════════════════╗")
print("║                HADES' LABYRINTH                      ║")
print(f"╚══════════════════════════════════════════════════════╝{RESET}")

pname = input("Enter your name HERO :") # input() pauses the game and waits for the player to type something, then saves it to pname

# this is a dictionary — think of it like a filing cabinet with labeled folders
# the key (like "1") opens that folder and inside is another dictionary with all that class's stats
# "cast" is how many spell slots (skill uses) the class starts with
classes = {
    "1": {"class": "Dictator", "hp": 150, "attack": 20, "defense": 15, "skill": "Absolute Decree", "cast": 6},
    "2": {"class": "Cop",      "hp": 80,  "attack": 30, "defense": 5,  "skill": "Police Brutality", "cast": 5},
    "3": {"class": "Fixer",    "hp": 100, "attack": 25, "defense": 10, "skill": "Loophole Stab",    "cast": 7},
    "4": {"class": "Nepotist", "hp": 90,  "attack": 25, "defense": 5,  "skill": "Inherited Blow",   "cast": 4}
}

print(f"\n{Y}Please choose your background (cannot be changed till the end!){RESET}") # \n adds a blank line before this text
print(f"{C}┌──────────────────────────────────────────────────────┐")
print("│  (1) DICTATOR   (2) COP   (3) FIXER   (4) NEPOTIST   │")
print(f"└──────────────────────────────────────────────────────┘{RESET}")

player = None # we set this to None (meaning empty/nothing) so the while loop below knows to keep asking

# while loops keep running as long as the condition is True
# "while player is None" means: keep looping until player has an actual value
while player is None:
    choice = input(f"{B}Selection > {RESET}") # waits for the player to type a number

    player = classes.get(choice) # .get() looks up a key in the dictionary, returns None if the key doesn't exist
    if not player: # "not player" is True when player is None (falsy), meaning bad input was given
        print(f"{R}Invalid choice. Please select 1, 2, 3, or 4.{RESET}")

# these variables track the player's progress throughout the whole game
level = 1           # what level the player is — goes up when exp hits the threshold
exp = 0             # experience points earned from killing monsters
current_hp = player['hp'] # current_hp can go up and down in battle; player['hp'] is the max
section = 0
room = 1            # which room of the labyrinth the player is in
game_running = True # boolean flag — when this becomes False the main loop stops and the game ends
max_hp = current_hp # saves the starting max hp for reference (not actively used but good to have)
current_slot = player['cast'] # how many skill uses the player currently has left

hero_gold = 0       # how much gold the player has to spend in the shop
inventory = []      # a list that holds the names of every item the player is carrying
equipped = {"weapon": None, "armor": None} # a dict tracking what's in each equipment slot, None means empty

# this big dictionary defines every item in the game
# the item name is the key (used everywhere to look up data)
# "type" controls how an item behaves: "weapon"/"armor" = equippable, "consumable" = used up on use
sample_items = {

    # ===== WEAPONS (go in the weapon slot, add attack) =====

    "Minotaur's Horns +13 atk": {
        "price": 75,     # how much it costs to buy from the shop
        "attack": 13,    # +13 to the player's attack stat when equipped
        "defense": 0,    # no defense bonus from this weapon
        "hp": 0,         # no hp bonus
        "cast": 0,       # no spell slot bonus
        "type": "weapon" # goes in the weapon slot (only one weapon can be equipped at a time)
    },

    "Harpe of Cronos +30 atk": { # the curved blade Perseus used to slay Medusa
        "price": 175,
        "attack": 30,    # very high attack for a shop weapon
        "defense": 0,
        "hp": 0,
        "cast": 3,       # also restores 3 spell slots when equipped, because it's a divine weapon
        "type": "weapon"
    },

    "Ares' Spear +20 atk": { # the war god's weapon, solid mid-tier option
        "price": 120,
        "attack": 20,
        "defense": 5,    # spear has a little reach so it gives a small defense bonus too
        "hp": 0,
        "cast": 0,
        "type": "weapon"
    },

    "Sword of Damocles +18 atk": { # the famous sword that hung by a thread over a king's head
        "price": 95,
        "attack": 18,
        "defense": 0,
        "hp": 0,
        "cast": 2,       # the danger of the sword sharpens your mind, giving 2 extra spell slots
        "type": "weapon"
    },

    "Wrath of Zeus +40 atk": { # the legendary thunder weapon, most powerful in the game
        "price": 250,
        "attack": 40,    # highest attack of any weapon
        "defense": 0,
        "hp": 0,
        "cast": 5,       # also gives +5 spell slots — worth saving up for
        "type": "weapon"
    },

    # ===== ARMOR (go in the armor slot, add defense or hp) =====

    "Nemean Lion's Pelt +10 def": { # the indestructible hide Heracles wore after killing the lion
        "price": 100,
        "attack": 0,
        "defense": 10,   # +10 defense, reduces damage from every monster hit
        "hp": 0,
        "cast": 0,
        "type": "armor"  # goes in the armor slot
    },

    "Hermes' Sandals +8 def": { # the winged sandals of the messenger god
        "price": 60,
        "attack": 0,
        "defense": 8,    # lighter defense bonus but cheaper
        "hp": 15,        # also adds 15 max hp because you can dodge better
        "cast": 0,
        "type": "armor"
    },

    "The Aegis +17 def": { # Zeus's divine shield, best armor in the game
        "price": 170,
        "attack": 0,
        "defense": 17,   # highest defense of any item
        "hp": 10,        # also adds a chunk of max hp
        "cast": 0,
        "type": "armor"
    },

    "Hephaestus' Plate +12 def": { # forged by the smith god himself
        "price": 130,
        "attack": 0,
        "defense": 12,
        "hp": 20,        # sturdy armor gives more hp than most
        "cast": 0,
        "type": "armor"
    },

    # ===== CONSUMABLES (disappear from inventory when used) =====

    "Apollo's Lyre +30 hp": { # Apollo's music soothes wounds, restores 30 hp
        "price": 30,
        "attack": 0,
        "defense": 0,
        "hp": 30,            # adds 30 to current_hp when used (capped at max hp)
        "cast": 0,
        "type": "consumable" # consumed on use — it's removed from inventory after
    },

    "Restora +hp and +mp": { # the food of the gods, restores a huge amount of both resources
        "price": 50,
        "attack": 0,
        "defense": 0,
        "hp": 200,       # restores 200 hp (likely fills you to max)
        "cast": 4,       # also restores 4 spell slots
        "type": "consumable"
    },

    "Nectar of the Gods +50 hp": { # the drink of the gods, strong single-use heal
        "price": 45,
        "attack": 0,
        "defense": 0,
        "hp": 50,        # restores 50 hp in one use
        "cast": 0,
        "type": "consumable"
    },

    "Phoenix Ashes": { # the only item that can revive you from death
        "price": 300,    # very expensive to buy but worth it as a safety net
        "attack": 0,
        "defense": 0,
        "hp": 9999,      # restores effectively all hp (capped to max by min() in use_consumable)
        "cast": 3,       # also recharges 3 spell slots on use
        "type": "consumable"
    },

}

# prints a summary of what the player chose before the game begins
print(f"\nYou selected: {player['class']} class")
print(f"HP: {player['hp']}, Attack: {player['attack']}, Defense: {player['defense']}")
print(f"Special skill: {player['skill']} | Spell Slots: {current_slot}")
print("now you're all set, let's begin your journey")
print("=" * 56) # "=" * 56 repeats the = character 56 times to make a divider line


def venture(): # defining a function — this block of code runs whenever we call venture() later
    # a list of tuples — each tuple has (event text, percent chance)
    # all chances add up to 100 so every roll hits something
    events = [
        ("A monster have appeared!", 45),
        ("A merchant appeared!", 20),
        ("You found something useful!", 15),
        ("You triggered a trap!", 15),
        ("An ominous enemy have appeared", 5),
    ]

    roll = random.randint(1, 100) # randint(1, 100) picks a whole number from 1 to 100 inclusive
    total = 0 # we start a running total at 0 and add each event's chance one by one

    for event, chance in events: # "for x, y in list" unpacks each tuple into two variables at once
        total += chance           # += means total = total + chance (shorthand addition)
        if roll <= total:         # if the roll landed within this event's range, it triggered
            print(f"\n{event}")   # f-strings let us put variables inside strings using {}
            return event          # return sends a value back to whoever called this function and exits it

    return "nothing" # this line only runs if somehow no event matched (shouldn't happen with 100% coverage)


def shop(): # the shop function handles buying and selling
    global hero_gold, inventory # global means we're using the hero_gold and inventory from OUTSIDE this function
                                 # without global, changes inside here wouldn't affect the real variables

    while True: # infinite loop — "True" never becomes False so it loops until we hit a break statement
        print(f"\n{Y}════════════════════ MERCHANT SHOP ════════════════════{RESET}")
        print("Gold:", hero_gold)

        item_list = list(sample_items.items()) # .items() gives us pairs of (key, value) from the dict
                                               # list() converts that into an actual list we can index by number

        for i, (item, data) in enumerate(item_list, start=1): # enumerate() adds a counter (i) to each item
                                                               # start=1 makes it count from 1 instead of 0
            print(f"{i}. {item} - {data['price']} gold")

        print("------------------------------------------------------")
        print("(0) Sell")
        print("(14) Exit Shop")

        choice = input("Choose item: ")

        if choice == "14":
            print("Leaving shop...")
            break # break exits the nearest while loop immediately

        elif choice == "0": # selling branch
            if len(inventory) == 0: # len() returns how many items are in the list
                print("\033[0;31mThere is nothing to sell, your inventory is empty!\033[0m")

            else:
                print("\n===== SELL ITEMS =====")

                for i, item in enumerate(inventory, start=1):
                    sell_price = sample_items[item]["price"] # looks up this item's price using its name as a key
                    print(f"{i}. {item} -> sell for {sell_price} gold")

                print("--------------------------")
                print("0. Exit")

                sell_choice = input("Choose an item you want to sell: ")

                if sell_choice == "0":
                    print("Exiting...")

                elif sell_choice.isdigit(): # .isdigit() returns True if every character is a digit (0-9)
                    index = int(sell_choice) - 1 # int() converts the string "2" into the number 2
                                                  # we subtract 1 because lists are 0-indexed (first item is index 0)

                    if 0 <= index < len(inventory): # checks the index is in a valid range
                        item_name = inventory[index]
                        sell_price = sample_items[item_name]["price"]

                        print("------------------------------------------------")
                        confirm = input(f"\033[0;32mSell {item_name} for\033[0m \033[0;33m{sell_price} gold\033[0m\033[0;32m? (y/n):\033[0m ")

                        if confirm.lower() == "y": # .lower() converts any uppercase letters to lowercase first
                            if equipped.get(sample_items[item_name]["type"]) == item_name:
                                equip_item(item_name) # calls equip_item() to remove the stat bonuses before selling
                            inventory.pop(index)  # .pop(index) removes the item at that position from the list
                            hero_gold += sell_price
                            print("------------------------------------------------")
                            print(f"\033[0;33mYou sold {item_name} for {sell_price} gold!\033[0m")
                        else:
                            print("\033[0;31mCancelled.\033[0m")
                    else:
                        print("Invalid choice.")
                else:
                    print("Enter numbers only.")

        elif choice.isdigit(): # buying branch
            index = int(choice) - 1

            if 0 <= index < len(item_list):
                item_name, item_data = item_list[index] # unpacks the (name, data) tuple at that index

                if hero_gold >= item_data["price"]:
                    hero_gold -= item_data["price"]
                    inventory.append(item_name) # .append() adds the item to the END of the list
                    print(f"You bought {item_name}!")
                    print(f"Go to inventory to equip or use it.")
                else:
                    print("Not enough gold!")
            else:
                print("Invalid choice")
        else:
            print("Enter numbers only")


def equip_item(item_name): # handles equipping and unequipping gear
    global equipped # we need global so changes to equipped persist after the function ends

    item = sample_items[item_name]  # fetches this item's stat block from the dictionary
    slot = item["type"]             # gets "weapon" or "armor" — decides which slot to put it in

    if equipped[slot] == item_name: # if this exact item is already in that slot, we're unequipping it
        equipped[slot] = None       # None means the slot is now empty
        player["attack"]  -= item.get("attack",  0) # .get("key", default) safely reads a key, returns 0 if missing
        player["defense"] -= item.get("defense", 0) # -= subtracts and updates the value in one step
        player["hp"]      -= item.get("hp",      0)
        player["cast"]    -= item.get("cast",     0)
        print(f"\nUnequipped {item_name}!")

    else: # equipping a new item
        if equipped[slot]: # if the slot already has something in it, unequip the old thing first
            old = sample_items[equipped[slot]] # looks up the old item's stats
            player["attack"]  -= old.get("attack",  0)
            player["defense"] -= old.get("defense", 0)
            player["hp"]      -= old.get("hp",      0)
            player["cast"]    -= old.get("cast",     0)
            print(f"Unequipped {equipped[slot]}!")

        equipped[slot] = item_name           # records the new item as the equipped one
        player["attack"]  += item.get("attack",  0) # += adds the new item's bonuses to the player's stats
        player["defense"] += item.get("defense", 0)
        player["hp"]      += item.get("hp",      0)
        player["cast"]    += item.get("cast",     0)
        print(f"\nEquipped {item_name}!")


def use_consumable(item_name): # handles using a consumable item from inventory
    global current_hp, current_slot, inventory # globals needed to modify these outside-scope variables

    item = sample_items[item_name]
    current_hp   = min(current_hp   + item["hp"],           player["hp"])    # min() picks the SMALLER of two values
    current_slot = min(current_slot + item.get("cast", 0),  player["cast"])  # so we never go above the player's max
    inventory.remove(item_name) # .remove() finds the first matching item in the list and deletes it
    print(f"\nUsed {item_name}! HP restored to {current_hp}/{player['hp']}")


def attempt_revive(): # checks if the player has a revive item and asks if they want to use it
    global current_hp, current_slot, inventory # need these globals to actually perform the revival

    if "Phoenix Ashes" in inventory: # "in" checks if a value exists anywhere in the list
        print(f"\n{Y}══════════════════════════════════════════════════════")
        print("  You feel a warmth in your satchel...")
        print("  An Phoenix Ashes glows faintly.")
        print(f"══════════════════════════════════════════════════════{RESET}")
        choice = input("Use the Phoenix Ashes to revive? (y/n): ")

        if choice.lower() == "y":
            inventory.remove("Phoenix Ashes") # removes it from inventory — one use only
            item = sample_items["Phoenix Ashes"] # gets the item's stats
            current_hp   = min(item["hp"],          player["hp"]) # restores hp fully (9999 capped to max)
            current_slot = min(current_slot + item.get("cast", 0), player["cast"]) # restores some spell slots
            print(f"\n{G}The elixir surges through your veins!")
            print(f"You have been revived! HP: {current_hp}/{player['hp']}{RESET}")
            return True # True means the revival happened, the fight should continue or restart
        else:
            print(f"{R}You chose not to drink it. Your journey ends here.{RESET}")
            return False # False means the player declined, game over

    return False # False means no elixir was found, game over as normal


def attack_monster(monster_hp, player_atk): # reduces the monster's hp by the player's attack
    monster_hp -= player_atk # -= subtracts player_atk from monster_hp and saves the result
    if monster_hp < 0: # clamp to 0 so hp never shows as negative
        monster_hp = 0
    print(f"You dealt {player_atk} damage!")
    return monster_hp # return sends the new value back to wherever attack_monster was called


def attack_player(player_hp, monster_atk, player_defense): # reduces player hp after monster attacks
    damage = monster_atk - player_defense # defense directly reduces the hit — higher defense = less damage
    if damage < 1: # monsters always do at least 1 damage so defense can't make you invincible
        damage = 1
    player_hp -= damage
    if player_hp < 0:
        player_hp = 0
    print(f"The monster dealt {damage} damage!")
    return player_hp


def monster_use_skill(monster_name, monster_hp, monster_atk, monster_skill): # handles enemy special moves
    global current_hp, current_slot # need these to deal damage to the player or drain their slots

    print(f"\n{R}The {monster_name} used {monster_skill}!{RESET}")

    if monster_skill == "Claw Swipe": # two rapid scratches — used by early monsters
        hit1 = max(1, monster_atk - player["defense"])         # first hit reduced by defense, at least 1
        hit2 = max(1, (monster_atk // 2) - player["defense"]) # second hit uses half attack, also at least 1
        # // is integer division — drops the decimal, so 7 // 2 = 3 not 3.5
        total = hit1 + hit2
        current_hp -= total
        if current_hp < 0:
            current_hp = 0
        print(f"{R}Two slashes! You took {hit1} + {hit2} = {total} damage!{RESET}")

    elif monster_skill == "Flare": # magic fire burst that ignores armor completely
        damage = monster_atk # no defense subtraction — raw damage goes straight through
        current_hp -= damage
        if current_hp < 0:
            current_hp = 0
        print(f"{R}Burns through your armor! You took {damage} damage!{RESET}")

    elif monster_skill == "Spectral Drain": # hits the player AND heals the monster at the same time
        heal   = monster_atk // 2 # heals for half the monster's attack stat
        monster_hp += heal         # adds hp to the monster
        damage = max(1, monster_atk - player["defense"])
        current_hp -= damage
        if current_hp < 0:
            current_hp = 0
        print(f"{R}Drained your life! You took {damage} damage and the enemy healed {heal} HP!{RESET}")

    elif monster_skill == "Savage Bite": # massive single chomp — very high damage
        damage = max(1, (monster_atk * 2) - player["defense"]) # multiplies attack by 2 before defense reduction
        current_hp -= damage
        if current_hp < 0:
            current_hp = 0
        print(f"{R}Massive bite! You took {damage} damage!{RESET}")

    elif monster_skill == "Dark Slash": # powerful late-game slash with a flat damage bonus
        damage = max(1, monster_atk + 10 - player["defense"]) # +10 is added to attack before defense reduces it
        current_hp -= damage
        if current_hp < 0:
            current_hp = 0
        print(f"{R}A powerful dark strike! You took {damage} damage!{RESET}")

    elif monster_skill == "Soul Rend": # hits AND permanently reduces the player's max hp
        damage = max(1, monster_atk - player["defense"])
        current_hp -= damage
        if current_hp < 0:
            current_hp = 0
        player["hp"] -= 20 # this directly modifies max hp in the player dict — the loss is permanent this fight
        print(f"{R}Your soul was sapped! You took {damage} damage and lost 20 max HP!{RESET}")

    elif monster_skill == "Ferocious Maw": # three-bite combo used by Cerberus, drains spell slots too
        hit1 = max(1, monster_atk         - player["defense"]) # first bite — normal damage
        hit2 = max(1, (monster_atk + 10)  - player["defense"]) # second bite — +10 bonus
        hit3 = max(1, (monster_atk + 15)  - player["defense"]) # third bite — +15 bonus
        total = hit1 + hit2 + hit3 # sum all three hits
        current_hp -= total
        if current_hp < 0:
            current_hp = 0
        current_slot -= 5  # drains 5 spell slots — can leave you unable to use skills
        if current_slot < 0: # spell slots can't go below 0
            current_slot = 0
        print(f"{R}Three Massive Bites! You took {hit1} + {hit2} + {hit3} = {total} damage and lost 5 spell slots!{RESET}")

    elif monster_skill == "Hellfire": # Cerberus second phase fire — deals 30% of your MAX hp as damage
        damage = int(0.3 * player["hp"]) # int() rounds down to a whole number since we can't have half hp
                                          # 0.3 * max_hp means the damage scales with how much hp you have
        current_hp -= damage
        if current_hp < 0:
            current_hp = 0
        print(f"{R}Cerberus breathes hellfire! You took {damage} damage!{RESET}")

    elif monster_skill == "Shadow Stab": # Hades phase 1 — hits AND heals Hades AND reduces your max hp
        damage  = max(1, monster_atk - player["defense"])
        recover = monster_atk // 2 # Hades heals for half his attack
        monster_hp += recover       # heals the boss
        current_hp -= damage
        if current_hp < 0:
            current_hp = 0
        player["hp"] -= 10 # permanently cuts 10 from your max hp — Hades is draining your life force
        print(f"{R}Hades stabs from the shadows! You took {damage} damage, lost 10 max HP, and Hades healed {recover} HP!{RESET}")

    elif monster_skill == "Wrath of Tartarus": # Hades phase 2 ultimate — drains hp, slots, and heals Hades
        damage  = max(1, monster_atk - player["defense"])
        recover = monster_atk // 3   # heals Hades for a third of his attack
        drain   = max(1, monster_atk // 15) # drains this many spell slots from the player
        current_slot -= drain
        if current_slot < 0:
            current_slot = 0
        monster_hp += recover
        current_hp -= damage
        if current_hp < 0:
            current_hp = 0
        player["hp"] -= 10
        print(f"{R}The Wrath of Tartarus erupts! You took {damage} damage, lost {drain} spell slots, lost 10 max HP, and Hades healed {recover} HP!{RESET}")

    return monster_hp # always return monster_hp because some skills changed it (heals)


def use_skill(monster_hp, monster_atk): # player's class skill — uses a spell slot and does something powerful
    global current_hp, current_slot

    if current_slot <= 0: # <= 0 means zero or somehow negative — either way no slots left
        print(f"\n{Y}No spell slots remaining! Level up to recharge.{RESET}")
        return monster_hp # returns hp unchanged so the monster doesn't take damage from a failed skill

    current_slot -= 1 # uses one slot before the skill fires
    skill = player["skill"]
    print(f"\n{G}You used {skill}! (Slots left: {current_slot}){RESET}")

    if skill == "Absolute Decree":
        damage = player["attack"] * 4 # multiplies attack by 4 — dictator hits extremely hard with skill
        monster_hp -= damage
        print(f"{G}The enemy was crushed for {damage} damage!{RESET}")

    elif skill == "Police Brutality":
        damage = int(13 + (player["attack"] * 0.5 * level)) # scales with both attack stat and current level
        # int() drops the decimal so damage is always a clean whole number
        monster_hp -= damage
        print(f"{G}You shot the enemy for {damage} damage!{RESET}")

    elif skill == "Loophole Stab":
        multiplier = random.uniform(1.5, 3.0) # uniform() picks a decimal number between 1.5 and 3.0
        damage = int(player["attack"] * multiplier) # int() rounds the result down to a whole number
        monster_hp -= damage
        print(f"{G}Critical strike! {damage} damage dealt!{RESET}")

    elif skill == "Inherited Blow":
        damage = int(player["attack"] * (level * 0.7)) # damage scales with level — stronger each level up
        monster_hp -= damage
        heal = damage // 3 # heals for one third of the damage dealt — // is integer division (no decimals)
        current_hp += heal
        if current_hp > player["hp"]: # cap healing at max hp
            current_hp = player["hp"]
        print(f"{G}You dealt {damage} damage!")
        print(f"You recovered {heal} HP!{RESET}")

    if monster_hp < 0:
        monster_hp = 0

    return monster_hp


def fight(monster_name, hp, atk, exp_reward, gold_reward, lore,  monster_skill=None, drops=[]):
    # monster_skill=None means it's optional — if you don't pass one in, the monster has no special move
    # drops=[] means it's also optional — if you don't pass drops, the monster drops nothing
    global current_hp, exp, hero_gold, level, current_slot

    monster_hp = hp
    print(f"\nA {monster_name} appears!")
    print(f"Lore: {lore}")

    while monster_hp > 0 and current_hp > 0: # both sides are alive, so battle continues

        #MONSTER FLEE CHECK 
        # if player's attack alone is enough to one-shot what's left of the monster, it might run
        if player["attack"] >= monster_hp:
            if random.random() < 0.25: # random.random() gives a float from 0.0 to 1.0
                                        # < 0.25 means there's a 25% chance this triggers
                print(f"\n{Y}The {monster_name} is overwhelmed and flees!{RESET}")
                exp      += exp_reward  // 2 # // 2 gives half, rounded down — partial reward for a flee
                hero_gold += gold_reward // 2
                print(f"Gained {exp_reward // 2} EXP and {gold_reward // 2} gold from scaring it off!")
                return True # True = player "won" this encounter even though monster ran

        #PLAYER TURN
        print(f"\n{G}Your HP: {current_hp}/{player['hp']} | Spell Slots: {current_slot}/{player['cast']}{RESET}")
        print(f"{R}{monster_name} HP: {monster_hp}{RESET}")
        print("=" * 56)
        print("\nChoose action:")
        print("(1) Attack")
        print("(2) Skill")
        print("(3) Use Item")
        print("(4) Run")

        combat_choice = input("> ")
        print("-" * 56)

        if combat_choice == "1":
            monster_hp = attack_monster(monster_hp, player["attack"])

        elif combat_choice == "2":
            monster_hp = use_skill(monster_hp, atk)

        elif combat_choice == "3":
            # list comprehension — builds a new list containing only items whose type is "consumable"
            usable = [i for i in inventory if sample_items[i]["type"] == "consumable"]
            if not usable: # "not usable" is True when the list is empty
                print("No consumables in inventory!")
                continue # "continue" skips the rest of this loop iteration and jumps back to the while condition
            for i, item in enumerate(usable, start=1):
                print(f"{i}. {item}")
            pick = input("Choose item (0 to cancel): ")
            if pick.isdigit() and 0 < int(pick) <= len(usable):
                use_consumable(usable[int(pick) - 1]) # int(pick) - 1 converts to 0-based index
            else:
                print("Cancelled.")
                continue

        elif combat_choice == "4":
            if random.random() < 0.7: # 70% success rate for running away
                print("\nYou escaped successfully!")
                return True
            else:
                print(f"{R}You failed to escape! You're wide open!{RESET}")
                # no continue here — failed escape still lets monster attack this turn

        else:
            print("Invalid action!")
            continue

        print(f"{monster_name} HP: {monster_hp}")

        #MONSTER DEATH CHECK 
        if monster_hp <= 0:
            print(f"\n{G}You defeated the {monster_name}!{RESET}")
            exp       += exp_reward
            hero_gold += gold_reward
            print(f"Gained {exp_reward} EXP and {gold_reward} gold!")

            for drop_item, drop_chance in drops: # loops through each possible drop as a (item, chance) tuple
                if random.randint(1, 100) <= drop_chance: # rolls a number — if it's within the drop chance, item drops
                    inventory.append(drop_item)
                    print(f"{Y}The {monster_name} dropped: {drop_item}!{RESET}")

            if exp >= level * 110: # 110 exp per level is the threshold — scales up each level
                level += 1
                player['hp']      += 15
                player['attack']  += 5
                player['defense'] += 3
                current_hp   = player['hp']   # full heal on level up
                current_slot = player['cast'] # full slot recharge on level up
                print(f"\n{G}LEVEL UP! Now level {level}!")
                print(f"HP +15 | Attack +5 | Defense +3 | Spell slots recharged!{RESET}")
            return True

        #  MONSTER TURN 
        # randint(1, 100) <= 50 means 50% chance the monster uses its skill
        if monster_skill and random.randint(1, 100) <= 50:
            monster_hp = monster_use_skill(monster_name, monster_hp, atk, monster_skill)
        else:
            current_hp = attack_player(current_hp, atk, player["defense"])

        print(f"Your HP: {current_hp}")

        #PLAYER DEATH CHECK
        if current_hp <= 0:
            print(f"\n{R}You died...{RESET}")

            revived = attempt_revive() # calls the revive function — returns True if player used an elixir
            if revived:
                continue # continues the battle loop — player is back up
            else:
                return False # False = player lost this fight for real


# ENEMY DATAS
# each entry is a tuple: (name, hp, atk, exp, gold, drops_list, skill_name, monster_lore)
# drops_list is a list of tuples: (item_name, percent_chance_to_drop)

monsters_early = [
    ("Imp",     40,  20, 10, 20,
     "A mischievous demon born from stray curses and broken promises.\nIt feeds on fear and enjoys scratching heroes before fleeing into the shadows.",
     "Claw Swipe",
     [("Apollo's Lyre +30 hp", 35)]),

    ("Hellcat", 50,  25, 40, 25,
     "A demonic feline with burning eyes and molten claws.\nIt stalks silently through dungeon corridors, striking when prey least expects it.",
     "Claw Swipe",
     [("Apollo's Lyre +30 hp", 30)]),

    ("Harpies",   60,  30, 30, 35,
     "Harpies are winged spirits that punishes the guilty and leave only ruin in their wake.\nBorn from curses they serve as relentless agents of violent tribulations.",
     "Claw Swipe",
     [("Apollo's Lyre +30 hp", 25)]),

    ("Fiend",   70,  30, 30, 35,
     "A corrupted being forged from hatred and war.\nStronger than common demons, it delights in prolonged suffering and brutal combat.",
     "Flare",
     [("Apollo's Lyre +30 hp", 25), ("Minotaur's Horns +13 atk", 15)])
]

monsters_mid = [
    ("Demon",     90,  35, 50, 45,
     "A true inhabitant of the abyss.\nIts body radiates heat and malice, and every step leaves scorch marks on the floor.",
     "Flare",
     [("Apollo's Lyre +30 hp", 30), ("Nemean Lion's Pelt +10 def", 20)]),

    ("Wraith",    110, 30, 50, 55,
     "A restless spirit bound to the dungeon by regret and vengeance.\nWeapons pass through its form unless fueled by strong will and resolve.",
     "Spectral Drain",
     [("Apollo's Lyre +30 hp", 25), ("Minotaur's Horns +13 atk", 20)]),

    ("Hellhound", 130, 40, 55, 60,
     "A monstrous beast born from ashes.\nIts flaming breath and relentless pursuit make escape nearly impossible.",
     "Savage Bite",
     [("Nemean Lion's Pelt +10 def", 25), ("Harpe of Cronos +30 atk", 10)]),

    ("Empusa",    110, 40, 60, 75,
     "A seductive servant of Hades, the Empusa lures travelers with a beautiful facade before revealing her true form.\nShe feeds on the life force of the ambitious, leaving nothing behind but cold memories and bloodstained dust in the Labyrinth's halls.",
     "Spectral Drain",
     [("Apollo's Lyre +30 hp", 25), ("Minotaur's Horns +13 atk", 20)])
]

monsters_late = [
    ("Fallen Angel", 160, 80, 67, 80,
     "Once a divine warrior, now corrupted by pride and betrayal.\nIts radiant wings are stained black, and it fights with sorrowful fury.",
     "Dark Slash",
     [("Harpe of Cronos +30 atk", 20), ("Restora +hp and +mp", 15)]),

    ("Shade of Zagreus",  180, 89, 75, 90,
     "A spectral echo of a prince who once defied the underworld.\nClad in tattered robes with eyes like glowing embers, he relentlessly lashes out at any soul that dares to stand in his path.",
     "Dark Slash",
     [("Harpe of Cronos +30 atk", 25), ("Restora +hp and +mp", 20)]),

    ("Shade of Thanatos",  200, 80, 80, 100,
     "A silent, hooded apparition carrying a heavy scythe.\nThis shade manifests as a cold, flickering remnant of Death's own inevitability,\nharvesting the lingering regrets of those whose time in the Labyrinth has finally run out.",
     "Soul Rend",
     [("Restora +hp and +mp", 25), ("Harpe of Cronos +30 atk", 20)]),

    ("Erinys",  250, 85, 100, 100,
     "A winged enforcer of divine vengeance.\nThe Erinys stalks the deepest halls of the Labyrinth, drawn to the scent of unconfessed crimes,\nensuring that those who escaped justice above face it here.",
     "Soul Rend",
     [("Restora +hp and +mp", 25), ("Harpe of Cronos +30 atk", 20)])
]


#MAIN GAME LOOP 
# "and" means ALL three conditions must be True for the loop to keep going
while game_running and room <= 60 and current_hp > 0:
    print(f"\n{'='*24} ROOM {room} {'='*24}")
    print(f"    HP: {current_hp}/{player['hp']} | Level: {level} | EXP: {exp} | Slots: {current_slot}/{player['cast']}")
    print("Gold:", hero_gold)
    print("\nchoose your action")
    print("(1)Venture onward")
    print("(2)Item")
    print("(3)Bail")

    action = input("> ")
    print("-" * 56)

    if action == "1":
        result = venture() # calls venture() and saves whatever event string it returned

        if result == "A monster have appeared!":
            if room <= 20:
                print("")
                monsters = monsters_early
            elif room <= 40:
                monsters = monsters_mid
            else:
                monsters = monsters_late

            enemy = random.choice(monsters) # random.choice() picks a random item from the list
            # passes the 7 elements of the tuple in the order fight() expects them
            # note: drops is index [5] and skill is index [6] in the tuple
            fight_result = fight(enemy[0], enemy[1], enemy[2], enemy[3], enemy[4], enemy[5], enemy[6], enemy[7])

            if not fight_result: # "not False" is True — so this triggers when the player lost
                game_running = False
                break

        elif result == "You found something useful!":
            useful = [
                ("money",     52), # 52% chance
                ("potion",    45), # 45% chance
                ("rare_item",  3)  # 3% chance — easy to miss on a first run
            ]

            roll  = random.randint(1, 100)
            total = 0

            for item, chance in useful:
                total += chance
                if roll <= total:
                    if item == "money":
                        gold_found = random.randint(20, 50)
                        hero_gold += gold_found
                        print(f"\nFound {gold_found} gold!")
                    elif item == "potion":
                        inventory.append("Apollo's Lyre +30 hp")
                        print(f"\nFound Apollo's Lyre +30 hp! Added to inventory.")
                    elif item == "rare_item":
                        rare_drops = ["Wrath of Zeus +40 atk", "The Aegis +17 def"]
                        found = random.choice(rare_drops) # picks one of the two rare items at random
                        inventory.append(found)
                        print(f"\n{Y}✦ Something shimmers in the dark...{RESET}")
                        print(f"You found: {found}! Added to inventory.")
                    break # stops checking the rest of the list once an item is found

        elif result == "You triggered a trap!":
            trap_damage = random.randint(10, 25)
            current_hp -= trap_damage
            print(f"You take {trap_damage} damage!")

            if current_hp <= 0:
                print(f"\n{R}The trap was lethal...{RESET}")
                revived = attempt_revive() # even trap deaths can be survived with the elixir
                if not revived:
                    game_running = False

        elif result == "A merchant appeared!":
            print("\nA merchant appears!")
            shop()

        elif result == "An ominous enemy have appeared":
            # CERBERUS MINI-OPTIONAL-BOSS (3 sequential fights, one per head)
            # each head must be defeated in order — losing any head ends the encounter
            print(f"\n{R}The guardian of the underworld blocks your path!{RESET}")
            if player["hp"] <= 350: # warns under-leveled players
                print(f"{Y}This monster is out of your league, retreat is recommended!{RESET}")

            # HEAD 1
            print(f"\n{R}── CERBERUS: LEFT HEAD ──{RESET}")
            head1_result = fight("Cerberus - Left Head", 300, 71, 50, 100, "A monstrous three-headed guardian born from the depths of Tartarus.\nEven severed from the whole, each head fights with savage independence.", "Ferocious Maw")
            # fight() returns True if won, False if lost

            if not head1_result: # player died to head 1 — stop here
                game_running = False

            else:
                # HEAD 2  only runs if head 1 was beaten 
                print(f"\n{R}── CERBERUS: RIGHT HEAD ──{RESET}")
                head2_result = fight("Cerberus - Right Head", 200, 85, 50, 100, "The right head snarls with blind fury, snapping at anything that moves.\nIt fights harder knowing its brothers are watching.", "Ferocious Maw")

                if not head2_result: # player died to head 2
                    game_running = False

                else:
                    # HEAD 3 the middle head, strongest, uses fire that damages based on hp so it is a threat no matter what level
                    print(f"\n{R}── CERBERUS: MIDDLE HEAD (FINAL) ──{RESET}")
                    head3_result = fight("Cerberus - Middle Head", 400, 80, 100, 200, "The dominant head, commanding the other two. Its breath carries the fire of Tartarus itself.\nThis is the last thing most souls ever see.", "Hellfire")

                    if not head3_result: # player died to head 3
                        game_running = False
                    else:
                        print(f"\n{G}Cerberus collapses. The path forward is open.{RESET}")

    section += 1 # increments section count — happens after every venture result regardless of outcome

    if section == 3:
            room += 1
            section = 0
            print(f"You Made it to room {room}")
            if room == 1:
                print("=" * 55)
                print("\nAfter meeting their end in the mortal world, " \
                "\na powerful historical figure awakens in the Labyrinth, " \
                "\na torturous underworld realm designed by Hades to test and confine the cursed.")
            elif room == 21:
                print("=" * 55)
                print("To escape, they must fight through floors of nightmare creatures, " \
                "\nfueled by the hope that defeating Hades will collapse the realm "
                "\nand allow all imprisoned souls to be reincarnated.")
            elif room == 41:
                print("=" * 55)
                print("As he ascends, the resistance from the monsters grows more intense, " \
                "\nreflecting a domain that hungers to break the will of its prisoners.")

    if room > 60: # final boss check — triggers when the room counter exceeds the cap
            print("\nYou have reached the deepest part of the labyrinth!")
            print("\nThe sovereign of this labyrinth stands before you")
            print("=" * 55)
            print("Hades: You thought you could buy your way out of the grave?")
            print("Death is the only contract you cannot bribe your way out of.")
            print('Now, let\'s see what\'s left of you once we strip away your "hard work".')

            #  HADES PHASE 1 
            boss_result = fight("Hades", 500, 100, 500, 1000, "The sovereign of the underworld, clad in obsidian armor that drinks in all light.\nHe has watched countless souls crumble before him, and he expects the same from you.", "Shadow Stab")

            if boss_result == True: # == True is explicit — same as "if boss_result:" but clearer for two-phase bosses
                print("=" * 55)
                print(f"{R}Hades gets engulfed in hellfire{RESET}")
                print("Hades: ENOUGH!")

                #  HADES PHASE 2 
                Sboss_result = fight("Hades", 800, 200, 500, 1000, "Stripped of patience, Hades sheds his regal composure entirely.\nWhat stands before you now is not a king — it is the raw, furious will of death itself.", "Wrath of Tartarus")

                if Sboss_result == True:
                    print("=" * 55)
                    print("Hades' body burns in ashes as his crown is the onl thing left." \
                    "\nonly at the very end does he realize the weight of his victory, " \
                    "\nhe must choose between shattering the Labyrinth forever to start a new life"
                    "\nor ascending the throne himself to prevent a total cosmic collapse.")
                    
                    print("   Choose Your Fate: (1)Ascend / (2)Start A New   ")

                    answer = input("> ")
                    if answer == 2:
                        print("=" * 55)
                        print("The Labyrinth begins to disappear as the light engulfs everything")
                        print("congratulations, You successfully escaped the Labyrinth of Hades!")
                        game_running = False # sets flag to False so the while loop exits cleanly

                    elif answer == 1:
                        print("=" * 55)
                        print("The Labyrinth remains as you adore hades crown as if it was your own..." \
                        "\nStarting today you will be the one to rule this place..." \
                        "\nBut not for long, for hades will someday be back...")
                        print("congratulations, You successfully conquer the Labyrinth of Hades!")
                        game_running = False # sets flag to False so the while loop exits cleanly

            break # break exits the main while loop no matter what happened with Hades

    elif action == "2": # inventory screen
        print("\n--- INVENTORY ---")
        print(f"Weapon: {equipped['weapon'] or 'None'} | Armor: {equipped['armor'] or 'None'}")
        # "x or 'None'" returns x if x is truthy, otherwise returns the string 'None'
        if len(inventory) == 0:
            print("Nothing yet...")
        else:
            for i, item in enumerate(inventory, start=1):
                item_type    = sample_items[item]["type"]
                equipped_tag = "" # starts as an empty string — only changes if the item is equipped
                if item_type in ("weapon", "armor") and equipped[item_type] == item:
                    equipped_tag = " [EQUIPPED]" # this string gets added to the end of the item name
                print(f"{i}. {item}{equipped_tag}")

        print("\n(E) Equip/Unequip  (U) Use consumable  (D) Discard" \
        "\n"
        "\n                                       (0) Back")
        inv_choice = input("> ")

        if inv_choice.lower() == "e": # .lower() so E and e both work
            item_num = input("Choose item number to equip/unequip: ")
            if item_num.isdigit():
                idx = int(item_num) - 1
                if 0 <= idx < len(inventory):
                    item_name = inventory[idx]
                    if sample_items[item_name]["type"] in ("weapon", "armor"):
                        equip_item(item_name)
                    else:
                        print("That item is not equippable!")
                else:
                    print("Invalid choice.")

        elif inv_choice.lower() == "u":
            item_num = input("Choose item number to use: ")
            if item_num.isdigit():
                idx = int(item_num) - 1
                if 0 <= idx < len(inventory):
                    item_name = inventory[idx]
                    if sample_items[item_name]["type"] == "consumable":
                        use_consumable(item_name)
                    else:
                        print("That item can only be equipped, not consumed!")
                else:
                    print("Invalid choice.")
        
        elif inv_choice.lower() == "d":
            item_num = input("Choose item number to discard: ")
            if item_num.isdigit():
                idx = int(item_num) - 1
        
        # Check if the index exists in the list
                if 0 <= idx < len(inventory):
            # Remove the item and store its name to tell the player
                    removed_item = inventory.pop(idx)
                    print(f"You threw away the {removed_item}.")
                else:
                    print("Invalid choice.")
            else:
                print("Please enter a valid number.")

    elif action == "3":
        print("\nYou try to bail... but the labyrinth won't let you leave!")
        print("You must press onward!")
