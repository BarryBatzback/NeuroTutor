# src/brain/unified_thinking.py
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import numpy as np
import time


class UnifiedThinkingEngine:
    """
    Единый движок мышления - координирует все модули ИИ
    """

    def __init__(self, brain):
        self.brain = brain
        self.critical = brain.critical_thinking if hasattr(brain, 'critical_thinking') else None
        self.improvisation = brain.improvisation if hasattr(brain, 'improvisation') else None
        self.multilingual = brain.multilingual if hasattr(brain, 'multilingual') else None
        self.situational = brain.situational if hasattr(brain, 'situational') else None
        self.self_learning = brain.self_learning if hasattr(brain, 'self_learning') else None

        # Параметры мышления
        self.thinking_mode = 'balanced'
        self.creativity_level = 0.7
        self.skepticism_level = 0.5

        # История мышления
        self.thought_history = []
        self.decision_log = []

        print("🧠 UnifiedThinkingEngine инициализирован")

    def process_query(self, query: str, context: Dict = None) -> Dict:
        """Полный цикл обработки запроса"""
        if context is None:
            context = {}

        start_time = time.time()
        thought_process = {
            'query': query,
            'context': context,
            'stages': {},
            'final_answer': None,
            'confidence': 0.0,
            'reasoning_path': []
        }

        # === ЭТАП 1: Понимание запроса ===
        thought_process['stages']['understanding'] = self._understand_query(query, context)

        # === ЭТАП 2: Критический анализ ===
        if self.critical and self.thinking_mode in ['balanced', 'deep']:
            thought_process['stages']['critical_analysis'] = self._critical_analysis(query, context)

        # === ЭТАП 3: Поиск знаний ===
        thought_process['stages']['knowledge_retrieval'] = self._retrieve_knowledge(query)

        # === ЭТАП 4: Творческое решение ===
        understanding = thought_process['stages']['understanding']
        if self.improvisation and self._needs_creativity(query, thought_process):
            thought_process['stages']['creative_solution'] = self._generate_creative_solution(
                query, context, understanding.get('domain')
            )

        # === ЭТАП 5: Синтез ответа ===
        thought_process['final_answer'] = self._synthesize_answer(query, thought_process)

        # === ЭТАП 6: Оценка уверенности ===
        thought_process['confidence'] = self._calculate_confidence(thought_process)

        # Логирование
        thought_process['duration'] = round(time.time() - start_time, 3)
        self._log_thought(thought_process)

        return thought_process

    def _understand_query(self, query: str, context: Dict) -> Dict:
        """Понимание запроса"""
        understanding = {
            'language': 'ru',
            'intent': 'question',
            'complexity': 'medium',
            'domain': None,
            'emotional_tone': 'neutral',
            'urgency': context.get('urgency', 'medium'),
            'user_level': context.get('user_level', 'general')
        }

        # Определение языка
        if self.multilingual:
            understanding['language'] = self.multilingual.detect_language(query)

        # Анализ намерения
        query_lower = query.lower()
        if any(w in query_lower for w in ['как', 'способ', 'метод', 'рассчитать']):
            understanding['intent'] = 'how_to'
        elif any(w in query_lower for w in ['почему', 'причина', 'объясни']):
            understanding['intent'] = 'explanation'
        elif any(w in query_lower for w in ['придумай', 'создай', 'идея', 'инновационный']):
            understanding['intent'] = 'creative'
        elif any(w in query_lower for w in ['можно ли', 'возможно']):
            understanding['intent'] = 'yes_no'

        # Оценка сложности
        words = query.split()
        understanding['complexity'] = 'hard' if len(words) > 12 else 'medium' if len(words) > 6 else 'simple'

        # Определение домена
        domains = {
            'mathematics': ['математика', 'уравнение', 'формула', 'интеграл', 'производная', 'расчёт'],
            'physics': ['физика', 'сила', 'энергия', 'скорость', 'гравитация', 'спутник'],
            'engineering': ['строительство', 'конструкция', 'балка', 'нагрузка', 'геодезия'],
            'automotive': ['автомобиль', 'двигатель', 'трансмиссия', 'дифференциал', 'колесо'],
            'technology': ['технология', 'алгоритм', 'программа', 'нейросеть', 'машинное обучение', 'ИИ'],
            'cartography': ['карта', 'картография', 'координаты', 'проекция']
        }

        for domain, keywords in domains.items():
            if any(kw in query_lower for kw in keywords):
                understanding['domain'] = domain
                break

        return understanding

    def _critical_analysis(self, query: str, context: Dict) -> Dict:
        """Критический анализ"""
        if not self.critical:
            return {'available': False}

        # Если запрос содержит утверждение для проверки
        if any(w in query.lower() for w in ['верно ли', 'правда ли', 'действительно']):
            return self.critical.analyze_information(query, context.get('sources', []))

        # Иначе - предварительная оценка
        return {
            'preliminary_assessment': 'informational_query',
            'requires_verification': False,
            'confidence_baseline': 0.7,
            'available': True
        }

    # src/brain/unified_thinking.py - замени метод _retrieve_knowledge

    def _retrieve_knowledge(self, query: str) -> Dict:
        """Поиск и извлечение знаний - ИСПРАВЛЕННАЯ ВЕРСИЯ"""

        # 1. Прямой поиск через search_knowledge
        direct_results = self.brain.search_knowledge(query) if hasattr(self.brain, 'search_knowledge') else []

        # 2. Ассоциативный поиск через think()
        associative_results = self.brain.think(query) if hasattr(self.brain, 'think') else []

        # 3. Поиск по отдельным словам (если прямой поиск не дал результатов)
        if len(direct_results) < 2:
            query_words = query.lower().split()
            for word in query_words:
                if len(word) > 4:  # Только значимые слова
                    word_results = self.brain.search_knowledge(word)
                    for neuron in word_results:
                        if neuron not in direct_results:
                            direct_results.append(neuron)

        # 4. Поиск по категориям (если запрос содержит ключевые слова категорий)
        category_keywords = {
            'строительств': ['Construction', 'нагрузка', 'балка', 'фундамент'],
            'авто': ['Automotive', 'двигатель', 'трансмиссия', 'дифференциал'],
            'физик': ['Physics', 'спутник', 'гравитация', 'сила'],
            'геодез': ['Geodesy', 'координат', 'карта', 'измерени'],
            'математ': ['Mathematics', 'уравнени', 'формула', 'расчёт']
        }

        query_lower = query.lower()
        for category, keywords in category_keywords.items():
            if any(kw in query_lower for kw in keywords):
                # Ищем нейроны этой категории
                for node_id, data in self.brain.graph.nodes(data=True):
                    neuron = data.get('neuron')
                    if neuron and data.get('category') == keywords[0]:
                        if neuron not in direct_results:
                            direct_results.append(neuron)

        # 5. Оценка релевантности
        relevance_scores = []
        for neuron in direct_results[:10]:  # Берём топ-10
            # Считаем совпадение слов
            query_words = set(query.lower().split())
            content_words = set(neuron.content.lower().split())
            overlap = len(query_words.intersection(content_words))

            relevance_scores.append({
                'content': neuron.content[:200],
                'confidence': 0.5 + (overlap * 0.1),  # Базовая + за совпадения
                'category': neuron.category,
                'uid': neuron.uid
            })

        # Сортируем по уверенности
        relevance_scores.sort(key=lambda x: x['confidence'], reverse=True)

        return {
            'direct_matches': len(direct_results),
            'associative_matches': len(associative_results),
            'top_results': relevance_scores[:5],
            'all_neurons': len(direct_results),
            'knowledge_gaps': self._identify_gaps(query, direct_results),
            'available': len(direct_results) > 0
        }

    def _identify_gaps(self, query: str, found_knowledge: List) -> List[str]:
        """Определяет пробелы в знаниях"""
        gaps = []

        if len(found_knowledge) < 2:
            gaps.append(f"Мало информации по теме: {query[:50]}...")

        query_words = set(query.lower().split())
        if len(query_words) > 8 and len(found_knowledge) < 3:
            gaps.append("Требуется более глубокий поиск")

        return gaps

    def _needs_creativity(self, query: str, thought_process: Dict) -> bool:
        """Определяет, нужно ли творческое решение"""
        understanding = thought_process['stages'].get('understanding', {})

        # Явные маркеры креативности
        creative_markers = ['придумай', 'создай', 'идея', 'нестандартно', 'оригинально', 'инновационный']
        if any(m in query.lower() for m in creative_markers):
            return True

        # Если знаний мало и запрос сложный
        knowledge = thought_process['stages'].get('knowledge_retrieval', {})
        if knowledge.get('direct_matches', 0) < 2 and knowledge.get('associative_matches', 0) < 3:
            return True

        # Если домен технический и требуется решение
        if understanding.get('intent') == 'how_to' and understanding.get('domain') in ['engineering', 'technology']:
            return True

        return False

    def _generate_creative_solution(self, query: str, context: Dict, domain: str = None) -> Dict:
        """Генерация творческого решения"""
        if not self.improvisation:
            return {'available': False}

        solution = self.improvisation.solve_creatively(query, domain)

        # Генерируем дополнительные идеи
        if solution:
            solution['brainstorm_ideas'] = self.improvisation.brainstorm(query, num_ideas=3)
            solution['available'] = True
        else:
            solution = {'available': False}

        return solution

    # src/brain/unified_thinking.py - замени метод _synthesize_answer

    def _synthesize_answer(self, query: str, thought_process: Dict) -> Dict:
        """Синтез финального ответа - ИСПРАВЛЕННАЯ ВЕРСИЯ"""

        stages = thought_process['stages']
        understanding = stages.get('understanding', {})
        knowledge = stages.get('knowledge_retrieval', {})

        answer = {
            'text': '',
            'type': 'informational',
            'sources': [],
            'confidence': 0.0,
            'structured': False
        }

        # 1. Если есть результаты поиска - используем их
        if knowledge.get('top_results') and len(knowledge['top_results']) > 0:
            best_results = knowledge['top_results'][:3]

            # Формируем ответ из найденных знаний
            answer_parts = []
            for i, result in enumerate(best_results, 1):
                content = result.get('content', '')
                if content and len(content) > 10:
                    answer_parts.append(f"{i}. {content}")
                    answer['sources'].append({
                        'category': result.get('category', 'unknown'),
                        'confidence': result.get('confidence', 0.5)
                    })

            if answer_parts:
                answer['text'] = "\n".join(answer_parts)
                answer['confidence'] = np.mean([r.get('confidence', 0.5) for r in best_results])
                answer['type'] = 'direct_answer'
                answer['structured'] = True

        # 2. Если нет прямого ответа но есть творческое решение
        creative = stages.get('creative_solution', {})
        if creative.get('available') and creative.get('solution'):
            if answer['text']:
                answer['text'] += f"\n\n💡 Творческий подход: {creative['solution']}"
            else:
                answer['text'] = creative['solution']
            answer['type'] = 'creative_solution'
            answer['confidence'] = max(answer['confidence'], creative.get('confidence', 0.5))

            if creative.get('brainstorm_ideas'):
                answer['text'] += "\n\n💭 Идеи для рассмотрения:\n"
                for idea in creative['brainstorm_ideas'][:3]:
                    answer['text'] += f"   • {idea}\n"

        # 3. Если есть пробелы в знаниях
        if knowledge.get('knowledge_gaps'):
            if answer['text']:
                answer['text'] += f"\n\n⚠️ Примечание: {'; '.join(knowledge['knowledge_gaps'][:2])}"
            else:
                answer['text'] = f"⚠️ {'; '.join(knowledge['knowledge_gaps'][:2])}"
            answer['type'] = 'partial_answer'

        # 4. Если вообще нет ответа - предлагаем обучение
        if not answer['text']:
            answer['text'] = f"""🤔 У меня пока недостаточно информации для ответа на этот вопрос.

    📚 Вы можете обучить меня:
    1. Отправьте текст с информацией по теме "{query[:50]}..."
    2. Или выберите "Учить из интернета" в меню

    🧠 В моей базе знаний:
       • Нейронов: {self.brain.graph.number_of_nodes()}
       • Категорий: {len(set(data.get('category', '') for _, data in self.brain.graph.nodes(data=True)))}"""
            answer['type'] = 'no_knowledge'
            answer['confidence'] = 0.2

        return answer

    def _calculate_confidence(self, thought_process: Dict) -> float:
        """Расчёт общей уверенности"""
        scores = []

        # Уверенность из знаний
        knowledge = thought_process['stages'].get('knowledge_retrieval', {})
        if knowledge.get('top_results'):
            for result in knowledge['top_results'][:3]:
                scores.append(result.get('confidence', 0.5))

        # Уверенность из критического анализа
        critical = thought_process['stages'].get('critical_analysis', {})
        if critical.get('confidence'):
            scores.append(critical['confidence'])

        # Уверенность из творческого решения
        creative = thought_process['stages'].get('creative_solution', {})
        if creative.get('confidence'):
            scores.append(creative['confidence'] * 0.8)

        # Базовая уверенность если нет данных
        if not scores:
            return 0.3

        return round(float(np.mean(scores)), 2)

    def _log_thought(self, thought_process: Dict):
        """Логирование процесса мышления"""
        self.thought_history.append({
            'timestamp': datetime.now(),
            'query': thought_process['query'][:100],
            'confidence': thought_process['confidence'],
            'duration': thought_process['duration'],
            'type': thought_process['final_answer']['type'] if thought_process['final_answer'] else 'unknown'
        })

        # Ограничиваем историю
        if len(self.thought_history) > 100:
            self.thought_history = self.thought_history[-100:]

    def learn_from_interaction(self, query: str, feedback: Dict):
        """Обучение на основе обратной связи"""
        if self.self_learning:
            self.self_learning.learn_from_interaction(query, None, feedback.get('feedback'),
                                                      feedback.get('success', False))

        self.decision_log.append({
            'query': query[:100],
            'feedback': feedback,
            'timestamp': datetime.now()
        })

    def get_thinking_stats(self) -> Dict:
        """Статистика работы движка"""
        return {
            'total_queries': len(self.thought_history),
            'avg_confidence': round(np.mean([t['confidence'] for t in self.thought_history]),
                                    2) if self.thought_history else 0,
            'avg_duration': round(np.mean([t['duration'] for t in self.thought_history]),
                                  3) if self.thought_history else 0,
            'mode': self.thinking_mode,
            'creativity_level': self.creativity_level,
            'recent_queries': [t['query'] for t in self.thought_history[-5:]]
        }