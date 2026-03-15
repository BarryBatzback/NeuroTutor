from src.brain.cortex import Cortex

brain = Cortex()
brain.load("optimized_brain_v2.pkl")

print("🧠 Чат с мозгом (напиши 'выход' для выхода)")
while True:
    query = input("\nТы: ")
    if query.lower() in ['выход', 'exit', 'quit']:
        break

    results = brain.think(query)
    if results:
        print("\nМозг: Нашёл ассоциации:")
        for neuron, activation, depth in results[:3]:
            indent = "  " * depth
            print(f"{indent}• {neuron.content[:100]}... (уверенность: {activation:.2f})")
    else:
        print("\nМозг: Я не знаю ответ на этот вопрос")