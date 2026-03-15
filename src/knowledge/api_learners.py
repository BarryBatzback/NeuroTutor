# src/knowledge/api_learners.py

import requests
import wikipedia
import wikipediaapi
import re
from typing import List, Dict, Optional
import time
from googlesearch import search
import feedparser
import arxiv
import warnings

warnings.filterwarnings('ignore')


class APILearner:
    """
    Класс для автоматического получения знаний из интернета через API
    """

    def __init__(self, brain, multilingual):
        """
        Инициализация

        Args:
            brain: экземпляр мозга
            multilingual: многоязычный процессор
        """
        self.brain = brain
        self.ml = multilingual
        self.learned_count = 0

        # Настройка Wikipedia для разных языков
        self.wiki_apis = {}
        for lang in ['ru', 'en', 'de', 'fr', 'es', 'it', 'zh', 'ja']:
            # ИСПРАВЛЕНО: не передавай user_agent как именованный аргумент
            self.wiki_apis[lang] = wikipediaapi.Wikipedia(lang)

        print("🌐 API Learner инициализирован")

    def learn_from_wikipedia(self, topic: str, language: str = 'ru', depth: int = 1) -> Dict:
        """
        Обучение из Wikipedia

        Args:
            topic: тема для изучения
            language: язык
            depth: глубина (1 - только статья, 2 - связанные статьи)

        Returns:
            Dict: статистика обучения
        """
        print(f"\n📚 Учусь из Wikipedia: {topic} ({language})")

        stats = {
            'topic': topic,
            'language': language,
            'articles': 0,
            'neurons': 0,
            'connections': 0
        }

        try:
            # Получаем статью
            wiki = self.wiki_apis.get(language, self.wiki_apis['ru'])
            page = wiki.page(topic)

            if not page.exists():
                print(f"❌ Статья '{topic}' не найдена")
                return stats

            # Обрабатываем основную статью
            neurons = self._process_wikipedia_page(page, f"Wiki:{language}")
            stats['neurons'] += len(neurons)
            stats['articles'] += 1

            print(f"   ✅ Основная статья: {len(neurons)} нейронов")

            # Если глубина > 1, обрабатываем связанные статьи
            if depth > 1:
                links = list(page.links.items())[:5]  # Первые 5 ссылок
                for title, link_page in links:
                    if link_page.exists():
                        print(f"   🔗 Связанная статья: {title}")
                        neurons = self._process_wikipedia_page(link_page, f"Wiki:{language}")
                        stats['neurons'] += len(neurons)
                        stats['articles'] += 1
                        time.sleep(0.5)  # Не перегружаем API

            return stats

        except Exception as e:
            print(f"❌ Ошибка при обучении из Wikipedia: {e}")
            return stats

    def _process_wikipedia_page(self, page, source: str) -> List:
        """
        Обработка страницы Wikipedia и создание нейронов

        Args:
            page: страница Wikipedia
            source: источник

        Returns:
            List: созданные нейроны
        """
        neurons = []

        # Разбиваем на секции
        sections = page.sections

        # Основное содержание как отдельный нейрон
        if page.summary and len(page.summary) > 50:
            content = f"{page.title}: {page.summary[:500]}..."
            neuron = self.ml.create_multilingual_neuron(
                self.brain,
                content,
                category=f"Wikipedia_{page.language}"
            )
            neurons.extend(neuron.values())

        # Обрабатываем секции
        for section in sections[:3]:  # Первые 3 секции
            if section.text and len(section.text) > 100:
                content = f"{page.title} - {section.title}: {section.text[:300]}..."
                neuron = self.ml.create_multilingual_neuron(
                    self.brain,
                    content,
                    category=f"Wikipedia_{page.language}"
                )
                neurons.extend(neuron.values())

        return neurons

    def learn_from_arxiv(self, query: str, max_results: int = 3) -> Dict:
        """
        Обучение из научных статей arXiv.org

        Args:
            query: поисковый запрос
            max_results: максимум результатов

        Returns:
            Dict: статистика обучения
        """
        print(f"\n📚 Учусь из arXiv: {query}")

        stats = {
            'query': query,
            'papers': 0,
            'neurons': 0
        }

        try:
            # Поиск статей
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )

            for paper in search.results():
                print(f"   📄 Статья: {paper.title}")

                # Создаем нейрон из заголовка и summary
                content = f"{paper.title}: {paper.summary[:500]}..."
                neurons = self.ml.create_multilingual_neuron(
                    self.brain,
                    content,
                    category="Science"
                )
                stats['neurons'] += len(neurons)
                stats['papers'] += 1

                # Добавляем метаданные
                for neuron in neurons.values():
                    self.brain.graph.nodes[neuron.uid]['arxiv_id'] = paper.entry_id
                    self.brain.graph.nodes[neuron.uid]['authors'] = ', '.join(str(a) for a in paper.authors)

                time.sleep(1)  # Пауза между запросами

            return stats

        except Exception as e:
            print(f"❌ Ошибка при обучении из arXiv: {e}")
            return stats

    def learn_from_google_books(self, query: str, max_results: int = 3) -> Dict:
        """
        Обучение из Google Books API

        Args:
            query: поисковый запрос
            max_results: максимум результатов

        Returns:
            Dict: статистика обучения
        """
        print(f"\n📚 Учусь из Google Books: {query}")

        stats = {
            'query': query,
            'books': 0,
            'neurons': 0
        }

        try:
            url = "https://www.googleapis.com/books/v1/volumes"
            params = {
                'q': query,
                'maxResults': max_results,
                'langRestrict': 'ru,en',
                'printType': 'books'
            }

            response = requests.get(url, params=params)
            data = response.json()

            if 'items' in data:
                for item in data['items']:
                    volume = item['volumeInfo']
                    title = volume.get('title', '')
                    subtitle = volume.get('subtitle', '')
                    description = volume.get('description', '')

                    if description:
                        content = f"{title}: {subtitle} - {description[:500]}..."
                        neurons = self.ml.create_multilingual_neuron(
                            self.brain,
                            content,
                            category="Books"
                        )
                        stats['neurons'] += len(neurons)
                        stats['books'] += 1

                        print(f"   📖 Книга: {title}")

            return stats

        except Exception as e:
            print(f"❌ Ошибка при обучении из Google Books: {e}")
            return stats

    def learn_from_wiktionary(self, word: str, language: str = 'ru') -> Dict:
        """
        Обучение определению слова из Wiktionary

        Args:
            word: слово для изучения
            language: язык

        Returns:
            Dict: статистика обучения
        """
        print(f"\n📚 Учу определение: {word} ({language})")

        stats = {
            'word': word,
            'definitions': 0,
            'neurons': 0
        }

        try:
            # Используем Wikipedia для получения определения
            wiki = self.wiki_apis[language]
            page = wiki.page(word)

            if page.exists() and page.summary:
                content = f"Определение {word}: {page.summary[:300]}..."
                neurons = self.ml.create_multilingual_neuron(
                    self.brain,
                    content,
                    category="Definitions"
                )
                stats['neurons'] += len(neurons)
                stats['definitions'] += 1
                print(f"   ✅ Определение добавлено")

            return stats

        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return stats

    def learn_from_news(self, topic: str, language: str = 'ru') -> Dict:
        """
        Обучение из новостей RSS

        Args:
            topic: тема
            language: язык

        Returns:
            Dict: статистика обучения
        """
        print(f"\n📚 Учусь из новостей: {topic}")

        # RSS ленты новостей по темам
        rss_feeds = {
            'science': {
                'ru': 'https://ria.ru/export/rss2/science/index.xml',
                'en': 'https://www.sciencedaily.com/rss/all.xml',
                'de': 'https://www.heise.de/rss/heise-atom.xml'
            },
            'technology': {
                'ru': 'https://habr.com/ru/rss/news/',
                'en': 'https://techcrunch.com/feed/',
                'de': 'https://www.heise.de/rss/heise-atom.xml'
            },
            'history': {
                'ru': 'https://historyrussia.org/feed',
                'en': 'https://www.history.com/.rss/full/'
            }
        }

        stats = {
            'topic': topic,
            'articles': 0,
            'neurons': 0
        }

        try:
            if topic in rss_feeds and language in rss_feeds[topic]:
                feed = feedparser.parse(rss_feeds[topic][language])

                for entry in feed.entries[:5]:  # Первые 5 новостей
                    title = entry.get('title', '')
                    summary = entry.get('summary', '')[:300]

                    if title and summary:
                        content = f"{title}: {summary}"
                        neurons = self.ml.create_multilingual_neuron(
                            self.brain,
                            content,
                            category=f"News_{topic}"
                        )
                        stats['neurons'] += len(neurons)
                        stats['articles'] += 1
                        print(f"   📰 Статья: {title[:50]}...")

            return stats

        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return stats

    def auto_learn(self, topic: str, depth: str = 'basic') -> Dict:
        """
        Автоматическое обучение по теме из всех доступных источников

        Args:
            topic: тема
            depth: глубина ('basic', 'medium', 'deep')

        Returns:
            Dict: общая статистика
        """
        print(f"\n🎓 АВТОМАТИЧЕСКОЕ ОБУЧЕНИЕ: {topic}")
        print("=" * 50)

        total_stats = {
            'topic': topic,
            'sources': 0,
            'total_neurons': 0
        }

        # Определяем языки для изучения
        languages = ['ru', 'en', 'de'] if depth in ['medium', 'deep'] else ['ru']

        # 1. Wikipedia на разных языках
        for lang in languages:
            wiki_stats = self.learn_from_wikipedia(topic, lang, depth=2 if depth == 'deep' else 1)
            total_stats['sources'] += 1
            total_stats['total_neurons'] += wiki_stats.get('neurons', 0)

        # 2. Определение из Wiktionary
        if depth in ['medium', 'deep']:
            for lang in languages[:1]:  # Только для основного языка
                dict_stats = self.learn_from_wiktionary(topic, lang)
                total_stats['sources'] += 1
                total_stats['total_neurons'] += dict_stats.get('neurons', 0)

        # 3. Научные статьи (если тема научная)
        if depth == 'deep':
            arxiv_stats = self.learn_from_arxiv(topic)
            total_stats['sources'] += 1
            total_stats['total_neurons'] += arxiv_stats.get('neurons', 0)

        # 4. Книги по теме
        if depth in ['medium', 'deep']:
            books_stats = self.learn_from_google_books(topic)
            total_stats['sources'] += 1
            total_stats['total_neurons'] += books_stats.get('neurons', 0)

        # 5. Новости по теме
        if depth == 'deep':
            for lang in languages:
                news_stats = self.learn_from_news(topic, lang)
                total_stats['sources'] += 1
                total_stats['total_neurons'] += news_stats.get('neurons', 0)

        print("\n" + "=" * 50)
        print(f"📊 ИТОГИ ОБУЧЕНИЯ ПО ТЕМЕ '{topic}':")
        print(f"   Источников: {total_stats['sources']}")
        print(f"   Новых нейронов: {total_stats['total_neurons']}")

        # Сохраняем мозг после обучения
        self.brain.save("brain_after_auto_learn.pkl")

        return total_stats