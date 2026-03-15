import networkx as nx
import random
import time
import hashlib
from .neuron import Neuron
from .synapse import Synapse
from .memory_manager import MemoryManager


class Cortex:
    """
    Главный класс мозга - кора, управляет всеми нейронами и синапсами
    """

    def __init__(self, load_from_file: str = None):
        """
        Инициализация мозга

        Args:
            load_from_file: путь к файлу для загрузки сохраненного состояния
        """
        self.graph = nx.DiGraph()  # Используем направленный граф
        self.memory = MemoryManager()

        # Параметры обучения (биологические)
        self.learning_rate = 0.1  # Скорость обучения
        self.forgetting_rate = 0.01  # Скорость забывания
        self.hebbian_factor = 0.05  # Коэффициент Хеббовского обучения

        # Статистика
        self.thought_count = 0

        # Загружаем сохраненное состояние если указано
        if load_from_file:
            self.load(load_from_file)

    def create_neuron(self, content: str, category: str = "general") -> Neuron:
        """
        Создать новый нейрон

        Args:
            content: содержание знания
            category: категория

        Returns:
            Neuron: созданный нейрон
        """
        # Создаем уникальный ID на основе контента и времени
        unique_string = f"{content}{time.time()}"
        uid = hashlib.md5(unique_string.encode()).hexdigest()[:8]

        neuron = Neuron(uid=uid, content=content, category=category)

        # Добавляем в граф
        self.graph.add_node(
            neuron.uid,
            neuron=neuron,
            category=category,
            created_at=neuron.created_at
        )

        print(f"🧠 Создан нейрон: {uid} ({category}): {content[:50]}...")
        return neuron

    def create_synapse(self, pre_neuron: Neuron, post_neuron: Neuron, weight: float = 0.1) -> Synapse:
        """
        Создать синаптическую связь между нейронами

        Args:
            pre_neuron: нейрон-источник
            post_neuron: нейрон-приемник
            weight: начальный вес связи

        Returns:
            Synapse: созданный синапс
        """
        # Проверяем, существует ли уже такая связь
        if self.graph.has_edge(pre_neuron.uid, post_neuron.uid):
            # Если существует, просто возвращаем существующий синапс
            return self.graph[pre_neuron.uid][post_neuron.uid]['synapse']

        synapse = Synapse(pre_neuron.uid, post_neuron.uid, weight)

        # Сохраняем синапс как атрибут ребра
        self.graph.add_edge(
            pre_neuron.uid,
            post_neuron.uid,
            synapse=synapse,
            weight=weight,
            created_at=time.time()
        )

        print(f"🔗 Создан синапс: {pre_neuron.uid[:6]} → {post_neuron.uid[:6]} (вес: {weight})")

        return synapse

    def add_knowledge(self, concept_id: str, content: str, category: str, related_concepts: list = None):
        """
        Добавить знание и связать его с существующими

        Args:
            concept_id: идентификатор понятия
            content: содержание
            category: категория
            related_concepts: список связанных понятий [(id, вес_связи), ...]
        """
        # Создаем нейрон
        neuron = Neuron(uid=concept_id, content=content, category=category)
        self.graph.add_node(neuron.uid, neuron=neuron, category=category)

        # Связываем с существующими нейронами
        if related_concepts:
            for rel_id, weight in related_concepts:
                if rel_id in self.graph.nodes:
                    # Получаем нейроны
                    pre_neuron = self.graph.nodes[concept_id]['neuron']
                    post_neuron = self.graph.nodes[rel_id]['neuron']
                    self.create_synapse(pre_neuron, post_neuron, weight)

        print(f"📚 Добавлено знание: {concept_id}")

    def think(self, input_concept: str) -> list:
        """
        Процесс мышления - активация нейронов по ассоциациям

        Args:
            input_concept: входное понятие (ID нейрона или текст)

        Returns:
            list: список активированных нейронов с уровнем активации
        """
        self.thought_count += 1

        # Ищем нейрон по ID или содержанию
        start_neuron = None
        for node_id, data in self.graph.nodes(data=True):
            neuron = data.get('neuron')
            if neuron and (neuron.uid == input_concept or
                           input_concept.lower() in neuron.content.lower()):
                start_neuron = neuron
                break

        if not start_neuron:
            return []

        # Запускаем процесс распространения активации
        activated = []
        visited = set()

        def propagate(current_neuron: Neuron, depth: int = 0):
            if depth > 3 or current_neuron.uid in visited:  # Ограничиваем глубину
                return

            visited.add(current_neuron.uid)

            # Стимулируем текущий нейрон
            output = current_neuron.stimulate(1.0 if depth == 0 else 0.5)

            if output > 0:
                activated.append((current_neuron, output, depth))

                # Передаем сигнал дальше по связям
                for successor in self.graph.successors(current_neuron.uid):
                    edge_data = self.graph.get_edge_data(current_neuron.uid, successor)
                    if edge_data and 'synapse' in edge_data:
                        synapse = edge_data['synapse']
                        next_neuron = self.graph.nodes[successor]['neuron']

                        # Сигнал проходит через синапс
                        signal = synapse.fire(output)
                        if signal > 0:
                            # Хеббовское обучение: нейроны, активирующиеся вместе, укрепляют связи
                            synapse.strengthen(self.hebbian_factor)
                            propagate(next_neuron, depth + 1)

        propagate(start_neuron)

        return activated

    def learn_from_feedback(self, concept_id: str, positive: bool = True):
        """
        Обучение на основе обратной связи

        Args:
            concept_id: ID концепции
            positive: положительная или отрицательная обратная связь
        """
        if concept_id not in self.graph:
            return

        neuron = self.graph.nodes[concept_id]['neuron']
        reinforcement = 0.1 if positive else -0.05

        # Обучаем нейрон
        neuron.learn(reinforcement)

        # Укрепляем или ослабляем связи
        for successor in self.graph.successors(concept_id):
            edge_data = self.graph.get_edge_data(concept_id, successor)
            if edge_data and 'synapse' in edge_data:
                synapse = edge_data['synapse']
                if positive:
                    synapse.strengthen(self.learning_rate)
                else:
                    synapse.weaken(self.learning_rate)

    def forget(self):
        """
        Процесс забывания - ослабление неиспользуемых связей
        """
        for u, v, data in self.graph.edges(data=True):
            if 'synapse' in data:
                synapse = data['synapse']
                # Чем старше синапс и чем реже использовался, тем быстрее забывается
                if synapse.age > 10 and len(synapse.history) < 5:
                    synapse.weaken(self.forgetting_rate)

    def save(self, filename: str = None) -> str:
        """
        Сохранить состояние мозга

        Args:
            filename: имя файла

        Returns:
            str: путь к сохраненному файлу
        """
        return self.memory.save_brain(self, filename)

    def load(self, filepath: str):
        """
        Загрузить состояние мозга

        Args:
            filepath: путь к файлу
        """
        data = self.memory.load_brain(filepath)
        if data and 'graph' in data:
            self.graph = data['graph']
            print(f"✅ Мозг загружен: {data.get('neuron_count', 0)} нейронов")

    def get_stats(self) -> dict:
        """
        Получить статистику мозга

        Returns:
            dict: статистика
        """
        return {
            'neurons': self.graph.number_of_nodes(),
            'synapses': self.graph.number_of_edges(),
            'thoughts': self.thought_count,
            'categories': self._count_categories()
        }

    def _count_categories(self) -> dict:
        """Подсчет нейронов по категориям"""
        categories = {}
        for node_id, data in self.graph.nodes(data=True):
            cat = data.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
        return categories

    def get_neuron_by_content(self, text: str) -> Neuron:
        """
        Найти нейрон по содержанию

        Args:
            text: текст для поиска

        Returns:
            Neuron: найденный нейрон или None
        """
        for node_id, data in self.graph.nodes(data=True):
            neuron = data.get('neuron')
            if neuron and text.lower() in neuron.content.lower():
                return neuron
        return None