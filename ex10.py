# turn-based battle game

import random

class Character:

    def __init__(self, name, hp, max_hp, attack_min, attack_max, potion_num = 0):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.attack_min = attack_min
        self.attack_max = attack_max
        self.potion_num = potion_num

class Game:

    def attack(self, attacker, target):
        damage = random.randint(attacker.attack_min, attacker.attack_max)
        print(f"{attacker.name} attacks {target.name} for {damage} damage.")
        target.hp = max(0, target.hp-damage)

    def heal(self, player):
        heal = random.randint(8, 15)
        if player.hp + heal > player.max_hp:
            print(f"{player.name} heals for {player.max_hp - player.hp} HP.")
            player.hp = player.max_hp
        else:
            player.hp += heal
            print(f"{player.name} heals for {heal} HP.")

    def use_potion(self, player):
        if player.hp + 30 > player.max_hp:
            print(f"{player.name} uses a potion and restores {player.max_hp - player.hp} HP.")
            player.hp = player.max_hp
        else:
            player.hp += 30
            print(f"{player.name} uses a potion and restores 30 HP.")
    def show_status(self, player, enemy):
        print(f"{player.name} HP: {player.hp}/{player.max_hp}")
        print(f"{enemy.name} HP: {enemy.hp}/{enemy.max_hp}")

    def check_winner(self, player, enemy):
        if player.hp == 0:
            print(f"{enemy.name} wins!")
            return True
        if enemy.hp == 0:
            print(f"{player.name} wins!")
            return True
        return False

def main():
    name = input("enter your name: ").strip()
    player = Character(name, 100, 100, 10, 20, 2)
    enemy = Character("Goblin", 80, 80, 8, 18)
    game = Game()
    while True:
        try:
            choice = int(input("1) Attack\n"
                               "2) Heal\n"
                               "3) Show status\n"
                               "4) Use potion\n"))
        except ValueError:
            print("Invalid choice")
            continue
        match choice:
            case 1:
                game.attack(player, enemy)
                if game.check_winner(player, enemy):
                    break
            case 2:
                game.heal(player)
            case 3:
                game.show_status(player, enemy)
                continue
            case 4:
                if player.potion_num > 0:
                    game.use_potion(player)
                    player.potion_num -= 1
                else:
                    print("No potions left")
                    continue
            case _:
                print("Invalid choice")
                continue
        game.attack(enemy, player)
        if game.check_winner(player, enemy):
            break


if __name__ == '__main__':
    main()