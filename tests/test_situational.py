# tests/test_situational.py
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from src.brain.cortex import Cortex


def test_situational():
    print("=" * 70)
    print("🌍 ТЕСТ МОДУЛЯ СИТУАТИВНОСТИ")
    print("=" * 70)

    brain = Cortex()

    # Тест 1: Анализ обычного запроса
    print("\n🔍 ТЕСТ 1: Обычный запрос")
    context1 = brain.situational.analyze_context("Что такое нейронная сеть?")
    print(f"📝 Запрос: Что такое нейронная сеть?")
    print(f"🕐 Время: {context1['time']['period']} (энергия: {context1['time']['energy_level']})")
    print(f"😊 Настроение: {context1['user_mood']['dominant']}")
    print(f"⚡ Срочность: {context1['urgency']:.2f}")
    print(f"📊 Сложность: {context1['query_complexity']:.2f}")
    print(f"🎯 Тип: {context1['query_type']}")

    # Тест 2: Срочный запутанный запрос
    print("\n🔍 ТЕСТ 2: Срочный запутанный запрос")
    context2 = brain.situational.analyze_context(
        "СРОЧНО!!! Не понимаю, как решить эту задачу по интегралам, помогите!!!")
    print(f"📝 Запрос: СРОЧНО!!! Не понимаю...")
    print(
        f"😊 Настроение: {context2['user_mood']['dominant']} (интенсивность: {context2['user_mood']['intensity']:.2f})")
    print(f"⚡ Срочность: {context2['urgency']:.2f}")
    print(f"📊 Сложность: {context2['query_complexity']:.2f}")
    print(f"🎯 Тип: {context2['query_type']}")

    # Тест 3: Адаптация ответа
    print("\n🔍 ТЕСТ 3: Адаптация ответа")
    base_response = "Нейронная сеть — это вычислительная модель, вдохновлённая биологическими нейронными сетями."

    adapted_urgent = brain.situational.adapt_response(base_response, context2)
    print(f"📄 Исходный: {base_response}")
    print(f"⚡ Адаптированный под срочность: {adapted_urgent}")

    # Тест 4: Рекомендация подхода
    print("\n🔍 ТЕСТ 4: Рекомендация подхода")
    approach = brain.situational.recommend_approach(context1['query_type'], context1)
    print(f"🎯 Тип запроса: {context1['query_type']}")
    print(f"📋 Рекомендуемая структура: {approach['structure']}")
    print(f"💡 Включать примеры: {approach['include_examples']}")
    print(f"📚 Глубина: {approach['technical_depth']:.2f}")

    # Тест 5: Статистика
    print("\n🔍 ТЕСТ 5: Статистика")
    stats = brain.situational.get_statistics()
    print(f"📊 Всего взаимодействий: {stats['total_interactions']}")
    print(f"😊 Распределение эмоций: {stats['emotion_distribution']}")
    print(f"🎯 Типы запросов: {stats['query_type_distribution']}")

    print("\n" + "=" * 70)
    print("✅ Тест ситуативности завершён!")


if __name__ == "__main__":
    test_situational()