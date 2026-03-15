import asyncio
import logging
from pathlib import Path
import sys

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from src.knowledge.api_learners import APILearner

# Добавляем путь к проекту
sys.path.append(str(Path(__file__).parent))

from src.brain.cortex import Cortex
from src.brain.multilingual import MultilingualProcessor
from src.knowledge.parser import KnowledgeParser

# Конфигурация
BOT_TOKEN = "8651180805:AAHAayQaPC1hP7ktISsm5gEh6mPaZb7jdBw"  # Вставь свой токен от @BotFather

# Инициализация
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Загружаем мозг
print("🧠 Загрузка мозга...")
brain = Cortex()
try:
    brain.load("data/models/multilingual_brain.pkl")
    print("✅ Мозг загружен")
except:
    print("⚠️ Создаём новый мозг")
    brain = Cortex()

# Многоязычный процессор
ml = MultilingualProcessor()


# Состояния для FSM
class LearnStates(StatesGroup):
    waiting_for_text = State()
    waiting_for_category = State()


api_learner = APILearner(brain, ml)


# Новые состояния
class LearnAPISates(StatesGroup):
    waiting_for_topic = State()
    waiting_for_depth = State()


# Новые кнопки в главном меню
def get_main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🔍 Поиск", callback_data="search"))
    builder.add(InlineKeyboardButton(text="📚 Учить", callback_data="learn"))
    builder.add(InlineKeyboardButton(text="🌍 Языки", callback_data="languages"))
    builder.add(InlineKeyboardButton(text="📊 Статистика", callback_data="stats"))
    builder.add(InlineKeyboardButton(text="🧠 О мозге", callback_data="about"))
    builder.add(InlineKeyboardButton(text="🌐 Учить из интернета", callback_data="learn_api"))  # НОВОЕ
    builder.adjust(2)
    return builder.as_markup()


# Обработчик для API обучения
@dp.callback_query(F.data == "learn_api")
async def cmd_learn_api(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "🌐 *Обучение из интернета*\n\n"
        "Я могу изучить любую тему из:\n"
        "• Wikipedia (на разных языках)\n"
        "• Научные статьи arXiv\n"
        "• Google Books\n"
        "• Новости\n\n"
        "Напиши тему, которую хочешь изучить:",
        parse_mode="Markdown"
    )
    await state.set_state(LearnAPISates.waiting_for_topic)
    await callback.answer()


@dp.message(LearnAPISates.waiting_for_topic)
async def process_api_topic(message: Message, state: FSMContext):
    topic = message.text

    await state.update_data(topic=topic)

    # Клавиатура выбора глубины
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="📘 Базовая", callback_data="depth_basic"))
    builder.add(InlineKeyboardButton(text="📚 Средняя", callback_data="depth_medium"))
    builder.add(InlineKeyboardButton(text="📖 Глубокая", callback_data="depth_deep"))

    await message.answer(
        f"Выбери глубину изучения для '{topic}':\n\n"
        "• Базовая: только Wikipedia\n"
        "• Средняя: Wikipedia + книги\n"
        "• Глубокая: все источники + научные статьи",
        reply_markup=builder.as_markup()
    )
    await state.set_state(LearnAPISates.waiting_for_depth)


@dp.callback_query(F.data.startswith("depth_"), LearnAPISates.waiting_for_depth)
async def process_api_depth(callback: types.CallbackQuery, state: FSMContext):
    depth = callback.data.replace("depth_", "")
    data = await state.get_data()
    topic = data['topic']

    await callback.message.edit_text(
        f"🔍 Изучаю '{topic}' (глубина: {depth})...\n"
        f"Это может занять некоторое время ⏳"
    )

    # Отправляем действие "печатает"
    await callback.bot.send_chat_action(callback.message.chat.id, "typing")

    # Запускаем обучение
    stats = api_learner.auto_learn(topic, depth)

    # Формируем отчет
    report = f"✅ *Изучение завершено!*\n\n"
    report += f"📚 Тема: {topic}\n"
    report += f"📊 Результаты:\n"
    report += f"   • Источников: {stats['sources']}\n"
    report += f"   • Новых нейронов: {stats['total_neurons']}\n\n"

    # Показываем, что узнали
    results = brain.think(topic)
    if results:
        report += "🧠 *Что я узнал:*\n"
        for neuron, activation, depth in results[:3]:
            report += f"   • {neuron.content[:100]}...\n"

    await callback.message.edit_text(report, parse_mode="Markdown")
    await state.clear()
    await callback.answer()

# Клавиатуры
def get_main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🔍 Поиск", callback_data="search"))
    builder.add(InlineKeyboardButton(text="📚 Учить", callback_data="learn"))
    builder.add(InlineKeyboardButton(text="🌍 Языки", callback_data="languages"))
    builder.add(InlineKeyboardButton(text="📊 Статистика", callback_data="stats"))
    builder.add(InlineKeyboardButton(text="🧠 О мозге", callback_data="about"))
    builder.adjust(2)
    return builder.as_markup()


def get_language_keyboard():
    builder = InlineKeyboardBuilder()
    for code, name in ml.supported_languages.items():
        builder.add(InlineKeyboardButton(text=f"🌍 {name}", callback_data=f"lang_{code}"))
    builder.add(InlineKeyboardButton(text="◀️ Назад", callback_data="back"))
    builder.adjust(3)
    return builder.as_markup()


# Обработчики команд
@dp.message(Command("start"))
async def cmd_start(message: Message):
    welcome_text = """
🧠 *Добро пожаловать в NeuroTutor!*

Я - искусственный интеллект, построенный по принципу человеческого мозга.
У меня есть нейроны и синапсы, я учусь и запоминаю информацию.

🌍 *Я понимаю много языков!*
Просто задай вопрос на любом языке.

📚 *Что я умею:*
• Отвечать на вопросы по физике, химии, математике
• Учиться из текстов
• Находить ассоциации между понятиями

Напиши свой вопрос или выбери действие в меню!
    """

    await message.answer(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )


@dp.message()
async def handle_message(message: Message):
    """Обработка текстовых сообщений"""
    query = message.text

    # Показываем, что бот думает
    await message.answer_chat_action("typing")

    # Многоязычный поиск
    results = ml.search_multilingual(brain, query)

    if results:
        # Определяем язык ответа
        response_lang = ml.detect_language(query)

        response = f"🧠 *Нашёл ассоциации:*\n\n"

        for i, (neuron, activation, depth) in enumerate(results[:5], 1):
            indent = "  " * depth

            # Получаем язык нейрона
            neuron_lang = brain.graph.nodes[neuron.uid].get('language', 'ru')

            # Если язык нейрона отличается от языка запроса, переводим
            if neuron_lang != response_lang and activation > 0.5:
                content = ml.translate(neuron.content, response_lang, neuron_lang)
                lang_mark = f"🌍 [{neuron_lang}→{response_lang}]"
            else:
                content = neuron.content
                lang_mark = f"🌐 [{neuron_lang}]"

            response += f"{indent}{i}. {content[:150]}...\n"
            response += f"{indent}   *Уверенность:* {activation:.2f} {lang_mark}\n\n"

        await message.answer(response, parse_mode="Markdown")
    else:
        # Если не нашли, предлагаем обучить
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📚 Обучить меня этому", callback_data=f"learn_{query}")]
        ])

        await message.answer(
            "🤔 Я не знаю ответ на этот вопрос.\n"
            "Хочешь обучить меня?",
            reply_markup=kb
        )


# Callback обработчики
@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data

    if data == "search":
        await callback.message.edit_text(
            "🔍 Напиши свой вопрос, и я поищу в своей базе знаний!",
            reply_markup=get_main_keyboard()
        )

    elif data == "learn":
        await callback.message.edit_text(
            "📚 Отправь мне текст, который хочешь, чтобы я выучил.\n"
            "Это может быть определение, формула или любой учебный материал.",
            reply_markup=get_main_keyboard()
        )
        await state.set_state(LearnStates.waiting_for_text)

    elif data == "languages":
        stats = ml.get_language_stats(brain)
        text = "🌍 *Поддерживаемые языки:*\n\n"
        for code, name in ml.supported_languages.items():
            count = stats.get(code, 0)
            text += f"• {name}: {count} нейронов\n"

        await callback.message.edit_text(
            text,
            parse_mode="Markdown",
            reply_markup=get_language_keyboard()
        )

    elif data.startswith("lang_"):
        lang = data.replace("lang_", "")
        name = ml.supported_languages.get(lang, lang)
        await callback.answer(f"Выбран язык: {name}")

    elif data == "stats":
        stats = brain.get_stats()
        text = f"""
📊 *Статистика мозга:*

🧠 *Нейронов:* {stats['neurons']}
🔗 *Синапсов:* {stats['synapses']}
💭 *Мыслей:* {stats['thoughts']}

📚 *По категориям:*
        """
        for cat, count in stats['categories'].items():
            text += f"   • {cat}: {count}\n"

        await callback.message.edit_text(
            text,
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )

    elif data == "about":
        text = """
🧠 *О моём мозге:*

Я построен по принципу человеческого мозга:
• *Нейроны* - хранят знания
• *Синапсы* - связи между знаниями
• *Активация* - процесс мышления
• *Обучение* - укрепление связей
• *Забывание* - ослабление неиспользуемых связей

🌍 *Многоязычность:*
Я понимаю и могу отвечать на 11 языках!

📚 *База знаний:*
Постоянно пополняется новыми фактами и определениями.
        """
        await callback.message.edit_text(
            text,
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )

    elif data.startswith("learn_"):
        query = data.replace("learn_", "")
        await callback.message.edit_text(
            f"📚 Отправь мне текст, который нужно запомнить про '{query}'",
            reply_markup=get_main_keyboard()
        )
        await state.set_state(LearnStates.waiting_for_text)
        await state.update_data(topic=query)

    elif data == "back":
        await callback.message.edit_text(
            "🧠 *Главное меню*",
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )

    await callback.answer()


@dp.message(LearnStates.waiting_for_text)
async def process_learning_text(message: Message, state: FSMContext):
    """Обработка текста для обучения"""
    text = message.text

    # Показываем, что бот думает
    await message.answer_chat_action("typing")

    # Определяем категорию (можно спросить у пользователя)
    data = await state.get_data()
    topic = data.get('topic', 'general')

    # Создаем многоязычный нейрон
    neurons = ml.create_multilingual_neuron(brain, text, topic)

    # Сохраняем мозг
    brain.save("multilingual_brain.pkl")

    await message.answer(
        f"✅ Я выучил этот текст на {len(neurons)} языках!\n"
        f"📚 Категория: {topic}\n"
        f"Теперь я смогу отвечать на вопросы по этой теме.",
        reply_markup=get_main_keyboard()
    )

    await state.clear()


async def main():
    print("🚀 Запуск NeuroTutor бота...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())