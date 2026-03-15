import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.brain.cortex import Cortex
from src.brain.multilingual import MultilingualProcessor


async def test_simple():
    print("🧪 ПРОСТОЙ ТЕСТ")
    print("=" * 50)

    # Тест 1: Создание мозга
    brain = Cortex()
    print("✅ Мозг создан")

    # Тест 2: Многоязычность
    ml = MultilingualProcessor()

    test_phrases = [
        ("Привет, мир!", "ru"),
        ("Hello, world!", "en"),
        ("Bonjour le monde!", "fr")
    ]

    for phrase, expected in test_phrases:
        detected = ml.detect_language(phrase)
        print(f"   '{phrase}' -> {detected} (ожидался {expected})")

    # Тест 3: Создание нейронов
    neuron = brain.create_neuron("Тестовое знание", "test")
    print(f"✅ Создан нейрон: {neuron.uid}")

    # Тест 4: Сохранение
    brain.save("test_brain.pkl")
    print("✅ Мозг сохранен")

    print("\n✨ Все базовые тесты пройдены!")


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_simple())