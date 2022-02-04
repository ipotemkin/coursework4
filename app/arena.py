""" Contains SingleTone and Arena"""

from __future__ import annotations

from threading import Lock
from typing import Dict, Any

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
        self.hero: HumanPlayer = NotImplemented
        self.enemy: CompPlayer = NotImplemented
        self.game_on = False

    def start_game(self) -> None:
        """
        sets game_on to True to signal the game started
        being used to show correct messages during the game and to discard other game's instances
        """
        self.game_on = True

    def is_game_on(self) -> bool:
        """
        returns True if the game is on or False if not
        """

        return self.game_on

    def end_game(self) -> str:
        """
        ends the game
        """

        self.game_on = False
        return "Бой окончен!"

    def regenerate_stamina(self) -> None:
        """
        regenerates the players' stamina
        """

        if not isinstance(self.hero, type(NotImplemented)):
            self.hero.regenerate_stamina(self.stamina)
        if not isinstance(self.enemy, type(NotImplemented)):
            self.enemy.regenerate_stamina(self.stamina)

        # - Прибавляем к очкам выносливости атакующего константу, умноженную на модификатор
        # выносливости **атакующего.**
        # - Прибавляем к очкам выносливости цели константу, умноженную на модификатор
        # выносливости **цели.**

    def check_health(self) -> str:
        """
        checks the players' health
        returns "" if OK, or the result of the game
        """

        try:
            if (self.hero.health > 0.0) and (self.enemy.health > 0.0):
                return ""
            self.end_game()
            if (self.hero.health < 0.0) and (self.enemy.health < 0.0):
                return "Ничья"
            if self.enemy.health < 0.0:
                return "Победил Игрок"
            return "Победил Противник"
        except AttributeError as error:
            raise NotImplementedError from error

    def check_health_and_regenerate(self, res: str) -> str:
        """
        checks and regenerates the players' health
        :returns the actions results string
        """

        if check_msg := self.check_health():
            return res + check_msg
        self.regenerate_stamina()
        return res

    def complete_turn(self, res: str) -> str:
        """
        completes the current turn
        used not to repeat the same code in attack(), use_skill() and skip_turn()
        :returns the turn results string
        """

        try:
            res = self.check_health_and_regenerate(res)
            if self.is_game_on():
                res += self.enemy.attack_or_use_skill(self.hero)
                return self.check_health_and_regenerate(res)
            return res
        except AttributeError as error:
            raise NotImplementedError from error

    def attack(self) -> str:
        """
        to conduct the player's attack and all the steps to complete the turn
        :returns the attack results string
        """

        if not self.game_on:
            return self.end_game()
        try:
            res = self.hero.attack(self.enemy)
        except AttributeError as error:
            raise NotImplementedError from error
        return self.complete_turn(res)

    def use_skill(self) -> str:
        """
        to apply the player's skill and do all the steps to complete the turn
        :returns the action results string
        """

        if not self.is_game_on():
            return self.end_game()
        try:
            res = self.hero.use_skill(self.enemy)
        except AttributeError as error:
            raise NotImplementedError from error
        return self.complete_turn(res)

    def skip_turn(self) -> str:
        """
        to apply the player's skip turn and do all the steps to complete the turn
        :returns the skip turn results string
        """

        return self.complete_turn("")
