import subprocess
import sys


def install_packages():
    """Установка всех необходимых пакетов"""

    packages = [
        'aiohttp',
        'asyncio',
        'cachetools',
        'spacy',
        'textblob',
        'scikit-learn',
        'langdetect',
        'deep-translator',
        'wikipedia',
        'wikipedia-api',
        'arxiv',
        'feedparser',
        'beautifulsoup4',
        'yt-dlp',
        'pytube',
        'duckduckgo-search',
        'schedule',
        'python-dotenv'
    ]

    print("📦 Установка пакетов...")

    for package in packages:
        print(f"   Установка {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    print("\n✅ Все пакеты установлены!")

    # Установка spaCy моделей
    print("\n📚 Установка NLP моделей...")
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "ru_core_news_sm"])
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])

    print("\n🎉 Готово! Теперь можно запускать тесты!")


if __name__ == "__main__":
    install_packages()