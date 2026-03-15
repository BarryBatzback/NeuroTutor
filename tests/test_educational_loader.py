# tests/test_educational_loader.py
import sys
import asyncio
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.brain.cortex import Cortex
from src.brain.multilingual import MultilingualProcessor
from src.knowledge.api_learners import APILearner
from src.knowledge.educational_loader import EducationalLoader


async def test_educational_loader():
    print("=" * 70)
    print("🎓 ТЕСТ ЗАГРУЗЧИКА УЧЕБНЫХ ЗНАНИЙ")
    print("=" * 70)

    # Создаем мозг
    brain = Cortex()

    # ИСПРАВЛЕНО: передаем brain в MultilingualProcessor
    ml = MultilingualProcessor(brain)
    api = APILearner(brain, ml)
    loader = EducationalLoader(brain, ml, api)

    # Тест 1: Загрузка школьной математики (5 класс)
    print("\n🔍 ТЕСТ 1: Школьная математика 5 класс")
    result1 = await loader.load_school_subject('mathematics', '5', 'дроби')
    print(f"   Результат: {result1.get('neurons_created', 0)} нейронов")

    # Тест 2: Загрузка школьной физики (7 класс)
    print("\n🔍 ТЕСТ 2: Школьная физика 7 класс")
    result2 = await loader.load_school_subject('physics', '7', 'механика основы')
    print(f"   Результат: {result2.get('neurons_created', 0)} нейронов")

    # Тест 3: Загрузка высшей математики
    print("\n🔍 ТЕСТ 3: Высшая математика")
    result3 = await loader.load_university_subject('higher_mathematics', 'математический анализ')
    print(f"   Результат: {result3.get('neurons_created', 0)} нейронов")

    # Тест 4: Загрузка геодезии
    print("\n🔍 ТЕСТ 4: Геодезия")
    result4 = await loader.load_university_subject('geodesy', 'gps технологии')
    print(f"   Результат: {result4.get('neurons_created', 0)} нейронов")

    # Тест 5: Статистика
    print("\n🔍 ТЕСТ 5: Статистика образовательных знаний")
    stats = loader.get_educational_stats()
    print(f"   Школьных нейронов: {stats['school_neurons']}")
    print(f"   Университетских нейронов: {stats['university_neurons']}")
    print(f"   Всего: {stats['total_educational']}")

    # Сохраняем мозг
    brain.save("educational_brain_test.pkl")
    print("\n💾 Мозг сохранен")

    print("\n" + "=" * 70)
    print("✅ ТЕСТ ЗАВЕРШЕН")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_educational_loader())