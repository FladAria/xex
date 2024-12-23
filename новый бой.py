
import random
import time

class Fighter:
    def __init__(self, name: str, health: float, damage: tuple[float, float], attack_speed: tuple[float, float]):
        self.name = name
        self.health = health
        self.damage = damage
        self.attack_speed = attack_speed
        self.next_attack_time = 0

    def sub(self, other: "Fighter"):
        if self.health <= 0:
            return self
        attack_delay = random.uniform(*self.attack_speed)
        self.next_attack_time += attack_delay
        time.sleep(attack_delay)
        damage_dealt = random.uniform(*self.damage)
        other.health -= damage_dealt
        return other


def battle(fighter1: Fighter, fighter2: Fighter, log_file: str = "logger.txt"):
    start_time = time.time()
    turn = 1
    fighters = [fighter1, fighter2]

    with open(log_file, "w") as f:
        while fighter1.health > 0 and fighter2.health > 0:
            f.write(f"---Раунд {turn}---\n")
            f.write(f"Здоровье {fighter1.name}: {fighter1.health:.2f}\n")
            f.write(f"Здоровье {fighter2.name}: {fighter2.health:.2f}\n")

            # Определяем, кто ходит следующим
            if fighters[0].next_attack_time <= fighters[1].next_attack_time:
                attacker = fighters[0]
                defender = fighters[1]
            else:
                attacker = fighters[1]
                defender = fighters[0]

            defender = attacker.sub(defender)

            damage_dealt = abs(defender.health - (defender.health + random.uniform(*attacker.damage)))
            f.write(f"{attacker.name} атаковал {defender.name}. Урон: {damage_dealt:.2f}\n")

            if defender.health <= 0:
                break

            # Обновляем список бойцов
            fighters = sorted([fighter1, fighter2], key=lambda x: x.next_attack_time)

            turn += 1

        end_time = time.time()
        total_time = end_time - start_time
        winner = fighter1 if fighter1.health > 0 else fighter2
        f.write(f"---Победитель: {winner.name}---\n")
        f.write(f"Время боя: {total_time:.2f} секунд\n")
def view_log(filepath):
    """Выводит содержимое лог-файла на консоль."""
    try:
        with open(filepath, 'r') as f:
            print(f.read())
    except FileNotFoundError:
        print(f"Файл {filepath} не найден.")
    except Exception as e:
        print(f"Ошибка при открытии файла: {e}")


# Пример использования:
fighter1 = Fighter("Боец 1", 100, (10, 20), (0.03, 0.04))
fighter2 = Fighter("Боец 2", 100, (15, 25), (0.035, 0.045))

battle(fighter1, fighter2)  # Проводим бой и записываем лог в "logger.txt"
view_log("logger.txt")