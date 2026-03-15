from src.brain.cortex import Cortex

brain = Cortex()
brain.load("multimodal_brain.pkl")
stats = brain.get_stats()

print(f"🧠 Всего нейронов: {stats['neurons']}")
print(f"🔗 Всего синапсов: {stats['synapses']}")
print("📚 По категориям:")
for cat, count in stats['categories'].items():
    print(f"   • {cat}: {count}")