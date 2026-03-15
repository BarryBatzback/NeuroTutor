# tests/test_real_conditions.py (исправленная версия)
import sys
from pathlib import Path
import time

sys.path.append(str(Path(__file__).parent.parent))

from src.brain.cortex import Cortex


def test_real_conditions():
    print("=" * 70)
    print("🧪 ТЕСТ РЕАЛЬНЫХ УСЛОВИЙ — ЕДИНОЕ МЫШЛЕНИЕ")
    print("=" * 70)

    # Создаём мозг
    brain = Cortex()

    # Заполняем техническими знаниями
    print("\n📚 Загружаем технические знания...")
    technical_knowledge = [
        # Высшая математика
        ("math_deriv", "Производная показывает скорость изменения функции", "Mathematics"),
        ("math_integral", "Интеграл вычисляет площадь под кривой", "Mathematics"),
        ("math_matrix", "Матрицы используются для линейных преобразований", "Mathematics"),

        # Геодезия и картография
        ("geo_coords", "Геодезические координаты: широта, долгота, высота", "Geodesy"),
        ("geo_projection", "Картографические проекции искажают поверхность Земли", "Cartography"),
        ("geo_gps", "GPS использует триангуляцию спутников для позиционирования", "Geodesy"),

        # Строительство
        ("build_materials", "Бетон — композитный материал из цемента, песка и щебня", "Construction"),
        ("build_loads", "Нагрузки на конструкции делятся на постоянные и временные", "Construction"),
        ("build_beam", "Нагрузка на балку рассчитывается через момент инерции и модуль упругости", "Construction"),

        # Автомобилестроение
        ("auto_engine", "ДВС преобразует химическую энергию топлива в механическую", "Automotive"),
        ("auto_differential", "Дифференциал позволяет колёсам вращаться с разной скоростью", "Automotive"),
        ("auto_transmission", "Трансмиссия передаёт крутящий момент от двигателя к колёсам", "Automotive"),

        # Физика
        ("phys_force", "Сила измеряется в Ньютонах: F = ma", "Physics"),
        ("phys_satellite", "Спутники не падают благодаря орбитальной скорости и гравитации", "Physics"),
        ("phys_energy", "Энергия сохраняется в замкнутой системе", "Physics"),

        # Технологии
        ("tech_ml", "Машинное обучение использует алгоритмы для анализа данных", "Technology"),
        ("tech_ai", "Искусственный интеллект имитирует человеческое мышление", "Technology")
    ]

    for uid, content, category in technical_knowledge:
        brain.add_knowledge(uid, content, category)

    # Создаём связи между связанными понятиями
    print("\n🔗 Создаём связи между знаниями...")
    brain.create_synapse(
        brain.graph.nodes['build_loads']['neuron'],
        brain.graph.nodes['build_beam']['neuron'],
        weight=0.8
    )
    brain.create_synapse(
        brain.graph.nodes['auto_differential']['neuron'],
        brain.graph.nodes['auto_transmission']['neuron'],
        weight=0.7
    )
    brain.create_synapse(
        brain.graph.nodes['phys_satellite']['neuron'],
        brain.graph.nodes['phys_force']['neuron'],
        weight=0.9
    )
    brain.create_synapse(
        brain.graph.nodes['tech_ml']['neuron'],
        brain.graph.nodes['geo_coords']['neuron'],
        weight=0.5
    )

    # === ТЕСТОВЫЕ ЗАПРОСЫ ===
    test_queries = [
        {
            'query': "Как рассчитать нагрузку на балку в строительстве?",
            'context': {'user_level': 'student', 'urgency': 'medium'},
            'expected': 'technical_solution'
        },
        {
            'query': "Почему спутники не падают на Землю?",
            'context': {'user_level': 'curious', 'urgency': 'low'},
            'expected': 'explanation'
        },
        {
            'query': "Придумай инновационный способ картографирования",
            'context': {'user_level': 'researcher', 'urgency': 'low'},
            'expected': 'creative'
        },
        {
            'query': "Как работает дифференциал в автомобиле?",
            'context': {'user_level': 'mechanic', 'urgency': 'high'},
            'expected': 'technical_explanation'
        },
        {
            'query': "Можно ли использовать машинное обучение в геодезии?",
            'context': {'user_level': 'engineer', 'urgency': 'medium'},
            'expected': 'interdisciplinary'
        }
    ]

    for i, test in enumerate(test_queries, 1):
        print(f"\n{'=' * 60}")
        print(f"🔍 ЗАПРОС {i}: {test['query']}")
        print(f"📋 Контекст: {test['context']}")
        print(f"🎯 Ожидаемый тип: {test['expected']}")
        print(f"{'-' * 60}")

        # Обрабатываем через единый движок
        result = brain.unified_thinking.process_query(
            test['query'],
            test['context']
        )

        # Выводим результат
        answer = result['final_answer']['text'] if result['final_answer'] else 'Нет ответа'
        print(f"💬 Ответ: {answer[:300]}...")
        print(f"📊 Уверенность: {result['confidence']:.2f}")
        print(f"🔧 Тип ответа: {result['final_answer']['type'] if result['final_answer'] else 'unknown'}")
        print(f"⏱️ Время обработки: {result['duration']:.3f} сек")

        # Показываем этапы мышления
        print(f"\n🧠 Этапы мышления:")
        for stage_name, stage_data in result['stages'].items():
            if isinstance(stage_data, dict):
                print(f"   • {stage_name}: {len(stage_data)} параметров")

        # Проверка соответствия
        actual_type = result['final_answer']['type'] if result['final_answer'] else 'unknown'
        match = "✅" if test['expected'] in actual_type or actual_type in test['expected'] else "⚠️"
        print(f"\n{match} Соответствие: {actual_type} vs {test['expected']}")

    # === ТЕСТ ОБУЧЕНИЯ ===
    print(f"\n{'=' * 60}")
    print("🔄 ТЕСТ ОБУЧЕНИЯ НА ОБРАТНОЙ СВЯЗИ")
    print(f"{'-' * 60}")

    brain.unified_thinking.learn_from_interaction(
        "Как рассчитать нагрузку на балку?",
        {'success': True, 'user_satisfaction': 0.9}
    )

    # === ФИНАЛЬНАЯ СТАТИСТИКА ===
    print(f"\n{'=' * 70}")
    print("📊 ИТОГОВАЯ СТАТИСТИКА ЕДИНОГО МЫШЛЕНИЯ")
    print(f"{'=' * 70}")

    stats = brain.unified_thinking.get_thinking_stats()
    print(f"   Всего обработано запросов: {stats['total_queries']}")
    print(f"   Средняя уверенность: {stats['avg_confidence']:.2f}")
    print(f"   Среднее время ответа: {stats['avg_duration']:.3f} сек")
    print(f"   Режим мышления: {stats['mode']}")
    print(f"   Уровень креативности: {stats['creativity_level']}")

    print(f"\n🧠 Статистика мозга:")
    brain_stats = brain.get_stats()
    print(f"   Нейронов: {brain_stats['neurons']}")
    print(f"   Синапсов: {brain_stats['synapses']}")
    print(f"   Категории: {brain_stats['categories']}")

    # Сохраняем
    brain.save("brain_unified_thinking.pkl")
    print(f"\n💾 Мозг сохранён: brain_unified_thinking.pkl")

    print(f"\n🎉 ТЕСТ РЕАЛЬНЫХ УСЛОВИЙ ЗАВЕРШЁН!")

    return brain


if __name__ == "__main__":
    test_real_conditions()