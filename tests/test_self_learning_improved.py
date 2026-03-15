# tests/test_self_learning_improved.py
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from src.brain.cortex import Cortex


def test_self_learning_improved():
    print("=" * 70)
    print("🔄 УЛУЧШЕННЫЙ ТЕСТ САМООБУЧЕНИЯ")
    print("=" * 70)

    brain = Cortex()

    # Добавляем больше знаний для контекста
    print("\n📚 Загружаем расширенную базу знаний...")
    knowledge = [
        ("math_1", "Производная показывает скорость изменения функции", "Math"),
        ("math_2", "Интеграл — операция, обратная дифференцированию", "Math"),
        ("math_3", "Предел функции — значение, к которому она стремится", "Math"),
        ("geo_1", "Система координат определяет положение точки", "Geodesy"),
        ("eng_1", "Напряжение в балке: σ = M·y/I", "Construction"),
        ("auto_1", "Крутящий момент передаётся через трансмиссию", "Automotive"),
        ("phys_1", "Сила равна массе на ускорение: F = ma", "Physics"),
        ("phys_2", "Энергия не создаётся и не уничтожается", "Physics"),
    ]
    for uid, content, cat in knowledge:
        brain.add_knowledge(uid, content, cat)

    # Активируем нейроны несколько раз (для self-test)
    print("\n🔁 Активируем нейроны...")
    for _ in range(3):
        brain.think("производная")
        brain.think("сила")

    # Тест 1: Обучение на успехе
    print("\n✅ ТЕСТ 1: Обучение на успехе")
    result1 = brain.self_learning.learn_from_interaction(
        "Что показывает производная?",
        "Скорость изменения функции",
        success=True
    )
    print(f"   Результат: {result1}")

    # Тест 2: Обнаружение пробела
    print("\n❌ ТЕСТ 2: Обнаружение пробела")
    result2 = brain.self_learning.learn_from_interaction(
        "Как рассчитать деформацию грунта?",
        "Недостаточно данных",
        success=False
    )
    print(f"   Результат: {result2}")

    # Тест 3: Самопроверка
    print("\n❓ ТЕСТ 3: Самопроверка")
    questions = brain.self_learning._generate_self_test_questions(3)
    print(f"   Сгенерировано вопросов: {len(questions)}")
    for i, q in enumerate(questions, 1):
        print(f"   {i}. {q['question'][:60]}...")

    # Тест 4: Статистика
    print("\n📊 ТЕСТ 4: Статистика")
    stats = brain.self_learning.get_learning_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")

    # Тест 5: Автономное изучение
    print("\n🔍 ТЕСТ 5: Автономное изучение")
    auto_result = brain.self_learning.autonomous_knowledge_acquisition(max_topics=2)
    print(f"   Результат: {auto_result}")

    print("\n" + "=" * 70)
    print("✅ ТЕСТ ЗАВЕРШЁН!")
    print("=" * 70)


if __name__ == "__main__":
    test_self_learning_improved()