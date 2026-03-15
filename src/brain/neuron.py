# src/brain/neuron.py

import time
import hashlib


class Neuron:
    """
    Класс нейрона - имитирует нейрон в мозге.
    Хранит знание и его состояние.
    """

    def __init__(self, uid: str = None, content: str = "", category: str = "general"):
        """
        Инициализация нейрона

        Args:
            uid: уникальный идентификатор (если None, создается автоматически)
            content: содержание знания (текст, формула)
            category: категория знания (Math, History, Science...)
        """
        if uid is None:
            # Создаем уникальный ID на основе контента и времени
            unique_string = f"{content}{time.time()}"
            self.uid = hashlib.md5(unique_string.encode()).hexdigest()[:8]
        else:
            self.uid = uid

        self.content = content
        self.category = category

        # Биологические параметры
        self.activation_level = 0.0  # Текущий уровень возбуждения (0.0 - 1.0)
        self.threshold = 0.5  # Порог срабатывания
        self.rest_potential = 0.1  # Потенциал покоя
        self.refractory_period = False  # Рефрактерный период (нейрон "отдыхает")
        self.last_fired_time = 0  # Время последнего срабатывания

        # Статистика
        self.firing_count = 0  # Сколько раз сработал
        self.created_at = time.time()  # Время создания
        self.last_access = time.time()  # Время последнего доступа

    def stimulate(self, input_signal: float) -> float:
        """
        Стимуляция нейрона входным сигналом

        Args:
            input_signal: входной сигнал (0.0 - 1.0)

        Returns:
            float: выходной сигнал после обработки
        """
        current_time = time.time()
        self.last_access = current_time

        # Если нейрон в рефрактерном периоде, он не реагирует
        if self.refractory_period:
            if current_time - self.last_fired_time > 0.1:  # 100 мс рефрактерности
                self.refractory_period = False
            else:
                return 0.0

        # Накопление сигнала
        self.activation_level += input_signal

        # Естественное затухание (имитация утечки потенциала)
        self.activation_level *= 0.95

        # Проверка порога срабатывания
        if self.activation_level >= self.threshold:
            return self.fire()

        return 0.0

    def fire(self) -> float:
        """
        Срабатывание нейрона (генерация потенциала действия)

        Returns:
            float: выходной сигнал
        """
        self.firing_count += 1
        self.last_fired_time = time.time()
        self.refractory_period = True

        # Сигнал зависит от того, насколько превышен порог
        output = self.activation_level * 1.5
        self.activation_level = self.rest_potential  # Сброс до потенциала покоя

        return min(1.0, output)  # Ограничиваем максимальный сигнал

    def learn(self, reinforcement: float):
        """
        Обучение нейрона (изменение порога чувствительности)

        Args:
            reinforcement: подкрепление (положительное или отрицательное)
        """
        # Если нейрон часто используется, он становится чувствительнее
        if reinforcement > 0:
            self.threshold = max(0.3, self.threshold - 0.01)
        else:
            self.threshold = min(0.8, self.threshold + 0.01)

    def get_info(self) -> dict:
        """
        Получить информацию о нейроне

        Returns:
            dict: словарь с параметрами нейрона
        """
        return {
            'uid': self.uid,
            'content': self.content[:50] + '...' if len(self.content) > 50 else self.content,
            'category': self.category,
            'activation': self.activation_level,
            'threshold': self.threshold,
            'firing_count': self.firing_count,
            'age': time.time() - self.created_at,
            'created_at': self.created_at
        }

    def __repr__(self) -> str:
        return f"Neuron({self.uid}: {self.content[:30]}..., act={self.activation_level:.2f})"