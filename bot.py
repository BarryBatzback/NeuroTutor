# bot.py - ИСПРАВЛЕННАЯ ВЕРСИЯ
import asyncio
import logging
import sys
import os
import tempfile
from pathlib import Path

# ВАЖНО: Сначала добавляем путь к проекту ДО всех других импортов из src
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Теперь импорты из проекта будут работать
from src.brain.cortex import Cortex
from src.brain.multilingual import MultilingualProcessor
from src.knowledge.api_learners import APILearner
from src.multimodal.vision import VisionProcessor
from src.multimodal.documents import DocumentProcessor
from src.multimodal.audio import AudioProcessor

# Импорты aiogram
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Конфигурация
BOT_TOKEN = "8651180805:AAHAayQaPC1hP7ktISsm5gEh6mPaZb7jdBw"

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Загрузка мозга
print("🧠 Загрузка мозга...")
brain = Cortex()
try:
    brain.load("data/models/multilingual_brain.pkl")
    print(f"✅ Мозг загружен: {brain.get_stats()['neurons']} нейронов")
except:
    print("⚠️ Создаём новый мозг")
    brain = Cortex()


# Состояния
class LearnStates(StatesGroup):
    waiting_for_text = State()


# Клавиатуры
def get_main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🔍 Поиск", callback_data="search"))
    builder.add(InlineKeyboardButton(text="📚 Учить", callback_data="learn"))
    builder.add(InlineKeyboardButton(text="📊 Статистика", callback_data="stats"))
    builder.add(InlineKeyboardButton(text="🧠 О мозге", callback_data="about"))
    builder.adjust(2)
    return builder.as_markup()


# Обработчики
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "🧠 *Добро пожаловать в NeuroTutor!*\n\n"
        "Я - ИИ с человеческим мышлением:\n"
        "• Критическое мышление\n"
        "• Импровизация\n"
        "• Многоязычность (11 языков)\n\n"
        "Задай вопрос или выбери действие!",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )


# В bot.py добавить:
@dp.message(F.text)
async def handle_message(message: Message):
    # 1. Обновить контекст ситуативности
    brain.situational.update_context(user_id, message.text)

    # 2. Критически оценить запрос
    analysis = brain.critical_thinking.analyze_information(message.text)

    # 3. Если нужна творческая задача
    if analysis['action'] == 'need_creativity':
        solution = brain.improvisation.solve_creatively(message.text)
        response = solution['solution']
    else:
        # 4. Обычный поиск
        results = brain.think(message.text)
        response = format_results(results)

    # 5. Адаптировать ответ под ситуацию
    adapted = brain.situational.adapt_response(response)

    await message.answer(adapted)

@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data
    try:
        await callback.answer()
    except:
        pass

    if data == "search":
        await callback.message.edit_text(
            "🔍 Напиши свой вопрос!",
            reply_markup=get_main_keyboard()
        )
    elif data == "learn":
        await callback.message.edit_text(
            "📚 Отправь текст для обучения",
            reply_markup=get_main_keyboard()
        )
        await state.set_state(LearnStates.waiting_for_text)
    elif data == "stats":
        stats = brain.get_stats()
        text = f"📊 *Статистика:*\n"
        text += f"🧠 Нейронов: {stats['neurons']}\n"
        text += f"🔗 Синапсов: {stats['synapses']}\n"
        text += f"💭 Мыслей: {stats['thoughts']}"
        await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=get_main_keyboard())
    elif data == "about":
        await callback.message.edit_text(
            "🧠 *О моём мозге:*\n\n"
            "• Нейроны хранят знания\n"
            "• Синапсы создают связи\n"
            "• Критическое мышление анализирует\n"
            "• Импровизация творит\n"
            "• 11 языков поддержки",
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )


@dp.message(LearnStates.waiting_for_text)
async def process_learning_text(message: Message, state: FSMContext):
    text = message.text
    neurons = brain.multilingual.create_multilingual_neuron(text, "learned")
    brain.save("multilingual_brain.pkl")

    await message.answer(
        f"✅ Выучил на {len(neurons)} языках!\n"
        f"Теперь смогу отвечать на вопросы.",
        reply_markup=get_main_keyboard()
    )
    await state.clear()


async def main():
    print("=" * 50)
    print("🚀 ЗАПУСК NEUROTUTOR БОТА")
    print("=" * 50)

    # Проверка токена
    if not BOT_TOKEN or BOT_TOKEN.startswith('YOUR_') or len(BOT_TOKEN) < 40:
        logger.error("❌ НЕВЕРНЫЙ ТОКЕН БОТА!")
        logger.error("Получи новый токен у @BotFather и вставь в BOT_TOKEN")
        return

    try:
        # Тестовый запрос к Telegram
        print("🔍 Проверка соединения с Telegram...")
        me = await bot.get_me()
        print(f"✅ Подключено: @{me.username}")
    except TelegramNetworkError as e:
        logger.error(f"❌ Ошибка сети: {e}")
        logger.error("Проверь:")
        logger.error("  • Интернет соединение")
        logger.error("  • Не заблокирован ли Telegram")
        logger.error("  • Настройки брандмауэра")
        logger.error("Попробуй использовать прокси (см. USE_PROXY в коде)")
        return
    except TelegramAPIError as e:
        logger.error(f"❌ Ошибка API Telegram: {e}")
        logger.error("Проверь правильность токена")
        return
    except Exception as e:
        logger.error(f"❌ Неожиданная ошибка: {e}")
        return

    print(f"🧠 Нейронов: {brain.get_stats()['neurons']}")
    print(f"🌍 Языков: {len(ml.supported_languages)}")
    print("=" * 50)

    # Запуск поллинга с обработкой ошибок
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ Ошибка при поллинге: {e}")
    finally:
        await bot.session.close()
        print("👋 Сессия закрыта")