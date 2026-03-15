import asyncio
from pathlib import Path
from src.brain.cortex import Cortex
from src.multimodal.documents import DocumentProcessor


async def learn_from_library():
    brain = Cortex()
    brain.load("multimodal_brain.pkl")
    docs = DocumentProcessor(brain, ml)

    # Обработай все книги в папке
    library = Path("my_books")
    for book in library.glob("*.pdf"):
        await docs.process_document(str(book))
        print(f"📚 Изучена книга: {book.name}")