"""This module contains skill classes for the application"""

from dataclasses import dataclass


@dataclass
class Skill:
    """
    abstract class for skills
    """

    name: str
    damage: float
    required_stamina: float

    def get_required_stamina(self) -> float:
        """
        returns the skill's stamina required
        """

        return self.required_stamina

    def get_name(self) -> str:
        """
        returns the skill's name
        """

        return self.name


class ConcreteSkill(Skill):
    """
    to create a skill
    """
