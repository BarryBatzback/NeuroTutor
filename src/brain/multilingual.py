import re
from typing import List, Dict, Tuple
from langdetect import detect, DetectorFactory
from deep_translator import GoogleTranslator
import hashlib

# Для воспроизводимости результатов
DetectorFactory.seed = 0


class MultilingualProcessor:
    """
    Многоязычный процессор для мозга
    Позволяет понимать и отвечать на разных языках
    """

    def __init__(self):
        # Поддерживаемые языки
        self.supported_languages = {
            'ru': 'русский',
            'en': 'english',
            'de': 'german',
            'fr': 'french',
            'es': 'spanish',
            'it': 'italian',
            'zh-cn': 'chinese',
            'ja': 'japanese',
            'ko': 'korean',
            'ar': 'arabic',
            'hi': 'hindi'
        }

        # Язык по умолчанию
        self.default_language = 'ru'

        # Кэш переводов для оптимизации
        self.translation_cache = {}

        print(f"🌍 Многоязычный процессор инициализирован")
        print(f"   Поддерживается языков: {len(self.supported_languages)}")

    def detect_language(self, text: str) -> str:
        """
        Определение языка текста

        Args:
            text: входной текст

        Returns:
            str: код языка
        """
        try:
            if not text or len(text.strip()) < 3:
                return self.default_language

            lang = detect(text)

            # Проверяем, поддерживается ли язык
            if lang not in self.supported_languages:
                print(f"⚠️ Язык {lang} не в списке поддерживаемых, используем русский")
                return self.default_language

            return lang
        except:
            return self.default_language

    def translate(self, text: str, target_lang: str = 'ru', source_lang: str = 'auto') -> str:
        """
        Перевод текста

        Args:
            text: текст для перевода
            target_lang: целевой язык
            source_lang: исходный язык (auto = автоматическое определение)

        Returns:
            str: переведенный текст
        """
        if not text or len(text.strip()) < 2:
            return text

        # Создаем ключ для кэша
        cache_key = hashlib.md5(f"{text}_{target_lang}_{source_lang}".encode()).hexdigest()

        # Проверяем кэш
        if cache_key in self.translation_cache:
            return self.translation_cache[cache_key]

        try:
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            translated = translator.translate(text)

            # Сохраняем в кэш
            self.translation_cache[cache_key] = translated

            return translated
        except Exception as e:
            print(f"⚠️ Ошибка перевода: {e}")
            return text

    def create_multilingual_neuron(self, brain, content: str, category: str = "general") -> Dict:
        """
        Создание многоязычного нейрона (с переводами)

        Args:
            brain: экземпляр мозга
            content: содержание на любом языке
            category: категория

        Returns:
            Dict: словарь с созданными нейронами на разных языках
        """
        # Определяем исходный язык
        source_lang = self.detect_language(content)

        neurons = {}

        # Создаем нейрон на исходном языке
        source_neuron = brain.create_neuron(
            content=content,
            category=category
        )
        neurons[source_lang] = source_neuron

        # Добавляем метку языка
        brain.graph.nodes[source_neuron.uid]['language'] = source_lang

        # Создаем переводы на все поддерживаемые языки
        for target_lang in self.supported_languages.keys():
            if target_lang != source_lang:
                try:
                    translated = self.translate(content, target_lang, source_lang)

                    # Создаем нейрон с переводом
                    trans_neuron = brain.create_neuron(
                        content=translated,
                        category=category
                    )
                    neurons[target_lang] = trans_neuron

                    # Добавляем метку языка
                    brain.graph.nodes[trans_neuron.uid]['language'] = target_lang

                    # Связываем нейроны между языками (сильная связь)
                    brain.create_synapse(source_neuron, trans_neuron, weight=0.95)
                    brain.create_synapse(trans_neuron, source_neuron, weight=0.95)

                except Exception as e:
                    print(f"⚠️ Ошибка создания перевода на {target_lang}: {e}")

        return neurons

    def search_multilingual(self, brain, query: str) -> List:
        """
        Многоязычный поиск

        Args:
            brain: экземпляр мозга
            query: запрос на любом языке

        Returns:
            List: результаты поиска
        """
        # Определяем язык запроса
        query_lang = self.detect_language(query)

        # Сначала ищем на языке запроса
        results = brain.think(query)

        if results:
            return results

        # Если не нашли, пробуем перевести запрос на другие языки
        for target_lang in self.supported_languages.keys():
            if target_lang != query_lang:
                try:
                    translated_query = self.translate(query, target_lang, query_lang)
                    results = brain.think(translated_query)

                    if results:
                        print(f"🔍 Нашёл через перевод: {query_lang} → {target_lang}")
                        return results
                except:
                    continue

        return []

    def get_language_stats(self, brain) -> Dict:
        """
        Статистика по языкам в мозге

        Args:
            brain: экземпляр мозга

        Returns:
            Dict: статистика
        """
        stats = {lang: 0 for lang in self.supported_languages.keys()}

        for node_id, data in brain.graph.nodes(data=True):
            if 'language' in data:
                lang = data['language']
                if lang in stats:
                    stats[lang] += 1

        return stats