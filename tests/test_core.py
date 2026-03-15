# tests/test_core.py
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.brain.cortex import Cortex


def test_core():
    print("=" * 60)
    print("🧪 ТЕСТ ЯДРА МОЗГА")
    print("=" * 60)

    brain = Cortex()

    # Добавляем знания
    brain.add_knowledge("test1", "Гравитация притягивает объекты", "Physics")
    brain.add_knowledge("test2", "Земля имеет форму шара", "Geography")

    # Статистика
    stats = brain.get_stats()
    print(f"\n📊 Статистика:")
    print(f"   Нейронов: {stats['neurons']}")
    print(f"   Синапсов: {stats['synapses']}")

    # Поиск
    results = brain.search_knowledge("гравитация")
    print(f"\n🔍 Поиск 'гравитация': {len(results)} результатов")

    # Мышление
    thoughts = brain.think("гравитация")
    print(f"💭 Мышление: {len(thoughts)} активаций")

    # Критическое мышление
    analysis = brain.critical_thinking.analyze_information(
        "Гравитация притягивает объекты",
        [{'type': 'academic', 'authority': 0.9}]
    )
    print(f"\n🧠 Критический анализ:")
    print(f"   Уверенность: {analysis['confidence']:.2f}")
    print(f"   Действие: {analysis['action']}")

    # Импровизация
    solution = brain.improvisation.solve_creatively(
        "Как улучшить обучение ИИ?"
    )
    print(f"\n🎭 Импровизация:")
    print(f"   Решение: {solution['solution'][:100]}...")
    print(f"   Уверенность: {solution['confidence']:.2f}")

    # Сохранение
    brain.save("test_brain.pkl")

    print("\n✅ Все тесты пройдены!")


if __name__ == "__main__":
    test_core()