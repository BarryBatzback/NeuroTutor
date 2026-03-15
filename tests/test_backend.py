# tests/test_backend.py
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.brain.cortex import Cortex
from src.brain.multilingual import MultilingualProcessor


def test_thinking_modules():
    print("=" * 70)
    print("🧪 ТЕСТ ВСЕХ МОДУЛЕЙ МЫШЛЕНИЯ")
    print("=" * 70)

    # Создаём мозг
    brain = Cortex()

    # Исправлено: передаём brain в MultilingualProcessor
    ml = MultilingualProcessor(brain)

    # Добавляем знания
    print("\n📚 Загружаем знания...")
    brain.add_knowledge("math_1", "Производная показывает скорость изменения функции", "Mathematics")
    brain.add_knowledge("phys_1", "Гравитация притягивает объекты", "Physics")
    brain.add_knowledge("tech_1", "Нейронные сети обучаются на данных", "Technology")

    # Тест 1: Единый процесс запроса
    print("\n🔍 ТЕСТ 1: Обработка запроса")
    results = brain.think("гравитация")
    if results:
        print(f"Найдено: {len(results)} ассоциаций")
        for neuron, confidence, depth in results[:3]:
            print(f"  • {neuron.content[:80]}... (уверенность: {confidence:.2f})")
    else:
        print("Ничего не найдено")

    # Тест 2: Критическое мышление
    print("\n🧠 ТЕСТ 2: Критическое мышление")
    analysis = brain.critical_thinking.analyze_information("Гравитация отталкивает объекты")
    print(f"Уверенность: {analysis['confidence']:.2f}")
    print(f"Вывод: {analysis['conclusion']}")
    print(f"Действие: {analysis['action']}")

    # Тест 3: Импровизация
    print("\n🎭 ТЕСТ 3: Импровизация")
    solution = brain.improvisation.solve_creatively("Как улучшить обучение ИИ?")
    print(f"Решение: {solution['solution'][:100]}...")
    print(f"Уверенность: {solution['confidence']:.2f}")

    # Тест 4: Многоязычность
    print("\n🌍 ТЕСТ 4: Многоязычность")
    lang = ml.detect_language("Привет, как дела?")
    print(f"Определён язык: {lang}")

    # Статистика
    print("\n" + "=" * 70)
    print("📊 ИТОГОВАЯ СТАТИСТИКА:")
    stats = brain.get_stats()
    print(f"Нейронов: {stats['neurons']}")
    print(f"Синапсов: {stats['synapses']}")
    print(f"Категорий: {stats['categories']}")
    print("=" * 70)

    # Сохраняем
    brain.save("brain_for_backend.pkl")
    print("\n✅ Мозг сохранён: brain_for_backend.pkl")


if __name__ == "__main__":
    test_thinking_modules()