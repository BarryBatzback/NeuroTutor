# test_imports.py
import sys
from pathlib import Path

# Добавляем путь
sys.path.insert(0, str(Path(__file__).parent))

print("🔍 Тестируем импорты...")

try:
    from src.brain.cortex import Cortex

    print("✅ Cortex импортирован успешно")

    # Пробуем создать экземпляр
    brain = Cortex()
    print("✅ Экземпляр Cortex создан успешно")

except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
except Exception as e:
    print(f"❌ Ошибка при создании: {e}")
    import traceback

    traceback.print_exc()