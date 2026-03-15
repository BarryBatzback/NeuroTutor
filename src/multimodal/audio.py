# src/multimodal/audio.py

import asyncio
from pathlib import Path
from typing import Dict, Optional
import wave
import json
import logging

logger = logging.getLogger(__name__)

try:
    import speech_recognition as sr

    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False

try:
    import whisper

    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

try:
    from pydub import AudioSegment

    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False


class AudioProcessor:
    """
    Обработчик аудио для мультимодального мозга
    Распознает речь, анализирует звук
    """

    def __init__(self, brain, multilingual):
        self.brain = brain
        self.ml = multilingual
        self.download_dir = Path("data/audio")
        self.download_dir.mkdir(parents=True, exist_ok=True)

        # Загружаем модели
        self.models = self._load_models()

        print("🎤 AudioProcessor инициализирован")
        print(f"   SpeechRecognition: {'✅' if SR_AVAILABLE else '❌'}")
        print(f"   Whisper: {'✅' if WHISPER_AVAILABLE else '❌'}")
        print(f"   Pydub: {'✅' if PYDUB_AVAILABLE else '❌'}")

    def _load_models(self):
        """Загрузка аудио моделей"""
        models = {}

        if WHISPER_AVAILABLE:
            try:
                models['whisper'] = whisper.load_model("tiny")  # tiny/base/small/medium/large
                print("   ✅ Загружена модель Whisper")
            except Exception as e:
                logger.error(f"Ошибка загрузки Whisper: {e}")

        return models

    async def process_audio(self, audio_path: str) -> Dict:
        """
        Обработка аудио файла

        Args:
            audio_path: путь к аудио файлу

        Returns:
            Dict: результаты анализа
        """
        results = {
            'text': '',
            'language': '',
            'duration': 0,
            'segments': [],
            'neurons_created': 0
        }

        try:
            # Получаем длительность
            if PYDUB_AVAILABLE:
                audio = AudioSegment.from_file(audio_path)
                results['duration'] = len(audio) / 1000.0

            # Распознаем речь
            if 'whisper' in self.models:
                loop = asyncio.get_event_loop()

                def _transcribe():
                    return self.models['whisper'].transcribe(audio_path)

                transcript = await loop.run_in_executor(None, _transcribe)

                results['text'] = transcript.get('text', '')
                results['language'] = transcript.get('language', '')
                results['segments'] = transcript.get('segments', [])

            elif SR_AVAILABLE:
                # Fallback на Google Speech Recognition
                recognizer = sr.Recognizer()
                with sr.AudioFile(audio_path) as source:
                    audio_data = recognizer.record(source)
                    try:
                        results['text'] = recognizer.recognize_google(audio_data, language='ru-RU')
                        results['language'] = 'ru'
                    except:
                        try:
                            results['text'] = recognizer.recognize_google(audio_data, language='en-US')
                            results['language'] = 'en'
                        except:
                            pass

            # Создаем нейроны
            if results['text']:
                neurons = self.ml.create_multilingual_neuron(
                    self.brain,
                    f"Распознанная речь: {results['text'][:500]}",
                    category="Audio_Transcript"
                )
                results['neurons_created'] += len(neurons)

            return results

        except Exception as e:
            logger.error(f"Ошибка обработки аудио: {e}")
            return results