# tests/test_api_learning.py
import sys
import asyncio
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.brain.cortex import Cortex
from src.brain.multilingual import MultilingualProcessor
from src.knowledge.api_learners import APILearner


async def test_api_learning():
    print("=" * 70)
    print("🌐 ТЕСТИРОВАНИЕ API ОБУЧЕНИЯ")
    print("=" * 70)

    # Создаем мозг
    brain = Cortex()
    ml = MultilingualProcessor()
    learner = APILearner(brain, ml)

    # Тестовые темы для изучения
    test_topics = [
        ("Гравитация", "basic"),
        ("Нейронные сети", "medium"),
        ("Квантовая физика", "basic")
    ]

    for topic, depth in test_topics:
        print(f"\n{'#' * 60}")
        print(f"ТЕМА: {topic} (глубина: {depth})")
        print('#' * 60)

        stats = await learner.auto_learn(topic, depth)

        if stats['total_neurons'] > 0:
            print(f"✅ Успешно изучено: {stats['total_neurons']} нейронов")
        else:
            print(f"⚠️ Не удалось изучить тему")

        await asyncio.sleep(2)  # Пауза между темами

    # Показываем итоговую статистику
    brain_stats = brain.get_stats()
    print("\n" + "=" * 70)
    print("📊 ИТОГОВАЯ СТАТИСТИКА МОЗГА:")
    print(f"   Всего нейронов: {brain_stats['neurons']}")
    print(f"   Всего синапсов: {brain_stats['synapses']}")
    print(f"   Категории: {brain_stats['categories']}")

    # Сохраняем обученный мозг
    brain.save("api_learned_brain.pkl")

    return brain, learner


async def interactive_learning():
    """Интерактивное обучение через консоль"""
    print("\n🎓 ИНТЕРАКТИВНОЕ ОБУЧЕНИЕ")
    print("=" * 70)

    brain = Cortex()
    try:
        brain.load("api_learned_brain.pkl")
        print("✅ Загружен существующий мозг")
    except:
        print("🆕 Создан новый мозг")

    ml = MultilingualProcessor()
    learner = APILearner(brain, ml)

    while True:
        print("\n" + "-" * 30)
        topic = input("Введите тему для изучения (или 'выход'): ").strip()

        if topic.lower() in ['выход', 'exit', 'quit']:
            break

        if not topic:
            continue

        depth = input("Глубина (basic/medium/deep) [basic]: ").strip() or 'basic'

        print(f"\n🔍 Изучаю '{topic}' (глубина: {depth})...")
        stats = await learner.auto_learn(topic, depth)

        print(f"\n✅ Результат: {stats['total_neurons']} новых нейронов")

        # Показываем, что мозг узнал
        results = brain.think(topic)
        if results:
            print("\n🧠 Что я узнал:")
            for neuron, activation, depth in results[:3]:
                print(f"   • {neuron.content[:100]}...")

    brain.save("api_learned_brain.pkl")


async def main():
    """Главная функция"""
    print("\nВыберите режим:")
    print("1. Автоматический тест")
    print("2. Интерактивное обучение")

    choice = input("\nВаш выбор (1/2): ").strip()

    if choice == "1":
        await test_api_learning()
    elif choice == "2":
        await interactive_learning()
    else:
        print("Неверный выбор")


if __name__ == "__main__":
    asyncio.run(main())