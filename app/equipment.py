"""This module contains equipment classes for the application"""

import sys
import os
import json
from pydantic.dataclasses import dataclass

from app.const import EQUIPMENT_FILE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EQUIPMENT_FILE_WITH_PATH = os.path.join(BASE_DIR, EQUIPMENT_FILE)


@dataclass
class Weapon:
    """
    to store a weapon's data
    """

    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float  # stamina consumption per hit


@dataclass
class Armor:
    """
    to store an armor's data
    """

    id: int
    name: str
    defence: float
    stamina_per_turn: float  # stamina consumption per turn


@dataclass
class EquipmentData:
    """
    to store the parsed equipment data
    """

    weapons: list[Weapon]
    armors: list[Armor]


class Equipment:
    """
    to get data from a JSON file and store in an object
    to interact with a character
    """

    def __init__(self, file_name: str = EQUIPMENT_FILE_WITH_PATH):
        try:
            self.equipment: EquipmentData = EquipmentData(**self._read_json(file_name))
        except (TypeError, AttributeError) as error:
            print("Error while parsing the JSON file:", error)
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

    def get_weapon(self, weapon_name: str) -> Weapon:
        """
        returns a weapon with the specified name
        """

        for weapon in self.equipment.weapons:
            if weapon.name == weapon_name:
                return weapon
        return NotImplemented

    def get_armor(self, armor_name: str) -> Armor:
        """
        returns an armor with the specified name
        """

        for armor in self.equipment.armors:
            if armor.name == armor_name:
                return armor
        return NotImplemented

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
    print(equipment.get_weapon("??????????????"))
    print(equipment.get_armor("??????????????"))
