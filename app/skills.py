"""This module contains skill classes for the application"""

from abc import ABC, abstractmethod
from typing import Any


class Skill(ABC):
    """
    abstract class for skills
    """

    damage_name: str
    required_stamina: str

    @abstractmethod
    def skill_effect(self) -> None:
        """
        for creating skills
        """

    @abstractmethod
    def use(self, user: Any, target: Any) -> None:
        """
        to use the class skill after checking the user's stamina
        """


class ConcreteSkill(Skill):
    """
    to create a skill
    """

    def skill_effect(self) -> None:
        pass

    def use(self, user: Any, target: Any) -> None:
        pass
