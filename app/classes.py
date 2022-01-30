"""This module contains classes for the application"""

from dataclasses import dataclass

from app.skills import ConcreteSkill


@dataclass
class UnitClass:
    """
    A base class for heroes
    """

    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: ConcreteSkill
