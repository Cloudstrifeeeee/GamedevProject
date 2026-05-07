import random


player_hp = random.randint(80, 120)
monster_hp = random.randint(50, 100)

player_atk = random.randint(10, 25)
monster_atk = random.randint(5, 20)

print(f"Player HP: {player_hp}")
print(f"Player Atk: {player_atk}")
print(f"Monster HP: {monster_hp}")
print(f"Monster Atk: {monster_atk}")


def attack_monster(hp:int, atk:int):

    damage = hp - atk
    print(f"you attacked the monster!")
    return damage
    
def attack_player(hp:int, atk:int):

    damage = hp - atk
    print(f"The monster counter attacked!")
    return damage


monster_hp = attack_monster(monster_hp, player_atk)
player_hp = attack_player(player_hp, monster_atk)

print(f"Monster remaning HP: {monster_hp}")
print(f"Player remaining HP: {player_hp}")

