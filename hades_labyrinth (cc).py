import random  # we need this to do anything "random" — rolling dice, picking enemies, coin flips, all of it lives here

# okay so these are just shortcuts for colors in the terminal
# your terminal understands these weird \033[ codes and turns them into actual colors
# instead of typing that ugly code every time, we just save them as single letters
R = "\033[31m"   # R for Red — used for damage, danger, enemy stuff
G = "\033[32m"   # G for Green — good things, healing, your HP bar
Y = "\033[33m"   # Y for Yellow — warnings, gold, loot notifications
C = "\033[36m"   # C for Cyan — menus and UI stuff
W = "\033[37m"   # W for White — just plain white text when you need it
B = "\033[1m"    # B for Bold — makes text thicc and loud
RESET = "\033[0m"  # this one's important — it turns OFF all the color/bold so text goes back to normal

# printing the title screen using box-drawing characters
# those ╔ ║ ╚ symbols are special Unicode characters that look like a box when lined up
print(f"{R}{B}╔══════════════════════════════════════════════════════╗")
print("║                HADES' LABYRINTH                      ║")
print(f"╚══════════════════════════════════════════════════════╝{RESET}")  # RESET at the end so everything after this is normal again

pname = input("Enter your name HERO :")  # input() stops the program and waits for the player to type — whatever they type gets saved in pname

# this is a dictionary — imagine it like a binder with tabs
# each tab (like "1") opens to another mini-binder with that class's stats inside
# "cast" is the number of spell slots that class gets — basically how many times they can use their special move
classes = {
    "1": {"class": "Dictator", "hp": 150, "attack": 20, "defense": 15, "skill": "Absolute Decree", "cast": 6},  # tanky, slower, hits hard with skill
    "2": {"class": "Cop",      "hp": 80,  "attack": 30, "defense": 5,  "skill": "Police Brutality", "cast": 5},  # glass cannon, attacks hit hard but dies fast
    "3": {"class": "Fixer",    "hp": 100, "attack": 25, "defense": 10, "skill": "Loophole Stab",    "cast": 7},  # balanced, most spell slots, good for beginners
    "4": {"class": "Nepotist", "hp": 90,  "attack": 25, "defense": 5,  "skill": "Inherited Blow",   "cast": 4}   # heals on skill use but low spell slots
}

print(f"\n{Y}Please choose your background (cannot be changed till the end!){RESET}")  # \n just adds an empty line above this so it doesn't look cramped
print(f"{C}┌──────────────────────────────────────────────────────┐")
print("│  (1) DICTATOR   (2) COP   (3) FIXER   (4) NEPOTIST   │")
print(f"└──────────────────────────────────────────────────────┘{RESET}")

player = None  # None basically means "nothing yet" — we use it as a placeholder until the player picks something valid

# this loop keeps running until the player picks a real class
# "while player is None" = keep looping as long as player is still empty
while player is None:
    choice = input(f"{B}Selection > {RESET}")  # ask the player to type 1, 2, 3, or 4

    player = classes.get(choice)  # .get() checks if that key exists in the dictionary — if they type "5" it just returns None
    if not player:  # "not player" is True when player is None — meaning they typed something wrong
        print(f"{R}Invalid choice. Please select 1, 2, 3, or 4.{RESET}")

# now we set up all the variables we'll track throughout the whole game
level = 1             # the player starts at level 1 — goes up as you earn EXP
exp = 0               # EXP starts at zero, you earn it by winning fights
current_hp = player['hp']   # current_hp is how much HP you have right now — starts equal to your class's max HP
section = 0           # tracks how many events have happened in the current room (resets every 3)
room = 1              # which room you're in — game ends at room 60 then boss
game_running = True   # this is like a light switch — when it's False, the main loop stops and the game ends
max_hp = current_hp   # saves your starting max HP for reference — useful if you want to show original stats
current_slot = player['cast']  # how many spell slots you have right now — starts at your class's max

hero_gold = 0      # your wallet — starts empty, earn gold by winning fights and finding treasure
inventory = []     # your bag — starts empty, items get added with .append() and removed with .remove() or .pop()
equipped = {"weapon": None, "armor": None}  # tracks what's in each gear slot — None means that slot is empty

# this is the master item catalog — every single item in the game is defined here
# the item's name is the key, and the value is another dictionary with all its stats
# "type" is super important — it tells the game whether to equip it or consume it
sample_items = {

    # ── WEAPONS ──────────────────────────────────────────────────────────────
    # weapons go in the weapon slot and boost your attack stat

    "Minotaur's Horns +13 atk": {
        "price": 75,      # costs 75 gold to buy from the merchant
        "attack": 13,     # gives you +13 attack while it's equipped
        "defense": 0,     # no defense bonus from this one
        "hp": 0,          # no HP bonus either
        "cast": 0,        # doesn't give extra spell slots
        "type": "weapon"  # this tells equip_item() to put it in the weapon slot
    },

    "Harpe of Cronos +30 atk": {  # the curved blade Perseus used to behead Medusa — pretty legendary
        "price": 175,
        "attack": 30,     # massive attack boost — one of the better weapons
        "defense": 0,
        "hp": 0,
        "cast": 3,        # bonus: also gives +3 spell slots because it's a divine artifact
        "type": "weapon"
    },

    "Ares' Spear +20 atk": {  # the war god's own spear — solid middle-of-the-road choice
        "price": 120,
        "attack": 20,
        "defense": 5,     # spears have reach so you get a small defense bonus too — nice
        "hp": 0,
        "cast": 0,
        "type": "weapon"
    },

    "Sword of Damocles +18 atk": {  # that famous sword hanging by a single hair over a king's head
        "price": 95,
        "attack": 18,
        "defense": 0,
        "hp": 0,
        "cast": 2,        # the constant danger keeps your mind sharp — 2 extra spell slots
        "type": "weapon"
    },

    "Wrath of Zeus +40 atk": {  # THE thunder weapon — most expensive and most powerful in the game
        "price": 250,
        "attack": 40,     # highest attack bonus of any weapon, period
        "defense": 0,
        "hp": 0,
        "cast": 5,        # also gives +5 spell slots — definitely worth saving up for
        "type": "weapon"
    },

    # ── ARMOR ─────────────────────────────────────────────────────────────────
    # armor goes in the armor slot and boosts defense or max HP

    "Nemean Lion's Pelt +10 def": {  # the hide from the lion Heracles killed — literally indestructible
        "price": 100,
        "attack": 0,
        "defense": 10,    # reduces incoming damage from every single enemy hit
        "hp": 0,
        "cast": 0,
        "type": "armor"   # goes in the armor slot — only one armor can be equipped at a time
    },

    "Hermes' Sandals +8 def": {  # the winged sandals of the messenger god — you dodge way better in these
        "price": 60,
        "attack": 0,
        "defense": 8,     # solid defense for the price
        "hp": 15,         # also boosts max HP because dodging means fewer hits land fully
        "cast": 0,
        "type": "armor"
    },

    "The Aegis +17 def": {  # Zeus's divine shield — the single best armor you can get
        "price": 170,
        "attack": 0,
        "defense": 17,    # highest defense bonus of any item in the game
        "hp": 10,         # also bumps your max HP a bit
        "cast": 0,
        "type": "armor"
    },

    "Hephaestus' Plate +12 def": {  # custom-forged by the god of the forge himself — very heavy, very sturdy
        "price": 130,
        "attack": 0,
        "defense": 12,
        "hp": 20,         # thick metal means more HP to burn through — biggest HP bonus in armor slot
        "cast": 0,
        "type": "armor"
    },

    # ── CONSUMABLES ───────────────────────────────────────────────────────────
    # consumables disappear from your inventory the moment you use them — one and done

    "Apollo's Lyre +30 hp": {  # Apollo's music literally heals you — restores 30 HP when used
        "price": 30,
        "attack": 0,
        "defense": 0,
        "hp": 30,              # adds 30 to your current HP — but won't go over your max
        "cast": 0,
        "type": "consumable"   # disappears from inventory after use — you can't re-use it
    },

    "Restora +hp and +mp": {  # basically ambrosia — the food of the gods heals almost everything
        "price": 50,
        "attack": 0,
        "defense": 0,
        "hp": 200,     # restores 200 HP — almost certainly fills you back to max
        "cast": 4,     # ALSO refills 4 spell slots — best all-around consumable
        "type": "consumable"
    },

    "Nectar of the Gods +50 hp": {  # the divine drink — strong heal in a single sip
        "price": 45,
        "attack": 0,
        "defense": 0,
        "hp": 50,      # restores 50 HP — better than the Lyre but pricier
        "cast": 0,
        "type": "consumable"
    },

    "Phoenix Ashes": {  # the only item that can bring you back from death — treat it like your life insurance
        "price": 300,   # super expensive but worth every gold coin as a safety net
        "attack": 0,
        "defense": 0,
        "hp": 9999,     # restores an absurd amount of HP — the min() in use_consumable caps it to your max anyway
        "cast": 3,      # also gives back 3 spell slots when you revive — nice bonus
        "type": "consumable"
    },
}

# show the player a quick summary of the class they picked before the game starts
print(f"\nYou selected: {player['class']} class")
print(f"HP: {player['hp']}, Attack: {player['attack']}, Defense: {player['defense']}")
print(f"Special skill: {player['skill']} | Spell Slots: {current_slot}")
print("now you're all set, let's begin your journey")
print("=" * 56)  # prints 56 equal signs in a row — makes a nice divider line between the setup and the game


# ─────────────────────────────────────────────────────────────────────────────
# FUNCTIONS — think of these as reusable machines. you build them once up here,
# then call them whenever you need them later in the game
# ─────────────────────────────────────────────────────────────────────────────

def venture():
    # this function picks a random event when you move forward in the labyrinth
    # it uses weighted chances so some events are rarer than others

    events = [
        ("A monster have appeared!",       45),  # 45% — most common, keeps combat frequent
        ("A merchant appeared!",           20),  # 20% — shop visits, nice but not too often
        ("You found something useful!",    15),  # 15% — free loot, always appreciated
        ("You triggered a trap!",          15),  # 15% — ouch, but fair
        ("An ominous enemy have appeared",  5),  # 5% — rare mini-boss, Cerberus encounter
    ]

    roll = random.randint(1, 100)  # picks a random number between 1 and 100 — like rolling a d100
    total = 0  # we'll use this as a running counter to figure out which event the roll landed in

    for event, chance in events:  # loops through each event — "event" gets the name, "chance" gets the number
        total += chance            # add this event's chance to our running total
        if roll <= total:          # if our roll is within the total so far, this event fired
            print(f"\n{event}")    # tell the player what happened
            return event           # send the event name back so the main loop knows what to do next

    return "nothing"  # fallback — mathematically shouldn't happen since chances add to 100, but just in case


def shop():
    # this whole function runs the merchant shop — buying, selling, browsing
    # global lets us read AND change these variables that live outside this function
    global hero_gold, inventory

    while True:  # keeps the shop open until the player chooses to leave — "True" never becomes False on its own
        print(f"\n{Y}════════════════════ MERCHANT SHOP ════════════════════{RESET}")
        print("Gold:", hero_gold)  # show how much gold they have before listing prices

        item_list = list(sample_items.items())  # .items() gives pairs of (item_name, item_data) — list() makes it indexable by number

        for i, (item, data) in enumerate(item_list, start=1):  # enumerate adds a counter — start=1 so we count from 1 not 0
            print(f"{i}. {item} - {data['price']} gold")       # show each item with its price

        print("------------------------------------------------------")
        print("(0) Sell")   # sell option
        print("(14) Exit Shop")  # leave option

        choice = input("Choose item: ")

        if choice == "14":
            print("Leaving shop...")
            break  # break jumps out of the while loop immediately — no more shopping

        elif choice == "0":
            # ── SELLING ──
            if len(inventory) == 0:  # len() counts how many items are in the list — 0 means empty
                print("\033[0;31mThere is nothing to sell, your inventory is empty!\033[0m")

            else:
                print("\n===== SELL ITEMS =====")

                for i, item in enumerate(inventory, start=1):
                    sell_price = sample_items[item]["price"]  # look up this item's price using its name as the key
                    print(f"{i}. {item} -> sell for {sell_price} gold")

                print("--------------------------")
                print("0. Exit")

                sell_choice = input("Choose an item you want to sell: ")

                if sell_choice == "0":
                    print("Exiting...")

                elif sell_choice.isdigit():  # .isdigit() checks every character is a number — blocks letters and symbols
                    index = int(sell_choice) - 1  # int() turns the string "2" into the actual number 2
                                                   # minus 1 because Python lists start at index 0, not 1

                    if 0 <= index < len(inventory):  # makes sure the number they typed actually points to a real item
                        item_name = inventory[index]
                        sell_price = sample_items[item_name]["price"]

                        print("------------------------------------------------")
                        confirm = input(f"\033[0;32mSell {item_name} for\033[0m \033[0;33m{sell_price} gold\033[0m\033[0;32m? (y/n):\033[0m ")

                        if confirm.lower() == "y":  # .lower() converts "Y" or "YES" to lowercase so both work
                            if equipped.get(sample_items[item_name]["type"]) == item_name:
                                equip_item(item_name)  # unequip it first so the stat bonuses get removed before we ditch it
                            inventory.pop(index)   # .pop(index) removes the item at that exact position and shifts everything over
                            hero_gold += sell_price
                            print("------------------------------------------------")
                            print(f"\033[0;33mYou sold {item_name} for {sell_price} gold!\033[0m")
                        else:
                            print("\033[0;31mCancelled.\033[0m")
                    else:
                        print("Invalid choice.")
                else:
                    print("Enter numbers only.")

        elif choice.isdigit():
            # ── BUYING ──
            index = int(choice) - 1  # convert to zero-based index

            if 0 <= index < len(item_list):
                item_name, item_data = item_list[index]  # unpack the tuple — item_name gets the name, item_data gets the stats

                if hero_gold >= item_data["price"]:    # can they afford it?
                    hero_gold -= item_data["price"]    # subtract the cost from their wallet
                    inventory.append(item_name)        # .append() drops the item into their bag
                    print(f"You bought {item_name}!")
                    print(f"Go to inventory to equip or use it.")
                else:
                    print("Not enough gold!")
            else:
                print("Invalid choice")
        else:
            print("Enter numbers only")


def equip_item(item_name):
    # handles putting on or taking off weapons and armor
    # we use global here because equipped is defined outside this function and we're changing it
    global equipped

    item = sample_items[item_name]  # grab this item's full stat block from the catalog
    slot = item["type"]             # "weapon" or "armor" — determines which slot to check

    if equipped[slot] == item_name:
        # this exact item is already equipped — so we're unequipping it
        equipped[slot] = None  # clear the slot — None means empty
        player["attack"]  -= item.get("attack",  0)  # .get("key", 0) returns the value or 0 if it doesn't exist — safe lookup
        player["defense"] -= item.get("defense", 0)  # -= means subtract and save — removes the bonus we added when we equipped it
        player["hp"]      -= item.get("hp",      0)
        player["cast"]    -= item.get("cast",     0)
        print(f"\nUnequipped {item_name}!")

    else:
        # equipping something new
        if equipped[slot]:  # if the slot already has something in it, strip the old item's bonuses first
            old = sample_items[equipped[slot]]  # look up the currently equipped item's stats
            player["attack"]  -= old.get("attack",  0)
            player["defense"] -= old.get("defense", 0)
            player["hp"]      -= old.get("hp",      0)
            player["cast"]    -= old.get("cast",     0)
            print(f"Unequipped {equipped[slot]}!")

        equipped[slot] = item_name          # record the new item as the equipped one
        player["attack"]  += item.get("attack",  0)   # += means add and save — apply the new item's bonuses
        player["defense"] += item.get("defense", 0)
        player["hp"]      += item.get("hp",      0)
        player["cast"]    += item.get("cast",     0)
        print(f"\nEquipped {item_name}!")


def use_consumable(item_name):
    # uses up a one-time-use item from your bag and applies its effects
    global current_hp, current_slot, inventory  # need these globals so changes here actually stick

    item = sample_items[item_name]
    current_hp   = min(current_hp + item["hp"], player["hp"])          # min() picks the smaller number — caps HP at max so you can't overheal
    current_slot = min(current_slot + item.get("cast", 0), player["cast"])  # same logic — spell slots can't go above your class max
    inventory.remove(item_name)  # .remove() finds the first match in the list and deletes it — item is gone for good
    print(f"\nUsed {item_name}! HP restored to {current_hp}/{player['hp']}")


def attempt_revive():
    # called when the player hits 0 HP — checks if Phoenix Ashes are in the bag and offers them
    global current_hp, current_slot, inventory

    if "Phoenix Ashes" in inventory:  # "in" scans the entire list and returns True if the item is anywhere in it
        print(f"\n{Y}══════════════════════════════════════════════════════")
        print("  You feel a warmth in your satchel...")
        print("  An Phoenix Ashes glows faintly.")
        print(f"══════════════════════════════════════════════════════{RESET}")
        choice = input("Use the Phoenix Ashes to revive? (y/n): ")

        if choice.lower() == "y":
            inventory.remove("Phoenix Ashes")          # one-use item — gone forever after this
            item = sample_items["Phoenix Ashes"]       # pull up the item's stats
            current_hp   = min(item["hp"], player["hp"])  # 9999 gets capped to max HP — effectively full heal
            current_slot = min(current_slot + item.get("cast", 0), player["cast"])  # also tops up some spell slots
            print(f"\n{G}The elixir surges through your veins!")
            print(f"You have been revived! HP: {current_hp}/{player['hp']}{RESET}")
            return True   # True = revival happened, the fight loop can continue
        else:
            print(f"{R}You chose not to drink it. Your journey ends here.{RESET}")
            return False  # False = player declined, game over

    return False  # False = no ashes in bag at all, game over


def attack_monster(monster_hp, player_atk):
    # player hits the monster — subtracts player's attack from monster HP and returns the new HP
    monster_hp -= player_atk  # -= is shorthand for monster_hp = monster_hp - player_atk
    if monster_hp < 0:         # clamp at 0 — we never want to display negative HP
        monster_hp = 0
    print(f"You dealt {player_atk} damage!")
    return monster_hp  # send the updated HP back to whoever called this function


def attack_player(player_hp, monster_atk, player_defense):
    # monster hits the player — defense reduces the hit, but minimum 1 damage always gets through
    damage = monster_atk - player_defense  # higher defense = less damage lands
    if damage < 1:  # even if your defense is higher than their attack, you still take 1 — no such thing as immunity
        damage = 1
    player_hp -= damage
    if player_hp < 0:
        player_hp = 0
    print(f"The monster dealt {damage} damage!")
    return player_hp  # return the updated HP so the fight loop can keep track


def monster_use_skill(monster_name, monster_hp, monster_atk, monster_skill):
    # this runs when a monster uses its special move instead of a normal attack
    # some skills heal the monster, so we return monster_hp at the end
    global current_hp, current_slot  # need these to damage the player or drain their spell slots

    print(f"\n{R}The {monster_name} used {monster_skill}!{RESET}")

    if monster_skill == "Claw Swipe":
        # two quick scratches — used by early enemies, not too deadly but adds up
        hit1 = max(1, monster_atk - player["defense"])          # first swipe — defense reduces it, at least 1
        hit2 = max(1, (monster_atk // 2) - player["defense"])   # second swipe — half power, // is integer divide (no decimals)
        total = hit1 + hit2
        current_hp -= total
        if current_hp < 0: current_hp = 0
        print(f"{R}Two slashes! You took {hit1} + {hit2} = {total} damage!{RESET}")

    elif monster_skill == "Flare":
        # magic fire blast — completely ignores your armor, raw damage goes straight through
        damage = monster_atk  # no defense subtraction at all — this one hurts no matter your gear
        current_hp -= damage
        if current_hp < 0: current_hp = 0
        print(f"{R}Burns through your armor! You took {damage} damage!{RESET}")

    elif monster_skill == "Spectral Drain":
        # life steal — deals damage AND heals the monster at the same time, nasty combo
        heal      = monster_atk // 2  # monster heals for half its attack stat — // keeps it a whole number
        monster_hp += heal             # add the heal directly to the monster's HP
        damage    = max(1, monster_atk - player["defense"])
        current_hp -= damage
        if current_hp < 0: current_hp = 0
        print(f"{R}Drained your life! You took {damage} damage and the enemy healed {heal} HP!{RESET}")

    elif monster_skill == "Savage Bite":
        # one massive chomp — attack gets doubled before defense reduces it, so it hits way harder than normal
        damage = max(1, (monster_atk * 2) - player["defense"])  # * 2 doubles the attack FIRST, then defense reduces
        current_hp -= damage
        if current_hp < 0: current_hp = 0
        print(f"{R}Massive bite! You took {damage} damage!{RESET}")

    elif monster_skill == "Dark Slash":
        # late-game slice with a flat +10 bonus on top of their attack — always hits harder than expected
        damage = max(1, monster_atk + 10 - player["defense"])  # +10 is added before defense reduces it
        current_hp -= damage
        if current_hp < 0: current_hp = 0
        print(f"{R}A powerful dark strike! You took {damage} damage!{RESET}")

    elif monster_skill == "Soul Rend":
        # truly nasty — deals damage AND permanently cuts your MAX HP by 20
        damage = max(1, monster_atk - player["defense"])
        current_hp -= damage
        if current_hp < 0: current_hp = 0
        player["hp"] -= 20  # this directly edits the max HP value — the loss is permanent for the rest of the game
        print(f"{R}Your soul was sapped! You took {damage} damage and lost 20 max HP!{RESET}")

    elif monster_skill == "Ferocious Maw":
        # Cerberus's three-bite combo — each bite hits harder than the last AND drains 5 spell slots
        hit1 = max(1, monster_atk         - player["defense"])  # bite 1 — base damage
        hit2 = max(1, (monster_atk + 10)  - player["defense"])  # bite 2 — +10 bonus damage
        hit3 = max(1, (monster_atk + 15)  - player["defense"])  # bite 3 — +15 bonus damage, the big one
        total = hit1 + hit2 + hit3
        current_hp -= total
        if current_hp < 0: current_hp = 0
        current_slot -= 5   # rips 5 spell slots away — can completely shut down skill-reliant players
        if current_slot < 0: current_slot = 0  # spell slots can never go below 0
        print(f"{R}Three Massive Bites! You took {hit1} + {hit2} + {hit3} = {total} damage and lost 5 spell slots!{RESET}")

    elif monster_skill == "Hellfire":
        # Cerberus's final head — deals 30% of your MAX HP as damage, so it scales with your power level
        damage = int(0.3 * player["hp"])  # 0.3 = 30% — int() rounds it down to a whole number since HP is always whole
        current_hp -= damage
        if current_hp < 0: current_hp = 0
        print(f"{R}Cerberus breathes hellfire! You took {damage} damage!{RESET}")

    elif monster_skill == "Shadow Stab":
        # Hades phase 1 — triple threat: damages you, heals Hades, and permanently lowers your max HP
        damage  = max(1, monster_atk - player["defense"])
        recover = monster_atk // 2   # Hades heals himself for half his attack
        monster_hp += recover         # add the heal to the boss HP
        current_hp -= damage
        if current_hp < 0: current_hp = 0
        player["hp"] -= 10  # permanent max HP reduction — Hades is literally draining your life force
        print(f"{R}Hades stabs from the shadows! You took {damage} damage, lost 10 max HP, and Hades healed {recover} HP!{RESET}")

    elif monster_skill == "Wrath of Tartarus":
        # Hades phase 2 ultimate — does damage, heals Hades, drains spell slots, AND cuts your max HP
        damage  = max(1, monster_atk - player["defense"])
        recover = monster_atk // 3    # heals Hades for a third of his attack
        drain   = max(1, monster_atk // 15)  # drains spell slots — at least 1, scales with his attack
        current_slot -= drain
        if current_slot < 0: current_slot = 0
        monster_hp += recover
        current_hp -= damage
        if current_hp < 0: current_hp = 0
        player["hp"] -= 10  # max HP keeps getting chipped away — this is why Hades is scary
        print(f"{R}The Wrath of Tartarus erupts! You took {damage} damage, lost {drain} spell slots, lost 10 max HP, and Hades healed {recover} HP!{RESET}")

    return monster_hp  # some skills healed the monster so we MUST return the updated HP


def use_skill(monster_hp, monster_atk):
    # player uses their class's special ability — costs one spell slot and does something powerful
    global current_hp, current_slot

    if current_slot <= 0:  # <= 0 covers zero AND negative (shouldn't happen but good to be safe)
        print(f"\n{Y}No spell slots remaining! Level up to recharge.{RESET}")
        return monster_hp  # return HP unchanged — skill failed, monster takes no damage

    current_slot -= 1  # burn one slot before the skill fires — no free uses
    skill = player["skill"]  # grab the skill name from the player's class data
    print(f"\n{G}You used {skill}! (Slots left: {current_slot}){RESET}")

    if skill == "Absolute Decree":
        # Dictator skill — pure raw power, multiplies attack by 4
        damage = player["attack"] * 4  # * 4 makes this hit absurdly hard — best burst damage in the game
        monster_hp -= damage
        print(f"{G}The enemy was crushed for {damage} damage!{RESET}")

    elif skill == "Police Brutality":
        # Cop skill — scales with both attack stat AND your current level, gets better as you level up
        damage = int(13 + (player["attack"] * 0.5 * level))  # formula: 13 base + (attack × 0.5 × level)
        # int() drops the decimal — 37.5 becomes 37, no fractions allowed in damage
        monster_hp -= damage
        print(f"{G}You shot the enemy for {damage} damage!{RESET}")

    elif skill == "Loophole Stab":
        # Fixer skill — random multiplier between 1.5x and 3x, you never know what you'll get
        multiplier = random.uniform(1.5, 3.0)  # uniform() picks a decimal (float) between 1.5 and 3.0 — like a lucky crit
        damage = int(player["attack"] * multiplier)  # int() rounds down so damage is always a clean number
        monster_hp -= damage
        print(f"{G}Critical strike! {damage} damage dealt!{RESET}")

    elif skill == "Inherited Blow":
        # Nepotist skill — scales with level AND heals you for a third of what you deal
        damage = int(player["attack"] * (level * 0.7))  # damage grows the higher your level — weak early, scary late
        monster_hp -= damage
        heal = damage // 3  # heal is one-third of the damage dealt — // is integer divide, keeps it a whole number
        current_hp += heal
        if current_hp > player["hp"]: current_hp = player["hp"]  # cap healing at max HP — can't overheal
        print(f"{G}You dealt {damage} damage!")
        print(f"You recovered {heal} HP!{RESET}")

    if monster_hp < 0: monster_hp = 0  # never let monster HP show as negative

    return monster_hp  # send back the updated monster HP


def fight(monster_name, hp, atk, exp_reward, gold_reward, lore, monster_skill=None, drops=[]):
    # THE MAIN FIGHT FUNCTION — this runs an entire battle from start to finish
    # monster_skill=None means the skill is optional — some monsters have no special move
    # drops=[] means drops are optional too — bosses for example have no loot drops
    global current_hp, exp, hero_gold, level, current_slot

    monster_hp = hp  # set the monster's HP to whatever was passed in — doesn't touch the original tuple
    print(f"\nA {monster_name} appears!")
    print(f"Lore: {lore}")  # print the monster's flavor text so the player knows what they're fighting

    # battle loop — keeps going as long as both sides are still alive
    while monster_hp > 0 and current_hp > 0:

        # ── MONSTER FLEE CHECK ──────────────────────────────────────────────
        if player["attack"] >= monster_hp:  # if your one hit could finish the monster off...
            if random.random() < 0.25:       # ...there's a 25% chance it gets scared and bolts
                # random.random() gives a float from 0.0 to 1.0 — below 0.25 = 25% chance
                print(f"\n{Y}The {monster_name} is overwhelmed and flees!{RESET}")
                exp       += exp_reward  // 2  # half rewards for a flee — // divides and rounds down
                hero_gold += gold_reward // 2
                print(f"Gained {exp_reward // 2} EXP and {gold_reward // 2} gold from scaring it off!")
                return True  # True = you "won" even though the monster ran

        # ── PLAYER TURN ─────────────────────────────────────────────────────
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
            monster_hp = attack_monster(monster_hp, player["attack"])  # normal attack — calls the function, saves the new HP

        elif combat_choice == "2":
            monster_hp = use_skill(monster_hp, atk)  # class skill — might do nothing if out of slots

        elif combat_choice == "3":
            # list comprehension — builds a new list on the fly with only items that are type "consumable"
            usable = [i for i in inventory if sample_items[i]["type"] == "consumable"]
            if not usable:  # "not usable" = True when the list is empty — nothing to use
                print("No consumables in inventory!")
                continue  # "continue" skips the rest of this loop body and goes back to the top of the while loop

            for i, item in enumerate(usable, start=1):
                print(f"{i}. {item}")  # show only the usable items, numbered from 1

            pick = input("Choose item (0 to cancel): ")
            if pick.isdigit() and 0 < int(pick) <= len(usable):  # valid number AND within range
                use_consumable(usable[int(pick) - 1])  # int(pick) - 1 converts "2" → 1 (zero-based index)
            else:
                print("Cancelled.")
                continue  # cancelled — skip the monster's turn too

        elif combat_choice == "4":
            if random.random() < 0.7:  # 70% success rate — running usually works but not always
                print("\nYou escaped successfully!")
                return True  # exit the fight entirely — back to the main loop
            else:
                print(f"{R}You failed to escape! You're wide open!{RESET}")
                # failed escape falls through — monster still gets to attack this turn

        else:
            print("Invalid action!")
            continue  # bad input — loop back and ask again, don't advance the turn

        print(f"{monster_name} HP: {monster_hp}")  # show the monster's HP after your action

        # ── MONSTER DEATH CHECK ─────────────────────────────────────────────
        if monster_hp <= 0:
            print(f"\n{G}You defeated the {monster_name}!{RESET}")
            exp       += exp_reward   # add the exp reward to your running total
            hero_gold += gold_reward  # add the gold reward to your wallet
            print(f"Gained {exp_reward} EXP and {gold_reward} gold!")

            for drop_item, drop_chance in drops:  # loop through every possible drop as a (item, chance) pair
                if random.randint(1, 100) <= drop_chance:  # roll against the drop chance — lucky roll = item drops
                    inventory.append(drop_item)
                    print(f"{Y}The {monster_name} dropped: {drop_item}!{RESET}")

            if exp >= level * 110:  # did you earn enough EXP to level up? threshold scales each level
                level += 1
                player['hp']      += 15  # max HP goes up
                player['attack']  += 5   # attack goes up
                player['defense'] += 3   # defense goes up
                current_hp   = player['hp']   # full heal on level up — your HP refills completely
                current_slot = player['cast']  # spell slots also fully recharge on level up
                print(f"\n{G}LEVEL UP! Now level {level}!")
                print(f"HP +15 | Attack +5 | Defense +3 | Spell slots recharged!{RESET}")
            return True  # fight's over, player won — back to the main loop

        # ── MONSTER TURN ────────────────────────────────────────────────────
        if monster_skill and random.randint(1, 100) <= 50:
            # 50% chance the monster uses its skill instead of a regular attack — if it has one
            monster_hp = monster_use_skill(monster_name, monster_hp, atk, monster_skill)
        else:
            current_hp = attack_player(current_hp, atk, player["defense"])  # regular attack

        print(f"Your HP: {current_hp}")  # show your HP after the monster's turn

        # ── PLAYER DEATH CHECK ──────────────────────────────────────────────
        if current_hp <= 0:
            print(f"\n{R}You died...{RESET}")
            revived = attempt_revive()  # see if the player has Phoenix Ashes and wants to use them
            if revived:
                continue  # player came back — loop goes back to the top and the fight continues
            else:
                return False  # no revive — return False means the player lost this fight for real


# ─────────────────────────────────────────────────────────────────────────────
# ENEMY DATA
# every monster is a tuple with this exact order:
# (name, hp, atk, exp, gold, lore_string, skill_name, drops_list)
# drops_list = list of (item_name, drop_chance_percent) pairs
# ─────────────────────────────────────────────────────────────────────────────

monsters_early = [  # rooms 1–20, intro enemies — weak enough to learn the combat on

    ("Imp", 40, 20, 10, 20,
     "A mischievous demon born from stray curses and broken promises.\n"
     "It feeds on fear and enjoys scratching heroes before fleeing into the shadows.",
     "Claw Swipe",
     [("Apollo's Lyre +30 hp", 35)]),   # 35% chance to drop the heal potion

    ("Hellcat", 50, 25, 40, 25,
     "A demonic feline with burning eyes and molten claws.\n"
     "It stalks silently through dungeon corridors, striking when prey least expects it.",
     "Claw Swipe",
     [("Apollo's Lyre +30 hp", 30)]),

    ("Harpies", 60, 30, 30, 35,
     "Harpies are winged spirits that punish the guilty and leave only ruin in their wake.\n"
     "Born from curses, they serve as relentless agents of violent tribulations.",
     "Claw Swipe",
     [("Apollo's Lyre +30 hp", 25)]),

    ("Fiend", 70, 30, 30, 35,
     "A corrupted being forged from hatred and war.\n"
     "Stronger than common demons, it delights in prolonged suffering and brutal combat.",
     "Flare",                          # Flare ignores armor — watch out even early on
     [("Apollo's Lyre +30 hp", 25), ("Minotaur's Horns +13 atk", 15)])  # two possible drops
]

monsters_mid = [  # rooms 21–40, tougher enemies — new skills and more HP, gear matters more here

    ("Demon", 90, 35, 50, 45,
     "A true inhabitant of the abyss.\n"
     "Its body radiates heat and malice, and every step leaves scorch marks on the floor.",
     "Flare",
     [("Apollo's Lyre +30 hp", 30), ("Nemean Lion's Pelt +10 def", 20)]),

    ("Wraith", 110, 30, 50, 55,
     "A restless spirit bound to the dungeon by regret and vengeance.\n"
     "Weapons pass through its form unless fueled by strong will and resolve.",
     "Spectral Drain",                 # heals itself — kill it fast or it'll outlast you
     [("Apollo's Lyre +30 hp", 25), ("Minotaur's Horns +13 atk", 20)]),

    ("Hellhound", 130, 40, 55, 60,
     "A monstrous beast born from ashes.\n"
     "Its flaming breath and relentless pursuit make escape nearly impossible.",
     "Savage Bite",                    # doubles attack before defense reduction — really hurts
     [("Nemean Lion's Pelt +10 def", 25), ("Harpe of Cronos +30 atk", 10)]),

    ("Empusa", 110, 40, 60, 75,
     "A seductive servant of Hades, the Empusa lures travelers with a beautiful facade before revealing her true form.\n"
     "She feeds on the life force of the ambitious, leaving nothing behind but cold memories and bloodstained dust.",
     "Spectral Drain",
     [("Apollo's Lyre +30 hp", 25), ("Minotaur's Horns +13 atk", 20)])
]

monsters_late = [  # rooms 41–60, endgame enemies — Soul Rend permanently lowers max HP, bring heals

    ("Fallen Angel", 160, 80, 67, 80,
     "Once a divine warrior, now corrupted by pride and betrayal.\n"
     "Its radiant wings are stained black, and it fights with sorrowful fury.",
     "Dark Slash",
     [("Harpe of Cronos +30 atk", 20), ("Restora +hp and +mp", 15)]),

    ("Shade of Zagreus", 180, 89, 75, 90,
     "A spectral echo of a prince who once defied the underworld.\n"
     "Clad in tattered robes with eyes like glowing embers, he relentlessly lashes out at any soul that dares stand in his path.",
     "Dark Slash",
     [("Harpe of Cronos +30 atk", 25), ("Restora +hp and +mp", 20)]),

    ("Shade of Thanatos", 200, 80, 80, 100,
     "A silent, hooded apparition carrying a heavy scythe.\n"
     "This shade manifests as a cold, flickering remnant of Death's own inevitability,\n"
     "harvesting the lingering regrets of those whose time in the Labyrinth has finally run out.",
     "Soul Rend",                      # permanently cuts your max HP — the scariest debuff in the game
     [("Restora +hp and +mp", 25), ("Harpe of Cronos +30 atk", 20)]),

    ("Erinys", 250, 85, 100, 100,
     "A winged enforcer of divine vengeance.\n"
     "The Erinys stalks the deepest halls of the Labyrinth, drawn to the scent of unconfessed crimes,\n"
     "ensuring that those who escaped justice above face it here.",
     "Soul Rend",
     [("Restora +hp and +mp", 25), ("Harpe of Cronos +30 atk", 20)])
]


# ─────────────────────────────────────────────────────────────────────────────
# MAIN GAME LOOP
# this while loop is the heartbeat of the entire game
# all three conditions must be True for it to keep running
# ─────────────────────────────────────────────────────────────────────────────

while game_running and room <= 60 and current_hp > 0:
    # header — shows the current room and all your stats at a glance
    print(f"\n{'='*24} ROOM {room} {'='*24}")
    print(f"    HP: {current_hp}/{player['hp']} | Level: {level} | EXP: {exp} | Slots: {current_slot}/{player['cast']}")
    print("Gold:", hero_gold)
    print("\nchoose your action")
    print("(1)Venture onward")  # move forward and trigger a random event
    print("(2)Item")            # open your inventory
    print("(3)Bail")            # try to leave (spoiler: you can't)

    action = input("> ")
    print("-" * 56)

    if action == "1":
        result = venture()  # roll the dice on what happens next — saves the event string it returns

        if result == "A monster have appeared!":
            # pick the right enemy pool based on current room number
            if room <= 20:
                monsters = monsters_early   # rooms 1–20, easier enemies
            elif room <= 40:
                monsters = monsters_mid     # rooms 21–40, mid-tier enemies
            else:
                monsters = monsters_late    # rooms 41–60, the hard ones

            enemy = random.choice(monsters)  # random.choice() picks one random tuple from the list
            # unpack all 8 elements of the tuple and pass them to fight() in the right order
            fight_result = fight(enemy[0], enemy[1], enemy[2], enemy[3], enemy[4], enemy[5], enemy[6], enemy[7])

            if not fight_result:  # fight returned False = player died and no revive happened
                game_running = False
                break  # break exits the while loop immediately — no point continuing

        elif result == "You found something useful!":
            # weighted table for what exactly you find — money is most common, rare items very rare
            useful = [
                ("money",     52),   # 52% — most likely outcome
                ("potion",    45),   # 45% — healing item
                ("rare_item",  3),   # 3% — legendary gear, very lucky
            ]

            roll  = random.randint(1, 100)
            total = 0

            for item, chance in useful:
                total += chance
                if roll <= total:  # same weighted-chance logic as venture() — roll falls into a bucket
                    if item == "money":
                        gold_found = random.randint(20, 50)  # random gold amount between 20 and 50
                        hero_gold += gold_found
                        print(f"\nFound {gold_found} gold!")
                    elif item == "potion":
                        inventory.append("Apollo's Lyre +30 hp")  # free heal item goes straight in your bag
                        print(f"\nFound Apollo's Lyre +30 hp! Added to inventory.")
                    elif item == "rare_item":
                        rare_drops = ["Wrath of Zeus +40 atk", "The Aegis +17 def"]  # one of two endgame items
                        found = random.choice(rare_drops)   # pick one at random
                        inventory.append(found)
                        print(f"\n{Y}✦ Something shimmers in the dark...{RESET}")
                        print(f"You found: {found}! Added to inventory.")
                    break  # stop checking once we've matched an outcome — don't double-trigger

        elif result == "You triggered a trap!":
            trap_damage = random.randint(10, 25)  # random damage between 10 and 25
            current_hp -= trap_damage
            print(f"You take {trap_damage} damage!")

            if current_hp <= 0:  # trap killed you — same death handling as combat
                print(f"\n{R}The trap was lethal...{RESET}")
                revived = attempt_revive()  # phoenix ashes can save you from traps too
                if not revived:
                    game_running = False  # no save, no revive, game over

        elif result == "A merchant appeared!":
            print("\nA merchant appears!")
            shop()  # hand control to the shop function — player stays there until they exit

        elif result == "An ominous enemy have appeared":
            # ── CERBERUS ENCOUNTER ───────────────────────────────────────────
            # three sequential fights — you must beat all three heads in order
            # each head is its own full fight() call, losing any one ends the encounter
            print(f"\n{R}The guardian of the underworld blocks your path!{RESET}")
            if player["hp"] <= 350:  # low max HP = probably under-leveled for this
                print(f"{Y}This monster is out of your league, retreat is recommended!{RESET}")

            print(f"\n{R}── CERBERUS: LEFT HEAD ──{RESET}")
            head1_result = fight(
                "Cerberus - Left Head", 300, 71, 50, 100,
                "A monstrous three-headed guardian born from the depths of Tartarus.\n"
                "Even severed from the whole, each head fights with savage independence.",
                "Ferocious Maw"   # no drops for boss fights — defaults to []
            )

            if not head1_result:
                game_running = False  # died on head 1 — the whole encounter is over

            else:
                print(f"\n{R}── CERBERUS: RIGHT HEAD ──{RESET}")
                head2_result = fight(
                    "Cerberus - Right Head", 200, 85, 50, 100,
                    "The right head snarls with blind fury, snapping at anything that moves.\n"
                    "It fights harder knowing its brothers are watching.",
                    "Ferocious Maw"
                )

                if not head2_result:
                    game_running = False  # died on head 2

                else:
                    print(f"\n{R}── CERBERUS: MIDDLE HEAD (FINAL) ──{RESET}")
                    head3_result = fight(
                        "Cerberus - Middle Head", 400, 80, 100, 200,
                        "The dominant head, commanding the other two. Its breath carries the fire of Tartarus itself.\n"
                        "This is the last thing most souls ever see.",
                        "Hellfire"  # Hellfire = 30% max HP damage — always scary
                    )

                    if not head3_result:
                        game_running = False  # died on the final head
                    else:
                        print(f"\n{G}Cerberus collapses. The path forward is open.{RESET}")

    # ── SECTION / ROOM COUNTER ───────────────────────────────────────────────
    section += 1  # every time you venture, that's one section — 3 sections = 1 room

    if section == 3:        # hit 3 sections? advance to the next room
        room    += 1        # increment the room counter
        section  = 0        # reset section back to 0 for the new room
        print(f"You Made it to room {room}")

        # story beats — only print at specific room milestones
        if room == 2:       # first room transition — introduce the setting
            print("=" * 55)
            print("\nAfter meeting their end in the mortal world, "
                  "\na powerful historical figure awakens in the Labyrinth, "
                  "\na torturous underworld realm designed by Hades to test and confine the cursed.")
        elif room == 21:    # crossing into mid-game — raise the stakes
            print("=" * 55)
            print("To escape, they must fight through floors of nightmare creatures, "
                  "\nfueled by the hope that defeating Hades will collapse the realm "
                  "\nand allow all imprisoned souls to be reincarnated.")
        elif room == 41:    # entering the final stretch
            print("=" * 55)
            print("As he ascends, the resistance from the monsters grows more intense, "
                  "\nreflecting a domain that hungers to break the will of its prisoners.")

    # ── FINAL BOSS CHECK ─────────────────────────────────────────────────────
    if room > 60:  # once you pass room 60, Hades is waiting — no more random events
        print("\nYou have reached the deepest part of the labyrinth!")
        print("\nThe sovereign of this labyrinth stands before you")
        print("=" * 55)
        print("Hades: You thought you could buy your way out of the grave?")
        print("Death is the only contract you cannot bribe your way out of.")
        print('Now, let\'s see what\'s left of you once we strip away your "hard work".')

        # ── HADES PHASE 1 ────────────────────────────────────────────────────
        boss_result = fight(
            "Hades", 500, 100, 500, 1000,
            "The sovereign of the underworld, clad in obsidian armor that drinks in all light.\n"
            "He has watched countless souls crumble before him, and he expects the same from you.",
            "Shadow Stab"  # drains max HP + heals himself — fight smartly
        )

        if boss_result == True:  # == True written explicitly so it's clear this is a two-phase check
            print("=" * 55)
            print(f"{R}Hades gets engulfed in hellfire{RESET}")
            print("Hades: ENOUGH!")

            # ── HADES PHASE 2 ─────────────────────────────────────────────────
            Sboss_result = fight(
                "Hades", 800, 200, 500, 1000,
                "Stripped of patience, Hades sheds his regal composure entirely.\n"
                "What stands before you now is not a king — it is the raw, furious will of death itself.",
                "Wrath of Tartarus"  # hardest skill in the game — does everything bad at once
            )

            if Sboss_result == True:  # you actually beat him — now choose your ending
                print("=" * 55)
                print("Hades' body burns in ashes as his crown is the only thing left."
                      "\nOnly at the very end does he realize the weight of his victory, "
                      "\nhe must choose between shattering the Labyrinth forever to start a new life"
                      "\nor ascending the throne himself to prevent a total cosmic collapse.")

                print("   Choose Your Fate: (1)Ascend / (2)Start A New   ")
                answer = input("> ")

                if answer == "2":  # escape ending
                    print("=" * 55)
                    print("The Labyrinth begins to disappear as the light engulfs everything")
                    print("congratulations, You successfully escaped the Labyrinth of Hades!")
                    game_running = False  # flip the switch — main loop exits cleanly

                elif answer == "1":  # conquer ending
                    print("=" * 55)
                    print("The Labyrinth remains as you adorn Hades' crown as if it was your own..."
                          "\nStarting today you will be the one to rule this place..."
                          "\nBut not for long, for Hades will someday be back...")
                    print("congratulations, You successfully conquered the Labyrinth of Hades!")
                    game_running = False  # flip the switch — main loop exits cleanly

        break  # break here exits the main while loop after the Hades encounter — game done no matter what

    elif action == "2":
        # ── INVENTORY SCREEN ─────────────────────────────────────────────────
        print("\n--- INVENTORY ---")
        print(f"Weapon: {equipped['weapon'] or 'None'} | Armor: {equipped['armor'] or 'None'}")
        # "x or 'None'" — if x is None (falsy), Python returns the string 'None' instead — clean display trick

        if len(inventory) == 0:
            print("Nothing yet...")
        else:
            for i, item in enumerate(inventory, start=1):
                item_type    = sample_items[item]["type"]
                equipped_tag = ""  # starts empty — only gets text added if this item is currently equipped
                if item_type in ("weapon", "armor") and equipped[item_type] == item:
                    equipped_tag = " [EQUIPPED]"  # tacks this onto the end of the item name in the list
                print(f"{i}. {item}{equipped_tag}")

        print("\n(E) Equip/Unequip  (U) Use consumable  (D) Discard"
              "\n"
              "\n                                       (0) Back")
        inv_choice = input("> ")

        if inv_choice.lower() == "e":  # .lower() so both "E" and "e" work
            item_num = input("Choose item number to equip/unequip: ")
            if item_num.isdigit():
                idx = int(item_num) - 1  # convert to zero-based index
                if 0 <= idx < len(inventory):
                    item_name = inventory[idx]
                    if sample_items[item_name]["type"] in ("weapon", "armor"):
                        equip_item(item_name)  # hand it to the equip function
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
                        use_consumable(item_name)  # hand it to the consumable function
                    else:
                        print("That item can only be equipped, not consumed!")
                else:
                    print("Invalid choice.")

        elif inv_choice.lower() == "d":
            item_num = input("Choose item number to discard: ")
            if item_num.isdigit():
                idx = int(item_num) - 1
                if 0 <= idx < len(inventory):      # make sure the index is valid before doing anything
                    removed_item = inventory.pop(idx)  # .pop(idx) removes it AND returns the item name
                    print(f"You threw away the {removed_item}.")
                else:
                    print("Invalid choice.")
            else:
                print("Please enter a valid number.")

    elif action == "3":
        # bail option — the game literally won't let you leave, it's a dungeon
        print("\nYou try to bail... but the labyrinth won't let you leave!")
        print("You must press onward!")
