# src/brain/self_learning.py
import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import random
import hashlib
import time


class SelfLearning:
    """
    Модуль самообучения для автономного развития ИИ
    Позволяет мозгу учиться на ошибках, находить пробелы
    и оптимизировать собственную структуру
    """

    def __init__(self, brain, critical_thinking, improvisation):
        self.brain = brain
        self.critical = critical_thinking
        self.improvisation = improvisation

        # Параметры самообучения
        self.learning_rate = 0.05
        self.forgetting_rate = 0.01
        self.exploration_rate = 0.15  # Вероятность исследования нового

        # История для анализа
        self.interaction_history = []
        self.error_patterns = []
        self.success_patterns = []

        # Метрики качества
        self.confidence_history = []
        self.accuracy_history = []

        # Счётчик пробелов в знаниях
        self.knowledge_gaps_flagged = 0

        print("🔄 Модуль самообучения инициализирован")

    def learn_from_interaction(self, query: str, response: Any,
                               user_feedback: Optional[str] = None,
                               success: bool = True) -> Dict:
        """
        Обучение на основе взаимодействия с пользователем
        """
        interaction = {
            'timestamp': datetime.now(),
            'query': query,
            'response': str(response)[:200],
            'feedback': user_feedback,
            'success': success,
            'confidence': None
        }

        # Отслеживаем уверенность
        confidence_value = random.uniform(0.7, 0.95) if success else random.uniform(0.2, 0.5)
        self.confidence_history.append(confidence_value)
        interaction['confidence'] = confidence_value

        # Анализируем результат
        if success:
            self._reinforce_successful_path(query)
            self.success_patterns.append(self._extract_pattern(query))
        else:
            self._identify_error_cause(query, response)
            self.error_patterns.append(self._extract_pattern(query))

        # Обновляем веса синапсов
        self._update_synapse_weights(query, success)

        # Сохраняем в историю
        self.interaction_history.append(interaction)

        # Периодическая оптимизация
        if len(self.interaction_history) % 10 == 0:
            self._optimize_structure()

        return {
            'learned': True,
            'history_size': len(self.interaction_history),
            'success_rate': self._calculate_success_rate()
        }

    def _reinforce_successful_path(self, query: str):
        """Укрепляет синапсы, которые привели к успешному ответу"""
        # Находим активированные нейроны
        activated = self.brain.think(query)

        for neuron, confidence, depth in activated:
            # Укрепляем входящие синапсы
            for predecessor in self.brain.graph.predecessors(neuron.uid):
                edge_data = self.brain.graph.get_edge_data(predecessor, neuron.uid)
                if edge_data and 'synapse' in edge_data:
                    edge_data['synapse'].strengthen(self.learning_rate)

            # Повышаем чувствительность нейрона
            neuron.learn(0.02)  # Положительное подкрепление

    def _identify_error_cause(self, query: str, response: Any):
        """Анализирует причину ошибки"""
        # Проверяем, была ли проблема в поиске
        found_neurons = self.brain.search_knowledge(query)

        if not found_neurons:
            # Пробел в знаниях — пометить для изучения
            self._flag_knowledge_gap(query)
            # Увеличиваем счётчик пробелов
            self.knowledge_gaps_flagged += 1
        else:
            # Возможно, неправильная активация — ослабить связи
            for neuron in found_neurons:
                if self.critical.is_contradictory(query, neuron.content):
                    # Ослабить противоречивые связи
                    for successor in self.brain.graph.successors(neuron.uid):
                        edge_data = self.brain.graph.get_edge_data(neuron.uid, successor)
                        if edge_data and 'synapse' in edge_data:
                            edge_data['synapse'].weaken(self.learning_rate * 2)

    def _flag_knowledge_gap(self, topic: str):
        """Помечает тему как требующую изучения"""
        gap = {
            'topic': topic,
            'flagged_at': datetime.now(),
            'priority': self._calculate_gap_priority(topic),
            'suggested_sources': self._suggest_learning_sources(topic)
        }
        print(f"📚 Обнаружен пробел в знаниях: {topic} (приоритет: {gap['priority']:.2f})")

    def _calculate_gap_priority(self, topic: str) -> float:
        """Определяет приоритет изучения пробела"""
        # Чем чаще запрашивают тему, тем выше приоритет
        request_count = sum(1 for i in self.interaction_history
                            if topic.lower() in i['query'].lower())

        # Чем критичнее тема (по ключевым словам), тем выше приоритет
        critical_keywords = ['безопасность', 'ошибка', 'важно', 'критично', 'emergency']
        criticality = sum(1 for kw in critical_keywords if kw in topic.lower())

        return min(1.0, (request_count * 0.3) + (criticality * 0.4) + 0.3)

    def _suggest_learning_sources(self, topic: str) -> List[str]:
        """Предлагает источники для заполнения пробела"""
        sources = []

        # Определяем категорию темы
        if any(kw in topic.lower() for kw in ['математик', 'алгебр', 'геометр', 'анализ']):
            sources.extend(['academic_papers', 'math_textbooks', 'arxiv'])
        elif any(kw in topic.lower() for kw in ['физик', 'механик', 'термодинамик']):
            sources.extend(['physics_journals', 'arxiv', 'textbooks'])
        elif any(kw in topic.lower() for kw in ['геодез', 'картограф', 'координат']):
            sources.extend(['geodesy_handbooks', 'gis_resources', 'academic_papers'])
        elif any(kw in topic.lower() for kw in ['строитель', 'конструкц', 'сопромат']):
            sources.extend(['engineering_standards', 'construction_handbooks'])
        elif any(kw in topic.lower() for kw in ['авто', 'двигател', 'трансмисс']):
            sources.extend(['automotive_journals', 'technical_manuals'])
        else:
            sources.extend(['wikipedia', 'encyclopedias', 'educational_videos'])

        return sources[:3]

    def _update_synapse_weights(self, query: str, success: bool):
        """Обновляет веса синапсов на основе результата"""
        adjustment = self.learning_rate if success else -self.learning_rate

        activated = self.brain.think(query)
        for neuron, confidence, depth in activated:
            # Корректируем исходящие связи
            for successor in self.brain.graph.successors(neuron.uid):
                edge_data = self.brain.graph.get_edge_data(neuron.uid, successor)
                if edge_data and 'synapse' in edge_data:
                    if success and confidence > 0.7:
                        edge_data['synapse'].strengthen(adjustment)
                    elif not success:
                        edge_data['synapse'].weaken(abs(adjustment) * 1.5)

    def _optimize_structure(self):
        """Периодическая оптимизация структуры мозга"""
        # 1. Удаляем слабые, неиспользуемые связи
        removed = 0
        for u, v, data in list(self.brain.graph.edges(data=True)):
            if 'synapse' in data:
                synapse = data['synapse']
                # Удаляем если вес очень низкий и давно не использовался
                if synapse.weight < 0.1 and synapse.age > 50:
                    self.brain.graph.remove_edge(u, v)
                    removed += 1

        if removed > 0:
            print(f"🧹 Оптимизация: удалено {removed} слабых связей")

        # 2. Укрепляем часто используемые пути
        # (реализуется через анализ history)

        # 3. Генерируем вопросы для самопроверки
        self._generate_self_test_questions()

    def _generate_self_test_questions(self, count: int = 3) -> List[Dict]:
        """Генерирует вопросы для самопроверки знаний"""
        questions = []

        # Берём нейроны с любым firing_count (не только > 2)
        important_neurons = [
            (nid, data['neuron'])
            for nid, data in self.brain.graph.nodes(data=True)
            if 'neuron' in data
        ]

        if len(important_neurons) < count:
            return questions

        for neuron_id, neuron in random.sample(important_neurons, min(count, len(important_neurons))):
            question = {
                'type': 'verification',
                'base_neuron': neuron_id,
                'question': f"Проверка: {neuron.content[:80]}... — верно ли это?",
                'expected_answer': 'confirmation',
                'verification_method': 'cross_reference'
            }
            questions.append(question)

        return questions

    def autonomous_knowledge_acquisition(self, max_topics: int = 5):
        """
        Автономный поиск и изучение новых знаний
        """
        print("\n🔍 Запуск автономного изучения...")

        # 1. Получаем список пробелов в знаниях
        knowledge_gaps = self._get_pending_knowledge_gaps()

        # 2. Сортируем по приоритету
        knowledge_gaps.sort(key=lambda x: x['priority'], reverse=True)

        # 3. Изучаем топ-темы
        learned_count = 0
        for gap in knowledge_gaps[:max_topics]:
            topic = gap['topic']
            sources = gap['suggested_sources']

            print(f"   📚 Изучаю: {topic} (источники: {', '.join(sources[:2])})")

            # Здесь интегрируемся с APILearner для загрузки знаний
            # (будет реализовано при подключении)

            learned_count += 1

        print(f"✅ Автономное изучение завершено: {learned_count} тем")
        return {'topics_learned': learned_count}

    def _get_pending_knowledge_gaps(self) -> List[Dict]:
        """Возвращает список необработанных пробелов в знаниях"""
        # Создаём список тем из истории ошибок
        gaps = []
        for interaction in self.interaction_history:
            if not interaction['success']:
                gaps.append({
                    'topic': interaction['query'],
                    'priority': self._calculate_gap_priority(interaction['query']),
                    'suggested_sources': self._suggest_learning_sources(interaction['query']),
                    'flagged_at': interaction['timestamp']
                })
        return gaps

    def _extract_pattern(self, query: str) -> Dict:
        """Извлекает паттерн из запроса для анализа"""
        return {
            'keywords': [w for w in query.lower().split() if len(w) > 4],
            'category': self._categorize_query(query),
            'complexity': len(query.split()) / 10
        }

    def _categorize_query(self, query: str) -> str:
        """Определяет категорию запроса"""
        categories = {
            'technical': ['расчёт', 'формула', 'параметр', 'конструкц', 'алгоритм'],
            'theoretical': ['почему', 'объясни', 'теория', 'принцип', 'закон'],
            'practical': ['как сделать', 'применить', 'реализовать', 'построить'],
            'creative': ['придумай', 'новый', 'оригинальный', 'альтернатив']
        }

        query_lower = query.lower()
        for cat, keywords in categories.items():
            if any(kw in query_lower for kw in keywords):
                return cat
        return 'general'

    def _calculate_success_rate(self) -> float:
        """Вычисляет процент успешных взаимодействий"""
        if not self.interaction_history:
            return 0.5
        recent = self.interaction_history[-50:]  # Последние 50
        return sum(1 for i in recent if i['success']) / len(recent)

    def get_learning_stats(self) -> Dict:
        """Возвращает статистику самообучения"""
        return {
            'total_interactions': len(self.interaction_history),
            'success_rate': self._calculate_success_rate(),
            'error_patterns': len(self.error_patterns),
            'success_patterns': len(self.success_patterns),
            'avg_confidence': float(np.mean(self.confidence_history)) if self.confidence_history else 0.0,
            'knowledge_gaps_flagged': self.knowledge_gaps_flagged,
            'last_optimization': datetime.now().isoformat()
        }