import asyncio
from src.brain.cortex import Cortex
from config.settings import MODELS_DIR, BOT_TOKEN
# В начале main.py добавь:
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def test_brain():
    print("🚀 Запуск тестирования биологического мозга...")
    brain = Cortex()

    # 1. Обучение (создание знаний)
    brain.add_knowledge("math_pythagoras", "Теорема Пифагора: a² + b² = c²", "Math")
    brain.add_knowledge("math_triangle", "Треугольник - фигура с тремя углами", "Math")
    brain.add_knowledge("hist_ww2", "Вторая мировая война 1939-1945", "History")

    # 2. Создание ассоциаций (синапсов)
    brain.connect("math_pythagoras", "math_triangle", 0.9)
    brain.connect("math_triangle", "math_pythagoras", 0.8)  # Обратная связь

    # 3. Мышление
    print("\n--- Запрос: math_pythagoras ---")
    thoughts = brain.think("math_pythagoras")
    for t in thoughts:
        print(f"💡 Ассоциация: {t['content']} (Уверенность: {t['confidence']})")

    # 4. Сохранение
    brain.save_state(MODELS_DIR / "brain_v1.pkl")


if __name__ == "__main__":
    # Пока запускаем тест мозга
    test_brain()

    # Позже раскомментируем запуск бота:
    # from src.bot.main import run_bot
    # asyncio.run(run_bot())