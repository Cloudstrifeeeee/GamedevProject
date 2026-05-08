# Add this into the choices - After Line 31
#----------------------------
print("--------------------------")
    print("4. Sell")



# NOTE: THIS SHOULD BE AFTER
# -------------------------
# if choice == "0":
# print("Leaving shop...")
# in [inventory_manage.py] - Line 36 & 37

        # ----------------------
        # SELLING SYSTEM
        # FOR SHOPPING SYSTEM 
        elif choice == "4":   

            # Checks if the player[user] inventory is empty or not
            if len(inventory) == 0:
                print("\033[0;31mThere is nothing to sell, your inventory is empty!\033[0m")

            else:
                print("\n===== SELL ITEMS =====")

                # Selling item brings back at least 50% of gold
                # Unsure if this is a more fair selling point since it doesn't round up for .5 above
                for i, item in enumerate(inventory, start=1):

                    sell_price = sample_items[item]["price"] // 2
                    
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

                        sell_price = sample_items[item_name]["price"] // 2

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
