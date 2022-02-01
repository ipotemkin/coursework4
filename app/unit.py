"""Sets up a hero's logics"""

from abc import ABC, abstractmethod

# from dataclasses import dataclass
from typing import Optional

# from app.classes import UnitClass
from app.equipment import Weapon, Armor


# @dataclass
class BaseUnit(ABC):
    """
    an abstract class for a hero
    """

    # name: str
    # hero: UnitClass
    # health: float
    # stamina: float
    # _weapon: Weapon
    # _armor: Armor
    # skill_used: bool

    def __init__(self, name: str, hero: str, health: float, stamina: float):
        self.name = name
        self.hero = hero
        self.health = health
        self.stamina = stamina
        self._weapon: Optional[Weapon] = None
        self._armor: Optional[Armor] = None
        self.skill_used: bool = False

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

    def _get_final_damage(self) -> None:
        """
        вычисление итогового урона (см. шаг IV)
        """

        # TODO

    def get_damage(self) -> float:
        """
        вычисление полученного урона персонажем (см. шаг IV)
        """

        # TODO
        return 1.0

    def use_skill(self) -> str:
        """
        применение умения к цели (см. шаг IV)
        """

        # TODO
        if self.skill_used:
            return "Навнык уже использован"
        self.skill_used = True
        # if stamina is enough:
        return f"{self.name} использует <skill's name> и наносит <урон> урона сопернику"
        # else:
        #     return f"{self.name} пыталтся использовать <skill's name>," \
        #            f" но у него не хватило выносливости"

    @abstractmethod
    def attack(self) -> str:
        """
        нанести удар (см. шаг IV)
        """

        return f"{self.name} атакует"


# class Unit(BaseUnit):
#     """
#     a hero unit
#     """
#
#     def attack(self) -> None:
#         pass

# unit = BaseUnit("", UnitClass(), 0.0, 0.0, "", "", False)


class HumanPlayer(BaseUnit):
    """
    A human player's class
    """

    def attack(self) -> str:
        # TODO
        return ""


class CompPlayer(BaseUnit):
    """
    A computer player's class
    """

    def attack(self) -> str:
        if not self.skill_used:
            self.use_skill()
        # TODO
        # if stamina is not enough:
        #     return f"{self.name} пыталься использовать <название оружия>," \
        #            f" но у него не хватило выносливости"
        # if armor is breached:
        return (
            f"{self.name}, используя {self.weapon.name},"
            f" пробивает {self.armor.name} соперника"
            f" и наносит {self.get_damage()} урона"
        )
        # else:
        #     return (
        #         f"{self.name}, используя {self.weapon.name}, наносит удар, но <название брони>"
        #         f"соперника его останавливает"
        #     )
