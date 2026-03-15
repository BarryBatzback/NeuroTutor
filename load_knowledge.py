# load_knowledge.py
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from src.brain.cortex import Cortex
from src.knowledge.technical_knowledge import TechnicalKnowledgeLoader


def main():
    print("=" * 70)
    print("📚 ЗАГРУЗКА ТЕХНИЧЕСКИХ ЗНАНИЙ")
    print("=" * 70)

    # Загружаем или создаём мозг
    brain = Cortex()
    try:
        brain.load("data/models/technical_brain.pkl")
        print("✅ Существующий мозг загружен")
    except:
        print("🆕 Создан новый мозг")

    # Создаём загрузчик
    loader = TechnicalKnowledgeLoader(brain)

    # Выбор глубины загрузки
    print("\nВыберите глубину загрузки:")
    print("1. Базовая (20 знаний на категорию)")
    print("2. Средняя (50 знаний на категорию)")
    print("3. Полная (все знания)")

    choice = input("\nВаш выбор (1-3): ").strip()
    depth_map = {'1': 'basic', '2': 'medium', '3': 'deep'}
    depth = depth_map.get(choice, 'basic')

    # Загружаем знания
    print(f"\n🔄 Загрузка знаний (глубина: {depth})...")
    stats = loader.load_all(depth)

    # Сохраняем мозг
    brain.save("technical_brain.pkl")

    # Вывод статистики
    print("\n" + "=" * 70)
    print("📊 СТАТИСТИКА ЗАГРУЗКИ:")
    print(f"   Всего нейронов: {stats['total_neurons']}")
    print("\n   По категориям:")
    for category, count in stats['by_category'].items():
        print(f"   • {category}: {count} нейронов")

    brain_stats = brain.get_stats()
    print(f"\n   Всего в мозге: {brain_stats['neurons']} нейронов")
    print(f"   Синапсов: {brain_stats['synapses']}")
    print("=" * 70)
    print("✅ Загрузка завершена!")


if __name__ == "__main__":
    main()