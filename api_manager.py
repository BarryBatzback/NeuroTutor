# api_manager.py (исправленная версия)
import asyncio
import aiohttp
import requests


async def test_all_apis():
    print("=" * 60)
    print("🔍 ТЕСТ ВСЕХ API ПОДКЛЮЧЕНИЙ")
    print("=" * 60)

    results = {}

    # Wikipedia - ИСПРАВЛЕНО
    try:
        import wikipedia
        wikipedia.set_lang("ru")
        page = wikipedia.page("Тест", auto_suggest=True)
        results['Wikipedia'] = 'OK'
        print(f"✅ Wikipedia: OK")
    except Exception as e:
        results['Wikipedia'] = 'FAIL'
        print(f"❌ Wikipedia: FAIL ({str(e)[:50]})")

    # arXiv
    try:
        import arxiv
        search = arxiv.Search(query="test", max_results=1)
        list(search.results())
        results['arXiv'] = 'OK'
        print(f"✅ arXiv: OK")
    except Exception as e:
        results['arXiv'] = 'FAIL'
        print(f"❌ arXiv: FAIL")

    # Google Books
    try:
        url = "https://www.googleapis.com/books/v1/volumes"
        params = {'q': 'test', 'maxResults': 1}
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            results['Google Books'] = 'OK'
            print(f"✅ Google Books: OK")
        else:
            results['Google Books'] = 'FAIL'
            print(f"❌ Google Books: FAIL ({response.status_code})")
    except Exception as e:
        results['Google Books'] = 'FAIL'
        print(f"❌ Google Books: FAIL")

    # GitHub
    try:
        url = "https://api.github.com"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            results['GitHub'] = 'OK'
            print(f"✅ GitHub: OK")
        else:
            results['GitHub'] = 'FAIL'
            print(f"❌ GitHub: FAIL")
    except Exception as e:
        results['GitHub'] = 'FAIL'
        print(f"❌ GitHub: FAIL")

    # Telegram
    try:
        from aiogram import Bot
        BOT_TOKEN = "8651180805:AAHAayQaPC1hP7ktISsm5gEh6mPaZb7jdBw"
        bot = Bot(token=BOT_TOKEN)
        await bot.get_me()
        await bot.session.close()
        results['Telegram'] = 'OK'
        print(f"✅ Telegram: OK")
    except Exception as e:
        results['Telegram'] = 'FAIL'
        print(f"❌ Telegram: FAIL ({str(e)[:50]})")

    # Итог
    print("=" * 60)
    ok_count = sum(1 for v in results.values() if v == 'OK')
    print(f"📊 Результат: {ok_count}/{len(results)} API работают")

    return results


if __name__ == "__main__":
    asyncio.run(test_all_apis())