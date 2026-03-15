# src/brain/situational.py
import re
from typing import List, Dict, Optional
from datetime import datetime
import numpy as np
from collections import Counter


class SituationalAwareness:
    """
    Модуль ситуативной осведомленности
    Понимает контекст, настроение, срочность и адаптирует общение
    """

    def __init__(self, brain):
        self.brain = brain

        # Текущий контекст
        self.context = {
            'user_id': None,
            'time': None,
            'urgency': 0.5,  # 0 - спокойно, 1 - срочно
            'mood': 'neutral',  # neutral, happy, sad, angry, confused, curious
            'conversation_history': [],
            'topic_focus': None,
            'formality': 0.5,  # 0 - неформально, 1 - формально
            'expertise_level': 0.5  # 0 - новичок, 1 - эксперт
        }

        # Словари для анализа эмоций
        self.emotion_keywords = {
            'happy': [
                'рад', 'отлично', 'прекрасно', 'спасибо', 'класс', 'удивительно',
                'замечательно', 'восхищаюсь', 'счастлив', 'доволен', 'круто',
                'супер', 'восхитительно', 'потрясающе', 'великолепно'
            ],
            'sad': [
                'грустно', 'плохо', 'устал', 'проблема', 'ошибка', 'не работает',
                'разочарован', 'печально', 'тяжело', 'больно', 'ужасно',
                'кошмар', 'отвратительно', 'мерзко'
            ],
            'angry': [
                'бесит', 'ужасно', 'когда', 'почему', 'неправильно', 'глупость',
                'возмущён', 'злой', 'раздражает', 'невыносимо', 'достал',
                'ненавижу', 'отстой', 'фу'
            ],
            'confused': [
                'не понимаю', 'как', 'что', 'зачем', 'объясни', 'помогите',
                'запутался', 'сложно', 'неясно', 'вопрос', 'странно',
                'непонятно', 'загадка', 'тайна'
            ],
            'curious': [
                'интересно', 'любопытно', 'хочу узнать', 'расскажи', 'почему',
                'как работает', 'объясни', 'подробнее', 'увлекательно',
                'захватывающе', 'интригующе'
            ]
        }

        # Ключевые слова срочности
        self.urgency_keywords = [
            'срочно', 'быстро', 'немедленно', 'asap', 'горит',
            'важно', 'скорее', 'безотлагательно', 'экстренно',
            'когда', 'скоро', 'время', 'дедлайн', 'срок', 'сейчас'
        ]

        # Индикаторы формальности
        self.formality_indicators = {
            'formal': [
                'уважаемый', 'просьба', 'благодарю', 'будьте добры',
                'не могли бы', 'извините', 'разрешите', 'почтенный'
            ],
            'informal': [
                'привет', 'пока', 'ок', 'спс', 'чё', 'как дела',
                'здорово', 'ку', 'хай', 'йоу'
            ]
        }

        # История взаимодействий для обучения
        self.interaction_history = []

        print("🌍 Модуль ситуативности инициализирован")

    def update_context(self, user_id: str, user_input: str, timestamp: datetime = None):
        """
        Обновляет контекст на основе ввода пользователя
        """
        if timestamp is None:
            timestamp = datetime.now()

        self.context['user_id'] = user_id
        self.context['time'] = timestamp

        # Анализируем ввод
        self.context['mood'] = self.detect_emotion(user_input)
        self.context['urgency'] = self.detect_urgency(user_input)
        self.context['formality'] = self.detect_formality(user_input)
        self.context['topic_focus'] = self.extract_topic(user_input)
        self.context['expertise_level'] = self.detect_user_expertise(user_input)

        # Добавляем в историю
        self.context['conversation_history'].append({
            'timestamp': timestamp,
            'input': user_input[:200],
            'mood': self.context['mood'],
            'urgency': self.context['urgency']
        })

        # Ограничиваем историю последними 20 сообщениями
        if len(self.context['conversation_history']) > 20:
            self.context['conversation_history'] = self.context['conversation_history'][-20:]

        # Сохраняем в историю взаимодействий
        self.interaction_history.append({
            'timestamp': timestamp,
            'input': user_input[:200],
            'context': self.context.copy()
        })

        return self.context

    # src/brain/situational.py - обнови detect_emotion

    def detect_emotion(self, text: str) -> str:
        text_lower = text.lower()

        # ПРОВЕРКА НА НЕЙТРАЛЬНЫЕ ФРАЗЫ
        neutral_phrases = [
            'привет', 'здравствуй', 'добрый день', 'добрый вечер',
            'как дела', 'как жизнь', 'что нового', 'приветствую'
        ]
        if any(phrase in text_lower for phrase in neutral_phrases):
            return 'neutral'

        # Подсчет баллов с ВЕСАМИ для разных слов
        scores = {emotion: 0 for emotion in self.emotion_keywords.keys()}

        # Слова с высоким приоритетом для anger
        anger_priority = ['бесит', 'достал', 'ненавижу', 'злой', 'раздражает']
        # Слова с высоким приоритетом для sad
        sad_priority = ['грустно', 'плохо', 'устал', 'печально', 'больно']

        for emotion, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    # Повышенный вес для приоритетных слов
                    if emotion == 'angry' and keyword in anger_priority:
                        scores[emotion] += 1.5
                    elif emotion == 'sad' and keyword in sad_priority:
                        scores[emotion] += 1.5
                    else:
                        scores[emotion] += 1

        # Учитываем знаки препинания
        if text.endswith('!!!'):
            scores['angry'] += 0.5
            scores['happy'] += 0.3
        elif text.endswith('!'):
            scores['angry'] += 0.3

        max_score = max(scores.values())
        if max_score == 0:
            return 'neutral'

        for emotion, score in scores.items():
            if score == max_score:
                return emotion

        return 'neutral'

    # В методе detect_urgency обнови:

    def detect_urgency(self, text: str) -> float:
        """
        Определяет уровень срочности (0.0 - 1.0)
        """
        text_lower = text.lower()
        urgency_count = 0.0

        # Слова с ВЫСОКИМ приоритетом (вес 1.0)
        high_urgency = ['горит', 'немедленно', 'срочно', 'экстренно', 'asap']
        for word in high_urgency:
            if word in text_lower:
                urgency_count += 1.0

        # Слова со СРЕДНИМ приоритетом (вес 0.5)
        medium_urgency = ['быстро', 'скорее', 'важно', 'когда', 'будет',
                          'ждать', 'долг', 'дедлайн', 'срок', 'время']
        for word in medium_urgency:
            if word in text_lower:
                urgency_count += 0.5

        # Знаки препинания
        if text.endswith('!!!'):
            urgency_count += 1.5
        elif text.endswith('!!'):
            urgency_count += 1.0
        elif text.endswith('!'):
            urgency_count += 0.5

        # Короткие сообщения с вопросом (часто срочные)
        if len(text) < 25 and '?' in text:
            urgency_count += 0.3

        # Нормализация (максимум 1.0)
        return min(1.0, urgency_count / 2.5)

    def detect_formality(self, text: str) -> float:
        """
        Определяет уровень формальности (0.0 - 1.0)
        """
        text_lower = text.lower()

        formal_score = sum(1 for word in self.formality_indicators['formal'] if word in text_lower)
        informal_score = sum(1 for word in self.formality_indicators['informal'] if word in text_lower)

        # Длина предложения тоже показатель
        words = text.split()
        if words:
            avg_word_length = np.mean([len(word) for word in words])
            if avg_word_length > 7:
                formal_score += 0.5

        total = formal_score + informal_score
        if total == 0:
            return 0.5

        return formal_score / total

    def extract_topic(self, text: str) -> Optional[str]:
        """
        Извлекает основную тему из сообщения
        """
        # Простая эвристика: ищем существительные с большой буквы
        keywords = ['о', 'про', 'тема', 'вопрос', 'проблема', 'касается']
        words = text.split()

        for i, word in enumerate(words):
            if word.lower() in keywords and i + 1 < len(words):
                return words[i + 1].strip('.,!?')

        # Если нет ключевых слов, берем первое значимое слово
        for word in words:
            clean_word = word.strip('.,!?')
            if len(clean_word) > 4 and clean_word[0].isupper():
                return clean_word

        return None

    def detect_user_expertise(self, user_input: str) -> float:
        text_lower = user_input.lower()

        # Технические термины (эксперт)
        technical_indicators = [
            'алгоритм', 'функция', 'параметр', 'переменная',
            'класс', 'объект', 'метод', 'интерфейс',
            'производная', 'интеграл', 'матрица', 'вектор',
            'градиент', 'оптимизация', 'нейрон', 'сеть',
            'квант', 'физика', 'химия', 'биология',
            'архитектура', 'система', 'модуль', 'протокол'
        ]

        # Индикаторы новичка (ОБНОВЛЕНО!)
        beginner_indicators = [
            'что это', 'как начать', 'помогите', 'не понимаю',
            'объясните', 'для чайников', 'простыми словами',
            'новичок', 'первый раз', 'никогда не',
            'такое', 'это такое', 'что такое'  # НОВЫЕ!
        ]

        tech_score = sum(1 for term in technical_indicators if term in text_lower)
        beginner_score = sum(1 for term in beginner_indicators if term in text_lower)

        total = tech_score + beginner_score
        if total == 0:
            return 0.5

        # Если есть индикаторы новичка - возвращаем низкий уровень
        if beginner_score > 0 and tech_score == 0:
            return 0.2

        return min(1.0, tech_score / max(total, 1))

    def adapt_response(self, base_response: str, context: Dict = None) -> str:
        if context is None:
            context = self.context

        mood = context.get('mood', 'neutral')
        urgency = context.get('urgency', 0.5)

        # ТОЛЬКО ОДИН префикс - срочность имеет приоритет
        if urgency > 0.7:
            adapted = self._make_concise(base_response)
            prefix = "⚡ "  # ТОЛЬКО молния
        elif mood == 'confused':
            adapted = self._make_detailed(base_response, context.get('expertise_level', 0.5))
            prefix = "📚 "  # ТОЛЬКО книга
        elif mood == 'sad':
            prefix = "💙 "
            adapted = base_response + "\n\nЕсли что-то непонятно, я помогу разобраться!"
        elif mood == 'curious':
            prefix = "🔍 "
            adapted = base_response + "\n\n🔎 Хотите узнать больше деталей?"
        elif mood == 'happy':
            prefix = "😄 "
            adapted = base_response
        elif mood == 'angry':
            prefix = "😐 "
            adapted = base_response
        else:
            prefix = ""
            adapted = base_response

        return prefix + adapted  # БЕЗ дублирования

    def _make_concise(self, text: str) -> str:
        """Делает ответ более кратким"""
        # Удаляем вводные слова
        intro_words = [
            'например', 'вообще', 'собственно', 'таким образом',
            'следовательно', 'более того', 'кроме того', 'итак'
        ]
        for word in intro_words:
            text = text.replace(word, '')

        # Ограничиваем длину
        sentences = text.split('.')
        if len(sentences) > 3:
            text = '.'.join(sentences[:3]) + '.'

        return text.strip()

    def _make_detailed(self, text: str, expertise: float) -> str:
        """Делает ответ более подробным"""
        if expertise < 0.3:
            # Для новичков
            additions = [
                "\n\n💡 *Простыми словами:* Давайте разберём на примере.",
                "\n\n📌 *Важно:* Обратите внимание на ключевые моменты.",
                "\n\n❓ *Есть вопросы?* Спрашивайте, я объясню подробнее!"
            ]
        elif expertise > 0.7:
            # Для экспертов
            additions = [
                "\n\n🔬 *Технические детали:* Для углублённого изучения...",
                "\n\n📊 *Данные:* Статистика показывает...",
                "\n\n📚 *Литература:* Рекомендуется изучить..."
            ]
        else:
            # Средний уровень
            additions = [
                "\n\n💡 *Пример:* Рассмотрим это на практике.",
                "\n\n📌 *Ключевые моменты:* Запомните эти детали.",
                "\n\n🔗 *Связь:* Это связано с тем, что мы обсуждали."
            ]

        return text + additions[0]

    def _make_formal(self, text: str) -> str:
        """Делает ответ более формальным"""
        replacements = {
            'привет': 'Здравствуйте',
            'пока': 'До свидания',
            'ок': 'Хорошо',
            'спс': 'Благодарю',
            'чё': 'что',
            'щас': 'сейчас',
            'давай': 'предлагаю',
            'норм': 'удовлетворительно'
        }
        for informal, formal in replacements.items():
            text = text.replace(informal, formal)

        return text

    def _make_informal(self, text: str) -> str:
        """Делает ответ более неформальным"""
        replacements = {
            'Здравствуйте': 'Привет',
            'До свидания': 'Пока',
            'Благодарю': 'Спасибо',
            'не могли бы': 'можешь',
            'будьте добры': 'пожалуйста',
            'предлагаю': 'давай',
            'удовлетворительно': 'норм'
        }
        for formal, informal in replacements.items():
            text = text.replace(formal, informal)

        return text

    def get_context_summary(self) -> Dict:
        """
        Возвращает сводку текущего контекста
        """
        return {
            'user_id': self.context['user_id'],
            'time': self.context['time'].strftime('%H:%M:%S') if self.context['time'] else None,
            'mood': self.context['mood'],
            'urgency': f"{self.context['urgency']:.2f}",
            'formality': f"{self.context['formality']:.2f}",
            'topic': self.context['topic_focus'],
            'history_length': len(self.context['conversation_history']),
            'expertise_level': f"{self.context['expertise_level']:.2f}"
        }

    def is_repeated_question(self, user_input: str, threshold: int = 5) -> bool:
        """
        Проверяет, задавал ли пользователь этот вопрос недавно
        """
        recent_history = self.context['conversation_history'][-threshold:]
        for entry in recent_history:
            if user_input.lower() in entry['input'].lower() or entry['input'].lower() in user_input.lower():
                return True
        return False

    def learn_from_interaction(self, user_input: str, response: str, feedback: str = None):
        """
        Учится на взаимодействии с пользователем
        """
        interaction = {
            'timestamp': datetime.now(),
            'input': user_input[:200],
            'response': response[:200],
            'feedback': feedback,
            'context': self.context.copy()
        }

        self.interaction_history.append(interaction)

        # Если есть обратная связь, адаптируем стиль
        if feedback:
            if 'понятно' in feedback.lower() or 'спасибо' in feedback.lower():
                # Пользователь доволен - сохраняем стиль
                self.context['expertise_level'] = self.detect_user_expertise(user_input)
            elif 'непонятно' in feedback.lower() or 'сложно' in feedback.lower():
                # Нужно упростить
                self.context['expertise_level'] = max(0, self.context['expertise_level'] - 0.1)

    def get_statistics(self) -> Dict:
        """
        Статистика работы модуля ситуативности
        """
        mood_counts = {}
        for entry in self.interaction_history:
            mood = entry['context'].get('mood', 'neutral')
            mood_counts[mood] = mood_counts.get(mood, 0) + 1

        return {
            'total_interactions': len(self.interaction_history),
            'mood_distribution': mood_counts,
            'average_urgency': float(np.mean([e['context'].get('urgency', 0.5)
                                              for e in self.interaction_history])) if self.interaction_history else 0.5,
            'average_formality': float(np.mean([e['context'].get('formality', 0.5)
                                                for e in
                                                self.interaction_history])) if self.interaction_history else 0.5
        }