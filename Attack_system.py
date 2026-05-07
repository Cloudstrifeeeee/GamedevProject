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


# MAIN FIGHT SYSTEM
# Controls the entire battle between player and monster
def fight(monster_name, hp, atk, exp_reward, gold_reward):

    # allows function to modify global variables
    global current_hp, exp, gold

    # set monster HP for this fight
    monster_hp = hp

    # show monster encounter message
    print(f"\nA {monster_name} appears!")

    # loop until either player or monster dies
    while monster_hp > 0 and current_hp > 0:

        
        # PLAYER TURN
        # player attacks monster
        monster_hp = attack_monster(monster_hp, player["attack"])

        # show monster HP after attack
        print(f"{monster_name} HP: {monster_hp}")

        # check if monster is defeated
        if monster_hp <= 0:
            print(f"\nYou defeated the {monster_name}!")

            # reward player
            exp += exp_reward
            gold += gold_reward

            print(f"Gained {exp_reward} EXP and {gold_reward} gold!")

            # end fight as win
            return True



        # MONSTER TURN
        # monster attacks player
        current_hp = attack_player(current_hp, atk, player["defense"])

        # show player HP after attack
        print(f"Your HP: {current_hp}")

        # check if player died
        if current_hp <= 0:
            print("\nYou died...")

            # end fight as loss
            return False
