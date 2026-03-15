# src/knowledge/learning_scheduler.py

import asyncio
from datetime import datetime, timedelta
import schedule
import time
from typing import List, Callable
import logging

logger = logging.getLogger(__name__)


class LearningScheduler:
    """
    Планировщик обучения - автоматическое обучение по расписанию
    """

    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.scheduled_jobs = []
        self.is_running = False
        self.loop = None

    def add_daily_learning(self, topic: str, time_str: str = "03:00",
                           depth: str = "medium"):
        """
        Добавление ежедневного обучения

        Args:
            topic: тема
            time_str: время в формате "HH:MM"
            depth: глубина
        """
        schedule.every().day.at(time_str).do(
            lambda: asyncio.create_task(
                self.orchestrator.learn_specific(topic, depth)
            )
        )
        self.scheduled_jobs.append({
            'type': 'daily',
            'topic': topic,
            'time': time_str,
            'depth': depth
        })
        print(f"📅 Добавлено ежедневное обучение: {topic} в {time_str}")

    def add_weekly_learning(self, topic: str, day: str, time_str: str = "10:00",
                            depth: str = "deep"):
        """
        Добавление еженедельного обучения

        Args:
            topic: тема
            day: день недели (monday, tuesday, ...)
            time_str: время
            depth: глубина
        """
        getattr(schedule.every(), day).at(time_str).do(
            lambda: asyncio.create_task(
                self.orchestrator.learn_specific(topic, depth)
            )
        )
        self.scheduled_jobs.append({
            'type': 'weekly',
            'topic': topic,
            'day': day,
            'time': time_str,
            'depth': depth
        })
        print(f"📅 Добавлено еженедельное обучение: {topic} по {day} в {time_str}")

    def add_topic_list_schedule(self, topics: List[str], interval_hours: int = 6):
        """
        Добавление расписания для списка тем

        Args:
            topics: список тем
            interval_hours: интервал между темами в часах
        """
        start_time = datetime.now()

        for i, topic in enumerate(topics):
            scheduled_time = start_time + timedelta(hours=i * interval_hours)
            time_str = scheduled_time.strftime("%H:%M")

            # Запускаем в указанное время
            schedule.every().day.at(time_str).do(
                lambda t=topic: asyncio.create_task(
                    self.orchestrator.learn_specific(t, "medium")
                )
            )

            self.scheduled_jobs.append({
                'type': 'scheduled',
                'topic': topic,
                'time': time_str,
                'interval': interval_hours
            })

        print(f"📅 Добавлено расписание для {len(topics)} тем")

    async def run(self):
        """Запуск планировщика"""
        self.is_running = True
        print("⏰ Планировщик обучения запущен")

        while self.is_running:
            schedule.run_pending()
            await asyncio.sleep(60)  # Проверка каждую минуту

    def stop(self):
        """Остановка планировщика"""
        self.is_running = False
        schedule.clear()
        print("⏰ Планировщик обучения остановлен")

    def list_jobs(self) -> List[Dict]:
        """Список запланированных задач"""
        return self.scheduled_jobs