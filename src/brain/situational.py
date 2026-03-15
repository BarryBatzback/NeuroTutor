# src/brain/situational.py
import re
from typing import Dict, List, Optional
from datetime import datetime
import numpy as np


class SituationalAwareness:
    """
    Модуль ситуативности - понимание контекста и адаптация поведения
    Позволяет ИИ учитывать обстоятельства, настроение пользователя,
    время, место и другие контекстуальные факторы
    """

    def __init__(self, brain):
        self.brain = brain
        self.context = {
            'time': None,
            'user_mood': None,
            'urgency': 0.5,
            'complexity_preference': 0.5,
            'conversation_history': [],
            'user_expertise': 'intermediate'
        }
        self.emotion_keywords = {
            'positive': ['рад', 'отлично', 'замечательно', 'спасибо', 'круто', 'супер'],
            'negative': ['грустно', 'плохо', 'не понимаю', 'сложно', 'устал', 'проблема'],
            'confused': ['непонятно', 'запутался', 'как', 'почему', 'что'],
            'urgent': ['срочно', 'быстро', 'немедленно', 'сейчас', 'важно']
        }
        print("🌍 Модуль ситуативности инициализирован")

    def analyze_context(self, user_input: str, user_id: str = None) -> Dict:
        """
        Анализирует контекст запроса пользователя
        Args:
            user_input: текст сообщения пользователя
            user_id: идентификатор пользователя (опционально)
        Returns:
            Dict: анализированный контекст
        """
        context = self.context.copy()

        # Определяем время
        context['time'] = self._get_time_context()

        # Анализируем настроение
        context['user_mood'] = self._detect_emotion(user_input)

        # Определяем срочность
        context['urgency'] = self._detect_urgency(user_input)

        # Оцениваем сложность запроса
        context['query_complexity'] = self._assess_complexity(user_input)

        # Определяем тип запроса
        context['query_type'] = self._identify_query_type(user_input)

        # Добавляем в историю
        self.context['conversation_history'].append({
            'input': user_input[:100],
            'timestamp': datetime.now(),
            'context': context.copy()
        })

        # Ограничиваем историю последними 10 сообщениями
        if len(self.context['conversation_history']) > 10:
            self.context['conversation_history'] = self.context['conversation_history'][-10:]

        return context

    def _get_time_context(self) -> Dict:
        """Определяет временной контекст"""
        now = datetime.now()
        hour = now.hour

        if 5 <= hour < 12:
            period = 'morning'
            energy_level = 0.8
        elif 12 <= hour < 18:
            period = 'afternoon'
            energy_level = 0.7
        elif 18 <= hour < 23:
            period = 'evening'
            energy_level = 0.5
        else:
            period = 'night'
            energy_level = 0.3

        return {
            'period': period,
            'hour': hour,
            'energy_level': energy_level,
            'is_weekend': now.weekday() >= 5
        }

    def _detect_emotion(self, text: str) -> Dict:
        """
        Определяет эмоциональную окраску текста
        """
        text_lower = text.lower()
        scores = {
            'positive': 0,
            'negative': 0,
            'confused': 0,
            'urgent': 0
        }

        for emotion, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    scores[emotion] += 1

        # Нормализуем
        total = sum(scores.values())
        if total > 0:
            scores = {k: v / total for k, v in scores.items()}

        # Определяем доминирующую эмоцию
        dominant = max(scores, key=scores.get) if max(scores.values()) > 0 else 'neutral'

        return {
            'dominant': dominant,
            'scores': scores,
            'intensity': max(scores.values())
        }

    def _detect_urgency(self, text: str) -> float:
        """
        Определяет уровень срочности запроса
        """
        urgent_words = ['срочно', 'быстро', 'немедленно', 'сейчас', 'важно',
                        'экстренно', 'асп', 'помогите', 'нужно']
        text_lower = text.lower()

        urgency_score = sum(1 for word in urgent_words if word in text_lower)

        # Учитываем знаки препинания
        if text.endswith('!') or text.endswith('!!!'):
            urgency_score += 0.5

        return min(1.0, urgency_score / 3)

    def _assess_complexity(self, text: str) -> float:
        """
        Оценивает сложность запроса
        """
        # Считаем количество технических терминов
        technical_terms = [
            'интеграл', 'производная', 'тензор', 'алгоритм', 'нейрон',
            'квантовый', 'дифференциал', 'матрица', 'вектор', 'функция'
        ]

        text_lower = text.lower()
        technical_count = sum(1 for term in technical_terms if term in text_lower)

        # Оцениваем длину и структуру
        words = text.split()
        sentence_count = text.count('.') + text.count('?') + text.count('!')

        complexity = (
                             len(words) / 20 +  # Длина
                             technical_count / 3 +  # Технические термины
                             sentence_count / 2  # Количество предложений
                     ) / 3

        return min(1.0, complexity)

    def _identify_query_type(self, text: str) -> str:
        """
        Определяет тип запроса пользователя
        """
        text_lower = text.lower()

        if any(word in text_lower for word in ['что такое', 'определение', 'это']):
            return 'definition'
        elif any(word in text_lower for word in ['как', 'способ', 'метод']):
            return 'how_to'
        elif any(word in text_lower for word in ['почему', 'причина', 'зачем']):
            return 'why'
        elif any(word in text_lower for word in ['реши', 'вычисли', 'найти']):
            return 'problem_solving'
        elif any(word in text_lower for word in ['сравни', 'разница', 'отличие']):
            return 'comparison'
        elif '?' in text:
            return 'question'
        else:
            return 'statement'

    def adapt_response(self, response: str, context: Dict) -> str:
        """
        Адаптирует ответ под контекст ситуации
        """
        adapted = response

        # Адаптация под срочность
        if context['urgency'] > 0.7:
            # Делаем ответ короче и прямее
            adapted = self._make_concise(adapted)

        # Адаптация под настроение
        emotion = context['user_mood']['dominant']
        if emotion == 'confused':
            adapted = self._add_clarity(adapted)
        elif emotion == 'negative':
            adapted = self._add_empathy(adapted)

        # Адаптация под время суток
        if context['time']['period'] == 'night':
            adapted = self._make_calmer(adapted)

        # Адаптация под сложность
        if context['query_complexity'] > 0.7:
            adapted = self._add_detail(adapted)
        else:
            adapted = self._simplify(adapted)

        return adapted

    def _make_concise(self, text: str) -> str:
        """Делает текст более кратким"""
        # Убираем лишние подробности
        sentences = text.split('. ')
        if len(sentences) > 2:
            return '. '.join(sentences[:2]) + '.'
        return text

    def _add_clarity(self, text: str) -> str:
        """Добавляет пояснения для запутавшегося пользователя"""
        return f"Давайте разберём по шагам:\n\n{text}\n\nЕсли что-то непонятно — спрашивайте!"

    def _add_empathy(self, text: str) -> str:
        """Добавляет эмпатию для расстроенного пользователя"""
        return f"Понимаю, что это может быть непросто. 😊\n\n{text}\n\nМы разберёмся вместе!"

    def _make_calmer(self, text: str) -> str:
        """Делает тон более спокойным для ночного времени"""
        return text.replace('!', '.').replace('ВАЖНО', 'важно')

    def _add_detail(self, text: str) -> str:
        """Добавляет детали для сложных запросов"""
        return text + "\n\n📚 *Дополнительно:* Если нужны более глубокие объяснения — дайте знать!"

    def _simplify(self, text: str) -> str:
        """Упрощает текст для начинающих"""
        # Простая замена сложных слов
        simplifications = {
            'интегрировать': 'объединить',
            'дифференцировать': 'различать',
            'оптимизировать': 'улучшить',
            'имплементировать': 'реализовать'
        }
        for complex_word, simple_word in simplifications.items():
            text = text.replace(complex_word, simple_word)
        return text

    def recommend_approach(self, query_type: str, context: Dict) -> Dict:
        """
        Рекомендует подход к ответу на основе типа запроса и контекста
        """
        approaches = {
            'definition': {
                'structure': 'simple',
                'include_examples': True,
                'technical_depth': context['query_complexity']
            },
            'how_to': {
                'structure': 'step_by_step',
                'include_examples': True,
                'technical_depth': 0.8
            },
            'why': {
                'structure': 'causal_chain',
                'include_examples': True,
                'technical_depth': 0.9
            },
            'problem_solving': {
                'structure': 'algorithmic',
                'include_examples': True,
                'technical_depth': 1.0
            },
            'comparison': {
                'structure': 'table',
                'include_examples': True,
                'technical_depth': 0.7
            },
            'question': {
                'structure': 'direct',
                'include_examples': context['query_complexity'] > 0.5,
                'technical_depth': context['query_complexity']
            },
            'statement': {
                'structure': 'conversational',
                'include_examples': False,
                'technical_depth': 0.3
            }
        }

        base_approach = approaches.get(query_type, approaches['question'])

        # Корректируем под контекст
        if context['urgency'] > 0.7:
            base_approach['structure'] = 'direct'
            base_approach['include_examples'] = False

        if context['user_mood']['dominant'] == 'confused':
            base_approach['technical_depth'] = min(0.5, base_approach['technical_depth'])

        return base_approach

    def get_user_profile(self, user_id: str) -> Dict:
        """
        Получает профиль пользователя на основе истории
        """
        history = self.context['conversation_history']

        if not history:
            return {
                'expertise': 'unknown',
                'preferred_complexity': 0.5,
                'common_topics': [],
                'interaction_count': 0
            }

        # Анализируем историю
        topics = []
        complexity_scores = []

        for entry in history:
            complexity_scores.append(entry['context'].get('query_complexity', 0.5))
            # Здесь можно добавить извлечение тем

        return {
            'expertise': 'intermediate' if np.mean(complexity_scores) > 0.5 else 'beginner',
            'preferred_complexity': np.mean(complexity_scores),
            'common_topics': topics,
            'interaction_count': len(history)
        }

    def update_user_expertise(self, user_id: str, new_level: str):
        """Обновляет уровень экспертизы пользователя"""
        if new_level in ['beginner', 'intermediate', 'advanced']:
            self.context['user_expertise'] = new_level

    def get_statistics(self) -> Dict:
        """Статистика работы модуля ситуативности"""
        history = self.context['conversation_history']

        emotions = [h['context']['user_mood']['dominant'] for h in history]
        query_types = [h['context']['query_type'] for h in history]

        return {
            'total_interactions': len(history),
            'emotion_distribution': {
                emotion: emotions.count(emotion) / len(emotions) if emotions else 0
                for emotion in ['positive', 'negative', 'confused', 'neutral']
            },
            'query_type_distribution': {
                qtype: query_types.count(qtype) / len(query_types) if query_types else 0
                for qtype in set(query_types)
            },
            'average_urgency': np.mean([h['context']['urgency'] for h in history]) if history else 0.5,
            'average_complexity': np.mean([h['context']['query_complexity'] for h in history]) if history else 0.5
        }