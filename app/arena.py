""" Contains SingleTone and Arena"""

from threading import Lock

# , Thread

from app.unit import HumanPlayer, CompPlayer


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

    def __init__(self, stamina: float, hero: HumanPlayer, enemy: CompPlayer):
        self.stamina = stamina
        self.hero = hero
        self.enemy = enemy
        self.game_on = False

    def start_game(self):
        # TODO
        self.game_on = True

    def next_turn(self):
        pass

    def regenerate_stamina(self):
        pass

    def check_health(self) -> None:
        """
        Ends the game if the players' health <= 0
        """

        if self.hero.health <= 0.0 or self.enemy.health <= 0.0:
            self.end_game()

    def end_game(self) -> str:
        # TODO
        return "Game results"

    def attack(self) -> str:
        self.next_turn()
        return "Results"

    def use_skill(self) -> str:
        self.next_turn()
        return "Results"
