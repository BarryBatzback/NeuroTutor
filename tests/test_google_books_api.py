# tests/test_google_books_api.py
import requests


def test_google_books():
    print("📖 Тест Google Books API")

    # Без API ключа (базовый тест)
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        'q': 'нейронные сети',
        'maxResults': 2,
        'langRestrict': 'ru'
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"   Статус: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Найдено книг: {len(data.get('items', []))}")
        elif response.status_code == 403:
            print(f"   ⚠️ Нужен API ключ (403 Forbidden)")
        else:
            print(f"   ❌ Ошибка: {response.status_code}")

    except requests.exceptions.Timeout:
        print(f"   ❌ Timeout - проверь интернет")
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Ошибка соединения - возможен блокировщик")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")


if __name__ == "__main__":
    test_google_books()