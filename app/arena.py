""" Contains SingleTone and Arena"""

from __future__ import annotations

from threading import Lock

# , Thread

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
    У нас теперь есть объект-блокировка для синхронизации потоков во время
    первого доступа к Одиночке.
    """

    def __call__(cls, *args: Any, **kwargs: Any) -> SingletonMeta:
        """
        Данная реализация не учитывает возможное изменение передаваемых
        аргументов в `__init__`.
        """
        # Теперь представьте, что программа была только-только запущена.
        # Объекта-одиночки ещё никто не создавал, поэтому несколько потоков
        # вполне могли одновременно пройти через предыдущее условие и достигнуть
        # блокировки. Самый быстрый поток поставит блокировку и двинется внутрь
        # секции, пока другие будут здесь его ожидать.
        with cls._lock:
            # Первый поток достигает этого условия и проходит внутрь, создавая
            # объект-одиночку. Как только этот поток покинет секцию и освободит
            # блокировку, следующий поток может снова установить блокировку и
            # зайти внутрь. Однако теперь экземпляр одиночки уже будет создан и
            # поток не сможет пройти через это условие, а значит новый объект не
            # будет создан.
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=SingletonMeta):
    """
    provides interaction between players
    """

    def __init__(
        self,
        # hero: HumanPlayer,
        # enemy: CompPlayer,
        stamina: float = STAMINA_RECOVER_PER_TURN,
    ):
        self.stamina = stamina
        self.hero: Optional[HumanPlayer] = None
        self.enemy: Optional[CompPlayer] = None
        self.game_on = False

    def start_game(self) -> None:
        # TODO
        # присваивает экземпляру класса Арена значение свойства Игрок и значение свойства Противник
        self.game_on = True

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
            return ". Ничья"
        if self.enemy.health < 0.0:
            return ". Победил Игрок"
        return ". Победил Противник"

    @staticmethod
    def end_game() -> str:
        return "Бой окончен!"

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

    def complete_turn(self, res: str) -> str:
        if check_msg := self.check_health():
            return res + check_msg
        self.regenerate_stamina()
        res += self.enemy.attack_or_use_skill(self.hero)
        if check_msg := self.check_health():
            return res + check_msg
        self.regenerate_stamina()
        return res
