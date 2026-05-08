import random

print("========DND presents : Let's eat in the Dungeon========")

pname = input("Enter your name HERO :")

classes = {
    "1": {"class": "Dictator", "hp": 150, "attack": 20, "defense": 15, "skill": "Absolute Decree"},
    "2": {"class": "Cop", "hp": 80, "attack": 15, "defense": 5, "skill": "Police Brutality"},
    "3": {"class": "Fixer", "hp": 100, "attack": 25, "defense": 10, "skill": "Loophole Stab"},
    "4": {"class": "Nepotist", "hp": 90, "attack": 15, "defense": 5, "skill": "Inherited Blow"}
}

print("Please choose your background (cannot be changed till the end!)")

player = None  

while player is None:  
    choice = input("(1)DICTATOR, (2)COP, (3)FIXER, (4)NEPOTIST: ")
    
    player = classes.get(choice)
    if not player:
        print("Invalid choice. Please select 1, 2, 3, or 4.")

level = 1
exp = 0
current_hp = player['hp']
floor = 1
game_running = True

# ================= ECONOMY SYSTEM =================
hero_gold = 0
inventory = []

sample_items = {
    "Cannon Ball +3 atk": {"price": 20},
    "Heavy Ball +10 atk": {"price": 75},
    "Basic Armor +3 def": {"price": 35}
}

print(f"\nYou selected: {player['class']} class")
print(f"HP: {player['hp']}, Attack: {player['attack']}, Defense: {player['defense']}")
print(f"Special skill: {player['skill']}")
print("now you're all set, let's begin your journey")
print("=" * 55)


def venture():
    events=[
        ("A monster have appeared!", 1), 
        ("A merchant appeared!", 40),
        ("You found something useful!", 25),
        ("You triggered a trap!", 15),
        ("An ominous enemy have appeared", 10),
        ("You found what seem to be an exit!", 50)
    ]#the event tupples, yall can add more here 
    
    roll = random.randint(1, 100)
    total = 0
    
    for event, chance in events: #unpacking the events tupples
        total += chance #increase a chance of an event to be triggered
        if roll <= total: # this line check if the random int falls within the range of an event
            print(f"\n{event}") # print out the event picked
            return event
    
    return "nothing"


# ================= SHOP SYSTEM =================
def shop():
    global hero_gold, inventory

    while True:
        print("\n===== MERCHANT SHOP =====")
        print("Gold:", hero_gold)

        item_list = list(sample_items.items())

        for i, (item, data) in enumerate(item_list, start=1):
            print(f"{i}. {item} - {data['price']} gold")

        # Add this into the choices - After Line 31
        #----------------------------
        print("--------------------------")
        print("4. Sell")

        print("0. Exit Shop")

        choice = input("Choose item: ")

        if choice == "0":
            print("Leaving shop...")
            break

        # ================= SELLING SYSTEM =================
        elif choice == "4":   

            # NOTE: THIS SHOULD BE AFTER
            # -------------------------
            # if choice == "0":
            # print("Leaving shop...")
            # in [inventory_manage.py] - Line 36 & 37

            # ----------------------
            # SELLING SYSTEM
            # FOR SHOPPING SYSTEM 

            # Checks if the player[user] inventory is empty or not
            if len(inventory) == 0:
                print("\033[0;31mThere is nothing to sell, your inventory is empty!\033[0m")

            else:
                print("\n===== SELL ITEMS =====")

                # Selling item brings back at least 50% of gold
                # NOW FIXED: full price instead of half
                for i, item in enumerate(inventory, start=1):

                    sell_price = sample_items[item]["price"]   # ✅ FIXED HERE
                    
                    print(f"{i}. {item} -> sell for {sell_price} gold")

                print("--------------------------")
                print("0. Exit")

                # Gives the player[user] the ability which item they want to sell OR cancel it
                sell_choice = input("Choose an item you want to sell: ")

                if sell_choice == "0":
                    print("Exiting...")

                elif sell_choice.isdigit():

                    index = int(sell_choice) - 1

                    if 0 <= index < len(inventory):

                        item_name = inventory[index]

                        sell_price = sample_items[item_name]["price"]   # ✅ FIXED HERE

                        print("------------------------------------------------")
                        confirm = input(f"\033[0;32mSell {item_name} for\033[0m \033[0;33m{sell_price} gold\033[0m\033[0;32m? (y/n):\033[0m ")

                        # If the player[user] choses to sell the item
                        # They will recieve gold and removes the item from their inventory
                        if confirm.lower() == "y":

                            inventory.pop(index)

                            hero_gold += sell_price

                            print("------------------------------------------------")
                            print(f"\033[0;33mYou sold {item_name} for {sell_price} gold!\033[0m")

                        else:
                            print("\033[0;31mCancelled.\033[0m")

                    else:
                        print("Invalid choice.")

                else:
                    print("Enter numbers only.")

            # This is the end of the selling system for the shopping system
            # ----------------------

        # ================= BUY SYSTEM =================
        elif choice.isdigit():

            index = int(choice) - 1

            if 0 <= index < len(item_list):

                item_name, item_data = item_list[index]

                if hero_gold >= item_data["price"]:

                    hero_gold -= item_data["price"]

                    #adds item/s to the list in the inventory
                    # Step 3 for inventory
                    inventory.append(item_name)

                    print(f"You bought {item_name}")

                else:
                    print("Not enough gold!")

            else:
                print("Invalid choice")

        else:
            print("Enter numbers only")


# ================= MAIN GAME LOOP =================
while game_running and floor <= 70 and current_hp > 0:
    print(f"\n{'='*20} FLOOR {floor} {'='*20}")
    print(f"HP: {current_hp}/{player['hp']} | Level: {level} | EXP: {exp}")
    print("Gold:", hero_gold)

    print("\nchoose your action")
    print("(1)Venture onward")
    print("(2)Item")
    print("(3)Equip")
    print("(4)Bail")

    action = input("> ")

    if action == "1":
        result = venture()

        if result == "A monster have appeared!":
            print("Monster encounter (not implemented)")

        elif result == "You found something useful!":
            gold_found = random.randint(20, 50)
            hero_gold += gold_found
            print(f"Found {gold_found} gold!")

        elif result == "You triggered a trap!":
            trap_damage = random.randint(10, 25)
            current_hp -= trap_damage
            print(f"You take {trap_damage} damage!")

            if current_hp <= 0:
                print("\nYou died...")
                game_running = False

        elif result == "A merchant appeared!":
            print("\nA merchant appears!")
            shop()

        elif result == "An ominous enemy have appeared":
            print("Boss fight (not implemented)")

        elif result == "You found what seem to be an exit!":
            print("You escaped!")
            break

        floor += 1

        if floor > 70:
            print("\nYou have reached the deepest floor!")

    elif action == "2": #change later
        print("\n--- INVENTORY ---")

        if len(inventory) == 0:
            print("Nothing yet...")
        else:
            for i, item in enumerate(inventory, start=1):
                print(f"{i}. {item}")

    elif action == "3": #change later
        print("\n--- EQUIPMENT ---")
        print(f"Weapon: None (Attack: {player['attack']})")
        print(f"Armor: None (Defense: {player['defense']})")

    elif action == "4": 
        print("\nYou try to bail... but the labyrinth won't let you leave!")
        print("You must press onward!")