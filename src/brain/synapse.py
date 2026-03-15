# src/brain/synapse.py
import time


class Synapse:
    """Класс синапса - связь между нейронами"""

    def __init__(self, pre_neuron_id: str, post_neuron_id: str, weight: float = 0.1):
        self.pre_id = pre_neuron_id
        self.post_id = post_neuron_id
        self.weight = weight
        self.history = []
        self.age = 0
        self.created_at = time.time()
        self.last_activated = time.time()

    def strengthen(self, amount: float = 0.1):
        """Укрепление связи (LTP)"""
        self.weight = min(1.0, self.weight + amount)
        self.history.append(('strengthen', amount, time.time()))
        self.age += 1

    def weaken(self, amount: float = 0.05):
        """Ослабление связи (LTD)"""
        self.weight = max(0.0, self.weight - amount)
        self.history.append(('weaken', amount, time.time()))
        self.age += 1

    def fire(self, activation_level: float = 1.0) -> float:
        """Передача сигнала"""
        self.last_activated = time.time()
        signal = activation_level * self.weight
        self.history.append(('fire', signal, time.time()))
        self.age += 1
        return signal

    def get_info(self) -> dict:
        return {
            'pre_neuron': self.pre_id,
            'post_neuron': self.post_id,
            'weight': self.weight,
            'age': self.age
        }

    def __repr__(self) -> str:
        return f"Synapse({self.pre_id[:6]} → {self.post_id[:6]}, weight={self.weight:.3f})"