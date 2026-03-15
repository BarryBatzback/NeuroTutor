import networkx as nx
import random
import time
import hashlib
from .neuron import Neuron
from .synapse import Synapse
from .memory_manager import MemoryManager
from .critical_thinking import CriticalThinking
from .improvisation import Improvisation
from .situational import SituationalAwareness
from .self_learning import SelfLearning
from .unified_thinking import UnifiedThinkingEngine

class Cortex:
    def __init__(self, load_from_file: str = None):
        self.graph = nx.DiGraph()
        self.memory = MemoryManager()

        # Параметры обучения
        self.learning_rate = 0.1
        self.forgetting_rate = 0.01
        self.hebbian_factor = 0.05
        self.thought_count = 0

        # Инициализация модулей
        self.critical_thinking = CriticalThinking(self)
        self.improvisation = Improvisation(self, self.critical_thinking)
        self.self_learning = SelfLearning(self, self.critical_thinking, self.improvisation)
        self.situational = SituationalAwareness(self)
        self.unified_thinking = UnifiedThinkingEngine(self)

        if load_from_file:
            self.load(load_from_file)


    def create_neuron(self, content: str, category: str = "general") -> Neuron:
        """Создать нейрон"""
        unique_string = f"{content}{time.time()}"
        uid = hashlib.md5(unique_string.encode()).hexdigest()[:8]
        neuron = Neuron(uid=uid, content=content, category=category)

        self.graph.add_node(
            neuron.uid,
            neuron=neuron,
            category=category,
            created_at=neuron.created_at
        )
        return neuron

    def create_synapse(self, pre_neuron: Neuron, post_neuron: Neuron, weight: float = 0.1) -> Synapse:
        """Создать синапс"""
        if self.graph.has_edge(pre_neuron.uid, post_neuron.uid):
            return self.graph[pre_neuron.uid][post_neuron.uid]['synapse']

        synapse = Synapse(pre_neuron.uid, post_neuron.uid, weight)
        self.graph.add_edge(
            pre_neuron.uid,
            post_neuron.uid,
            synapse=synapse,
            weight=weight,
            created_at=time.time()
        )
        return synapse

    def add_knowledge(self, concept_id: str, content: str, category: str,
                      related_concepts: list = None):
        """Добавить знание"""
        neuron = Neuron(uid=concept_id, content=content, category=category)
        self.graph.add_node(neuron.uid, neuron=neuron, category=category)

        if related_concepts:
            for rel_id, weight in related_concepts:
                if rel_id in self.graph.nodes:
                    pre_neuron = neuron
                    post_neuron = self.graph.nodes[rel_id]['neuron']
                    self.create_synapse(pre_neuron, post_neuron, weight)

    def think(self, input_concept: str) -> list:
        """Процесс мышления"""
        self.thought_count += 1
        start_neurons = []
        input_lower = input_concept.lower()

        for node_id, data in self.graph.nodes(data=True):
            neuron = data.get('neuron')
            if neuron and (neuron.uid == input_concept or input_lower in neuron.content.lower()):
                start_neurons.append(neuron)

        if not start_neurons:
            return []

        all_activated = []
        visited = set()

        def propagate(current_neuron: Neuron, depth: int = 0):
            if depth > 3 or current_neuron.uid in visited:
                return
            visited.add(current_neuron.uid)

            output = current_neuron.stimulate(1.0 if depth == 0 else 0.5)
            if output > 0:
                all_activated.append((current_neuron, output, depth))

                for successor in self.graph.successors(current_neuron.uid):
                    edge_data = self.graph.get_edge_data(current_neuron.uid, successor)
                    if edge_data and 'synapse' in edge_data:
                        synapse = edge_data['synapse']
                        next_neuron = self.graph.nodes[successor]['neuron']
                        signal = synapse.fire(output)
                        if signal > 0:
                            synapse.strengthen(self.hebbian_factor)
                            propagate(next_neuron, depth + 1)

        for neuron in start_neurons:
            propagate(neuron)

        return all_activated

    def search_knowledge(self, query: str) -> list:
        """Улучшенный поиск знаний по запросу"""
        results = []
        query_lower = query.lower()
        query_words = query_lower.split()

        # Расширим поиск на однокоренные слова
        word_roots = {
            'нагрузк': ['нагрузка', 'нагрузки', 'нагрузке', 'нагрузкой'],
            'балк': ['балка', 'балки', 'балке', 'балкой', 'балок'],
            'гравит': ['гравитация', 'гравитации', 'гравитацию', 'тяготение'],
            'автомобил': ['автомобиль', 'автомобиля', 'автомобиле', 'авто', 'машина'],
            'строитель': ['строительство', 'строитель', 'строения', 'конструкц'],
            'спутник': ['спутник', 'спутника', 'спутнике', 'спутников'],
            'дифференциал': ['дифференциал', 'дифференциала', 'дифференциале']
        }

        for node_id, data in self.graph.nodes(data=True):
            neuron = data.get('neuron')
            if not neuron:
                continue

            content_lower = neuron.content.lower()
            content_words = content_lower.split()

            # 1. Проверяем точное вхождение
            if query_lower in content_lower:
                results.append(neuron)
                continue

            # 2. Проверяем вхождение отдельных слов
            matches = sum(1 for word in query_words if word in content_words)
            if matches >= 1:
                results.append(neuron)
                continue

            # 3. Проверяем однокоренные слова
            for root, variations in word_roots.items():
                if root in query_lower:
                    if any(var in content_lower for var in variations):
                        results.append(neuron)
                        break

            # 4. Проверяем ключевые понятия
            key_concepts = {
                'гравитация': ['притягивает', 'тяготение', 'gravity', 'спутник', 'орбита'],
                'вода': ['кипит', 'замерзает', 'жидкость', 'h2o'],
                'земля': ['планета', 'шар', 'круглая', 'сферическая'],
                'автомобиль': ['колёса', 'двигатель', 'трансмиссия', 'дифференциал'],
                'строительство': ['бетон', 'конструкц', 'нагрузк', 'балк', 'фундамент']
            }

            for concept, keywords in key_concepts.items():
                if concept in query_lower:
                    if any(keyword in content_lower for keyword in keywords):
                        if neuron not in results:
                            results.append(neuron)
                        break

        # Убираем дубликаты
        seen = set()
        unique_results = []
        for neuron in results:
            if neuron.uid not in seen:
                seen.add(neuron.uid)
                unique_results.append(neuron)

        return unique_results

    def get_stats(self) -> dict:
        """Статистика мозга"""
        categories = {}
        for node_id, data in self.graph.nodes(data=True):
            cat = data.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1

        return {
            'neurons': self.graph.number_of_nodes(),
            'synapses': self.graph.number_of_edges(),
            'thoughts': self.thought_count,
            'categories': categories
        }

    def save(self, filename: str = None) -> str:
        """Сохранить мозг"""
        import pickle
        from pathlib import Path

        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"brain_{timestamp}.pkl"

        save_dir = Path("data/models")
        save_dir.mkdir(parents=True, exist_ok=True)
        filepath = save_dir / filename

        save_data = {
            'graph': self.graph,
            'stats': self.get_stats(),
            'timestamp': time.time()
        }

        with open(filepath, 'wb') as f:
            pickle.dump(save_data, f)

        print(f"💾 Мозг сохранен: {filepath}")
        return str(filepath)

    def load(self, filepath: str):
        """Загрузить мозг"""
        import pickle
        from pathlib import Path

        filepath = Path(filepath)
        if not filepath.exists():
            print(f"❌ Файл не найден: {filepath}")
            return

        with open(filepath, 'rb') as f:
            data = pickle.load(f)

        if 'graph' in data:
            self.graph = data['graph']
            print(f"✅ Мозг загружен: {data.get('stats', {}).get('neuron_count', '?')} нейронов")