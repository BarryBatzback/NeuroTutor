# test_import.py
import networkx as nx
import numpy as np
from src.brain.cortex import Cortex

print("✅ Все модули импортированы успешно!")

brain = Cortex()
print(f"🧠 Мозг создан: {brain.get_stats()['neurons']} нейронов")