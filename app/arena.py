""" Contains SingleTone and Arena"""

from threading import Lock

# , Thread

from app.unit import HumanPlayer, CompPlayer
from app.const import STAMINA_RECOVER_PER_TURN


class SingletonMeta(type):
    """
    Это потокобезопасная реализация класса Singleton.
    """

    _instances = {}

    _lock: Lock = Lock()
    """
    У нас теперь есть объект-блокировка для синхронизации потоков во время
    первого доступа к Одиночке.
    """

    def __call__(cls, *args, **kwargs):
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
        hero: HumanPlayer,
        enemy: CompPlayer,
        stamina: float = STAMINA_RECOVER_PER_TURN,
    ):
        self.stamina = stamina
        self.hero = hero
        self.enemy = enemy
        self.game_on = False

    def start_game(self) -> None:
        # TODO
        # присваивает экземпляру класса Арена значение свойства Игрок и значение свойства Противник
        self.game_on = True

    def next_turn(self) -> str:
        # проверка, осталось ли еще здоровье у игроков.
        if self.check_health():
            self.regenerate_stamina()
            # TODO
            # противник наносит удар
            # и снова наступает ход игрока
            return ""
        return self.end_game()
        # Если да, тогда происходит восстановление выносливости игроков, противник наносит удар,
        # и снова наступает ход игрока. Если нет, тогда метод «Проверка здоровья игроков» возвращает
        # строку с результатом боя.

    def regenerate_stamina(self) -> None:
        self.hero.stamina = self.stamina * self.hero.get_stamina_mod()
        self.enemy.stamina = self.stamina * self.enemy.get_stamina_mod()

        # - Прибавляем к очкам выносливости атакующего константу, умноженную на модификатор
        # выносливости **атакующего.**
        # - Прибавляем к очкам выносливости цели константу, умноженную на модификатор
        # выносливости **цели.**

    def check_health(self) -> bool:
        return (self.hero.health > 0.0) and (self.enemy.health > 0.0)

    def end_game(self) -> str:
        # TODO
        return "Game results"

    def attack(self) -> str:
        self.next_turn()
        return "Results"

    def use_skill(self) -> str:
        self.next_turn()
        return "Results"
