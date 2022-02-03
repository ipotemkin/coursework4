"""Sets up a hero's logics"""

# from abc import ABC, abstractmethod

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from random import uniform, randint

from app.classes import UnitClass, warrior, thief
from app.equipment import Weapon, Armor, Equipment


@dataclass
class BaseUnit:
    """
    an base class for a hero
    """

    name: str
    unit_class: UnitClass
    health: float
    stamina: float
    _weapon: Optional[Weapon] = None
    _armor: Optional[Armor] = None
    skill_used: bool = False

    @property
    def weapon(self) -> Optional[Weapon]:
        """
        a weapon getter
        """

        return self._weapon

    @weapon.setter
    def weapon(self, new_weapon: Weapon) -> None:
        if isinstance(new_weapon, Weapon):
            self._weapon = new_weapon
        else:
            print("Not a valid instance of Weapon")

    @property
    def armor(self) -> Optional[Armor]:
        """
        an armor getter
        """

        return self._armor

    @armor.setter
    def armor(self, new_armor: Armor) -> None:
        if isinstance(new_armor, Armor):
            self._armor = new_armor
        else:
            print("Not a valid instance of Armor")

    def get_damage(self, damage: float) -> None:
        """
        вычисление полученного урона персонажем (см. шаг IV)
        """

        self.health = round(self.health - damage, 1)

    def get_stamina_mod(self) -> float:
        return self.unit_class.get_stamina_mod()

    def stamina_for_defend_enough(self) -> bool:
        return self.stamina >= self.armor.stamina_per_turn

    def stamina_for_attack_enough(self) -> bool:
        return self.stamina >= self.weapon.stamina_per_hit

    def _get_final_damage(self, other: BaseUnit) -> float:
        """
        calculates the final damage of an attack
        """

        damage_from_weapon = uniform(self.weapon.min_damage, self.weapon.max_damage)
        attacking_damage = round(damage_from_weapon * self.unit_class.attack, 1)

        _armor = other.armor.defence * other.unit_class.armor
        target_armor = _armor if other.stamina_for_defend_enough() else 0.0

        return round(max(attacking_damage - target_armor, 0.0), 1)

    def attack(self, other: BaseUnit) -> str:
        """
        нанести удар (см. шаг IV)
        """

        if not self.stamina_for_attack_enough():
            return (
                f"{self.name} пытался использовать {self.weapon.name},"
                f" но у него не хватило выносливости"
            )

        final_damage = self._get_final_damage(other)
        other.get_damage(final_damage)

        self.stamina -= self.weapon.stamina_per_hit
        other.stamina -= other.armor.stamina_per_turn

        if final_damage > 0:
            return (
                f"{self.name}, используя {self.weapon.name},"
                f" пробивает {other.armor.name} соперника и наносит {final_damage} урона"
            )
        return (
            f"{self.name}, используя {self.weapon.name}, наносит удар,"
            f" но {other.armor.name} соперника его останавливает"
        )

    def use_skill(self, other: BaseUnit) -> str:
        """
        применение умения к цели (см. шаг IV)
        """

        if self.skill_used:
            return "Навык уже использован"

        # if stamina is enough:
        if self.stamina >= self.unit_class.get_required_stamina():
            self.skill_used = True
            other.get_damage(self.unit_class.skill.damage)
            return (
                f"{self.name} использует {self.unit_class.get_skill_name()}"
                f" и наносит {self.unit_class.skill.damage} урона сопернику"
            )
        return (
            f"{self.name} пытался использовать {self.unit_class.get_skill_name()},"
            f" но у него не хватило выносливости"
        )

    def regenerate_stamina(self, factor: float) -> None:
        self.stamina = min(
            round(self.stamina + factor * self.get_stamina_mod(), 1),
            self.unit_class.max_stamina,
        )


class HumanPlayer(BaseUnit):
    """
    A human player's class
    """


class CompPlayer(BaseUnit):
    """
    A computer player's class
    """

    def attack_or_use_skill(self, other: BaseUnit) -> str:
        if (
            randint(1, 10) == 5
        ) and not self.skill_used:  # 10% chance to use the hero's skill
            return self.use_skill(other)
        return self.attack(other)


if __name__ == "__main__":
    equipment = Equipment()

    hero = HumanPlayer("Отважный герой", warrior, 10.0, 10.0)
    hero.weapon = equipment.get_weapon("топорик")
    hero.armor = equipment.get_armor("кожаная броня")
    print(hero)

    enemy = CompPlayer("Гнусный вор", thief, 10.0, 10.0)
    enemy.weapon = equipment.get_weapon("ножик")
    enemy.armor = equipment.get_armor("футболка")
    print(enemy)

    print("Turn #1")
    print(hero.attack(enemy))
    print(hero)
    print(enemy)

    print("Turn #2")
    print(enemy.attack(hero))
    print(hero)
    print(enemy)

    print("Turn #3")
    print(hero.attack(enemy))
    print(hero)
    print(enemy)

    print("Turn #4")
    print(enemy.attack(hero))
    print(hero)
    print(enemy)

    print("Turn #5")
    print(hero.use_skill(enemy))
    print(hero)
    print(enemy)

    print("Turn #6")
    print(enemy.attack_or_use_skill(hero))
    print(hero)
    print(enemy)

    print("Turn #7")
    print(hero.use_skill(enemy))
    print(hero)
    print(enemy)

    # hero2 = BaseUnit("hero2", "hero2", 10.0, 10.0)
    # print(hero2)
