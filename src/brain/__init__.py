class Cortex:
    def __init__(self, load_from_file: str = None):
        """
        Инициализация мозга

        Args:
            load_from_file: путь к файлу для загрузки сохраненного состояния
        """
        self.graph = nx.DiGraph()  # Используем направленный граф
        self.memory = MemoryManager()

        # Параметры обучения (биологические)
        self.learning_rate = 0.1  # Скорость обучения
        self.forgetting_rate = 0.01  # Скорость забывания
        self.hebbian_factor = 0.05  # Коэффициент Хеббовского обучения

        # Статистика
        self.thought_count = 0

        # Добавить ЭТУ строку:
        self.critical_thinking = CriticalThinking(self)

        # Загружаем сохраненное состояние если указано
        if load_from_file:
            self.load(load_from_file)