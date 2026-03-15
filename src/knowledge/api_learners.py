# src/knowledge/api_learners.py
import asyncio
import aiohttp
import requests
from typing import List, Dict, Optional
import time
from datetime import datetime
import hashlib
import logging
import wikipedia
import wikipediaapi
import arxiv

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APILearner:
    """
    Класс для автоматического получения знаний из интернета через API
    С исправленным Google Books и улучшенной обработкой ошибок
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
        self.session = None

        # Кэш для предотвращения повторных запросов
        self.cache = {}
        self.cache_ttl = 3600  # 1 час

        # Настройка Wikipedia для разных языков
        self.wiki_apis = {}
        for lang in ['ru', 'en', 'de', 'fr', 'es', 'it', 'zh', 'ja']:
            self.wiki_apis[lang] = wikipediaapi.Wikipedia(
                language=lang,
                extract_format=wikipediaapi.ExtractFormat.WIKI,
                user_agent='NeuroTutor/1.0 (Educational AI Project)'
            )

        # Rate limiting
        self.last_request_time = {}
        self.min_request_interval = 1.0  # Минимальный интервал между запросами (сек)

        print("🌐 API Learner инициализирован")
        print(f"   Поддерживается языков Wikipedia: {len(self.wiki_apis)}")

    async def __aenter__(self):
        """Асинхронная инициализация сессии"""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Асинхронное закрытие сессии"""
        if self.session:
            await self.session.close()

    def _check_rate_limit(self, source: str):
        """Проверка rate limiting"""
        now = time.time()
        if source in self.last_request_time:
            elapsed = now - self.last_request_time[source]
            if elapsed < self.min_request_interval:
                time.sleep(self.min_request_interval - elapsed)
        self.last_request_time[source] = time.time()

    def _get_cache_key(self, source: str, topic: str, language: str) -> str:
        """Создание ключа для кэша"""
        return hashlib.md5(f"{source}:{topic}:{language}".encode()).hexdigest()

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
            # Проверка кэша
            cache_key = self._get_cache_key('wikipedia', topic, language)
            if cache_key in self.cache:
                cached_time, cached_data = self.cache[cache_key]
                if time.time() - cached_time < self.cache_ttl:
                    print(f"   ✅ Использован кэш")
                    return cached_data

            self._check_rate_limit('wikipedia')

            # Получаем статью
            wiki = self.wiki_apis.get(language, self.wiki_apis['ru'])
            page = wiki.page(topic)

            if not page.exists():
                print(f"   ❌ Статья '{topic}' не найдена")
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

            # Сохраняем в кэш
            self.cache[cache_key] = (time.time(), stats)

            return stats

        except Exception as e:
            logger.error(f"❌ Ошибка при обучении из Wikipedia: {e}")
            return stats

    def _process_wikipedia_page(self, page, source: str) -> List:
        """
        Обработка страницы Wikipedia и создание нейронов
        """
        neurons = []

        # Основное содержание как отдельный нейрон
        if page.summary and len(page.summary) > 50:
            content = f"{page.title}: {page.summary[:500]}..."
            neuron_dict = self.ml.create_multilingual_neuron(
                self.brain,
                content,
                category=f"Wikipedia_{page.language}"
            )
            neurons.extend(list(neuron_dict.values()))

        # Обрабатываем секции
        for section in page.sections[:3]:  # Первые 3 секции
            if section.text and len(section.text) > 100:
                content = f"{page.title} - {section.title}: {section.text[:300]}..."
                neuron_dict = self.ml.create_multilingual_neuron(
                    self.brain,
                    content,
                    category=f"Wikipedia_{page.language}"
                )
                neurons.extend(list(neuron_dict.values()))

        return neurons

    def learn_from_arxiv(self, topic: str, max_results: int = 3) -> Dict:
        """
        Обучение из научных статей arXiv.org
        """
        print(f"\n📚 Учусь из arXiv: {topic}")

        stats = {
            'topic': topic,
            'papers': 0,
            'neurons': 0
        }

        try:
            self._check_rate_limit('arxiv')

            # Поиск статей
            search = arxiv.Search(
                query=topic,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )

            for paper in search.results():
                print(f"   📄 Статья: {paper.title[:80]}...")

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
            logger.error(f"❌ Ошибка при обучении из arXiv: {e}")
            return stats

    async def learn_from_google_books(self, topic: str, language: str = 'ru', max_results: int = 3) -> Dict:
        """
        Обучение из Google Books API
        ИСПРАВЛЕНО: с обработкой rate limiting и ошибок
        """
        print(f"\n📚 Учусь из Google Books: {topic} ({language})")

        stats = {
            'topic': topic,
            'books': 0,
            'neurons': 0,
            'error': None
        }

        try:
            self._check_rate_limit('google_books')

            params = {
                'q': topic,
                'maxResults': max_results,
                'langRestrict': language,
                'printType': 'books'
            }

            async with self.session.get(
                    'https://www.googleapis.com/books/v1/volumes',
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=10)
            ) as response:

                if response.status == 200:
                    data = await response.json()

                    if 'items' in data:
                        for item in data['items']:
                            volume = item.get('volumeInfo', {})
                            title = volume.get('title', 'Unknown')
                            description = volume.get('description', '')

                            if description and len(description) > 50:
                                content = f"{title}: {description[:500]}..."
                                neurons = self.ml.create_multilingual_neuron(
                                    self.brain,
                                    content,
                                    category="Books"
                                )
                                stats['neurons'] += len(neurons)
                                stats['books'] += 1
                                print(f"   📖 Книга: {title[:60]}...")
                            else:
                                print(f"   ⚠️ Книга без описания: {title}")
                    else:
                        print(f"   ⚠️ Книги не найдены")

                elif response.status == 429:
                    print(f"   ⚠️ Превышен лимит запросов (429). Ждём 60 секунд...")
                    await asyncio.sleep(60)
                    stats['error'] = 'rate_limit'
                    # Повторяем запрос
                    return await self.learn_from_google_books(topic, language, max_results)

                elif response.status == 403:
                    print(f"   ⚠️ Доступ запрещён (403). Возможно нужен API ключ")
                    stats['error'] = 'forbidden'

                else:
                    print(f"   ❌ Ошибка HTTP: {response.status}")
                    stats['error'] = f'http_{response.status}'

            return stats

        except asyncio.TimeoutError:
            print(f"   ❌ Timeout при запросе к Google Books")
            stats['error'] = 'timeout'
            return stats

        except Exception as e:
            logger.error(f"❌ Ошибка при обучении из Google Books: {e}")
            stats['error'] = str(e)
            return stats

    async def learn_from_openlibrary(self, topic: str, max_results: int = 3) -> Dict:
        """
        Обучение из OpenLibrary (бесплатная альтернатива Google Books)
        """
        print(f"\n📚 Учусь из OpenLibrary: {topic}")

        stats = {
            'topic': topic,
            'books': 0,
            'neurons': 0
        }

        try:
            self._check_rate_limit('openlibrary')

            params = {
                'q': topic,
                'limit': max_results
            }

            async with self.session.get(
                    'http://openlibrary.org/search.json',
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=10)
            ) as response:

                if response.status == 200:
                    data = await response.json()

                    for doc in data.get('docs', [])[:max_results]:
                        title = doc.get('title', 'Unknown')
                        authors = doc.get('author_name', ['Unknown'])[:2]
                        year = doc.get('first_publish_year', '')

                        content = f"{title} ({year}): Авторы - {', '.join(authors)}"
                        neurons = self.ml.create_multilingual_neuron(
                            self.brain,
                            content,
                            category="Books"
                        )
                        stats['neurons'] += len(neurons)
                        stats['books'] += 1
                        print(f"   📖 Книга: {title[:60]}...")

                else:
                    print(f"   ❌ Ошибка HTTP: {response.status}")

            return stats

        except Exception as e:
            logger.error(f"❌ Ошибка при обучении из OpenLibrary: {e}")
            return stats

    async def auto_learn(self, topic: str, depth: str = 'basic') -> Dict:
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
            'total_neurons': 0,
            'errors': []
        }

        # Определяем языки для изучения
        languages = ['ru', 'en', 'de'] if depth in ['medium', 'deep'] else ['ru']

        # 1. Wikipedia на разных языках
        for lang in languages:
            wiki_stats = self.learn_from_wikipedia(topic, lang, depth=2 if depth == 'deep' else 1)
            total_stats['sources'] += 1
            total_stats['total_neurons'] += wiki_stats.get('neurons', 0)
            if wiki_stats.get('articles', 0) == 0:
                total_stats['errors'].append(f'wikipedia_{lang}')

        # 2. Научные статьи (если тема научная)
        if depth in ['medium', 'deep']:
            arxiv_stats = self.learn_from_arxiv(topic, max_results=2)
            total_stats['sources'] += 1
            total_stats['total_neurons'] += arxiv_stats.get('neurons', 0)
            if arxiv_stats.get('papers', 0) == 0:
                total_stats['errors'].append('arxiv')

        # 3. Книги (Google Books + OpenLibrary как fallback)
        if depth in ['medium', 'deep']:
            # Пробуем Google Books
            async with self:
                books_stats = await self.learn_from_google_books(topic, 'ru', max_results=2)

            if books_stats.get('error'):
                print(f"   ⚠️ Google Books не сработал, используем OpenLibrary")
                # Fallback на OpenLibrary
                openlib_stats = await self.learn_from_openlibrary(topic, max_results=2)
                total_stats['sources'] += 1
                total_stats['total_neurons'] += openlib_stats.get('neurons', 0)
            else:
                total_stats['sources'] += 1
                total_stats['total_neurons'] += books_stats.get('neurons', 0)

        print("\n" + "=" * 50)
        print(f"📊 ИТОГИ ОБУЧЕНИЯ ПО ТЕМЕ '{topic}':")
        print(f"   Источников: {total_stats['sources']}")
        print(f"   Новых нейронов: {total_stats['total_neurons']}")
        if total_stats['errors']:
            print(f"   Ошибки: {', '.join(total_stats['errors'])}")

        # Сохраняем мозг после обучения
        self.brain.save("brain_after_auto_learn.pkl")

        return total_stats