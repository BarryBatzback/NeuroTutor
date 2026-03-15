import sys
import warnings

warnings.filterwarnings('ignore')

# Проверка версии Python
PY_VERSION = sys.version_info
if PY_VERSION.major == 3 and PY_VERSION.minor >= 14:
    print("⚠️ Внимание: Используется Python 3.14+ (экспериментальная версия)")
    print("   Некоторые библиотеки могут быть недоступны")

# Безопасные импорты - ТОЛЬКО проверенные библиотеки
import asyncio
import aiohttp
import requests
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Optional, Set, Any
import hashlib
import time
from dataclasses import dataclass
from collections import defaultdict
import json
import re
from pathlib import Path
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class LearningSource:
    """Класс для описания источника знаний"""
    name: str
    priority: int  # 1-10 (выше = важнее)
    speed: float  # скорость получения (сек)
    quality: float  # качество информации (0-1)
    languages: List[str]
    cost: float  # стоимость API (0 - бесплатно)
    rate_limit: int  # запросов в минуту


class OptimizedLearner:
    """
    Упрощенная оптимизированная система обучения
    Совместима с Python 3.14+
    """

    def __init__(self, brain, multilingual, cache_size: int = 1000):
        """
        Инициализация оптимизированного обучения

        Args:
            brain: экземпляр мозга
            multilingual: многоязычный процессор
            cache_size: размер кэша
        """
        self.brain = brain
        self.ml = multilingual

        # Простой кэш в памяти
        self.cache = {}
        self.cache_size = cache_size

        # Статистика
        self.stats = defaultdict(int)
        self.learning_history = []

        # Thread pool для параллелизации
        self.thread_pool = ThreadPoolExecutor(max_workers=5)

        # Сессия для HTTP запросов
        self.session = None

        # Инициализируем источники
        self.sources = self._initialize_sources()

        print(f"🚀 OptimizedLearner инициализирован (Python {sys.version_info.major}.{sys.version_info.minor})")
        print(f"   Источников: {len(self.sources)}")
        print(f"   Thread pool: 5 workers")

    def _initialize_sources(self) -> Dict[str, LearningSource]:
        """Инициализация рабочих источников (без проблемных библиотек)"""

        return {
            # Wikipedia - работает через requests
            'wikipedia': LearningSource(
                name='Wikipedia',
                priority=10,
                speed=0.5,
                quality=0.9,
                languages=['ru', 'en', 'de', 'fr', 'es'],
                cost=0,
                rate_limit=200
            ),

            # arXiv - работает через feedparser
            'arxiv': LearningSource(
                name='arXiv',
                priority=8,
                speed=1.0,
                quality=0.95,
                languages=['en'],
                cost=0,
                rate_limit=50
            ),

            # Google Books - работает через aiohttp
            'google_books': LearningSource(
                name='Google Books',
                priority=7,
                speed=1.0,
                quality=0.85,
                languages=['ru', 'en'],
                cost=0,
                rate_limit=100
            ),

            # GitHub - работает через aiohttp
            'github': LearningSource(
                name='GitHub',
                priority=6,
                speed=1.0,
                quality=0.85,
                languages=['en'],
                cost=0,
                rate_limit=60
            ),

            # StackOverflow - работает через aiohttp
            'stackoverflow': LearningSource(
                name='StackOverflow',
                priority=7,
                speed=0.5,
                quality=0.9,
                languages=['en'],
                cost=0,
                rate_limit=60
            ),

            # OpenLibrary - бесплатная альтернатива Google Books
            'openlibrary': LearningSource(
                name='OpenLibrary',
                priority=6,
                speed=0.5,
                quality=0.7,
                languages=['ru', 'en'],
                cost=0,
                rate_limit=100
            ),

            # DuckDuckGo - поиск
            'duckduckgo': LearningSource(
                name='DuckDuckGo',
                priority=5,
                speed=0.5,
                quality=0.6,
                languages=['ru', 'en'],
                cost=0,
                rate_limit=100
            ),

            # NewsAPI - новости (если есть ключ)
            'news_api': LearningSource(
                name='News API',
                priority=5,
                speed=0.8,
                quality=0.6,
                languages=['ru', 'en'],
                cost=1,  # Требуется ключ
                rate_limit=100
            )
        }

    async def __aenter__(self):
        """Асинхронная инициализация"""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Асинхронное закрытие"""
        if self.session:
            await self.session.close()
        self.thread_pool.shutdown(wait=False)

    def _get_cache_key(self, source: str, topic: str, language: str) -> str:
        """Создание ключа для кэша"""
        return hashlib.md5(f"{source}:{topic}:{language}".encode()).hexdigest()

    async def _fetch_wikipedia(self, topic: str, language: str) -> Optional[Dict]:
        """
        Получение данных из Wikipedia (через requests)
        """
        cache_key = self._get_cache_key('wikipedia', topic, language)

        # Проверяем кэш
        if cache_key in self.cache:
            self.stats['cache_hits'] += 1
            return self.cache[cache_key]

        try:
            # Используем thread pool для requests
            loop = asyncio.get_event_loop()

            def _get_wiki():
                try:
                    # Пробуем через requests напрямую к API Wikipedia
                    url = f"https://{language}.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(topic)}"
                    headers = {'User-Agent': 'NeuroTutor/1.0'}
                    response = requests.get(url, headers=headers, timeout=5)

                    if response.status_code == 200:
                        data = response.json()
                        return {
                            'title': data.get('title', ''),
                            'summary': data.get('extract', ''),
                            'url': data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                            'source': 'wikipedia'
                        }
                except:
                    pass

                # Fallback на простой поиск
                try:
                    import wikipedia
                    wikipedia.set_lang(language)
                    page = wikipedia.page(topic)
                    return {
                        'title': page.title,
                        'summary': page.summary[:1000],
                        'url': page.url,
                        'source': 'wikipedia'
                    }
                except:
                    return None

            result = await loop.run_in_executor(self.thread_pool, _get_wiki)

            if result:
                # Сохраняем в кэш
                if len(self.cache) >= self.cache_size:
                    # Простая очистка - удаляем первый элемент
                    self.cache.pop(next(iter(self.cache)))
                self.cache[cache_key] = result
                self.stats['wikipedia'] += 1

            return result

        except Exception as e:
            logger.error(f"Wikipedia error: {e}")
            self.stats['errors'] += 1
            return None

    async def _fetch_arxiv(self, topic: str, max_results: int = 2) -> List[Dict]:
        """
        Получение данных из arXiv
        """
        cache_key = self._get_cache_key('arxiv', topic, 'en')

        if cache_key in self.cache:
            self.stats['cache_hits'] += 1
            return self.cache[cache_key]

        try:
            # Используем arXiv API через aiohttp
            params = {
                'search_query': f'all:{topic}',
                'start': 0,
                'max_results': max_results
            }

            async with self.session.get(
                    'http://export.arxiv.org/api/query',
                    params=params
            ) as response:
                if response.status == 200:
                    text = await response.text()

                    # Простой парсинг XML
                    papers = []
                    import xml.etree.ElementTree as ET
                    root = ET.fromstring(text)

                    for entry in root.findall('{http://www.w3.org/2005/Atom}entry')[:max_results]:
                        title = entry.find('{http://www.w3.org/2005/Atom}title')
                        summary = entry.find('{http://www.w3.org/2005/Atom}summary')
                        url = entry.find('{http://www.w3.org/2005/Atom}id')

                        if title is not None and summary is not None:
                            papers.append({
                                'title': title.text.strip() if title.text else '',
                                'summary': summary.text.strip()[:500] if summary.text else '',
                                'url': url.text if url is not None else '',
                                'source': 'arxiv'
                            })

                    # Сохраняем в кэш
                    if len(self.cache) >= self.cache_size:
                        self.cache.pop(next(iter(self.cache)))
                    self.cache[cache_key] = papers
                    self.stats['arxiv'] += 1

                    return papers
            return []

        except Exception as e:
            logger.error(f"arXiv error: {e}")
            self.stats['errors'] += 1
            return []

    async def _fetch_google_books(self, topic: str, language: str, max_results: int = 2) -> List[Dict]:
        """
        Получение данных из Google Books
        """
        cache_key = self._get_cache_key('google_books', topic, language)

        if cache_key in self.cache:
            self.stats['cache_hits'] += 1
            return self.cache[cache_key]

        try:
            params = {
                'q': topic,
                'maxResults': max_results,
                'langRestrict': language,
                'printType': 'books'
            }

            async with self.session.get(
                    'https://www.googleapis.com/books/v1/volumes',
                    params=params
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    books = []

                    for item in data.get('items', []):
                        volume = item.get('volumeInfo', {})
                        books.append({
                            'title': volume.get('title', ''),
                            'description': volume.get('description', '')[:500],
                            'authors': volume.get('authors', [])[:2],
                            'url': volume.get('infoLink', ''),
                            'source': 'google_books'
                        })

                    # Сохраняем в кэш
                    if len(self.cache) >= self.cache_size:
                        self.cache.pop(next(iter(self.cache)))
                    self.cache[cache_key] = books
                    self.stats['google_books'] += 1

                    return books
            return []

        except Exception as e:
            logger.error(f"Google Books error: {e}")
            self.stats['errors'] += 1
            return []

    async def _fetch_openlibrary(self, topic: str, max_results: int = 2) -> List[Dict]:
        """
        Получение данных из OpenLibrary (бесплатная альтернатива)
        """
        cache_key = self._get_cache_key('openlibrary', topic, 'en')

        if cache_key in self.cache:
            self.stats['cache_hits'] += 1
            return self.cache[cache_key]

        try:
            params = {
                'q': topic,
                'limit': max_results
            }

            async with self.session.get(
                    'http://openlibrary.org/search.json',
                    params=params
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    books = []

                    for doc in data.get('docs', [])[:max_results]:
                        books.append({
                            'title': doc.get('title', ''),
                            'authors': doc.get('author_name', ['Unknown'])[:2],
                            'year': doc.get('first_publish_year', ''),
                            'url': f"https://openlibrary.org{doc.get('key', '')}",
                            'source': 'openlibrary'
                        })

                    # Сохраняем в кэш
                    if len(self.cache) >= self.cache_size:
                        self.cache.pop(next(iter(self.cache)))
                    self.cache[cache_key] = books
                    self.stats['openlibrary'] += 1

                    return books
            return []

        except Exception as e:
            logger.error(f"OpenLibrary error: {e}")
            self.stats['errors'] += 1
            return []

    async def _fetch_github(self, topic: str, max_results: int = 2) -> List[Dict]:
        """
        Получение данных из GitHub
        """
        cache_key = self._get_cache_key('github', topic, 'en')

        if cache_key in self.cache:
            self.stats['cache_hits'] += 1
            return self.cache[cache_key]

        try:
            params = {
                'q': topic,
                'sort': 'stars',
                'order': 'desc',
                'per_page': max_results
            }

            headers = {'Accept': 'application/vnd.github.v3+json'}

            async with self.session.get(
                    'https://api.github.com/search/repositories',
                    params=params,
                    headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    repos = []

                    for item in data.get('items', []):
                        repos.append({
                            'name': item.get('full_name', ''),
                            'description': item.get('description', '')[:300],
                            'url': item.get('html_url', ''),
                            'stars': item.get('stargazers_count', 0),
                            'language': item.get('language', 'Unknown'),
                            'source': 'github'
                        })

                    # Сохраняем в кэш
                    if len(self.cache) >= self.cache_size:
                        self.cache.pop(next(iter(self.cache)))
                    self.cache[cache_key] = repos
                    self.stats['github'] += 1

                    return repos
            return []

        except Exception as e:
            logger.error(f"GitHub error: {e}")
            self.stats['errors'] += 1
            return []

    async def _fetch_stackoverflow(self, topic: str, max_results: int = 2) -> List[Dict]:
        """
        Получение данных из StackOverflow
        """
        cache_key = self._get_cache_key('stackoverflow', topic, 'en')

        if cache_key in self.cache:
            self.stats['cache_hits'] += 1
            return self.cache[cache_key]

        try:
            params = {
                'order': 'desc',
                'sort': 'relevance',
                'intitle': topic,
                'site': 'stackoverflow',
                'pagesize': max_results
            }

            async with self.session.get(
                    'https://api.stackexchange.com/2.3/search',
                    params=params
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    questions = []

                    for item in data.get('items', []):
                        questions.append({
                            'title': item.get('title', ''),
                            'score': item.get('score', 0),
                            'answer_count': item.get('answer_count', 0),
                            'tags': item.get('tags', [])[:3],
                            'url': item.get('link', ''),
                            'is_answered': item.get('is_answered', False),
                            'source': 'stackoverflow'
                        })

                    # Сохраняем в кэш
                    if len(self.cache) >= self.cache_size:
                        self.cache.pop(next(iter(self.cache)))
                    self.cache[cache_key] = questions
                    self.stats['stackoverflow'] += 1

                    return questions
            return []

        except Exception as e:
            logger.error(f"StackOverflow error: {e}")
            self.stats['errors'] += 1
            return []

    async def _fetch_news_api(self, topic: str, language: str, max_results: int = 2) -> List[Dict]:
        """
        Получение новостей (требуется API ключ)
        """
        api_key = os.getenv('NEWS_API_KEY', '')
        if not api_key:
            return []

        cache_key = self._get_cache_key('news_api', topic, language)

        if cache_key in self.cache:
            self.stats['cache_hits'] += 1
            return self.cache[cache_key]

        try:
            params = {
                'q': topic,
                'language': language,
                'pageSize': max_results,
                'apiKey': api_key
            }

            async with self.session.get(
                    'https://newsapi.org/v2/everything',
                    params=params
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    articles = []

                    for article in data.get('articles', []):
                        articles.append({
                            'title': article.get('title', ''),
                            'description': article.get('description', '')[:300],
                            'url': article.get('url', ''),
                            'source': article.get('source', {}).get('name', 'News'),
                            'published': article.get('publishedAt', '')
                        })

                    # Сохраняем в кэш
                    if len(self.cache) >= self.cache_size:
                        self.cache.pop(next(iter(self.cache)))
                    self.cache[cache_key] = articles
                    self.stats['news_api'] += 1

                    return articles
            return []

        except Exception as e:
            logger.error(f"News API error: {e}")
            return []

    async def optimized_learn(self, topic: str, depth: str = 'medium',
                              languages: List[str] = None, use_cache: bool = True) -> Dict:
        """
        Оптимизированное обучение

        Args:
            topic: тема для изучения
            depth: глубина ('fast', 'medium', 'deep')
            languages: языки
            use_cache: использовать кэш

        Returns:
            Dict: статистика обучения
        """
        if languages is None:
            languages = ['ru', 'en']

        start_time = time.time()

        print(f"\n🎓 ОБУЧЕНИЕ: {topic}")
        print(f"   Глубина: {depth}")
        print(f"   Языки: {languages}")

        # Выбираем источники в зависимости от глубины
        sources_to_use = ['wikipedia']

        if depth in ['medium', 'deep']:
            sources_to_use.extend(['arxiv', 'google_books', 'github', 'openlibrary'])

        if depth == 'deep':
            sources_to_use.extend(['stackoverflow', 'news_api'])

        print(f"   Источников: {len(sources_to_use)}")

        # Создаем задачи
        tasks = []
        source_names = []

        for source in sources_to_use:
            if source == 'wikipedia':
                for lang in languages[:1]:  # Только первый язык для скорости
                    tasks.append(self._fetch_wikipedia(topic, lang))
                    source_names.append(f"wikipedia_{lang}")

            elif source == 'arxiv':
                tasks.append(self._fetch_arxiv(topic, 2))
                source_names.append('arxiv')

            elif source == 'google_books':
                for lang in languages[:1]:
                    tasks.append(self._fetch_google_books(topic, lang, 2))
                    source_names.append(f"google_books_{lang}")

            elif source == 'openlibrary':
                tasks.append(self._fetch_openlibrary(topic, 2))
                source_names.append('openlibrary')

            elif source == 'github':
                tasks.append(self._fetch_github(topic, 2))
                source_names.append('github')

            elif source == 'stackoverflow':
                tasks.append(self._fetch_stackoverflow(topic, 2))
                source_names.append('stackoverflow')

            elif source == 'news_api':
                for lang in languages[:1]:
                    tasks.append(self._fetch_news_api(topic, lang, 2))
                    source_names.append(f"news_api_{lang}")

        # Выполняем все задачи параллельно
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Обрабатываем результаты и создаем нейроны
        neurons_created = 0
        successful_sources = []

        for source_name, result in zip(source_names, results):
            if isinstance(result, Exception):
                logger.error(f"   ❌ {source_name}: {str(result)[:50]}...")
                continue

            if result:
                if isinstance(result, list):
                    for item in result:
                        if item:
                            content = self._extract_content(item)
                            if content and len(content) > 50:
                                # Создаем нейрон
                                neurons = self.ml.create_multilingual_neuron(
                                    self.brain,
                                    content,
                                    category=f"Learned_{source_name.split('_')[0]}"
                                )
                                neurons_created += len(neurons)

                    if result:
                        successful_sources.append(source_name)
                        print(f"   ✅ {source_name}: {len(result)} элементов")

                elif isinstance(result, dict):
                    content = self._extract_content(result)
                    if content and len(content) > 50:
                        neurons = self.ml.create_multilingual_neuron(
                            self.brain,
                            content,
                            category=f"Learned_{source_name.split('_')[0]}"
                        )
                        neurons_created += len(neurons)
                        successful_sources.append(source_name)
                        print(f"   ✅ {source_name}: 1 элемент")

        elapsed = time.time() - start_time

        stats = {
            'topic': topic,
            'depth': depth,
            'languages': languages,
            'sources_used': len(successful_sources),
            'sources_list': successful_sources,
            'neurons_created': neurons_created,
            'time_elapsed': round(elapsed, 2),
            'cache_hits': self.stats['cache_hits'],
            'errors': self.stats['errors']
        }

        # Сохраняем в историю
        self.learning_history.append(stats)

        print(f"\n📊 Результат:")
        print(f"   ✅ Нейронов создано: {neurons_created}")
        print(f"   ✅ Источников: {len(successful_sources)}")
        print(f"   ⏱️  Время: {elapsed:.2f} сек")
        print(f"   💾 Кэш попаданий: {self.stats['cache_hits']}")

        return stats

    def _extract_content(self, data: Any) -> str:
        """Извлечение текстового содержания"""
        if isinstance(data, dict):
            # Пробуем разные ключи
            for key in ['summary', 'description', 'content', 'title', 'extract', 'body']:
                if key in data and data[key]:
                    value = data[key]
                    if isinstance(value, str):
                        return value
                    elif isinstance(value, list) and value:
                        return str(value[0])
            return str(data)
        elif isinstance(data, str):
            return data
        return ""

    def get_stats(self) -> Dict:
        """Получить статистику обучения"""
        return {
            'total_sessions': len(self.learning_history),
            'total_neurons': sum(s.get('neurons_created', 0) for s in self.learning_history),
            'total_time': sum(s.get('time_elapsed', 0) for s in self.learning_history),
            'cache_hits': self.stats['cache_hits'],
            'errors': self.stats['errors'],
            'recent_topics': [s.get('topic', '') for s in self.learning_history[-5:]],
            'source_stats': {k: v for k, v in self.stats.items()
                             if k not in ['cache_hits', 'errors'] and v > 0}
        }