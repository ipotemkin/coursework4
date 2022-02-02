"""This module contains skill classes for the application"""

from abc import ABC, abstractmethod
from typing import Optional

# from app.unit import BaseUnit


class Skill(ABC):
    """
    abstract class for skills
    """

    def __init__(self, name: str, damage: float, stamina: float):
        self.name = name
        self.damage = damage
        self.required_stamina = stamina

    def __repr__(self) -> str:
        return f"{self.name} (damage={self.damage}, stamina={self.required_stamina})"

    @abstractmethod
    def skill_effect(self) -> None:
        """
        for creating skills
        """

    # @abstractmethod
    def use(self, user: str, target: str) -> Optional[str]:
        """
        to use the class skill after checking the user's stamina
        """

        # if user.stamina >= self.required_stamina:
        #     return self.skill_effect()
        # return f"{user.name} попытался использовать {self.name},
        # но у него не хватило выносливости."

    def get_required_stamina(self) -> float:
        return self.required_stamina

    def get_skill_name(self) -> str:
        return self.name


class ConcreteSkill(Skill):
    """
    to create a skill
    """

    def skill_effect(self) -> None:
        pass

    # def use(self, user: Any, target: Any) -> None:
    #     pass
