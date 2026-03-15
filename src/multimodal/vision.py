# src/multimodal/vision.py

import asyncio
import aiohttp
import base64
from io import BytesIO
from PIL import Image
import pytesseract
import cv2
import numpy as np
from typing import List, Dict, Optional, Any
import hashlib
import os
from pathlib import Path
import logging

# Безопасные импорты для ML моделей
try:
    import torch
    import torchvision

    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("⚠️ torch не установлен. Некоторые функции будут ограничены")

try:
    from transformers import pipeline, ViTImageProcessor, ViTForImageClassification

    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("⚠️ transformers не установлен")

try:
    import easyocr

    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False
    print("⚠️ easyocr не установлен")

try:
    from ultralytics import YOLO

    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("⚠️ ultralytics не установлен")

logger = logging.getLogger(__name__)


class VisionProcessor:
    """
    Обработчик изображений для мультимодального мозга
    Может: распознавать объекты, читать текст, классифицировать изображения
    """

    def __init__(self, brain, multilingual):
        self.brain = brain
        self.ml = multilingual
        self.cache = {}

        # Загружаем модели
        self.models = self._load_models()

        # Создаем папку для загрузок
        self.download_dir = Path("data/uploads")
        self.download_dir.mkdir(parents=True, exist_ok=True)

        print("👁️ VisionProcessor инициализирован")
        print(f"   Torch: {'✅' if TORCH_AVAILABLE else '❌'}")
        print(f"   Transformers: {'✅' if TRANSFORMERS_AVAILABLE else '❌'}")
        print(f"   EasyOCR: {'✅' if EASYOCR_AVAILABLE else '❌'}")
        print(f"   YOLO: {'✅' if YOLO_AVAILABLE else '❌'}")

    def _load_models(self) -> Dict:
        """Загрузка всех моделей"""
        models = {}

        try:
            # Модель для классификации изображений
            if TRANSFORMERS_AVAILABLE:
                models['classifier'] = pipeline(
                    "image-classification",
                    model="google/vit-base-patch16-224"
                )
                print("   ✅ Загружена модель классификации")

            # YOLO для детекции объектов
            if YOLO_AVAILABLE:
                models['detector'] = YOLO('yolov8n.pt')  # nano версия
                print("   ✅ Загружена YOLO модель")

            # EasyOCR для распознавания текста
            if EASYOCR_AVAILABLE:
                models['ocr'] = easyocr.Reader(['ru', 'en'], gpu=False)
                print("   ✅ Загружена OCR модель")

        except Exception as e:
            logger.error(f"Ошибка загрузки моделей: {e}")

        return models

    async def process_image(self, image_data: bytes, source: str = "unknown") -> Dict:
        """
        Обработка изображения - создание нейронов на основе визуальной информации

        Args:
            image_data: байты изображения
            source: источник (URL, файл, telegram)

        Returns:
            Dict: результаты обработки
        """
        # Создаем хэш для кэша
        img_hash = hashlib.md5(image_data).hexdigest()[:10]

        if img_hash in self.cache:
            return self.cache[img_hash]

        results = {
            'objects': [],
            'text': [],
            'classification': [],
            'features': {},
            'neurons_created': 0
        }

        try:
            # Конвертируем в PIL Image
            img = Image.open(BytesIO(image_data))

            # Сохраняем для отладки
            img_path = self.download_dir / f"image_{img_hash}.jpg"
            img.save(img_path)

            # 1. Классификация изображения
            if 'classifier' in self.models:
                classes = self.models['classifier'](img)
                results['classification'] = classes[:3]  # Топ-3

            # 2. Детекция объектов
            if 'detector' in self.models:
                # Конвертируем в OpenCV формат
                img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                detections = self.models['detector'](img_cv)

                for detection in detections[0].boxes.data:
                    x1, y1, x2, y2, conf, cls = detection.tolist()
                    class_name = self.models['detector'].names[int(cls)]
                    results['objects'].append({
                        'object': class_name,
                        'confidence': conf,
                        'bbox': [x1, y1, x2, y2]
                    })

            # 3. Распознавание текста
            if 'ocr' in self.models:
                img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                ocr_results = self.models['ocr'].readtext(img_cv)

                for (bbox, text, confidence) in ocr_results:
                    results['text'].append({
                        'text': text,
                        'confidence': confidence,
                        'bbox': bbox
                    })

            # Создаем нейроны на основе найденной информации
            neurons_created = await self._create_vision_neurons(results, source, img_path)
            results['neurons_created'] = neurons_created

            # Сохраняем в кэш
            self.cache[img_hash] = results

            return results

        except Exception as e:
            logger.error(f"Ошибка обработки изображения: {e}")
            return results

    async def _create_vision_neurons(self, results: Dict, source: str, img_path: Path) -> int:
        """
        Создание нейронов на основе визуальной информации
        """
        count = 0

        # Нейрон для общей сцены
        if results['classification']:
            top_class = results['classification'][0]['label']
            scene_text = f"Изображение содержит: {top_class}"

            neurons = self.ml.create_multilingual_neuron(
                self.brain,
                scene_text,
                category=f"Vision_Scene"
            )
            count += len(neurons)

            # Добавляем метаданные
            for neuron in neurons.values():
                self.brain.graph.nodes[neuron.uid]['image_path'] = str(img_path)
                self.brain.graph.nodes[neuron.uid]['classification'] = results['classification']

        # Нейроны для каждого обнаруженного объекта
        obj_counts = {}
        for obj in results['objects']:
            obj_name = obj['object']
            obj_counts[obj_name] = obj_counts.get(obj_name, 0) + 1

        for obj_name, obj_count in obj_counts.items():
            obj_text = f"На изображении обнаружено {obj_count} объектов типа '{obj_name}'"

            neurons = self.ml.create_multilingual_neuron(
                self.brain,
                obj_text,
                category=f"Vision_Object"
            )
            count += len(neurons)

        # Нейроны для распознанного текста
        for text_item in results['text']:
            text_content = text_item['text']
            if len(text_content) > 5:
                text_text = f"На изображении найден текст: {text_content}"

                neurons = self.ml.create_multilingual_neuron(
                    self.brain,
                    text_text,
                    category=f"Vision_Text"
                )
                count += len(neurons)

        return count

    async def process_image_url(self, url: str) -> Dict:
        """
        Обработка изображения по URL
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        image_data = await response.read()
                        return await self.process_image(image_data, source=url)
        except Exception as e:
            logger.error(f"Ошибка загрузки по URL: {e}")
            return {}

    def get_stats(self) -> Dict:
        """Статистика обработки"""
        return {
            'cache_size': len(self.cache),
            'models_loaded': list(self.models.keys()),
            'torch_available': TORCH_AVAILABLE,
            'transformers_available': TRANSFORMERS_AVAILABLE,
            'yolo_available': YOLO_AVAILABLE,
            'ocr_available': EASYOCR_AVAILABLE
        }