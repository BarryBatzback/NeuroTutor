# tests/test_unified_search.py
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.brain.cortex import Cortex
from src.brain.unified_thinking import UnifiedThinkingEngine


def test_unified_search():
    print("=" * 70)
    print("🔍 ТЕСТ ПОИСКА В UNIFIED THINKING")
    print("=" * 70)

    # Загружаем мозг
    brain = Cortex()
    brain.load("data/models/brain_unified_thinking.pkl")

    print(f"\n📊 В мозге: {brain.get_stats()['neurons']} нейронов")
    print(f"📚 Категории: {brain.get_stats()['categories']}")

    # Тестовые запросы
    test_queries = [
        "нагрузка",
        "балка",
        "строительство",
        "спутник",
        "гравитация",
        "дифференциал",
        "автомобиль"
    ]

    print("\n" + "=" * 70)
    print("ПРОВЕРКА ПОИСКА ПО СЛОВАМ:")
    print("=" * 70)

    for query in test_queries:
        results = brain.search_knowledge(query)
        print(f"\n🔍 Запрос: '{query}'")
        print(f"   Найдено: {len(results)}")
        for neuron in results[:3]:
            print(f"   • {neuron.content[:60]}...")

    # Тест через unified thinking
    print("\n" + "=" * 70)
    print("ПРОВЕРКА ЧЕРЕЗ UNIFIED THINKING:")
    print("=" * 70)

    engine = UnifiedThinkingEngine(brain)

    query = "нагрузка на балку"
    result = engine.process_query(query)

    print(f"\n📝 Запрос: {query}")
    print(f"📊 Найдено знаний: {result['stages']['knowledge_retrieval']['direct_matches']}")
    print(f"💬 Ответ: {result['final_answer']['text'][:200]}...")
    print(f"🎯 Тип: {result['final_answer']['type']}")
    print(f"📊 Уверенность: {result['confidence']:.2f}")


if __name__ == "__main__":
    test_unified_search()