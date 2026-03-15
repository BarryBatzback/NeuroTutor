# tests/test_learning.py

import sys
import os
from pathlib import Path

# Добавляем путь к корневой папке проекта в sys.path
# Это нужно чтобы Python нашел наши модули src
sys.path.append(str(Path(__file__).parent.parent))

from src.brain.cortex import Cortex
from src.knowledge.parser import KnowledgeParser


def test_learning():
    print("🧪 ТЕСТИРОВАНИЕ ОБУЧЕНИЯ ИЗ ТЕКСТА")
    print("=" * 50)

    # Создаем мозг
    brain = Cortex()
    parser = KnowledgeParser(brain)

    # Правильный путь к файлу (относительно корня проекта)
    # Используем Path для кросс-платформенной совместимости
    textbook_path = Path(__file__).parent.parent / "data" / "raw" / "physics_101.txt"

    print(f"🔍 Ищем файл: {textbook_path}")

    if not textbook_path.exists():
        print(f"❌ Файл не найден: {textbook_path}")
        print("\n💡 Создаю файл с учебником автоматически...")

        # Создаем папку если её нет
        textbook_path.parent.mkdir(parents=True, exist_ok=True)

        # Создаем учебник
        create_sample_textbook(textbook_path)
        print(f"✅ Файл создан: {textbook_path}")

    # Обрабатываем учебник
    stats = parser.parse_textbook(
        filepath=str(textbook_path),
        category="Physics"
    )

    print("\n📊 Статистика обучения:")
    print(f"   Создано нейронов: {stats['neurons_created']}")
    print(f"   Обработано предложений: {stats['sentences']}")

    # Тестируем полученные знания
    print("\n💭 Тестирование знаний:")

    test_queries = ["Ньютон", "гравитация", "закон", "температура"]

    for query in test_queries:
        print(f"\n🔍 Запрос: '{query}'")
        results = brain.think(query)

        if results:
            for neuron, activation, depth in results[:3]:  # Показываем топ-3
                indent = "  " * depth
                print(f"   {indent}• {neuron.content[:80]}... (уверенность: {activation:.2f})")
        else:
            print("   Ничего не найдено")

    # Сохраняем обученный мозг
    brain.save("brain_after_learning.pkl")

    # Показываем статистику
    stats = brain.get_stats()
    print(f"\n📈 Итоговая статистика мозга:")
    print(f"   Нейронов: {stats['neurons']}")
    print(f"   Синапсов: {stats['synapses']}")
    print(f"   Категории: {stats['categories']}")

    return brain


def create_sample_textbook(filepath: Path):
    """Создает пример учебника если файл не найден"""

    textbook_content = """# Основы физики

## Механика
Механика - это раздел физики, изучающий движение тел и взаимодействие между ними.

Исаак Ньютон открыл три закона движения. Первый закон Ньютона гласит, что тело сохраняет состояние покоя или равномерного прямолинейного движения, пока на него не подействуют другие тела. Второй закон Ньютона описывает связь между силой, массой и ускорением: F = ma. Третий закон Ньютона говорит о том, что действие равно противодействию.

Гравитация - это фундаментальное взаимодействие. Закон всемирного тяготения Ньютона описывает притяжение между телами.

## Термодинамика
Температура - мера средней кинетической энергии молекул. Теплота - форма передачи энергии.

Первый закон термодинамики представляет собой закон сохранения энергии для тепловых процессов.

## Электричество
Электрический заряд - фундаментальное свойство частиц. Закон Кулона описывает взаимодействие зарядов.

Алессандро Вольта изобрел первый электрический элемент - вольтов столб.

## Оптика
Свет - это электромагнитная волна. Скорость света в вакууме составляет приблизительно 300000 км/с.

Линзы бывают собирающие и рассеивающие. Оптическая сила линзы измеряется в диоптриях.
"""

    # Записываем файл
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(textbook_content)

    print(f"📝 Создан пример учебника с основами физики")


if __name__ == "__main__":
    brain = test_learning()