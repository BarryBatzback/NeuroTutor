# tests/test_api_learning.py

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.brain.cortex import Cortex
from src.brain.multilingual import MultilingualProcessor
from src.knowledge.api_learners import APILearner


def test_api_learning():
    print("🌐 ТЕСТИРОВАНИЕ API ОБУЧЕНИЯ")
    print("=" * 50)

    # Создаем мозг
    brain = Cortex()
    ml = MultilingualProcessor()
    learner = APILearner(brain, ml)

    # Тестовые темы для изучения
    test_topics = [
        ("Гравитация", "basic"),
        ("Quantum mechanics", "medium"),
        ("Искусственный интеллект", "basic")
    ]

    for topic, depth in test_topics:
        print(f"\n{'#' * 60}")
        stats = learner.auto_learn(topic, depth)

        if stats['total_neurons'] > 0:
            print(f"✅ Успешно изучено: {stats['total_neurons']} нейронов")
        else:
            print(f"⚠️ Не удалось изучить тему")

    # Показываем итоговую статистику
    brain_stats = brain.get_stats()
    print("\n" + "=" * 50)
    print("📊 ИТОГОВАЯ СТАТИСТИКА МОЗГА:")
    print(f"   Всего нейронов: {brain_stats['neurons']}")
    print(f"   Всего синапсов: {brain_stats['synapses']}")

    # Сохраняем обученный мозг
    brain.save("api_learned_brain.pkl")

    return brain, learner


def interactive_learning():
    """Интерактивное обучение через консоль"""
    print("\n🎓 ИНТЕРАКТИВНОЕ ОБУЧЕНИЕ")
    print("=" * 50)

    brain = Cortex()
    brain.load("api_learned_brain.pkl")
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
        stats = learner.auto_learn(topic, depth)

        print(f"\n✅ Результат: {stats['total_neurons']} новых нейронов")

        # Показываем, что мозг узнал
        results = brain.think(topic)
        if results:
            print("\n🧠 Что я узнал:")
            for neuron, activation, depth in results[:3]:
                print(f"   • {neuron.content[:100]}...")


if __name__ == "__main__":
    # Сначала тест
    test_api_learning()

    # Затем интерактивный режим
    answer = input("\nХотите попробовать интерактивное обучение? (да/нет): ")
    if answer.lower() in ['да', 'yes', 'y']:
        interactive_learning()