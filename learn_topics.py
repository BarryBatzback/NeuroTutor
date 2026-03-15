import asyncio
from src.brain.cortex import Cortex
from src.brain.multilingual import MultilingualProcessor
from src.knowledge.optimized_learner import OptimizedLearner


async def learn_many():
    brain = Cortex()
    brain.load("optimized_brain_v2.pkl")
    ml = MultilingualProcessor()

    async with OptimizedLearner(brain, ml) as learner:
        topics = [
            "Квантовая физика",
            "Машинное обучение",
            "История Древнего Рима",
            "Алгоритмы сортировки",
            "Базы данных SQL"
        ]

        for topic in topics:
            await learner.optimized_learn(topic, 'medium')
            brain.save("brain_updated.pkl")


asyncio.run(learn_many())