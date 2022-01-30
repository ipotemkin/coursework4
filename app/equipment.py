"""This module contains equipment classes for the application"""

# from dataclasses import dataclass
import sys
import json
from typing import List, Optional
from pydantic.dataclasses import dataclass

from app.const import EQUIPMENT_FILE


@dataclass
class Weapon:
    """
    to store a weapon's data
    """

    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float


@dataclass
class Armor:
    """
    to store an armor's data
    """

    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class EquipmentData:
    """
    to store the parsed equipment data
    """

    weapons: List[Weapon]
    armors: List[Armor]


class Equipment:
    """
    to get data from a JSON file and store in an object
    """

    def __init__(self, file_name: str = EQUIPMENT_FILE):
        # self.equipment = EquipmentData(**self._read_json(file_name))
        try:
            self.equipment = EquipmentData(**self._read_json(file_name))
        except (TypeError, AttributeError) as error:
            print("Error while parsinng the JSON file:", error)
            # raise ValueError
            sys.exit(1)

    @staticmethod
    def _read_json(file_name: str) -> dict:
        try:
            with open(file_name, "r", encoding="utf-8") as file_handler:
                data = json.load(file_handler)
        except FileNotFoundError as error:
            print(error)
            sys.exit(1)
        return data

    def get_weapon(self, weapon_name: str) -> Optional[Weapon]:
        """
        returns a weapon with the specified name
        """

        for weapon in self.equipment.weapons:
            if weapon.name == weapon_name:
                return weapon
        return None

    def get_armor(self, armor_name: str) -> Optional[Armor]:
        """
        returns an armor with the specified name
        """

        for armor in self.equipment.armors:
            if armor.name == armor_name:
                return armor
        return None

    def get_weapon_names(self) -> list:
        """
        returns weapons' names
        """

        return [weapon.name for weapon in self.equipment.weapons]

    def get_armor_names(self) -> list:
        """
        returns armors' names
        """

        return [armor.name for armor in self.equipment.armors]


# for debug only
if __name__ == "__main__":
    equipment = Equipment()
    print(equipment.equipment)
    print("armors:", equipment.get_armor_names())
    print("weapons:", equipment.get_weapon_names())
    print(equipment.get_weapon("ладошки"))
    print(equipment.get_armor("панцирь"))
