import re
import os
from pathlib import Path
import json
from typing import List, Dict, Tuple
import hashlib
from collections import Counter


class KnowledgeParser:
    """
    Парсер для извлечения знаний из текстовых файлов
    Улучшенная версия с более умным извлечением концепций
    """

    def __init__(self, brain):
        """
        Инициализация парсера

        Args:
            brain: экземпляр мозга (Cortex), в который будем добавлять знания
        """
        self.brain = brain
        self.topics = {}
        self.keywords_cache = {}

        # Стоп-слова (слова, которые не могут быть концепциями)
        self.stop_words = {
            'это', 'что', 'как', 'для', 'который', 'такой', 'также', 'все',
            'еще', 'уже', 'будет', 'быть', 'есть', 'они', 'оно', 'она', 'мы',
            'вы', 'ты', 'меня', 'тебя', 'него', 'нее', 'них', 'вас', 'нас',
            'когда', 'потом', 'затем', 'после', 'сейчас', 'теперь', 'всегда',
            'иногда', 'никогда', 'везде', 'всюду', 'там', 'тут', 'здесь',
            'так', 'такой', 'такая', 'такое', 'такие', 'поэтому', 'потому',
            'зачем', 'почему', 'откуда', 'куда', 'где', 'кто', 'что-то'
        }

    def parse_textbook(self, filepath: str, category: str = "general") -> Dict:
        """
        Парсинг учебника (текстового файла) и добавление знаний в мозг

        Args:
            filepath: путь к файлу
            category: категория знаний (Physics, Math, History...)

        Returns:
            Dict: статистика обработки
        """
        print(f"\n📖 Читаю учебник: {filepath}")
        print(f"📚 Категория: {category}")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"❌ Ошибка чтения файла: {e}")
            return {'error': str(e)}

        # Разбиваем на предложения
        sentences = self._split_sentences(text)
        print(f"📝 Найдено предложений: {len(sentences)}")

        # Извлекаем все возможные концепции
        concepts = self._extract_all_concepts(sentences)
        print(f"🔑 Извлечено концепций: {len(concepts)}")

        # Создаем нейроны для концепций
        created_neurons = []
        for concept in concepts:
            try:
                neuron = self.brain.create_neuron(
                    content=concept['text'],
                    category=category
                )
                created_neurons.append(neuron)

                # Добавляем метаданные
                self.brain.graph.nodes[neuron.uid]['source'] = filepath
                self.brain.graph.nodes[neuron.uid]['importance'] = concept['importance']
                self.brain.graph.nodes[neuron.uid]['keywords'] = concept.get('keywords', [])

            except Exception as e:
                print(f"⚠️ Ошибка создания нейрона: {e}")
                continue

        # Создаем связи между нейронами
        self._create_intelligent_connections(sentences, created_neurons)

        stats = {
            'file': filepath,
            'category': category,
            'sentences': len(sentences),
            'concepts': len(concepts),
            'neurons_created': len(created_neurons)
        }

        print(f"✅ Учебник обработан: создано {len(created_neurons)} нейронов")
        return stats

    def _split_sentences(self, text: str) -> List[str]:
        """Разбить текст на предложения"""
        # Убираем заголовки
        text = re.sub(r'^#.*$', '', text, flags=re.MULTILINE)

        # Разбиваем по точкам, восклицательным и вопросительным знакам
        sentences = re.split(r'[.!?]+', text)

        # Очищаем и фильтруем
        sentences = [
            s.strip()
            for s in sentences
            if len(s.strip()) > 15 and not s.strip().startswith('#')
        ]

        return sentences

    def _extract_all_concepts(self, sentences: List[str]) -> List[Dict]:
        """
        Извлечение всех возможных концепций из текста
        """
        concepts = []
        seen_texts = set()

        for sentence in sentences:
            # Извлекаем именованные сущности (слова с большой буквы)
            named_entities = re.findall(r'\b[А-Я][а-я]+\b', sentence)

            # Извлекаем термины в кавычках
            quoted_terms = re.findall(r'"([^"]+)"', sentence)

            # Извлекаем определения по паттернам
            definition_matches = self._extract_definitions(sentence)

            # Извлекаем ключевые термины (существительные)
            key_terms = self._extract_key_terms(sentence)

            # Объединяем все найденное
            all_candidates = []

            # Добавляем именованные сущности
            for entity in named_entities:
                if len(entity) > 3 and entity.lower() not in self.stop_words:
                    all_candidates.append({
                        'text': entity,
                        'importance': 0.7,
                        'type': 'entity'
                    })

            # Добавляем цитаты
            for quote in quoted_terms:
                if len(quote) > 5:
                    all_candidates.append({
                        'text': quote,
                        'importance': 0.8,
                        'type': 'quote'
                    })

            # Добавляем определения
            for definition in definition_matches:
                all_candidates.append({
                    'text': definition,
                    'importance': 1.0,
                    'type': 'definition'
                })

            # Добавляем ключевые термины
            for term in key_terms:
                if term not in [c['text'] for c in all_candidates]:
                    all_candidates.append({
                        'text': term,
                        'importance': 0.6,
                        'type': 'term'
                    })

            # Добавляем целые предложения как концепции (если они важные)
            if self._is_important_sentence(sentence):
                if len(sentence) < 200 and sentence not in seen_texts:
                    all_candidates.append({
                        'text': sentence,
                        'importance': 0.5,
                        'type': 'fact'
                    })
                    seen_texts.add(sentence)

            # Добавляем все найденное в общий список
            for candidate in all_candidates:
                # Проверяем на дубликаты
                text_key = candidate['text'][:50]
                if text_key not in seen_texts:
                    concepts.append(candidate)
                    seen_texts.add(text_key)

        # Удаляем дубликаты и сортируем по важности
        unique_concepts = {}
        for c in concepts:
            key = c['text'][:50]
            if key not in unique_concepts or c['importance'] > unique_concepts[key]['importance']:
                unique_concepts[key] = c

        # Сортируем по важности
        sorted_concepts = sorted(
            unique_concepts.values(),
            key=lambda x: x['importance'],
            reverse=True
        )

        return sorted_concepts

    def _extract_definitions(self, sentence: str) -> List[str]:
        """Извлечение определений из предложения"""
        definitions = []

        # Паттерны определений
        patterns = [
            r'([А-Яа-я][^\.]+?)\s+[-—]\s+([^\.]+)',  # "Термин - определение"
            r'([А-Яа-я][^\.]+?)\s+[-—]+\s+это\s+([^\.]+)',  # "Термин — это ..."
            r'([А-Яа-я][^\.]+?)\s+называется\s+([^\.]+)',  # "... называется ..."
            r'([А-Яа-я][^\.]+?)\s+представляет\s+собой\s+([^\.]+)',  # "... представляет собой ..."
            r'([А-Яа-я][^\.]+?)\s+[-—]+\s+одна\s+из\s+([^\.]+)',  # "... - одна из ..."
        ]

        for pattern in patterns:
            matches = re.findall(pattern, sentence)
            for match in matches:
                if isinstance(match, tuple):
                    definition = f"{match[0]} - {match[1]}"
                else:
                    definition = match

                if len(definition) < 200:
                    definitions.append(definition)

        return definitions

    def _extract_key_terms(self, sentence: str) -> List[str]:
        """Извлечение ключевых терминов из предложения"""
        # Находим все слова длиной больше 4 букв
        words = re.findall(r'\b[а-яА-Я]{4,}\b', sentence.lower())

        # Фильтруем стоп-слова
        words = [w for w in words if w not in self.stop_words]

        # Считаем частоту (для контекста всего текста)
        word_freq = Counter(words)

        # Выбираем самые частые
        key_terms = []
        for word, freq in word_freq.most_common(5):
            if freq > 0:
                key_terms.append(word)

        return key_terms

    def _is_important_sentence(self, sentence: str) -> bool:
        """Проверка, является ли предложение важным"""
        # Маркеры важности
        importance_markers = [
            'закон', 'теорема', 'правило', 'принцип', 'формула',
            'открыл', 'изобрел', 'создал', 'разработал',
            'важно', 'основной', 'главный', 'ключевой',
            'определение', 'свойство', 'характеристика'
        ]

        sentence_lower = sentence.lower()
        for marker in importance_markers:
            if marker in sentence_lower:
                return True

        return False

    def _create_intelligent_connections(self, sentences: List[str], neurons: List):
        """
        Умное создание связей между нейронами
        """
        if not neurons or len(neurons) < 2:
            print("   Недостаточно нейронов для создания связей")
            return

        # Создаем индекс ключевых слов для каждого нейрона
        neuron_keywords = {}
        for neuron in neurons:
            # Извлекаем ключевые слова из содержания нейрона
            content_lower = neuron.content.lower()
            words = re.findall(r'\b[а-яА-Я]{4,}\b', content_lower)
            keywords = set([w for w in words if w not in self.stop_words])
            neuron_keywords[neuron.uid] = keywords

        # Создаем матрицу связей
        connections = {}

        # Анализируем каждое предложение
        for sentence in sentences:
            sentence_lower = sentence.lower()

            # Находим нейроны, которые могут быть связаны с этим предложением
            active_neurons = []
            for neuron in neurons:
                # Проверяем, есть ли ключевые слова нейрона в предложении
                keywords = neuron_keywords[neuron.uid]
                if any(keyword in sentence_lower for keyword in keywords):
                    active_neurons.append(neuron)

            # Создаем связи между активными нейронами
            if len(active_neurons) > 1:
                for i in range(len(active_neurons)):
                    for j in range(i + 1, len(active_neurons)):
                        key = tuple(sorted([active_neurons[i].uid, active_neurons[j].uid]))
                        connections[key] = connections.get(key, 0) + 1

        # Создаем синапсы для найденных связей
        created_count = 0
        for (uid1, uid2), count in connections.items():
            try:
                # Вес зависит от частоты совместной встречаемости
                weight = min(0.9, count * 0.15)

                # Создаем синапс только если вес достаточно большой
                if weight > 0.3:
                    neuron1 = self.brain.graph.nodes[uid1]['neuron']
                    neuron2 = self.brain.graph.nodes[uid2]['neuron']

                    self.brain.create_synapse(neuron1, neuron2, weight)
                    created_count += 1
                    print(f"🔗 Связано: {neuron1.content[:30]}... ↔ {neuron2.content[:30]}... (вес: {weight:.2f})")

            except Exception as e:
                print(f"⚠️ Ошибка создания связи: {e}")

        if created_count == 0:
            print("   🤔 Связей не найдено. Попробуйте добавить больше текста или улучшить ключевые слова.")
        else:
            print(f"   ✅ Создано {created_count} новых связей")


# src/knowledge/tokenizer.py (оставляем как есть)

class SimpleTokenizer:
    """
    Простой токенизатор для обработки текста
    """

    def __init__(self):
        self.word_counts = {}
        self.total_words = 0

    def tokenize(self, text: str) -> List[str]:
        """
        Разбить текст на слова (токены)
        """
        # Приводим к нижнему регистру и убираем знаки препинания
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        # Разбиваем на слова
        words = text.split()
        # Фильтруем короткие слова
        words = [w for w in words if len(w) > 2]

        return words

    def extract_keywords(self, text: str, top_n: int = 10) -> List[Tuple[str, float]]:
        """
        Извлечение ключевых слов из текста
        """
        words = self.tokenize(text)

        # Считаем частоту слов
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1

        # Нормализуем
        max_freq = max(word_freq.values()) if word_freq else 1
        keywords = [(word, freq / max_freq) for word, freq in word_freq.items()]

        # Сортируем по важности
        keywords.sort(key=lambda x: x[1], reverse=True)

        return keywords[:top_n]