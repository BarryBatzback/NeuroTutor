# tests/test_self_learning.py
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from src.brain.cortex import Cortex


def test_self_learning():
    print("=" * 70)
    print("🔄 ТЕСТ МОДУЛЯ САМООБУЧЕНИЯ")
    print("=" * 70)

    brain = Cortex()

    # Добавляем базовые знания
    print("\n📚 Загружаем базу знаний...")
    knowledge = [
        ("math_1", "Производная показывает скорость изменения функции", "Math"),
        ("math_2", "Интеграл — операция, обратная дифференцированию", "Math"),
        ("geo_1", "Система координат определяет положение точки в пространстве", "Geodesy"),
        ("eng_1", "Напряжение в балке рассчитывается по формуле σ = M·y/I", "Construction"),
        ("auto_1", "Крутящий момент двигателя передаётся через трансмиссию", "Automotive")
    ]
    for uid, content, cat in knowledge:
        brain.add_knowledge(uid, content, cat)

    # Тест 1: Обучение на успешном ответе
    print("\n✅ ТЕСТ 1: Обучение на успехе")
    query1 = "Что показывает производная?"
    response1 = "Скорость изменения функции"
    result1 = brain.self_learning.learn_from_interaction(query1, response1, success=True)
    print(f"   Запрос: {query1}")
    print(f"   Результат: {result1}")

    # Тест 2: Обучение на ошибке (пробел в знаниях)
    print("\n❌ ТЕСТ 2: Обнаружение пробела в знаниях")
    query2 = "Как рассчитать деформацию грунта под фундаментом?"
    response2 = "Недостаточно данных для точного ответа"
    result2 = brain.self_learning.learn_from_interaction(query2, response2, success=False)
    print(f"   Запрос: {query2}")
    print(f"   Результат: {result2}")

    # Тест 3: Генерация вопросов для самопроверки
    print("\n❓ ТЕСТ 3: Самопроверка")
    questions = brain.self_learning._generate_self_test_questions(3)
    for i, q in enumerate(questions, 1):
        print(f"   {i}. {q['question']}")

    # Тест 4: Статистика обучения
    print("\n📊 ТЕСТ 4: Статистика")
    stats = brain.self_learning.get_learning_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")

    # Тест 5: Автономное изучение (заглушка)
    print("\n🔍 ТЕСТ 5: Автономное изучение")
    auto_result = brain.self_learning.autonomous_knowledge_acquisition(max_topics=2)
    print(f"   Результат: {auto_result}")

    print("\n" + "=" * 70)
    print("✅ ТЕСТ САМООБУЧЕНИЯ ЗАВЕРШЁН")
    print("=" * 70)


if __name__ == "__main__":
    test_self_learning()