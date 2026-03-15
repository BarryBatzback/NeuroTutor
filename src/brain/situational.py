# src/brain/situational.py
import re
from typing import Dict, List, Optional
from datetime import datetime
import numpy as np


class SituationalAwareness:
    """
    Модуль ситуативности - понимание контекста и адаптация поведения
    """

    def __init__(self, brain, critical_thinking=None):
        """
        Инициализация модуля ситуативности
        Args:
            brain: экземпляр Cortex
            critical_thinking: экземпляр CriticalThinking (опционально)
        """
        self.brain = brain
        self.critical = critical_thinking

        # Контекст по умолчанию
        self.context = {
            'time_of_day': None,
            'user_mood': None,
            'urgency_level': 0.5,
            'user_expertise': 0.5,
            'conversation_history': [],
            'cultural_context': 'ru',
            'communication_style': 'neutral'
        }

        # Словари для анализа
        self.emotion_keywords = {
            'positive': ['рад', 'отлично', 'замечательно', 'супер', 'класс',
                         'хорошо', 'прекрасно', 'восхищён', 'доволен'],
            'negative': ['грустно', 'плохо', 'ужасно', 'разочарован', 'злюсь',
                         'расстроен', 'недоволен', 'печально', 'кошмар'],
            'confused': ['не понимаю', 'запутался', 'сложно', 'неясно',
                         'помогите', 'объясните', 'что это'],
            'urgent': ['срочно', 'быстро', 'немедленно', 'сейчас',
                       'как можно скорее', 'экстренно']
        }

        print("🌍 Модуль ситуативности инициализирован")

    def analyze_situation(self, user_input: str, meta: Dict = None) -> Dict:
        """Анализирует текущую ситуацию и контекст"""
        if meta is None:
            meta = {}

        # Обновляем время
        self.context['time_of_day'] = self._get_time_of_day()

        # Анализируем текст пользователя
        self.context['user_mood'] = self._detect_emotion(user_input)
        self.context['urgency_level'] = self._detect_urgency(user_input)
        self.context['user_expertise'] = self._estimate_expertise(user_input)

        # Применяем метаданные если есть
        if meta:
            if 'location' in meta:
                self.context['location'] = meta['location']
            if 'device' in meta:
                self.context['device'] = meta['device']

        # Добавляем в историю
        self.context['conversation_history'].append({
            'input': user_input[:200],
            'mood': self.context['user_mood'],
            'urgency': self.context['urgency_level'],
            'timestamp': datetime.now()
        })

        # Ограничиваем историю последними 10 сообщениями
        if len(self.context['conversation_history']) > 10:
            self.context['conversation_history'] = self.context['conversation_history'][-10:]

        return self.context.copy()

    def _get_time_of_day(self) -> str:
        """Определяет время суток"""
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 18:
            return 'afternoon'
        elif 18 <= hour < 23:
            return 'evening'
        else:
            return 'night'

    def _detect_emotion(self, text: str) -> str:
        """Определяет эмоциональную окраску текста"""
        text_lower = text.lower()
        scores = {}

        for emotion, keywords in self.emotion_keywords.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                scores[emotion] = score

        if not scores:
            return 'neutral'

        return max(scores, key=scores.get)

    def _detect_urgency(self, text: str) -> float:
        """Определяет уровень срочности (0-1)"""
        text_lower = text.lower()
        urgent_words = self.emotion_keywords['urgent']

        urgency_count = sum(1 for word in urgent_words if word in text_lower)

        if '?' in text and '!' in text:
            urgency_count += 1
        if text_lower.startswith('помогите') or text_lower.startswith('срочно'):
            urgency_count += 2

        return min(1.0, urgency_count * 0.25)

    def _estimate_expertise(self, text: str) -> float:
        """Оценивает уровень экспертности пользователя (0-1)"""
        beginner_indicators = [
            'что это', 'как работает', 'объясните просто', 'для чайников',
            'не понимаю', 'впервые слышу', 'с чего начать'
        ]

        expert_indicators = [
            'оптимизация', 'алгоритмическая сложность', 'асимптотика',
            'тензор', 'градиент', 'рекуррентный', 'параллелизм'
        ]

        text_lower = text.lower()

        beginner_score = sum(1 for ind in beginner_indicators if ind in text_lower)
        expert_score = sum(1 for ind in expert_indicators if ind in text_lower)

        if beginner_score > expert_score:
            return max(0.0, 0.5 - beginner_score * 0.15)
        elif expert_score > beginner_score:
            return min(1.0, 0.5 + expert_score * 0.15)
        else:
            return 0.5

    def adapt_response(self, base_response: str, context: Dict = None, confidence: float = 0.5) -> str:
        """Адаптирует ответ под ситуацию"""
        if context is None:
            context = self.context

        response = base_response

        # Адаптация под срочность
        if context.get('urgency_level', 0.5) > 0.8:
            response = "🚨 " + response[:200]  # Коротко и срочно

        # Адаптация под настроение
        mood = context.get('user_mood', 'neutral')
        if mood == 'confused':
            response = "📚 Поясняю просто: " + response
        elif mood == 'negative':
            response = "💪 Не переживайте! " + response

        # Адаптация под уровень экспертности
        expertise = context.get('user_expertise', 0.5)
        if expertise < 0.3:
            response = response.replace('алгоритм', 'способ').replace('оптимизация', 'улучшение')

        return response

    def get_statistics(self) -> Dict:
        """Статистика работы модуля"""
        history = self.context.get('conversation_history', [])

        emotions = [h.get('mood', 'neutral') for h in history]

        return {
            'total_interactions': len(history),
            'emotion_distribution': {
                emotion: emotions.count(emotion) / len(emotions) if emotions else 0
                for emotion in ['positive', 'negative', 'confused', 'neutral']
            },
            'average_urgency': np.mean([h.get('urgency', 0.5) for h in history]) if history else 0.5
        }