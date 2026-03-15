# tests/test_telegram_api.py
import asyncio
from aiogram import Bot


async def test_telegram():
    print("🤖 Тест Telegram API")

    # Твой токен
    BOT_TOKEN = "8651180805:AAHAayQaPC1hP7ktISsm5gEh6mPaZb7jdBw"

    print(f"   Токен: {BOT_TOKEN[:15]}...")

    # Проверка 1: Длина токена
    if len(BOT_TOKEN) < 40:
        print(f"   ❌ Токен слишком короткий!")
        return

    # Проверка 2: Подключение
    try:
        print(f"   🔍 Подключение к api.telegram.org...")
        bot = Bot(token=BOT_TOKEN)
        me = await bot.get_me()
        print(f"   ✅ Бот: @{me.username} ({me.full_name})")
        await bot.session.close()
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        print(f"
        Возможные
        причины: ")
        print(f"   1. Telegram заблокирован провайдером")
        print(f"   2. Неправильный токен")
        print(f"   3. Брандмауэр блокирует соединение")
        print(f"
        Решение: ")
        print(f"   • Попробуй VPN или прокси")
        print(f"   • Проверь токен у @BotFather")
        print(f"   • Отключи антивирус временно")

        if __name__ == "__main__":
            asyncio.run(test_telegram())