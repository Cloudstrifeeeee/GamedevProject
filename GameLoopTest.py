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
gold = 0
current_hp = player['hp']
floor = 1
game_running = True

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
            #basically as total accumulates it pick an event that can be triggered 
            print(f"\n{event}") # print out the event picked
            return event
    return "nothing"

while game_running and floor <= 70 and current_hp > 0:
    print(f"\n{'='*20} FLOOR {floor} {'='*20}")
    print(f"HP: {current_hp}/{player['hp']} | Level: {level} | EXP: {exp}")
    
    
    print("\n            " + "="*30 + "            ")
    print("choose your action")
    print("(1)Venture onward")
    print("(2)Item")
    print("(3)Equip")
    print("(4)Bail")
    
    action = input("> ")

    if action == "1":
        result = venture()

        if result == "A monster have appeared":
            monsters = [
                ("Imp", 40, 10, 30, 20),
                ("Hell cats", 50, 12, 40, 25),
                ("Lesser Fiends", 70, 15, 60, 35)
            ]
            enemy = random.choice(monsters)
            fight_result = fight(enemy[0], enemy[1], enemy[2], enemy[3], enemy[4])
             #please define the fight mechanics using fight or something so this would work for the encounters
            if not fight_result:
                game_running = False
                break
        
        elif result == "something useful":
            print("\nYou found something useful!")
            gold_found = random.randint(20, 50)
            print(f"Found {gold_found} gold!")
        
        elif result == "a trap was triggered!":
            print("\nYou triggered a trap!")
            trap_damage = random.randint(10, 25)
            current_hp -= trap_damage
            print(f"You take {trap_damage} damage! HP: {current_hp}/{player['hp']}")
            
            if current_hp <= 0:
                print("\nThe trap was fatal...This is where your journey ends...")
                game_running = False
                break
        
        elif result == "a merchant appears!":
            print("\nA wandering merchant appears!")
            print("(Shop coming soon...)")
        
        elif result == "An ominous enemy have appeared":
            print("\nAn ominous enemy have appeared")
            boss_result = fight("Cerberus", 120, 20, 150, 100)
            if not boss_result:
                game_running = False
                break

        elif result == "You found what seem to be an exit!":
            print("\nYou found a door that seems to be the exit")
            print("You manage to escape that hellish place and" \
            "\nnow getting ready for your next life, congratulation")
            break


        
    elif action == "2": #change later
        print("\n--- INVENTORY ---")
        print("Nothing yet...")
        print("(Items will be added later)")
    
    elif action == "3": #change later
        print("\n--- EQUIPMENT ---")
        print(f"Weapon: None (Attack: {player['attack']})")
        print(f"Armor: None (Defense: {player['defense']})")
    
    elif action == "4": 
        print("\nYou try to bail... but the labyrinth won't let you leave!")
        print("You must press onward!")
    
