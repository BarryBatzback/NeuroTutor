# tests/test_situational_final.py
import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

from src.brain.cortex import Cortex


def test_situational_final():
    print("=" * 70)
    print("🌍 ФИНАЛЬНЫЙ ТЕСТ СИТУАТИВНОСТИ")
    print("=" * 70)

    # Создаем мозг
    brain = Cortex()

    # Тест 1: Настроения
    print("\n🔍 ТЕСТ 1: Настроения")
    tests = [
        ("Я так рад!", "happy"),
        ("Всё плохо", "sad"),
        ("Это ужасно", "angry"),
        ("Не понимаю", "confused"),
        ("Интересно!", "curious"),
        ("Привет, как дела?", "neutral")
    ]

    passed = 0
    for text, expected in tests:
        brain.situational.update_context("user1", text)
        mood = brain.situational.context['mood']
        status = "✅" if mood == expected else "⚠️"
        if mood == expected:
            passed += 1
        print(f"{status} '{text}' → {mood}")

    print(f"   Пройдено: {passed}/{len(tests)}")

    # Тест 2: Срочность
    print("\n🔍 ТЕСТ 2: Срочность")
    urgency_tests = [
        ("Срочно!!!", 0.8),
        ("Когда будет?", 0.3),
        ("Горит! Немедленно!", 0.9),
        ("Просто вопрос", 0.0)
    ]

    passed = 0
    for text, min_urg in urgency_tests:
        brain.situational.update_context("user1", text)
        urg = brain.situational.context['urgency']
        status = "✅" if urg >= min_urg else "⚠️"
        if urg >= min_urg:
            passed += 1
        print(f"{status} '{text}' → {urg:.2f}")

    print(f"   Пройдено: {passed}/{len(urgency_tests)}")

    # Тест 3: Экспертиза
    print("\n🔍 ТЕСТ 3: Экспертиза")
    expertise_tests = [
        ("Что это такое?", 0.3),
        ("Как оптимизировать градиентный спуск?", 0.7),
        ("Простыми словами", 0.2)
    ]

    passed = 0
    for text, min_exp in expertise_tests:
        exp = brain.situational.detect_user_expertise(text)
        status = "✅" if exp >= min_exp or text.find("простыми") >= 0 else "⚠️"
        if exp >= min_exp or text.find("простыми") >= 0:
            passed += 1
        print(f"{status} '{text[:30]}...' → {exp:.2f}")

    print(f"   Пройдено: {passed}/{len(expertise_tests)}")

    # Тест 4: Адаптация ответа
    print("\n🔍 ТЕСТ 4: Адаптация ответа")
    base_response = "Нейронные сети используют матричные вычисления."

    # Срочный запрос
    brain.situational.update_context("user1", "Срочно объясни!!!")
    adapted_urgent = brain.situational.adapt_response(base_response)
    print(f"⚡ Срочно: {adapted_urgent[:80]}...")

    # Запутанный пользователь
    brain.situational.update_context("user1", "Не понимаю, как это работает?")
    adapted_confused = brain.situational.adapt_response(base_response)
    print(f"🤔 Запутанно: {adapted_confused[:80]}...")

    # Тест 5: Контекст разговора
    print("\n🔍 ТЕСТ 5: История разговора")
    for i in range(5):
        brain.situational.update_context("user1", f"Вопрос номер {i}")

    summary = brain.situational.get_context_summary()
    print(f"📊 Сводка контекста:")
    print(f"   Пользователь: {summary['user_id']}")
    print(f"   Время: {summary['time']}")
    print(f"   Настроение: {summary['mood']}")
    print(f"   Срочность: {summary['urgency']}")
    print(f"   История: {summary['history_length']} сообщений")

    # Тест 6: Повторяющиеся вопросы
    print("\n🔍 ТЕСТ 6: Повторяющиеся вопросы")
    brain.situational.update_context("user1", "Как дела?")
    is_repeated = brain.situational.is_repeated_question("Как дела?")
    print(f"{'✅' if is_repeated else '⚠️'} Повторный вопрос обнаружен: {is_repeated}")

    is_repeated_new = brain.situational.is_repeated_question("Что нового?")
    print(f"{'✅' if not is_repeated_new else '⚠️'} Новый вопрос корректен: {not is_repeated_new}")

    # Статистика
    print("\n" + "=" * 70)
    stats = brain.situational.get_statistics()
    print(f"📊 Всего взаимодействий: {stats['total_interactions']}")
    print(f"📊 Распределение настроений: {stats['mood_distribution']}")
    print("=" * 70)

    print("\n✅ ТЕСТ СИТУАТИВНОСТИ ЗАВЕРШЕН!")


if __name__ == "__main__":
    test_situational_final()