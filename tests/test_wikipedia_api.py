# tests/test_wikipedia_api.py
import wikipedia
import wikipediaapi

# Тест 1: wikipedia библиотекой
try:
    wikipedia.set_lang("ru")
    page = wikipedia.page("Гравитация", auto_suggest=True)
    print(f"✅ Wikipedia: {page.title}")
except Exception as e:
    print(f"❌ Wikipedia ошибка: {e}")

# Тест 2: wikipedia-api - ИСПРАВЛЕНО!
try:
    # ПРАВИЛЬНАЯ ИНИЦИАЛИЗАЦИЯ С USER_AGENT
    wiki = wikipediaapi.Wikipedia(
        language='ru',
        user_agent='NeuroTutor/1.0 ( Educational AI Project )'
    )
    page = wiki.page("Гравитация")
    print(f"✅ WikiAPI: {page.exists()}")
except Exception as e:
    print(f"❌ WikiAPI ошибка: {e}")