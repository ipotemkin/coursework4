"""This module contains classes for the application"""

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
    stamina: float  # модификатор выносливости
    armor: float  # модификатор защиты
    skill: Optional[ConcreteSkill] = None


class MetaUnitClass(type):
    """
    A metaclass to provide child classes with iteration and length calculation
    """

    instances: List[ProUnitClass] = []

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

    # def __iter__(self):
    #     return (instance for instance in self.__class__.instances)

    # def __len__(self):
    #     return len(self.items)
    #
    # def __getitem__(self, item):
    #     return self.items[item]


# ferocious_kick = ConcreteSkill(name="Свирепый пинок", damage=12.0, stamina=6.0)


warrior = UnitClass(
    name="Воин",
    max_health=60.0,
    max_stamina=30.0,
    attack=0.8,
    stamina=0.9,
    armor=1.2,
)

ranger = UnitClass(
    name="Рейнджер",
    max_health=60.0,
    max_stamina=30.0,
    attack=0.8,
    stamina=0.9,
    armor=1.2,
)

thief = UnitClass(
    name="Вор",
    max_health=50.0,
    max_stamina=25.0,
    attack=1.5,
    stamina=1.2,
    armor=1.0,
)

if __name__ == "__main__":
    print([item.name for item in UnitClass.instances])
    print(UnitClass[0])
    print(UnitClass[0].name)
    print(len(UnitClass))
    print(UnitClass.get_unit_names())
    for unit in UnitClass:
        print(unit)

    # print([item.name for item in MetaUnitClass.items])
