# src/brain/cortex.py
import networkx as nx
import time
import hashlib
from .neuron import Neuron
from .synapse import Synapse
from .memory_manager import MemoryManager
from .critical_thinking import CriticalThinking
from .improvisation import Improvisation
from .multilingual import MultilingualProcessor
from .situational import SituationalAwareness
from .self_learning import SelfLearning


class Cortex:
    """
    Главный класс мозга - интегрирует все модули мышления
    """

    def __init__(self, load_from_file: str = None):
        self.graph = nx.DiGraph()
        self.memory = MemoryManager()

        # Параметры обучения
        self.learning_rate = 0.1
        self.forgetting_rate = 0.01
        self.hebbian_factor = 0.05
        self.thought_count = 0

        # === МОДУЛИ МЫШЛЕНИЯ (ВАЖЕН ПОРЯДОК!) ===
        self.critical_thinking = CriticalThinking(self)
        self.improvisation = Improvisation(self, self.critical_thinking)
        self.multilingual = MultilingualProcessor(self)
        self.situational = SituationalAwareness(self, self.critical_thinking)
        self.self_learning = SelfLearning(self, self.critical_thinking, self.improvisation)

        if load_from_file:
            self.load(load_from_file)

    def create_neuron(self, content: str, category: str = "general") -> Neuron:
        unique_string = f"{content}{time.time()}"
        uid = hashlib.md5(unique_string.encode()).hexdigest()[:8]
        neuron = Neuron(uid=uid, content=content, category=category)
        self.graph.add_node(neuron.uid, neuron=neuron, category=category)
        return neuron

    def create_synapse(self, pre_neuron: Neuron, post_neuron: Neuron, weight: float = 0.1) -> Synapse:
        if self.graph.has_edge(pre_neuron.uid, post_neuron.uid):
            return self.graph[pre_neuron.uid][post_neuron.uid]['synapse']
        synapse = Synapse(pre_neuron.uid, post_neuron.uid, weight)
        self.graph.add_edge(pre_neuron.uid, post_neuron.uid, synapse=synapse, weight=weight)
        return synapse

    def add_knowledge(self, concept_id: str, content: str, category: str, related_concepts: list = None):
        neuron = Neuron(uid=concept_id, content=content, category=category)
        self.graph.add_node(neuron.uid, neuron=neuron, category=category)
        if related_concepts:
            for rel_id, weight in related_concepts:
                if rel_id in self.graph.nodes:
                    pre_neuron = neuron
                    post_neuron = self.graph.nodes[rel_id]['neuron']
                    self.create_synapse(pre_neuron, post_neuron, weight)

    def think(self, input_concept: str) -> list:
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
        results = []
        query_lower = query.lower()
        query_words = query_lower.split()

        for node_id, data in self.graph.nodes(data=True):
            neuron = data.get('neuron')
            if not neuron:
                continue
            content_lower = neuron.content.lower()
            if query_lower in content_lower:
                results.append(neuron)
                continue
            content_words = content_lower.split()
            matches = sum(1 for word in query_words if word in content_words)
            if matches >= 1:
                results.append(neuron)

        seen = set()
        unique_results = []
        for neuron in results:
            if neuron.uid not in seen:
                seen.add(neuron.uid)
                unique_results.append(neuron)

        return unique_results

    def process_query(self, query: str, context: dict = None) -> dict:
        """
        Единый интерфейс для обработки запроса через все модули мышления
        """
        if context is None:
            context = {}

        # 1. Анализируем ситуацию
        situational_context = self.situational.analyze_situation(query, context)

        # 2. Ищем знания
        knowledge = self.search_knowledge(query)

        # 3. Критический анализ (если нужно)
        if self.situational._is_factual_query(query):
            analysis = self.critical_thinking.analyze_information(query)
        else:
            analysis = {'confidence': 0.7, 'conclusion': 'informational_query'}

        # 4. Творческое решение (если знаний мало)
        if len(knowledge) < 2 or self.situational._needs_creativity(query):
            solution = self.improvisation.solve_creatively(query)
            response = solution['solution']
            confidence = solution['confidence']
        else:
            response = " | ".join([n.content[:100] for n in knowledge[:3]])
            confidence = max([k[1] for k in self.think(query)]) if self.think(query) else 0.5

        # 5. Адаптируем ответ под ситуацию
        adapted_response = self.situational.adapt_response(response, situational_context, confidence)

        # 6. Обучаемся на взаимодействии
        self.self_learning.learn_from_interaction(query, adapted_response, success=True)

        return {
            'response': adapted_response,
            'confidence': confidence,
            'knowledge_used': len(knowledge),
            'context': situational_context,
            'analysis': analysis
        }

    def save(self, filename: str = None) -> str:
        return self.memory.save_brain(self, filename)

    def load(self, filepath: str):
        data = self.memory.load_brain(filepath)
        if data and 'graph' in data:
            self.graph = data['graph']

    def get_stats(self) -> dict:
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