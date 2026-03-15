# src/brain/multilingual.py
from typing import List, Dict
from langdetect import detect
from deep_translator import GoogleTranslator
import hashlib


class MultilingualProcessor:
    """Многоязычный процессор"""

    def __init__(self, brain):
        self.brain = brain
        self.supported_languages = {
            'ru': 'русский', 'en': 'english', 'de': 'german',
            'fr': 'french', 'es': 'spanish', 'it': 'italian',
            'ja': 'japanese', 'ko': 'korean', 'zh-cn': 'chinese'
        }
        self.default_language = 'ru'
        self.translation_cache = {}
        print("🌍 Многоязычный процессор инициализирован")

    def detect_language(self, text: str) -> str:
        """Определение языка"""
        try:
            if not text or len(text.strip()) < 3:
                return self.default_language
            lang = detect(text)
            return lang if lang in self.supported_languages else self.default_language
        except:
            return self.default_language

    def translate(self, text: str, target_lang: str = 'ru', source_lang: str = 'auto') -> str:
        """Перевод текста"""
        if not text or len(text.strip()) < 2:
            return text

        cache_key = hashlib.md5(f"{text}_{target_lang}".encode()).hexdigest()
        if cache_key in self.translation_cache:
            return self.translation_cache[cache_key]

        try:
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            translated = translator.translate(text)
            self.translation_cache[cache_key] = translated
            return translated
        except Exception as e:
            print(f"⚠️ Ошибка перевода: {e}")
            return text

    def search_multilingual(self, query: str) -> List:
        """Многоязычный поиск"""
        query_lang = self.detect_language(query)
        results = self.brain.think(query)

        if not results:
            for target_lang in ['en', 'ru']:
                if target_lang != query_lang:
                    translated = self.translate(query, target_lang, query_lang)
                    results = self.brain.think(translated)
                    if results:
                        break

        return results

    def create_multilingual_neuron(self, content: str, category: str = "general") -> Dict:
        """Создание многоязычного нейрона"""
        source_lang = self.detect_language(content)
        neurons = {}

        source_neuron = self.brain.create_neuron(content=content, category=category)
        neurons[source_lang] = source_neuron
        self.brain.graph.nodes[source_neuron.uid]['language'] = source_lang

        for target_lang in ['en', 'de', 'fr']:
            if target_lang != source_lang:
                try:
                    translated = self.translate(content, target_lang, source_lang)
                    trans_neuron = self.brain.create_neuron(content=translated, category=category)
                    neurons[target_lang] = trans_neuron
                    self.brain.graph.nodes[trans_neuron.uid]['language'] = target_lang
                    self.brain.create_synapse(source_neuron, trans_neuron, weight=0.95)
                except:
                    pass

        return neurons

    def get_language_stats(self, brain) -> Dict:
        stats = {lang: 0 for lang in self.supported_languages.keys()}
        for node_id, data in brain.graph.nodes(data=True):
            if 'language' in data:
                lang = data['language']
                if lang in stats:
                    stats[lang] += 1
        return stats