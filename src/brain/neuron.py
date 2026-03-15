# src/brain/neuron.py
import time
import hashlib


class Neuron:
    """Класс нейрона - базовая единица знания"""

    def __init__(self, uid: str = None, content: str = "", category: str = "general"):
        if uid is None:
            unique_string = f"{content}{time.time()}"
            self.uid = hashlib.md5(unique_string.encode()).hexdigest()[:8]
        else:
            self.uid = uid

        self.content = content
        self.category = category

        # Биологические параметры
        self.activation_level = 0.0
        self.threshold = 0.5
        self.rest_potential = 0.1
        self.refractory_period = False
        self.last_fired_time = 0

        # Статистика
        self.firing_count = 0
        self.created_at = time.time()
        self.last_access = time.time()

    def stimulate(self, input_signal: float) -> float:
        """Стимуляция нейрона"""
        current_time = time.time()
        self.last_access = current_time

        if self.refractory_period:
            if current_time - self.last_fired_time > 0.1:
                self.refractory_period = False
            else:
                return 0.0

        self.activation_level += input_signal
        self.activation_level *= 0.95

        if self.activation_level >= self.threshold:
            return self.fire()
        return 0.0

    def fire(self) -> float:
        """Срабатывание нейрона"""
        self.firing_count += 1
        self.last_fired_time = time.time()
        self.refractory_period = True

        output = self.activation_level * 1.5
        self.activation_level = self.rest_potential
        return min(1.0, output)

    def learn(self, reinforcement: float):
        """Обучение нейрона"""
        if reinforcement > 0:
            self.threshold = max(0.3, self.threshold - 0.01)
        else:
            self.threshold = min(0.8, self.threshold + 0.01)

    def get_info(self) -> dict:
        return {
            'uid': self.uid,
            'content': self.content[:50] + '...' if len(self.content) > 50 else self.content,
            'category': self.category,
            'activation': self.activation_level,
            'firing_count': self.firing_count
        }

    def __repr__(self) -> str:
        return f"Neuron({self.uid}: {self.content[:30]}...)"