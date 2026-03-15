import time


class Synapse:
    """
    Класс синапса - имитирует связь между нейронами в мозге.
    Хранит вес связи и историю активаций.
    """

    def __init__(self, pre_neuron_id: str, post_neuron_id: str, weight: float = 0.1):
        """
        Инициализация синапса

        Args:
            pre_neuron_id: ID нейрона-источника (пресинаптический нейрон)
            post_neuron_id: ID нейрона-приемника (постсинаптический нейрон)
            weight: сила связи (0.0 - 1.0)
        """
        self.pre_id = pre_neuron_id
        self.post_id = post_neuron_id
        self.weight = weight  # Сила связи (0.0 - 1.0)
        self.history = []  # История активаций (для сложного обучения)
        self.age = 0  # Возраст синапса (количество обновлений)
        self.created_at = time.time()
        self.last_activated = time.time()

    def strengthen(self, amount: float = 0.1):
        """
        Долговременная потенциация (LTP) - укрепление связи
        Имитирует процесс запоминания

        Args:
            amount: величина укрепления
        """
        self.weight = min(1.0, self.weight + amount)
        self.history.append(('strengthen', amount, time.time()))
        self.age += 1

    def weaken(self, amount: float = 0.05):
        """
        Долговременная депрессия (LTD) - ослабление связи
        Имитирует процесс забывания

        Args:
            amount: величина ослабления
        """
        self.weight = max(0.0, self.weight - amount)
        self.history.append(('weaken', amount, time.time()))
        self.age += 1

    def fire(self, activation_level: float = 1.0) -> float:
        """
        Активация синапса (передача сигнала)

        Args:
            activation_level: уровень активации пресинаптического нейрона (0.0 - 1.0)

        Returns:
            float: сила прошедшего сигнала с учетом веса синапса
        """
        self.last_activated = time.time()

        # Сигнал ослабляется пропорционально весу синапса
        signal = activation_level * self.weight

        # Записываем в историю
        self.history.append(('fire', signal, time.time()))

        # Синапс "стареет" при каждом использовании
        self.age += 1

        return signal

    def get_efficiency(self) -> float:
        """
        Получить эффективность синапса с учетом возраста

        Returns:
            float: эффективность (0.0 - 1.0)
        """
        # Со временем синапс может деградировать, если не используется
        time_since_last = time.time() - self.last_activated
        decay = min(0.5, time_since_last / (3600 * 24 * 30))  # 30 дней для полной деградации
        return self.weight * (1 - decay)

    def get_info(self) -> dict:
        """
        Получить информацию о синапсе

        Returns:
            dict: словарь с параметрами синапса
        """
        return {
            'pre_neuron': self.pre_id,
            'post_neuron': self.post_id,
            'weight': self.weight,
            'age': self.age,
            'efficiency': self.get_efficiency(),
            'history_length': len(self.history),
            'created_at': time.ctime(self.created_at),
            'last_activated': time.ctime(self.last_activated)
        }

    def __repr__(self) -> str:
        return f"Synapse({self.pre_id[:6]} → {self.post_id[:6]}, weight={self.weight:.3f})"