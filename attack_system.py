
def attack_monster(monster_hp, player_atk):

    monster_hp -= player_atk

    if monster_hp < 0:
        monster_hp = 0

    print(f"You dealt {player_atk} damage!")
    return monster_hp


def attack_player(player_hp, monster_atk, player_defense):

    damage = monster_atk - player_defense

    if damage < 1:
        damage = 1

    player_hp -= damage

    if player_hp < 0:
        player_hp = 0

    print(f"The monster dealt {damage} damage!")
    return player_hp


def fight(name, hp, atk, exp_reward, gold_reward):
    global current_hp, exp, gold

    monster_hp = hp

    print(f"\nA {name} appears!")

    while monster_hp > 0 and current_hp > 0:

       
        monster_hp = attack_monster(monster_hp, player["attack"])
        print(f"{name} HP: {monster_hp}")

        if monster_hp <= 0:
            print(f"\nYou defeated the {name}!")
            exp += exp_reward
            gold += gold_reward
            print(f"Gained {exp_reward} EXP and {gold_reward} gold!")
            return True

       
        current_hp = attack_player(current_hp, atk, player["defense"])
        print(f"Your HP: {current_hp}")

        if current_hp <= 0:
            print("\nYou died...")
            return False
