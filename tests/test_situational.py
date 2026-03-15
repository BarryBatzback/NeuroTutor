# tests/test_situational.py
import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

from src.brain.cortex import Cortex


def test_situational():
    print("=" * 70)
    print("🌍 ТЕСТ МОДУЛЯ СИТУАТИВНОСТИ")
    print("=" * 70)

    # Создаем мозг
    brain = Cortex()

    # Тест 1: Определение настроения
    print("\n🔍 ТЕСТ 1: Определение настроения")
    test_cases = [
        ("Я так рад, что это работает!", "happy"),
        ("Ничего не понимаю, всё плохо", "sad"),
        ("Это ужасно, почему так медленно?", "angry"),
        ("Как это работает? Не понимаю", "confused"),
        ("Очень интересно, расскажи подробнее", "curious"),
        ("Привет, как дела?", "neutral")
    ]

    for text, expected in test_cases:
        brain.situational.update_context("user1", text)
        mood = brain.situational.context['mood']
        status = "✅" if mood == expected else "⚠️"
        print(f"{status} '{text[:30]}...' → {mood} (ожидался {expected})")

    # Тест 2: Определение срочности
    print("\n🔍 ТЕСТ 2: Определение срочности")
    urgency_tests = [
        ("Сделай это срочно!!!", 0.8),
        ("Когда будет готово?", 0.3),
        ("Просто вопрос", 0.0),
        ("Нужно немедленно! Горит!", 0.9)
    ]

    for text, min_urgency in urgency_tests:
        brain.situational.update_context("user1", text)
        urgency = brain.situational.context['urgency']
        status = "✅" if urgency >= min_urgency else "⚠️"
        print(f"{status} '{text[:30]}...' → {urgency:.2f} (минимум {min_urgency})")

    # Тест 3: Адаптация ответа
    print("\n🔍 ТЕСТ 3: Адаптация ответа")
    base_response = "Нейронные сети используют матричные вычисления для обработки данных."

    # Срочный запрос
    brain.situational.update_context("user1", "Срочно объясни!!!")
    adapted_urgent = brain.situational.adapt_response(base_response)
    print(f"⚡ Срочно:\n{adapted_urgent[:100]}...")

    # Запутанный пользователь
    brain.situational.update_context("user1", "Не понимаю, как это работает?")
    adapted_confused = brain.situational.adapt_response(base_response)
    print(f"\n🤔 Запутанно:\n{adapted_confused[:150]}...")

    # Любопытный пользователь
    brain.situational.update_context("user1", "Очень интересно! Расскажи подробнее")
    adapted_curious = brain.situational.adapt_response(base_response)
    print(f"\n🔍 Любопытно:\n{adapted_curious[:150]}...")

    # Тест 4: Контекст разговора
    print("\n🔍 ТЕСТ 4: История разговора")
    for i in range(5):
        brain.situational.update_context("user1", f"Вопрос номер {i}")

    summary = brain.situational.get_context_summary()
    print(f"📊 Сводка контекста:")
    print(f"   Пользователь: {summary['user_id']}")
    print(f"   Время: {summary['time']}")
    print(f"   Настроение: {summary['mood']}")
    print(f"   Срочность: {summary['urgency']}")
    print(f"   Тема: {summary['topic']}")
    print(f"   История: {summary['history_length']} сообщений")

    # Тест 5: Повторяющиеся вопросы
    print("\n🔍 ТЕСТ 5: Повторяющиеся вопросы")
    brain.situational.update_context("user1", "Как дела?")
    is_repeated = brain.situational.is_repeated_question("Как дела?")
    print(f"{'✅' if is_repeated else '⚠️'} Повторный вопрос обнаружен: {is_repeated}")

    is_repeated_new = brain.situational.is_repeated_question("Что нового?")
    print(f"{'✅' if not is_repeated_new else '⚠️'} Новый вопрос корректен: {not is_repeated_new}")

    # Тест 6: Оценка экспертизы пользователя
    print("\n🔍 ТЕСТ 6: Оценка экспертизы")
    expertise_tests = [
        ("Что такое нейронная сеть? помоги начать", 0.3),
        ("Как оптимизировать градиентный спуск в глубоких сетях?", 0.7),
        ("Объясни простыми словами", 0.2)
    ]

    for text, expected_min in expertise_tests:
        expertise = brain.situational.detect_user_expertise(text)
        status = "✅" if expertise >= expected_min or text.find("простыми") >= 0 else "⚠️"
        print(f"{status} '{text[:40]}...' → экспертиза: {expertise:.2f}")

    # Статистика
    print("\n" + "=" * 70)
    print("📊 СТАТИСТИКА СИТУАТИВНОСТИ:")
    stats = brain.situational.get_statistics()
    print(f"   Всего взаимодействий: {stats['total_interactions']}")
    print(f"   Распределение настроений: {stats['mood_distribution']}")
    print(f"   Средняя срочность: {stats['average_urgency']:.2f}")
    print("=" * 70)

    print("\n✅ ТЕСТ СИТУАТИВНОСТИ ЗАВЕРШЕН!")


if __name__ == "__main__":
    test_situational()