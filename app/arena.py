""" Contains SingleTone and Arena"""

from __future__ import annotations

from threading import Lock
from typing import Optional, Dict, Any

from app.unit import HumanPlayer, CompPlayer
from app.const import STAMINA_RECOVER_PER_TURN


class SingletonMeta(type):
    """
    Это потокобезопасная реализация класса Singleton.
    """

    _instances: Dict[SingletonMeta, SingletonMeta] = {}

    _lock: Lock = Lock()
    """
    объект-блокировка для синхронизации потоков во время
    первого доступа к Одиночке.
    """

    def __call__(cls, *args: Any, **kwargs: Any) -> SingletonMeta:
        """
        Данная реализация не учитывает возможное изменение передаваемых
        аргументов в `__init__`.
        """
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=SingletonMeta):
    """
    provides interaction between players
    """

    def __init__(self, stamina: float = STAMINA_RECOVER_PER_TURN):
        self.stamina = stamina
        self.hero: Optional[HumanPlayer] = None
        self.enemy: Optional[CompPlayer] = None
        self.game_on = False

    def start_game(self) -> None:
        # TODO
        # присваивает экземпляру класса Арена значение свойства Игрок и значение свойства Противник
        self.game_on = True

    def is_game_on(self) -> bool:
        return self.game_on

    def end_game(self) -> str:
        self.game_on = False
        return "Бой окончен!"

    def regenerate_stamina(self) -> None:
        self.hero.regenerate_stamina(self.stamina)
        self.enemy.regenerate_stamina(self.stamina)

        # - Прибавляем к очкам выносливости атакующего константу, умноженную на модификатор
        # выносливости **атакующего.**
        # - Прибавляем к очкам выносливости цели константу, умноженную на модификатор
        # выносливости **цели.**

    def check_health(self) -> str:
        if (self.hero.health > 0.0) and (self.enemy.health > 0.0):
            return ""
        self.game_on = False
        if (self.hero.health < 0.0) and (self.enemy.health < 0.0):
            return "Ничья"
        if self.enemy.health < 0.0:
            return "Победил Игрок"
        return "Победил Противник"

    def check_health_and_regenerate(self, res: str):
        if check_msg := self.check_health():
            return res + check_msg
        self.regenerate_stamina()
        return res

    def complete_turn(self, res: str) -> str:
        res = self.check_health_and_regenerate(res)
        res += self.enemy.attack_or_use_skill(self.hero)
        return self.check_health_and_regenerate(res)

    def attack(self) -> str:
        if not self.game_on:
            return self.end_game()
        res = self.hero.attack(self.enemy)
        return self.complete_turn(res)

    def use_skill(self) -> str:
        if not self.game_on:
            return self.end_game()
        res = self.hero.use_skill(self.enemy)
        return self.complete_turn(res)

    def skip_turn(self) -> str:
        return self.complete_turn("")
