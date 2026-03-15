import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.brain.cortex import Cortex
from src.brain.multilingual import MultilingualProcessor


def test_multilingual():
    print("🌍 ТЕСТИРОВАНИЕ МНОГОЯЗЫЧНОГО МОЗГА")
    print("=" * 50)

    # Создаем мозг и процессор
    brain = Cortex()
    ml = MultilingualProcessor()

    # Создаем многоязычные нейроны
    print("\n📚 Создание многоязычных знаний:")

    concepts = [
        ("Гравитация - это сила притяжения между объектами", "Physics"),
        ("Newton's first law states that an object at rest stays at rest", "Physics"),
        ("Wasser besteht aus H2O Molekülen", "Chemistry"),
        ("L'eau est composée de molécules H2O", "Chemistry"),
    ]

    for content, category in concepts:
        neurons = ml.create_multilingual_neuron(brain, content, category)
        print(f"   Создано нейронов: {len(neurons)} для '{content[:30]}...'")

    # Статистика по языкам
    lang_stats = ml.get_language_stats(brain)
    print(f"\n📊 Статистика по языкам:")
    for lang, count in lang_stats.items():
        if count > 0:
            print(f"   {ml.supported_languages[lang]}: {count} нейронов")

    # Тестируем поиск на разных языках
    print("\n🔍 Тестирование поиска:")

    test_queries = [
        ("гравитация", "ru"),
        ("gravity", "en"),
        ("Schwerkraft", "de"),
        ("water", "en"),
        ("вода", "ru"),
        ("l'eau", "fr"),
    ]

    for query, expected_lang in test_queries:
        print(f"\n📝 Запрос: '{query}' (ожидаемый язык: {expected_lang})")

        detected = ml.detect_language(query)
        print(f"   Определён язык: {detected} ({ml.supported_languages[detected]})")

        results = ml.search_multilingual(brain, query)

        if results:
            for neuron, activation, depth in results[:2]:
                indent = "  " * depth
                lang = brain.graph.nodes[neuron.uid].get('language', 'unknown')
                print(f"   {indent}• [{lang}] {neuron.content[:60]}... (уверенность: {activation:.2f})")
        else:
            print("   ❌ Ничего не найдено")

    # Сохраняем многоязычный мозг
    brain.save("multilingual_brain.pkl")

    return brain, ml


if __name__ == "__main__":
    brain, ml = test_multilingual()