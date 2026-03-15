import os
from pathlib import Path

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Пуки к данным
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = DATA_DIR / "models"
LOGS_DIR = DATA_DIR / "logs"

# Создаем папки, если их нет
for directory in [DATA_DIR, MODELS_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# --- ГИПЕРПАРАМЕТРЫ МОЗГА ---
BRAIN_CONFIG = {
    "learning_rate": 0.1,       # Как быстро укрепляются связи
    "forgetting_rate": 0.98,    # Коэффициент забывания за цикл (ближе к 1 = долгая память)
    "activation_threshold": 0.3,# Минимальный вес связи для "воспоминания"
    "max_connections": 50,      # Максимум связей у одного нейрона (чтобы не перегружать)
    "decay_interval": 3600,     # Интервал забывания в секундах (1 час для теста)
}

# Telegram Bot Token (лучше вынести в .env, но пока так)
BOT_TOKEN = "ТВОЙ_ТОКЕН_ОТ_BOTFATHER"

# Логирование
LOG_LEVEL = "INFO"