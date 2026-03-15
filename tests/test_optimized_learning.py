# tests/test_optimized_learning.py

import sys
import asyncio
import os
from pathlib import Path
from datetime import datetime
import json

# Добавляем путь к проекту
sys.path.append(str(Path(__file__).parent.parent))

from src.brain.cortex import Cortex
from src.brain.multilingual import MultilingualProcessor
from src.knowledge.optimized_learner import OptimizedLearner, LearningOrchestrator
from src.knowledge.learning_scheduler import LearningScheduler


class TestOptimizedLearning:
    """
    Полное тестирование оптимизированной системы обучения
    """

    def __init__(self):
        self.results_dir = Path(__file__).parent / "test_results"
        self.results_dir.mkdir(exist_ok=True)

        self.test_log = []
        self.start_time = datetime.now()

        print("=" * 70)
        print("🧪 ЗАПУСК ПОЛНОГО ТЕСТИРОВАНИЯ ОПТИМИЗИРОВАННОЙ СИСТЕМЫ")
        print("=" * 70)

    def log(self, message: str, level: str = "INFO"):
        """Логирование с временем"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        self.test_log.append(log_entry)

    async def test_initialization(self) -> bool:
        """Тест 1: Инициализация компонентов"""
        self.log("\n📦 ТЕСТ 1: Инициализация компонентов", "TEST")

        try:
            # Создаем мозг
            brain = Cortex()
            self.log("✅ Cortex создан")

            # Многоязычный процессор
            ml = MultilingualProcessor()
            self.log(f"✅ MultilingualProcessor создан, языков: {len(ml.supported_languages)}")

            # Оптимизированный обучатель
            async with OptimizedLearner(brain, ml) as learner:
                self.log(f"✅ OptimizedLearner создан, источников: {len(learner.sources)}")

                # Проверяем наличие основных источников
                essential_sources = ['wikipedia', 'arxiv', 'google_books']
                missing = [s for s in essential_sources if s not in learner.sources]

                if missing:
                    self.log(f"⚠️ Отсутствуют источники: {missing}", "WARN")
                else:
                    self.log("✅ Все основные источники доступны")

            return True

        except Exception as e:
            self.log(f"❌ Ошибка инициализации: {e}", "ERROR")
            return False

    async def test_wikipedia_learning(self):
        """Тест 2: Обучение из Wikipedia"""
        self.log("\n📚 ТЕСТ 2: Обучение из Wikipedia", "TEST")

        brain = Cortex()
        ml = MultilingualProcessor()

        async with OptimizedLearner(brain, ml) as learner:
            # Тест на разных языках
            test_cases = [
                ("Квантовая физика", "ru"),
                ("Quantum mechanics", "en"),
                ("Quantenphysik", "de")
            ]

            for topic, lang in test_cases:
                self.log(f"\n   🔍 Тест: '{topic}' ({lang})")

                # Используем напрямую метод Wikipedia
                result = await learner._fetch_wikipedia(topic, lang)

                if result:
                    self.log(f"   ✅ Найдена статья: {result.get('title', '')}")
                    self.log(f"   📝 Длина описания: {len(result.get('summary', ''))} символов")
                    self.log(f"   🔗 Ссылок: {len(result.get('links', []))}")
                    self.log(f"   📂 Категорий: {len(result.get('categories', []))}")
                else:
                    self.log(f"   ❌ Статья не найдена", "WARN")

                # Небольшая пауза
                await asyncio.sleep(1)

    async def test_arxiv_learning(self):
        """Тест 3: Обучение из arXiv"""
        self.log("\n📄 ТЕСТ 3: Обучение из arXiv", "TEST")

        brain = Cortex()
        ml = MultilingualProcessor()

        async with OptimizedLearner(brain, ml) as learner:
            test_topics = [
                "machine learning",
                "quantum computing",
                "neural networks"
            ]

            for topic in test_topics:
                self.log(f"\n   🔍 Тест: '{topic}'")

                results = await learner._fetch_arxiv(topic, max_results=2)

                if results:
                    self.log(f"   ✅ Найдено статей: {len(results)}")
                    for i, paper in enumerate(results, 1):
                        self.log(f"      {i}. {paper.get('title', '')[:80]}...")
                        self.log(f"         Авторы: {', '.join(paper.get('authors', [])[:2])}")
                        if paper.get('published'):
                            self.log(f"         Дата: {paper.get('published')}")
                else:
                    self.log(f"   ❌ Статьи не найдены", "WARN")

                await asyncio.sleep(1)

    async def test_google_books_learning(self):
        """Тест 4: Обучение из Google Books"""
        self.log("\n📖 ТЕСТ 4: Обучение из Google Books", "TEST")

        brain = Cortex()
        ml = MultilingualProcessor()

        async with OptimizedLearner(brain, ml) as learner:
            test_cases = [
                ("нейронные сети", "ru"),
                ("artificial intelligence", "en"),
                ("deep learning", "en")
            ]

            for topic, lang in test_cases:
                self.log(f"\n   🔍 Тест: '{topic}' ({lang})")

                results = await learner._fetch_google_books(topic, lang, max_results=2)

                if results:
                    self.log(f"   ✅ Найдено книг: {len(results)}")
                    for i, book in enumerate(results, 1):
                        self.log(f"      {i}. {book.get('title', '')}")
                        if book.get('authors'):
                            self.log(f"         Авторы: {', '.join(book.get('authors', []))}")
                else:
                    self.log(f"   ❌ Книги не найдены", "WARN")

                await asyncio.sleep(1)

    async def test_github_learning(self):
        """Тест 5: Обучение из GitHub"""
        self.log("\n💻 ТЕСТ 5: Обучение из GitHub", "TEST")

        brain = Cortex()
        ml = MultilingualProcessor()

        async with OptimizedLearner(brain, ml) as learner:
            test_topics = [
                "neural-network",
                "machine-learning",
                "deep-learning"
            ]

            for topic in test_topics:
                self.log(f"\n   🔍 Тест: '{topic}'")

                results = await learner._fetch_github(topic, 'en', max_results=2)

                if results:
                    self.log(f"   ✅ Найдено репозиториев: {len(results)}")
                    for i, repo in enumerate(results, 1):
                        self.log(f"      {i}. {repo.get('name', '')}")
                        self.log(f"         ⭐ Звезд: {repo.get('stars', 0)}")
                        self.log(f"         📝 {repo.get('description', 'Нет описания')[:50]}")
                else:
                    self.log(f"   ❌ Репозитории не найдены", "WARN")

                await asyncio.sleep(1)

    async def test_stackoverflow_learning(self):
        """Тест 6: Обучение из StackOverflow"""
        self.log("\n❓ ТЕСТ 6: Обучение из StackOverflow", "TEST")

        brain = Cortex()
        ml = MultilingualProcessor()

        async with OptimizedLearner(brain, ml) as learner:
            test_topics = [
                "python async",
                "neural network",
                "git merge"
            ]

            for topic in test_topics:
                self.log(f"\n   🔍 Тест: '{topic}'")

                results = await learner._fetch_stackoverflow(topic, max_results=2)

                if results:
                    self.log(f"   ✅ Найдено вопросов: {len(results)}")
                    for i, q in enumerate(results, 1):
                        self.log(f"      {i}. {q.get('title', '')[:70]}...")
                        self.log(f"         👍 {q.get('score', 0)} | 📝 {q.get('answer_count', 0)} ответов")
                else:
                    self.log(f"   ❌ Вопросы не найдены", "WARN")

                await asyncio.sleep(1)

    async def test_semantic_scholar_learning(self):
        """Тест 7: Обучение из Semantic Scholar"""
        self.log("\n🎓 ТЕСТ 7: Обучение из Semantic Scholar", "TEST")

        brain = Cortex()
        ml = MultilingualProcessor()

        async with OptimizedLearner(brain, ml) as learner:
            test_topics = [
                "transformer architecture",
                "neural networks",
                "deep learning"
            ]

            for topic in test_topics:
                self.log(f"\n   🔍 Тест: '{topic}'")

                results = await learner._fetch_semantic_scholar(topic, max_results=2)

                if results:
                    self.log(f"   ✅ Найдено статей: {len(results)}")
                    for i, paper in enumerate(results, 1):
                        self.log(f"      {i}. {paper.get('title', '')[:70]}...")
                        self.log(f"         📚 Цитирований: {paper.get('citations', 0)}")
                        if paper.get('venue'):
                            self.log(f"         📰 {paper.get('venue')}")
                else:
                    self.log(f"   ❌ Статьи не найдены", "WARN")

                await asyncio.sleep(1)

    async def test_multilingual_detection(self):
        """Тест 8: Определение языка и перевод"""
        self.log("\n🌍 ТЕСТ 8: Многоязычность", "TEST")

        brain = Cortex()
        ml = MultilingualProcessor()

        test_phrases = [
            ("Привет, как дела?", "ru"),
            ("Hello, how are you?", "en"),
            ("Bonjour, comment ça va?", "fr"),
            ("Hallo, wie geht's?", "de"),
            ("Ciao, come stai?", "it"),
            ("Hola, ¿cómo estás?", "es"),
            ("こんにちは、お元気ですか？", "ja"),
            ("你好，你好吗？", "zh-cn")
        ]

        for phrase, expected in test_phrases:
            detected = ml.detect_language(phrase)
            status = "✅" if detected == expected else "⚠️"
            self.log(f"   {status} '{phrase[:20]}...' → {detected} (ожидался {expected})")

            # Тест перевода на русский
            translated = ml.translate(phrase, 'ru')
            self.log(f"      Перевод на русский: {translated[:50]}...")

            await asyncio.sleep(0.5)

    async def test_optimized_learning_single(self):
        """Тест 9: Оптимизированное обучение одной теме"""
        self.log("\n🚀 ТЕСТ 9: Оптимизированное обучение одной теме", "TEST")

        brain = Cortex()
        ml = MultilingualProcessor()

        async with OptimizedLearner(brain, ml) as learner:
            test_topic = "Искусственный интеллект"

            self.log(f"\n   📚 Тема: {test_topic}")

            # Быстрое обучение
            self.log("   ⚡ Режим: fast")
            stats_fast = await learner.optimized_learn(test_topic, 'fast', ['ru'])

            self.log(f"      Нейронов создано: {stats_fast.get('neurons_created', 0)}")
            self.log(f"      Источников использовано: {stats_fast.get('sources_used', 0)}")
            self.log(f"      Время: {stats_fast.get('time_elapsed', 0):.2f} сек")

            # Среднее обучение
            self.log("\n   📚 Режим: medium")
            stats_medium = await learner.optimized_learn(test_topic, 'medium', ['ru', 'en'])

            self.log(f"      Нейронов создано: {stats_medium.get('neurons_created', 0)}")
            self.log(f"      Источников использовано: {stats_medium.get('sources_used', 0)}")
            self.log(f"      Время: {stats_medium.get('time_elapsed', 0):.2f} сек")

            # Статистика
            total = stats_fast.get('neurons_created', 0) + stats_medium.get('neurons_created', 0)
            self.log(f"\n   📊 Всего нейронов по теме: {total}")

    async def test_parallel_learning(self):
        """Тест 10: Параллельное обучение нескольким темам"""
        self.log("\n⚡ ТЕСТ 10: Параллельное обучение", "TEST")

        brain = Cortex()
        ml = MultilingualProcessor()

        async with OptimizedLearner(brain, ml) as learner:
            topics = [
                "Нейронные сети",
                "Машинное обучение",
                "Глубокое обучение"
            ]

            self.log(f"\n   📚 Тем для параллельного обучения: {len(topics)}")

            results = await learner.parallel_batch_learn(
                topics,
                depth='fast',
                languages=['ru'],
                max_concurrent=3
            )

            for topic, stats in zip(topics, results):
                self.log(
                    f"   • {topic}: {stats.get('neurons_created', 0)} нейронов, {stats.get('time_elapsed', 0):.2f} сек")

    async def test_recursive_learning(self):
        """Тест 11: Рекурсивное обучение"""
        self.log("\n🔄 ТЕСТ 11: Рекурсивное обучение", "TEST")

        brain = Cortex()
        ml = MultilingualProcessor()

        async with OptimizedLearner(brain, ml) as learner:
            topic = "Python programming"

            self.log(f"\n   📚 Основная тема: {topic}")
            self.log("   🔍 Глубина рекурсии: 2")

            result = await learner.recursive_learn(topic, depth=2, max_per_level=2)

            def print_tree(node, level=0):
                indent = "   " * level
                self.log(f"{indent}📌 {node['topic']} ({node['neurons']} нейронов)")
                for child in node.get('children', []):
                    print_tree(child, level + 1)

            print_tree(result)

    async def test_adaptive_learning(self):
        """Тест 12: Адаптивное обучение"""
        self.log("\n🎯 ТЕСТ 12: Адаптивное обучение", "TEST")

        brain = Cortex()
        ml = MultilingualProcessor()

        async with OptimizedLearner(brain, ml) as learner:
            topic = "Квантовые вычисления"
            target = 20

            self.log(f"\n   📚 Тема: {topic}")
            self.log(f"   🎯 Цель: {target} нейронов")

            result = await learner.adaptive_learn(topic, target_neurons=target, max_iterations=3)

            self.log(f"\n   📊 Результат:")
            self.log(f"      Нейронов: {result.get('total_neurons', 0)}")
            self.log(f"      Итераций: {result.get('iterations', 0)}")
            self.log(f"      Источников: {len(result.get('sources_used', []))}")
            self.log(f"      Время: {result.get('total_time', 0):.2f} сек")

    async def test_orchestrator(self):
        """Тест 13: Оркестратор обучения"""
        self.log("\n🎼 ТЕСТ 13: Оркестратор обучения", "TEST")

        brain = Cortex()
        ml = MultilingualProcessor()
        orchestrator = LearningOrchestrator(brain, ml)

        await orchestrator.start()

        # Добавляем темы в очередь
        topics = [
            ("Математический анализ", 3),
            ("Линейная алгебра", 2),
            ("Теория вероятностей", 1)
        ]

        for topic, priority in topics:
            await orchestrator.add_topic(topic, priority)
            self.log(f"   📝 Добавлено: {topic} (приоритет: {priority})")

        self.log(f"   📊 Размер очереди: {orchestrator.get_queue_size()}")

        # Обучаем одну тему сразу
        self.log("\n   ⚡ Немедленное обучение:")
        stats = await orchestrator.learn_specific("Python", 'fast')
        self.log(f"      Нейронов создано: {stats.get('neurons_created', 0)}")

        await orchestrator.stop()
        self.log("   ✅ Оркестратор остановлен")

    async def test_cache_efficiency(self):
        """Тест 14: Эффективность кэширования"""
        self.log("\n💾 ТЕСТ 14: Эффективность кэширования", "TEST")

        brain = Cortex()
        ml = MultilingualProcessor()

        async with OptimizedLearner(brain, ml) as learner:
            topic = "Искусственный интеллект"

            self.log(f"\n   🔍 Первый запрос (без кэша):")
            start = asyncio.get_event_loop().time()
            result1 = await learner._fetch_wikipedia(topic, 'ru')
            time1 = asyncio.get_event_loop().time() - start
            self.log(f"      Время: {time1:.2f} сек")

            self.log(f"\n   🔍 Второй запрос (с кэшем):")
            start = asyncio.get_event_loop().time()
            result2 = await learner._fetch_wikipedia(topic, 'ru')
            time2 = asyncio.get_event_loop().time() - start
            self.log(f"      Время: {time2:.2f} сек")

            if time2 < time1:
                self.log(f"   ✅ Кэш работает: ускорение в {time1 / time2:.1f} раз")
            else:
                self.log(f"   ⚠️ Кэш не сработал", "WARN")

    async def test_source_quality_evaluation(self):
        """Тест 15: Оценка качества источников"""
        self.log("\n📊 ТЕСТ 15: Оценка качества источников", "TEST")

        brain = Cortex()
        ml = MultilingualProcessor()

        async with OptimizedLearner(brain, ml) as learner:
            test_cases = [
                ("quantum physics", "science"),
                ("python programming", "technology"),
                ("ancient rome", "history"),
                ("general topic", "general")
            ]

            for topic, expected_category in test_cases:
                self.log(f"\n   🔍 Тема: '{topic}'")

                # Определяем категорию
                category = learner._categorize_topic(topic)
                self.log(f"      Категория: {category} (ожидалась {expected_category})")

                # Оцениваем качество разных источников
                sources_to_test = ['arxiv', 'wikipedia', 'github', 'jstor']

                self.log(f"      Оценка качества источников:")
                for source in sources_to_test:
                    quality = learner._evaluate_source_quality(source, topic)
                    stars = "⭐" * int(quality * 5)
                    self.log(f"         {source:15}: {quality:.2f} {stars}")

    async def run_all_tests(self):
        """Запуск всех тестов"""

        tests = [
            self.test_initialization,
            self.test_wikipedia_learning,
            self.test_arxiv_learning,
            self.test_google_books_learning,
            self.test_github_learning,
            self.test_stackoverflow_learning,
            self.test_semantic_scholar_learning,
            self.test_multilingual_detection,
            self.test_optimized_learning_single,
            self.test_parallel_learning,
            self.test_recursive_learning,
            self.test_adaptive_learning,
            self.test_orchestrator,
            self.test_cache_efficiency,
            self.test_source_quality_evaluation
        ]

        results = []

        for i, test in enumerate(tests, 1):
            try:
                self.log(f"\n{'=' * 60}")
                self.log(f"ЗАПУСК ТЕСТА {i}/{len(tests)}")
                self.log(f"{'=' * 60}")

                await test()
                results.append(True)

            except Exception as e:
                self.log(f"❌ Тест провален: {e}", "ERROR")
                import traceback
                traceback.print_exc()
                results.append(False)

        # Итоговый отчет
        self.print_final_report(results)

    def print_final_report(self, results):
        """Финальный отчет"""
        elapsed = datetime.now() - self.start_time

        print("\n" + "=" * 70)
        print("📊 ФИНАЛЬНЫЙ ОТЧЕТ ТЕСТИРОВАНИЯ")
        print("=" * 70)

        passed = sum(results)
        total = len(results)

        print(f"\n✅ Успешно: {passed}/{total}")
        print(f"❌ Провалено: {total - passed}/{total}")
        print(f"⏱️  Время выполнения: {elapsed.total_seconds():.2f} сек")

        print("\n📝 Детали по тестам:")
        test_names = [
            "Инициализация",
            "Wikipedia",
            "arXiv",
            "Google Books",
            "GitHub",
            "StackOverflow",
            "Semantic Scholar",
            "Многоязычность",
            "Оптимизированное обучение",
            "Параллельное обучение",
            "Рекурсивное обучение",
            "Адаптивное обучение",
            "Оркестратор",
            "Кэширование",
            "Оценка источников"
        ]

        for name, result in zip(test_names, results):
            status = "✅" if result else "❌"
            print(f"   {status} {name}")

        # Сохраняем лог
        log_file = self.results_dir / f"test_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(self.test_log))

        print(f"\n💾 Лог сохранен: {log_file}")


async def main():
    """Главная функция"""
    tester = TestOptimizedLearning()

    # Спрашиваем, какие тесты запускать
    print("\nВыберите режим тестирования:")
    print("1. Все тесты")
    print("2. Только быстрые тесты")
    print("3. Только внешние API")
    print("4. Только многоязычность")
    print("5. Свой выбор")

    choice = input("\nВаш выбор (1-5): ").strip()

    if choice == "1":
        await tester.run_all_tests()
    elif choice == "2":
        # Только быстрые тесты (без внешних API)
        tests = [
            tester.test_initialization,
            tester.test_multilingual_detection,
            tester.test_cache_efficiency,
            tester.test_source_quality_evaluation
        ]
        for test in tests:
            await test()
    elif choice == "3":
        # Только внешние API
        tests = [
            tester.test_wikipedia_learning,
            tester.test_arxiv_learning,
            tester.test_google_books_learning,
            tester.test_github_learning,
            tester.test_stackoverflow_learning
        ]
        for test in tests:
            await test()
    elif choice == "4":
        # Только многоязычность
        await tester.test_multilingual_detection()
    else:
        # Свой выбор
        await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())