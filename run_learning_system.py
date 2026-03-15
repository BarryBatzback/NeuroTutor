# run_learning_system.py

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from src.brain.cortex import Cortex
from src.brain.multilingual import MultilingualProcessor
from src.knowledge.optimized_learner import OptimizedLearner, LearningOrchestrator
from src.knowledge.learning_scheduler import LearningScheduler


async def main():
    print("=" * 60)
    print("🧠 ЗАПУСК ОПТИМИЗИРОВАННОЙ СИСТЕМЫ ОБУЧЕНИЯ")
    print("=" * 60)

    # Загружаем или создаем мозг
    brain = Cortex()
    try:
        brain.load("data/models/optimized_brain.pkl")
        print("✅ Мозг загружен")
    except:
        print("🆕 Создан новый мозг")

    # Многоязычный процессор
    ml = MultilingualProcessor()

    # Создаем оркестратор
    orchestrator = LearningOrchestrator(brain, ml)
    await orchestrator.start()

    # Создаем планировщик
    scheduler = LearningScheduler(orchestrator)

    # Добавляем темы для изучения
    topics = [
        "Квантовая физика",
        "Нейронные сети",
        "Искусственный интеллект",
        "Философия сознания",
        "Космология",
        "Генетика",
        "Нанотехнологии"
    ]

    # Добавляем в очередь
    for topic in topics:
        await orchestrator.add_topic(topic, priority=5)

    # Добавляем ежедневное обучение
    scheduler.add_daily_learning("Новости науки", "09:00", "fast")
    scheduler.add_daily_learning("Технологические тренды", "18:00", "fast")

    # Добавляем еженедельное глубокое обучение
    scheduler.add_weekly_learning("Глубокое обучение", "sunday", "15:00", "deep")

    # Запускаем планировщик в фоне
    scheduler_task = asyncio.create_task(scheduler.run())

    # Интерактивный режим
    print("\n📝 Интерактивный режим. Команды:")
    print("  /learn <тема> [глубина] - изучить тему")
    print("  /queue - показать очередь")
    print("  /stats - статистика")
    print("  /exit - выход")

    try:
        while True:
            command = input("\n> ").strip()

            if command.startswith("/learn"):
                parts = command[7:].strip().split()
                if parts:
                    topic = parts[0]
                    depth = parts[1] if len(parts) > 1 else "medium"
                    await orchestrator.learn_specific(topic, depth)
                else:
                    print("Использование: /learn <тема> [глубина]")

            elif command == "/queue":
                size = orchestrator.get_queue_size()
                print(f"📊 В очереди: {size} тем")

            elif command == "/stats":
                stats = orchestrator.get_stats()
                print(f"📊 Статистика обучения:")
                print(f"   Всего сессий: {stats.get('total_sessions', 0)}")
                print(f"   Всего нейронов: {stats.get('total_neurons', 0)}")
                print(f"   Кэш попаданий: {stats.get('cache_hits', 0)}")
                print(f"   Последние темы: {stats.get('recent_topics', [])}")

            elif command == "/exit":
                break

            else:
                print("Неизвестная команда")

    except KeyboardInterrupt:
        print("\n\n🛑 Получен сигнал прерывания")

    finally:
        # Останавливаем все
        scheduler.stop()
        scheduler_task.cancel()
        await orchestrator.stop()

        # Сохраняем мозг
        brain.save("optimized_brain.pkl")
        print("✅ Мозг сохранен")


if __name__ == "__main__":
    asyncio.run(main())