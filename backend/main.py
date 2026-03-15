# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import sys
from pathlib import Path

# Добавляем путь к проекту
sys.path.append(str(Path(__file__).parent.parent))

from src.brain.cortex import Cortex
from src.brain.multilingual import MultilingualProcessor
from src.brain.critical_thinking import CriticalThinking
from src.brain.improvisation import Improvisation


# Модели данных
class QueryRequest(BaseModel):
    query: str
    language: str = 'ru'
    depth: str = 'normal'  # fast, normal, deep


class QueryResponse(BaseModel):
    answer: str
    confidence: float
    sources: List[str]
    thinking_process: Dict


class LearnRequest(BaseModel):
    content: str
    category: str
    language: str = 'ru'


class LearnResponse(BaseModel):
    success: bool
    neurons_created: int
    message: str


class BrainStats(BaseModel):
    neurons: int
    synapses: int
    categories: Dict[str, int]
    thoughts: int


# Инициализация FastAPI
app = FastAPI(
    title="NeuroTutor API",
    description="API для ИИ с человеческим мышлением",
    version="1.0.0"
)

# CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Глобальные переменные
brain = None
ml = None


@app.on_event("startup")
async def startup_event():
    """Инициализация при запуске"""
    global brain, ml

    print("🧠 Инициализация мозга...")
    brain = Cortex()

    try:
        brain.load("data/models/technical_brain.pkl")
        print("✅ Мозг загружен")
    except Exception as e:
        print(f"⚠️ Мозг не найден, создаём новый: {e}")

    ml = MultilingualProcessor()
    print("🌍 Многоязычный процессор готов")


@app.get("/")
async def root():
    """Информация об API"""
    return {
        "name": "NeuroTutor API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": [
            "/query",
            "/learn",
            "/stats",
            "/health"
        ]
    }


@app.get("/health")
async def health_check():
    """Проверка здоровья"""
    return {
        "status": "healthy",
        "brain_loaded": brain is not None,
        "neurons": brain.get_stats()['neurons'] if brain else 0
    }


@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Обработка запроса к мозгу
    """
    if not brain:
        raise HTTPException(status_code=500, detail="Мозг не инициализирован")

    # Определяем язык запроса
    detected_lang = ml.detect_language(request.query)

    # Поиск в мозге
    results = brain.think(request.query)

    # Формируем ответ
    if results:
        answer_parts = []
        sources = []

        for neuron, confidence, depth in results[:5]:
            content = neuron.content

            # Перевод если нужно
            if detected_lang != request.language and confidence > 0.5:
                neuron_lang = brain.graph.nodes[neuron.uid].get('language', 'ru')
                if neuron_lang != request.language:
                    content = ml.translate(content, request.language, neuron_lang)

            answer_parts.append(f"• {content}")
            sources.append(neuron.category)

        answer = "\n".join(answer_parts)
        avg_confidence = sum(c for _, c, _ in results[:5]) / len(results[:5])

        thinking_process = {
            'language_detected': detected_lang,
            'results_found': len(results),
            'depth': request.depth
        }

        return QueryResponse(
            answer=answer,
            confidence=round(avg_confidence, 2),
            sources=list(set(sources)),
            thinking_process=thinking_process
        )
    else:
        return QueryResponse(
            answer="К сожалению, у меня нет информации по этому вопросу. Вы можете обучить меня.",
            confidence=0.0,
            sources=[],
            thinking_process={'language_detected': detected_lang, 'results_found': 0}
        )


@app.post("/learn", response_model=LearnResponse)
async def learn_content(request: LearnRequest):
    """
    Обучение мозга новому контенту
    """
    if not brain:
        raise HTTPException(status_code=500, detail="Мозг не инициализирован")

    try:
        # Создаём многоязычный нейрон
        neurons = ml.create_multilingual_neuron(
            brain,
            request.content,
            request.category
        )

        # Сохраняем мозг
        brain.save("technical_brain.pkl")

        return LearnResponse(
            success=True,
            neurons_created=len(neurons),
            message=f"Выучено на {len(neurons)} языках!"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats", response_model=BrainStats)
async def get_stats():
    """
    Статистика мозга
    """
    if not brain:
        raise HTTPException(status_code=500, detail="Мозг не инициализирован")

    stats = brain.get_stats()

    return BrainStats(
        neurons=stats['neurons'],
        synapses=stats['synapses'],
        categories=stats['categories'],
        thoughts=stats['thoughts']
    )


@app.get("/categories")
async def get_categories():
    """
    Список категорий знаний
    """
    if not brain:
        raise HTTPException(status_code=500, detail="Мозг не инициализирован")

    stats = brain.get_stats()

    return {
        "categories": stats['categories'],
        "total": sum(stats['categories'].values())
    }


@app.post("/critical/analyze")
async def critical_analyze(query: str):
    """
    Критический анализ информации
    """
    if not brain or not hasattr(brain, 'critical_thinking'):
        raise HTTPException(status_code=500, detail="Модуль критического мышления недоступен")

    analysis = brain.critical_thinking.analyze_information(query)

    return {
        "information": query[:100],
        "confidence": analysis['confidence'],
        "conclusion": analysis['conclusion'],
        "action": analysis['action'],
        "contradictions": len(analysis.get('contradictions', [])),
        "verifications": len(analysis.get('verifications', []))
    }


@app.post("/improvisation/solve")
async def improvisation_solve(problem: str):
    """
    Творческое решение проблемы
    """
    if not brain or not hasattr(brain, 'improvisation'):
        raise HTTPException(status_code=500, detail="Модуль импровизации недоступен")

    solution = brain.improvisation.solve_creatively(problem)

    return {
        "problem": problem,
        "solution": solution['solution'],
        "analogies": solution['analogies'],
        "confidence": solution['confidence']
    }


# Запуск сервера
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)