"""Sets up a hero's logics"""

# from abc import ABC, abstractmethod

from dataclasses import dataclass
from typing import Optional

from random import uniform, randint

from app.classes import UnitClass
from app.equipment import Weapon, Armor


# @dataclass
# class ProBaseUnit:
#     """
#     a pro class for a BaseUnit to use benefits of dataclasses
#     """
#
#     name: str
#     hero_type: UnitClass
#     health: float
#     stamina: float
#     _weapon: Optional[Weapon] = None
#     _armor: Optional[Armor] = None
#     skill_used: bool = False


# @dataclass  # – here mypy raises an error:
# Only concrete class can be given where "Type[BaseUnit]" is expected
@dataclass
class BaseUnit:
    """
    an abstract class for a hero
    """

    # use this block with @dataclass in line 27
    name: str
    hero_type: UnitClass
    health: float
    stamina: float
    _weapon: Optional[Weapon] = None
    _armor: Optional[Armor] = None
    skill_used: bool = False

    # def __init__(self, name: str, hero: str, health: float, stamina: float):
    #     self.name = name
    #     self.hero = hero
    #     self.health = health
    #     self.stamina = stamina
    #     self._weapon: Optional[Weapon] = None
    #     self._armor: Optional[Armor] = None
    #     self.skill_used: bool = False

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

    # def _get_final_damage(self) -> None:
    #     """
    #     вычисление итогового урона (см. шаг IV)
    #     """
    #
    #     # TODO

    def get_damage(self, damage: float) -> None:
        """
        вычисление полученного урона персонажем (см. шаг IV)
        """

        self.health -= damage

    # @abstractmethod
    # def attack(self, other: ProBaseUnit) -> str:
    #     pass

    # def attack(self, other: ProBaseUnit) -> str:
    #     """
    #     нанести удар (см. шаг IV)
    #     """
    #
    #     if self.stamina < self.weapon.stamina_per_hit:
    #         return f"{self.name} пытался использовать {self.weapon.name}," \
    #                f" но у него не хватило выносливости"
    #
    #     damage_from_weapon = uniform(self.weapon.min_damage, self.weapon.max_damage*10)
    #     attacking_damage = round(damage_from_weapon * self.hero_type.attack, 1)
    #
    #     if other.stamina < other._armor.stamina_per_turn:
    #         target_armor = 0.0
    #     else:
    #         target_armor = other._armor.defence * other.hero_type.armor
    #
    #     final_damage = attacking_damage - target_armor
    #
    #     other.health -= final_damage
    #
    #     self.stamina -= self.weapon.stamina_per_hit
    #     other.stamina -= other._armor.stamina_per_turn
    #
    #     return ""
    #     # return f"{self.name} атакует"

    def get_stamina_mod(self) -> float:
        return self.hero_type.get_stamina_mod()

    def stamina_for_defend_enough(self) -> bool:
        return self.stamina >= self.armor.stamina_per_turn

    def stamina_for_attack_enough(self) -> bool:
        return self.stamina >= self.weapon.stamina_per_hit


class Unit(BaseUnit):
    """
    a hero unit
    derived from BaseUnit in order to use BaseUnit type as arguments
    """

    def _get_final_damage(self, other: BaseUnit) -> float:
        """
        calculates the final damage of an attack
        """

        damage_from_weapon = uniform(self.weapon.min_damage, self.weapon.max_damage)
        attacking_damage = round(damage_from_weapon * self.hero_type.attack, 1)

        if other.stamina_for_defend_enough():
            target_armor = other.armor.defence * other.hero_type.armor
        else:
            target_armor = 0.0

        return max(attacking_damage - target_armor, 0.0)

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

        # TODO
        if self.skill_used:
            return "Навык уже использован"

        # if stamina is enough:
        if self.stamina >= self.hero_type.get_required_stamina():
            self.skill_used = True
            other.get_damage(self.hero_type.skill.damage)

            return (
                f"{self.name} использует {self.hero_type.get_skill_name()}"
                f" и наносит {self.hero_type.skill.damage} урона сопернику"
            )
        return (
            f"{self.name} пыталтся использовать {self.hero_type.get_skill_name()},"
            f" но у него не хватило выносливости"
        )


# unit = BaseUnit("", UnitClass(), 0.0, 0.0, "", "", False)


class HumanPlayer(Unit):
    """
    A human player's class
    """

    # def attack(self) -> str:
    #     # TODO
    #     return ""


class CompPlayer(Unit):
    """
    A computer player's class
    """

    def attack_or_use_skill(self, other: BaseUnit) -> str:
        if (randint(1, 10) == 5) and not self.skill_used:  # 10% chance to use the hero's skill
            return self.use_skill(other)
        return self.attack(other)

    # def attack(self) -> str:
    #     if not self.skill_used:
    #         self.use_skill()
    #     # TODO
    #     # if stamina is not enough:
    #     #     return f"{self.name} пыталься использовать <название оружия>," \
    #     #            f" но у него не хватило выносливости"
    #     # if armor is breached:
    #     return (
    #         f"{self.name}, используя {self.weapon.name},"
    #         f" пробивает {self.armor.name} соперника"
    #         f" и наносит {self.get_damage()} урона"
    #     )
    #     # else:
    #     #     return (
    #     #         f"{self.name}, используя {self.weapon.name}, наносит удар, но <название брони>"
    #     #         f"соперника его останавливает"
    #     #     )


if __name__ == "__main__":
    hero_type = HumanPlayer("hero", "hero", 10.0, 10.0)
    print(hero_type)
    # hero2 = BaseUnit("hero2", "hero2", 10.0, 10.0)
    # print(hero2)
