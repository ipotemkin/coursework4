"""
This module contains classes for heroes' types (to not confuse with python classes)
1. ProUnitClass - a parent dataclass to get it easy (using all benefits of dataclasses
2. MetaUnitClass - a meta class to implement a list of instances of the class
3. UnitClass - a base class to build heroes' types
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List, Generator, Any

from app.skills import ConcreteSkill


@dataclass
class ProUnitClass:
    """
    A predecessor for the heroes' base class
    """

    name: str
    max_health: float
    max_stamina: float
    attack: float  # модификатор атаки
    stamina_mod: float  # модификатор выносливости
    armor: float  # модификатор защиты
    skill: ConcreteSkill = NotImplemented

    def get_stamina_mod(self) -> float:
        """
        to get a stamina modifier
        """

        return self.stamina_mod

    def get_required_stamina(self) -> float:
        """
        to get a required stamina of the skill
        """

        return self.skill.get_required_stamina()

    def get_skill_name(self) -> str:
        """
        to get the skill name
        """

        return self.skill.get_skill_name()


class MetaUnitClass(type):
    """
    A metaclass to provide child classes with iteration and length calculation
    """

    instances: List[UnitClass] = []

    def __getitem__(cls, index: int) -> ProUnitClass:
        return cls.instances[index]

    def __len__(cls) -> int:
        return len(cls.instances)

    def __iter__(cls) -> Generator:
        return (instance for instance in cls.__class__.instances)


class UnitClass(ProUnitClass, metaclass=MetaUnitClass):
    """
    Heroes' classes
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__class__.instances.append(self)

    @classmethod
    def get_unit_names(cls) -> List[str]:
        """
        To get a list of the class instances' names
        """

        return [instance.name for instance in cls.instances]

    @classmethod
    def get_unit_by_name(cls, name: str) -> Optional[UnitClass]:
        """
        To get a instance with the specified name
        """

        for instance in cls.instances:
            if instance.name == name:
                return instance
        return None


# heroes types (classes) implementation ---------------------------------------------

ferocious_kick = ConcreteSkill(name="Свирепый пинок", damage=12.0, stamina=6.0)
stiff_shot = ConcreteSkill(name="Мощный укол", damage=15.0, stamina=5.0)
tickling = ConcreteSkill(name="Щекотка", damage=5.0, stamina=3.0)

warrior = UnitClass(
    name="Воин",
    max_health=60.0,
    max_stamina=30.0,
    attack=0.8,
    stamina_mod=0.9,
    armor=1.2,
    skill=stiff_shot,
)

ranger = UnitClass(
    name="Рейнджер",
    max_health=60.0,
    max_stamina=30.0,
    attack=0.8,
    stamina_mod=0.9,
    armor=1.2,
    skill=ferocious_kick,
)

thief = UnitClass(
    name="Вор",
    max_health=50.0,
    max_stamina=25.0,
    attack=1.5,
    stamina_mod=1.2,
    armor=1.0,
    skill=tickling,
)

# for debug only
if __name__ == "__main__":
    print([item.name for item in UnitClass.instances])
    print(UnitClass[0])
    print(UnitClass[0].name)
    print(len(UnitClass))
    print(UnitClass.get_unit_names())
    for unit in UnitClass:
        print(unit)

    # print([item.name for item in MetaUnitClass.items])
