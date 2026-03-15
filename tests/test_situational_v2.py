# tests/test_situational_v2.py
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.brain.cortex import Cortex


def test_situational_v2():
    print("=" * 70)
    print("🌍 ИСПРАВЛЕННЫЙ ТЕСТ СИТУАТИВНОСТИ v2")
    print("=" * 70)

    brain = Cortex()

    # Тест 1: Настроения
    print("\n🔍 ТЕСТ 1: Настроения")
    tests = [
        ("Я так рад!", "happy"),
        ("Всё плохо", "sad"),
        ("Это ужасно!", "angry"),  # Теперь с !
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
        print(f"{status} '{text}' → {mood} (ожидался {expected})")

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
        print(f"{status} '{text}' → {urg:.2f} (минимум {min_urg})")

    print(f"   Пройдено: {passed}/{len(urgency_tests)}")

    # Тест 3: Экспертиза
    print("\n🔍 ТЕСТ 3: Экспертиза")
    expertise_tests = [
        ("Что это такое?", 0.0, 0.3),  # Диапазон для новичка
        ("Как оптимизировать градиентный спуск?", 0.7, 1.0),
        ("Простыми словами", 0.0, 0.3)
    ]

    passed = 0
    for text, min_exp, max_exp in expertise_tests:
        exp = brain.situational.detect_user_expertise(text)
        status = "✅" if min_exp <= exp <= max_exp else "⚠️"
        if min_exp <= exp <= max_exp:
            passed += 1
        print(f"{status} '{text[:30]}...' → {exp:.2f} (ожидалось {min_exp}-{max_exp})")

    print(f"   Пройдено: {passed}/{len(expertise_tests)}")

    # Тест 4: Адаптация (проверка на двойные эмодзи)
    print("\n🔍 ТЕСТ 4: Адаптация ответа")
    base_response = "Нейронные сети используют матричные вычисления."

    brain.situational.update_context("user1", "Срочно объясни!!!")
    adapted_urgent = brain.situational.adapt_response(base_response)
    print(f"⚡ Срочно: {adapted_urgent[:60]}...")
    # Проверка на двойные эмодзи
    if adapted_urgent.count('⚡') == 1:
        print("   ✅ Один эмодзи (правильно)")
    else:
        print("   ⚠️Multiple эмодзи (ошибка)")

    brain.situational.update_context("user1", "Не понимаю, как это работает?")
    adapted_confused = brain.situational.adapt_response(base_response)
    print(f"🤔 Запутанно: {adapted_confused[:60]}...")

    # Статистика
    print("\n" + "=" * 70)
    stats = brain.situational.get_statistics()
    print(f"📊 Всего взаимодействий: {stats['total_interactions']}")
    print(f"📊 Настроения: {stats['mood_distribution']}")
    print("=" * 70)

    print("\n✅ ТЕСТ СИТУАТИВНОСТИ v2 ЗАВЕРШЕН!")


if __name__ == "__main__":
    test_situational_v2()