import sys
import asyncio
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.brain.cortex import Cortex
from src.brain.multilingual import MultilingualProcessor
from src.knowledge.optimized_learner import OptimizedLearner


async def test_simple_optimized():
    print("=" * 60)
    print("🧪 ТЕСТ УПРОЩЕННОЙ ОПТИМИЗИРОВАННОЙ СИСТЕМЫ")
    print("=" * 60)

    # Создаем мозг
    brain = Cortex()
    ml = MultilingualProcessor()

    print(f"\n📊 Многоязычный процессор:")
    print(f"   Поддерживается языков: {len(ml.supported_languages)}")

    # Тест определения языка
    test_texts = [
        ("Привет, как дела?", "ru"),
        ("Hello, how are you?", "en"),
        ("Bonjour, comment ça va?", "fr")
    ]

    for text, expected in test_texts:
        detected = ml.detect_language(text)
        print(f"   '{text[:20]}...' -> {detected} (ожидался {expected})")

    # Тест OptimizedLearner
    async with OptimizedLearner(brain, ml) as learner:
        print(f"\n🚀 OptimizedLearner создан")
        print(f"   Источников: {len(learner.sources)}")

        # Тест обучения
        test_topics = [
            ("Python programming", "fast"),
            ("Нейронные сети", "medium")
        ]

        for topic, depth in test_topics:
            stats = await learner.optimized_learn(topic, depth, ['ru', 'en'])
            print(f"\n   📚 {topic}: {stats['neurons_created']} нейронов за {stats['time_elapsed']} сек")

    # Итог
    brain_stats = brain.get_stats()
    print(f"\n📊 ИТОГОВАЯ СТАТИСТИКА МОЗГА:")
    print(f"   Нейронов: {brain_stats['neurons']}")
    print(f"   Синапсов: {brain_stats['synapses']}")

    brain.save("optimized_brain_v2.pkl")
    print(f"\n💾 Мозг сохранен")


if __name__ == "__main__":
    asyncio.run(test_simple_optimized())