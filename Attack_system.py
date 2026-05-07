#put this above or before the main loop


# PLAYER ATTACK SYSTEM
# This function reduces the monster's HP based on player attack
def attack_monster(monster_hp, player_atk):

    # subtract player attack from monster HP
    monster_hp -= player_atk

    # prevent HP from going below 0
    if monster_hp < 0:
        monster_hp = 0

    # display damage dealt
    print(f"You dealt {player_atk} damage!")

    # return updated monster HP back to fight system
    return monster_hp


# MONSTER ATTACK SYSTEM
# This function reduces player HP based on monster attack and player defense
def attack_player(player_hp, monster_atk, player_defense):

    # calculate damage after defense reduction
    damage = monster_atk - player_defense

    # minimum damage is 1 (so defense doesn't fully block attacks)
    if damage < 1:
        damage = 1

    # subtract damage from player HP
    player_hp -= damage

    # prevent HP from going below 0
    if player_hp < 0:
        player_hp = 0

    # display damage dealt to player
    print(f"The monster dealt {damage} damage!")

    # return updated player HP
    return player_hp

# SKILL SYSTEM
# Handles player special abilities
def use_skill(monster_hp, monster_atk):

    # allows modification of player HP
    global current_hp

    # get player's class skill
    skill = player["skill"]

    # display skill usage
    print(f"\nYou used {skill}!")



    # =========================
    # DICTATOR SKILL
    # =========================
    if skill == "Absolute Decree":

        # heavy damage attack
        damage = player["attack"] * 2

        # reduce monster HP
        monster_hp -= damage

        print(f"The enemy was crushed for {damage} damage!")



    # =========================
    # COP SKILL
    # =========================
    elif skill == "Police Brutality":

        # bonus damage attack
        damage = player["attack"] + 15

        monster_hp -= damage

        print(f"You beat the enemy for {damage} damage!")



    # =========================
    # FIXER SKILL
    # =========================
    elif skill == "Loophole Stab":

        # random critical damage
        damage = player["attack"] + random.randint(10, 25)

        monster_hp -= damage

        print(f"Critical strike! {damage} damage dealt!")



    # =========================
    # NEPOTIST SKILL
    # =========================
    elif skill == "Inherited Blow":

        # damage + heal skill
        damage = player["attack"] + 10

        monster_hp -= damage

        # healing amount
        heal = 10

        # restore player HP
        current_hp += heal

        # prevent overhealing
        if current_hp > player["hp"]:
            current_hp = player["hp"]

        print(f"You dealt {damage} damage!")
        print(f"You recovered {heal} HP!")



    # prevent monster HP from becoming negative
    if monster_hp < 0:
        monster_hp = 0

    # return updated monster HP
    return monster_hp


# MAIN FIGHT SYSTEM
# Handles the battle between player and monster
def fight(monster_name, hp, atk, exp_reward, gold_reward):

    # allows this function to modify global variables
    global current_hp, exp, gold

    # set monster HP for this battle
    monster_hp = hp

    # encounter message
    print(f"\nA {monster_name} appears!")

    # battle loop
    # continues until either the monster or player dies
    while monster_hp > 0 and current_hp > 0:

        # =========================
        # PLAYER TURN
        # =========================

        # display combat choices
        print("\nChoose action:")
        print("(1) Attack")
        print("(2) Skill")

        # ask player for combat input
        combat_choice = input("> ")

        # NORMAL ATTACK
        if combat_choice == "1":

            # call attack function
            # reduces monster HP using player attack stat
            monster_hp = attack_monster(
                monster_hp,
                player["attack"]
            )

        # SKILL ATTACK
        elif combat_choice == "2":

            # use class special skill
            monster_hp = use_skill(
                monster_hp,
                atk
            )

        # INVALID INPUT
        else:

            # prevent invalid actions
            print("Invalid action!")

            # restart current loop iteration
            continue

        # show remaining monster HP
        print(f"{monster_name} HP: {monster_hp}")



        # =========================
        # CHECK IF MONSTER DIED
        # =========================

        if monster_hp <= 0:

            # victory message
            print(f"\nYou defeated the {monster_name}!")

            # reward player
            exp += exp_reward
            gold += gold_reward

            # display rewards
            print(f"Gained {exp_reward} EXP and {gold_reward} gold!")

            # player wins battle
            return True



        # =========================
        # MONSTER TURN
        # =========================

        # monster attacks player
        current_hp = attack_player(
            current_hp,
            atk,
            player["defense"]
        )

        # display updated player HP
        print(f"Your HP: {current_hp}")



        # =========================
        # CHECK IF PLAYER DIED
        # =========================

        if current_hp <= 0:

            # death message
            print("\nYou died...")

            # player loses battle
            return False
