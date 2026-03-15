# src/multimodal/video.py

import asyncio
import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional
import tempfile
import subprocess
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class VideoProcessor:
    """
    Обработчик видео для мультимодального мозга
    Извлекает ключевые кадры, анализирует сцены
    """

    def __init__(self, brain, multilingual, vision_processor):
        self.brain = brain
        self.ml = multilingual
        self.vision = vision_processor
        self.download_dir = Path("data/videos")
        self.download_dir.mkdir(parents=True, exist_ok=True)

        print("📹 VideoProcessor инициализирован")

    async def process_video(self, video_path: str, sample_rate: int = 30) -> Dict:
        """
        Обработка видео файла

        Args:
            video_path: путь к видео
            sample_rate: частота выборки кадров (кадров в секунду)

        Returns:
            Dict: результаты анализа
        """
        results = {
            'duration': 0,
            'fps': 0,
            'total_frames': 0,
            'key_scenes': [],
            'objects': {},
            'neurons_created': 0
        }

        try:
            cap = cv2.VideoCapture(video_path)

            # Получаем информацию о видео
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / fps

            results['duration'] = duration
            results['fps'] = fps
            results['total_frames'] = total_frames

            # Извлекаем ключевые кадры
            frame_interval = int(fps / sample_rate)
            frame_count = 0
            scene_changes = []
            prev_frame = None

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                if frame_count % frame_interval == 0:
                    # Проверяем смену сцены
                    if prev_frame is not None:
                        diff = np.mean(np.abs(frame - prev_frame))
                        if diff > 30:  # Порог смены сцены
                            scene_changes.append(frame_count / fps)

                    # Сохраняем ключевой кадр
                    timestamp = frame_count / fps
                    frame_path = self.download_dir / f"frame_{timestamp:.2f}.jpg"
                    cv2.imwrite(str(frame_path), frame)

                    # Анализируем кадр
                    _, img_encoded = cv2.imencode('.jpg', frame)
                    vision_results = await self.vision.process_image(
                        img_encoded.tobytes(),
                        source=f"video_frame_{timestamp}"
                    )

                    results['neurons_created'] += vision_results.get('neurons_created', 0)

                    # Собираем статистику объектов
                    for obj in vision_results.get('objects', []):
                        obj_name = obj['object']
                        results['objects'][obj_name] = results['objects'].get(obj_name, 0) + 1

                    prev_frame = frame

                frame_count += 1

            cap.release()

            # Создаем нейрон для описания видео
            video_description = f"Видео длительностью {duration:.2f} секунд. "
            video_description += f"Обнаружены объекты: {', '.join(results['objects'].keys())}"

            neurons = self.ml.create_multilingual_neuron(
                self.brain,
                video_description,
                category="Video"
            )
            results['neurons_created'] += len(neurons)

            return results

        except Exception as e:
            logger.error(f"Ошибка обработки видео: {e}")
            return results

    async def process_youtube(self, url: str) -> Dict:
        """
        Обработка YouTube видео
        """
        try:
            # Скачиваем видео
            import yt_dlp

            ydl_opts = {
                'format': 'best[height<=480]',
                'outtmpl': str(self.download_dir / '%(title)s.%(ext)s'),
                'quiet': True
            }

            loop = asyncio.get_event_loop()

            def _download():
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    return filename, info

            video_path, info = await loop.run_in_executor(None, _download)

            # Обрабатываем видео
            results = await self.process_video(video_path)

            # Добавляем метаданные
            results['title'] = info.get('title', '')
            results['uploader'] = info.get('uploader', '')
            results['description'] = info.get('description', '')[:200]

            return results

        except Exception as e:
            logger.error(f"Ошибка обработки YouTube: {e}")
            return {}