# learn_from_photos.py
import asyncio
from pathlib import Path
from src.brain.cortex import Cortex
from src.multimodal.vision import VisionProcessor


async def learn_from_photos():
    brain = Cortex()
    brain.load("multimodal_brain.pkl")
    vision = VisionProcessor(brain, ml)

    # Обработай все фото в папке
    photos = Path("my_photos").glob("*.jpg")
    for photo in photos:
        with open(photo, 'rb') as f:
            await vision.process_image(f.read())

    brain.save("brain_with_memories.pkl")