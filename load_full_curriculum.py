# load_full_curriculum.py
import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from src.brain.cortex import Cortex
from src.brain.multilingual import MultilingualProcessor
from src.knowledge.api_learners import APILearner
from src.knowledge.educational_loader import EducationalLoader


async def main():
    print("=" * 70)
    print("🎓 ЗАГРУЗКА ПОЛНОЙ УЧЕБНОЙ ПРОГРАММЫ")
    print("=" * 70)

    # Создаем или загружаем мозг
    brain = Cortex()
    try:
        brain.load("educational_brain.pkl")
        print("✅ Загружен существующий мозг")
    except:
        print("🆕 Создан новый мозг")

    ml = MultilingualProcessor()
    api = APILearner(brain, ml)
    loader = EducationalLoader(brain, ml, api)

    # Выбор предметов для загрузки
    print("
    📚 Выберите
    предметы
    для
    загрузки: ")
    print("1. Школьная математика (5-11 класс)")
    print("2. Школьная физика (7-11 класс)")
    print("3. Высшая математика")
    print("4. Геодезия")
    print("5. Картография")
    print("6. Строительство")
    print("7. Автомобилестроение")
    print("8. ВСЁ СРАЗУ")
    print("0. Пропустить")

    choice = input("
    Ваш
    выбор(1 - 8, 0): ").strip()

    subjects = []
    if choice == '1':
        subjects = ['school_math']
    elif choice == '2':
        subjects = ['school_physics']
    elif choice == '3':
        subjects = ['higher_math']
    elif choice == '4':
        subjects = ['geodesy']
    elif choice == '5':
        subjects = ['cartography']
    elif choice == '6':
        subjects = ['construction']
    elif choice == '7':
        subjects = ['automotive']
    elif choice == '8':
        subjects = None  # Все предметы
    elif choice == '0':
        print("Загрузка пропущена")
    return
    else:
    print("Неверный выбор")
    return


    # Загружаем
    results = await loader.load_full_curriculum(subjects)

    # Итоговая статистика
    stats = loader.get_educational_stats()
    print("
          " + " = " * 70)
    print("📊 ИТОГОВАЯ СТАТИСТИКА МОЗГА:")
    brain_stats = brain.get_stats()
    print(f"   Всего нейронов: {brain_stats['neurons']}")
    print(f"   Всего синапсов: {brain_stats['synapses']}")
    print(f"   Школьных знаний: {stats['school_neurons']}")
    print(f"   Университетских знаний: {stats['university_neurons']}")
    print("=" * 70)

# Сохраняем
brain.save("educational_brain_full.pkl")
print("
💾 Мозг
сохранен
как
educational_brain_full.pkl
")

if __name__ == "__main__":
    asyncio.run(main())