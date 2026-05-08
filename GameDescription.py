
def print_description():

    # Create the paragraph text with \n for line breaks
    paragraph = ( 

    "You will build a text-based dungeon adventure game that runs entirely in the terminal.\n"
    "The player explores rooms, fights monsters, collects loot, and tries to clear the dungeon.\n"
    "Everything happens through typed commands — no graphics, no GUI.\n"
    "You can do modularization for clearer and much better code debugging and readability.\n\n"

    "INSTRUCTIONS:\n\n"

    "THE DUNGEON\n"
    "Your dungeon must have at least 3 rooms.\n"
    "Each room should have a name, a description, and connections to the other rooms.\n"
    "The player must be able to navigate through the rooms.\n"
    "Each rooms can contain both monster or loots or anything.\n"
    "Example: Boss Chamber, Tavern\n\n"

    "THE PLAYER\n"
    "The player must be able to enter name for it's character and select a class.\n"
    "Each class should have it's own stats. Must have hp and attack\n"
    "The player should have inventory and skills.\n"
    "Can pick up items and use them.\n"
    "Example of Class: Warrior\n"
    "Example of Inventory: Longsword\n\n"

    "THE MONSTER\n"
    "There should be at least 4 different types of monster.\n"
    "Can have name and a description or lore.\n"
    "Monsters have their own stats, minimum of having hp and attack.\n"
    "Monsters can have skills.\n"
    "Monsters can drop loot\n"
    "There must be at least 1 BOSS type monster.\n"
    "Example: Goblin Type: Elite\n\n"

    "THE ITEMS\n"
    "There should be at least 2 types of items, namely weapons and armors.\n"
    "Items have their own stat to add to the player after pickup or usage.\n"
    "Can be discarded.\n"
    "Can be dropped by a monster or found inside a room or chest.\n\n"

    "THE GAME\n"
    "Must have win/lose combat system between the player and the monster.\n"
    "If the player dies the game would be over. The program should end.\n"
    "There must be a clear mechanics to clear the dungeon or complete the game.\n"
    "Example: Game Completed: You have defeated all the bosses!"
    )

    # Print the paragraph
    print(paragraph)

if __name__ == "__main__":
    try:
        print_description()
    except Exception as e:
        print(f"An error occurred: {e}")
