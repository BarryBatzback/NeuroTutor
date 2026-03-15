# 🧠 NeuroTutor - ИИ с человеческим мышлением

## Возможности

- ✅ **Биологическая структура** - нейроны и синапсы
- ✅ **Критическое мышление** - анализ и проверка информации
- ✅ **Импровизация** - творческие решения
- ✅ **Многоязычность** - 11 языков
- ✅ **Мультимодальность** - изображения, документы
- ✅ **Обучение из API** - Wikipedia, arXiv, Google Books

## Установка

```bash
# 1. Клонировать репозиторий
git clone https://github.com/yourusername/NeuroTutor.git
cd NeuroTutor

# 2. Создать виртуальное окружение
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Создать .env файл
cp .env.example .env
# Отредактировать .env и добавить BOT_TOKEN

# 5. Запустить тесты
python tests/test_core.py

# 6. Запустить бота
python bot.py