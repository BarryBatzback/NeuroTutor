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


# В bot.py, замени handle_message на:

@dp.message(F.text & ~F.command)
async def handle_message(message: Message):
    """Обработка текстовых сообщений через единое мышление"""
    query = message.text

    # Показываем, что бот думает
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    # Контекст из сообщения
    context = {
        'user_id': message.from_user.id,
        'chat_id': message.chat.id,
        'timestamp': datetime.now()
    }

    # Обрабатываем через единый движок мышления
    result = brain.unified_thinking.process_query(query, context)

    # Формируем ответ
    answer = result['final_answer']['text']
    confidence = result['confidence']

    # Добавляем индикатор уверенности
    if confidence > 0.8:
        confidence_mark = "✅"
    elif confidence > 0.6:
        confidence_mark = "🟡"
    else:
        confidence_mark = "🔶"

    response = f"{confidence_mark} {answer}"

    # Если есть дополнительные идеи (креативный режим)
    if result['stages'].get('creative_solution', {}).get('brainstorm_ideas'):
        response += "\n\n💡 Дополнительные идеи:"
        for idea in result['stages']['creative_solution']['brainstorm_ideas'][:2]:
            response += f"\n   • {idea}"

    # Если есть пробелы в знаниях
    knowledge = result['stages'].get('knowledge_retrieval', {})
    if knowledge.get('knowledge_gaps'):
        response += f"\n\n📚 Хотите, чтобы я изучил: {knowledge['knowledge_gaps'][0][:50]}...?"
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📖 Да, изучи это", callback_data=f"learn_gap_{hash(query) % 10000}")]
        ])
        await message.answer(response, reply_markup=kb)
    else:
        await message.answer(response)

    # Обучаемся на реакции (упрощённо)
    # В реальном боте здесь можно отслеживать реакции пользователя
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