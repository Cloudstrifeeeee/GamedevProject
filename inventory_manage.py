hero_gold = 100

sample_items = {
    "Cannon Ball +3 atk": {"price": 20},
    "Heavy Ball +10 atk": {"price": 75},
    "Basic Armor +3 def": {"price": 35}
}

#inventory empty list
# Step 1 for inventory
inventory = []

while True:
    print("\nGold:", hero_gold)
    print("1. Shop")
    print("2. Inventory")
    print("3. Exit")

    action = input("> ")

    # SHOP
    # Step 2 for inventory
    if action == "1":

        print("\n===== ITEMS SHOP =====")

        item_list = list(sample_items.items())

        for i, (item, data) in enumerate(item_list, start=1):
            print(f"{i}. {item} - {data['price']} gold")

        print("0. Exit Shop")

        choice = input("Choose item: ")

        if choice == "0":
            print("Leaving shop...")

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

    # INVENTORY
    # Step 4 for inventory
    elif action == "2":

        print("\n===== INVENTORY =====")
        
        
        #checks if inventory is empty
        # Step 5 for inventory
        if len(inventory) == 0:
            print("Inventory is empty")

        #if inventory is not empty prints items from inventory list
        else:
            #enumerates items from the inventory
            # Step 6 for inventory
            for i, item in enumerate(inventory, start=1):

                #prints the list of baught items
                # Step 5 for inventory
                print(f"{i}. {item}")

    # EXIT
    elif action == "3":
        print("Goodbye")
        break

    else:
        print("Invalid action")