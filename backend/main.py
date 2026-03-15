# backend/main.py
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import sys
from pathlib import Path
import asyncio

# Добавляем путь к проекту
sys.path.append(str(Path(__file__).parent.parent))

from src.brain.cortex import Cortex
from src.brain.multilingual import MultilingualProcessor
from src.knowledge.api_learners import APILearner


# Модели данных
class QueryRequest(BaseModel):
    query: str
    language: str = 'ru'
    depth: str = 'normal'  # fast, normal, deep
    context: Optional[Dict] = {}


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


class AutoLearnRequest(BaseModel):
    topic: str
    depth: str = 'basic'  # basic, medium, deep
    sources: Optional[List[str]] = None


# Инициализация FastAPI
app = FastAPI(
    title="NeuroTutor API",
    description="API для ИИ с человеческим мышлением",
    version="2.0.0"
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
api_learner = None


@app.on_event("startup")
async def startup_event():
    """Инициализация при запуске"""
    global brain, ml, api_learner

    print("🧠 Инициализация мозга...")
    brain = Cortex()

    try:
        brain.load("data/models/brain_after_learning.pkl")
        print("✅ Мозг загружен")
    except Exception as e:
        print(f"⚠️ Мозг не найден, создаём новый: {e}")
        brain = Cortex()

    ml = MultilingualProcessor()
    api_learner = APILearner(brain, ml)
    print("🌍 Многоязычный процессор готов")
    print("🌐 API Learner готов")


@app.get("/")
async def root():
    """Информация об API"""
    return {
        "name": "NeuroTutor API",
        "version": "2.0.0",
        "status": "running",
        "modules": [
            "critical_thinking",
            "improvisation",
            "situational_awareness",
            "multilingual",
            "self_learning"
        ],
        "endpoints": [
            "/query",
            "/learn",
            "/auto-learn",
            "/stats",
            "/health",
            "/thinking/critical",
            "/thinking/improvisation"
        ]
    }


@app.get("/health")
async def health_check():
    """Проверка здоровья"""
    return {
        "status": "healthy",
        "brain_loaded": brain is not None,
        "neurons": brain.get_stats()['neurons'] if brain else 0,
        "synapses": brain.get_stats()['synapses'] if brain else 0
    }


@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Обработка запроса через все модули мышления
    """
    if not brain:
        raise HTTPException(status_code=500, detail="Мозг не инициализирован")

    # Обрабатываем через единый интерфейс
    result = brain.process_query(request.query, request.context)

    # Определяем источники
    sources = []
    if result['knowledge_used'] > 0:
        sources.append("internal_knowledge")
    if result['thinking_process'].get('creativity_applied', False):
        sources.append("improvisation")

    return QueryResponse(
        answer=result['response'],
        confidence=result['confidence'],
        sources=sources,
        thinking_process=result
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
        neurons = ml.create_multilingual_neuron(brain, request.content, request.category)

        # Сохраняем мозг
        brain.save("brain_after_learning.pkl")

        return LearnResponse(
            success=True,
            neurons_created=len(neurons),
            message=f"Выучено на {len(neurons)} языках!"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/auto-learn")
async def auto_learn(request: AutoLearnRequest, background_tasks: BackgroundTasks):
    """
    Автоматическое обучение из интернета
    """
    if not api_learner:
        raise HTTPException(status_code=500, detail="API Learner не инициализирован")

    # Запускаем обучение в фоне (может занять время)
    background_tasks.add_task(api_learner.auto_learn, request.topic, request.depth)

    return {
        "status": "learning_started",
        "topic": request.topic,
        "depth": request.depth,
        "message": "Обучение запущено в фоновом режиме"
    }


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


@app.get("/thinking/critical")
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


@app.post("/thinking/improvisation")
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


# Запуск сервера
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)