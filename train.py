# train.py

import asyncio
import sys
from pathlib import Path
import argparse
from datetime import datetime
import json

# Добавляем путь к проекту
sys.path.append(str(Path(__file__).parent))

from src.brain.cortex import Cortex
from src.brain.multilingual import MultilingualProcessor
from src.knowledge.optimized_learner import OptimizedLearner
from src.multimodal.vision import VisionProcessor
from src.multimodal.documents import DocumentProcessor
from src.multimodal.audio import AudioProcessor


class TrainingOrchestrator:
    """
    Оркестратор обучения - управляет всеми режимами обучения
    """

    def __init__(self):
        self.brain = None
        self.ml = None
        self.learner = None
        self.vision = None
        self.docs = None
        self.audio = None
        self.start_time = None
        self.stats = {
            'sessions': [],
            'total_neurons': 0,
            'total_time': 0
        }

        print("=" * 60)
        print("🧠 ТРЕНЕР МУЛЬТИМОДАЛЬНОГО МОЗГА v1.0")
        print("=" * 60)

    async def initialize(self, brain_path: str = None):
        """Инициализация всех компонентов"""
        print("\n📦 Инициализация компонентов...")

        # Загружаем или создаем мозг
        self.brain = Cortex()
        if brain_path and Path(brain_path).exists():
            self.brain.load(brain_path)
            print(f"✅ Мозг загружен: {brain_path}")
        else:
            print("🆕 Создан новый мозг")

        # Многоязычный процессор
        self.ml = MultilingualProcessor()

        # Обучатель из интернета
        self.learner = await OptimizedLearner(self.brain, self.ml).__aenter__()

        # Мультимодальные процессоры
        self.vision = VisionProcessor(self.brain, self.ml)
        self.docs = DocumentProcessor(self.brain, self.ml)
        self.audio = AudioProcessor(self.brain, self.ml)

        print("✅ Все компоненты готовы к работе")

        self.start_time = datetime.now()

    async def shutdown(self):
        """Завершение работы"""
        print("\n🛑 Завершение работы...")

        if self.learner:
            await self.learner.__aexit__(None, None, None)

        # Сохраняем статистику
        self.save_stats()

        # Сохраняем мозг
        if self.brain:
            filename = f"brain_trained_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
            self.brain.save(filename)

        elapsed = datetime.now() - self.start_time
        print(f"\n⏱️  Общее время: {elapsed.total_seconds():.2f} сек")
        print("👋 До свидания!")

    def save_stats(self):
        """Сохранение статистики"""
        stats_file = Path("training_stats.json")

        # Загружаем существующую статистику
        if stats_file.exists():
            with open(stats_file, 'r', encoding='utf-8') as f:
                old_stats = json.load(f)
                self.stats['sessions'] = old_stats.get('sessions', []) + self.stats['sessions']

        # Сохраняем
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, ensure_ascii=False, indent=2)

        print(f"\n📊 Статистика сохранена в {stats_file}")

    async def train_from_internet(self, topic: str, depth: str = 'medium'):
        """
        Режим 1: Обучение из интернета
        """
        print(f"\n🌐 ОБУЧЕНИЕ ИЗ ИНТЕРНЕТА: {topic}")
        print("=" * 40)

        stats = await self.learner.optimized_learn(topic, depth)

        self.stats['sessions'].append({
            'type': 'internet',
            'topic': topic,
            'depth': depth,
            'neurons': stats['neurons_created'],
            'time': stats['time_elapsed']
        })
        self.stats['total_neurons'] += stats['neurons_created']
        self.stats['total_time'] += stats['time_elapsed']

        return stats

    async def train_from_image(self, image_path: str):
        """
        Режим 2: Обучение из изображения
        """
        print(f"\n📸 ОБУЧЕНИЕ ИЗ ИЗОБРАЖЕНИЯ: {image_path}")
        print("=" * 40)

        with open(image_path, 'rb') as f:
            image_data = f.read()

        results = await self.vision.process_image(image_data, source=image_path)

        self.stats['sessions'].append({
            'type': 'image',
            'source': image_path,
            'neurons': results['neurons_created'],
            'objects': len(results.get('objects', [])),
            'texts': len(results.get('text', []))
        })
        self.stats['total_neurons'] += results['neurons_created']

        return results

    async def train_from_document(self, doc_path: str):
        """
        Режим 3: Обучение из документа
        """
        print(f"\n📄 ОБУЧЕНИЕ ИЗ ДОКУМЕНТА: {doc_path}")
        print("=" * 40)

        results = await self.docs.process_document(doc_path)

        self.stats['sessions'].append({
            'type': 'document',
            'source': doc_path,
            'format': results.get('type', 'unknown'),
            'neurons': results.get('neurons_created', 0)
        })
        self.stats['total_neurons'] += results.get('neurons_created', 0)

        return results

    async def train_from_audio(self, audio_path: str):
        """
        Режим 4: Обучение из аудио
        """
        print(f"\n🎤 ОБУЧЕНИЕ ИЗ АУДИО: {audio_path}")
        print("=" * 40)

        results = await self.audio.process_audio(audio_path)

        self.stats['sessions'].append({
            'type': 'audio',
            'source': audio_path,
            'neurons': results.get('neurons_created', 0),
            'duration': results.get('duration', 0)
        })
        self.stats['total_neurons'] += results.get('neurons_created', 0)

        return results

    async def train_batch(self, topics: list, depth: str = 'medium'):
        """
        Режим 5: Пакетное обучение
        """
        print(f"\n📦 ПАКЕТНОЕ ОБУЧЕНИЕ: {len(topics)} тем")
        print("=" * 40)

        results = await self.learner.parallel_batch_learn(topics, depth)

        total_neurons = sum(r.get('neurons_created', 0) for r in results)
        total_time = sum(r.get('time_elapsed', 0) for r in results)

        self.stats['sessions'].append({
            'type': 'batch',
            'topics': topics,
            'count': len(topics),
            'neurons': total_neurons,
            'time': total_time
        })
        self.stats['total_neurons'] += total_neurons
        self.stats['total_time'] += total_time

        return results

    async def train_recursive(self, topic: str, depth: int = 2):
        """
        Режим 6: Рекурсивное обучение
        """
        print(f"\n🔄 РЕКУРСИВНОЕ ОБУЧЕНИЕ: {topic} (глубина {depth})")
        print("=" * 40)

        result = await self.learner.recursive_learn(topic, depth)

        def count_neurons(node):
            total = node.get('neurons', 0)
            for child in node.get('children', []):
                total += count_neurons(child)
            return total

        total_neurons = count_neurons(result)

        self.stats['sessions'].append({
            'type': 'recursive',
            'topic': topic,
            'depth': depth,
            'neurons': total_neurons
        })
        self.stats['total_neurons'] += total_neurons

        return result

    def show_stats(self):
        """Показать статистику"""
        print("\n📊 ТЕКУЩАЯ СТАТИСТИКА МОЗГА")
        print("=" * 40)

        if self.brain:
            stats = self.brain.get_stats()
            print(f"🧠 Нейронов: {stats['neurons']}")
            print(f"🔗 Синапсов: {stats['synapses']}")
            print(f"💭 Мыслей: {stats['thoughts']}")
            print("\n📚 По категориям:")
            for cat, count in stats['categories'].items():
                print(f"   • {cat}: {count}")

        print(f"\n📈 Сессий обучения: {len(self.stats['sessions'])}")
        print(f"🎯 Всего создано нейронов: {self.stats['total_neurons']}")

    async def interactive_mode(self):
        """Интерактивный режим"""
        print("\n🎮 ИНТЕРАКТИВНЫЙ РЕЖИМ")
        print("=" * 40)
        print("Доступные команды:")
        print("  /internet <тема> [глубина] - обучение из интернета")
        print("  /image <путь> - обучение из изображения")
        print("  /doc <путь> - обучение из документа")
        print("  /audio <путь> - обучение из аудио")
        print("  /batch <тема1,тема2,...> - пакетное обучение")
        print("  /recursive <тема> [глубина] - рекурсивное обучение")
        print("  /stats - показать статистику")
        print("  /save [имя] - сохранить мозг")
        print("  /exit - выход")

        while True:
            try:
                cmd = input("\n> ").strip()

                if cmd == "/exit":
                    break

                elif cmd == "/stats":
                    self.show_stats()

                elif cmd.startswith("/save"):
                    parts = cmd.split()
                    filename = parts[1] if len(parts) > 1 else None
                    if filename:
                        self.brain.save(filename)
                    else:
                        filename = f"brain_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
                        self.brain.save(filename)

                elif cmd.startswith("/internet"):
                    parts = cmd[10:].strip().split()
                    if parts:
                        topic = parts[0]
                        depth = parts[1] if len(parts) > 1 else "medium"
                        await self.train_from_internet(topic, depth)
                    else:
                        print("❌ Укажите тему")

                elif cmd.startswith("/image"):
                    path = cmd[7:].strip()
                    if path and Path(path).exists():
                        await self.train_from_image(path)
                    else:
                        print(f"❌ Файл не найден: {path}")

                elif cmd.startswith("/doc"):
                    path = cmd[5:].strip()
                    if path and Path(path).exists():
                        await self.train_from_document(path)
                    else:
                        print(f"❌ Файл не найден: {path}")

                elif cmd.startswith("/audio"):
                    path = cmd[7:].strip()
                    if path and Path(path).exists():
                        await self.train_from_audio(path)
                    else:
                        print(f"❌ Файл не найден: {path}")

                elif cmd.startswith("/batch"):
                    topics_str = cmd[7:].strip()
                    if topics_str:
                        topics = [t.strip() for t in topics_str.split(',')]
                        await self.train_batch(topics)
                    else:
                        print("❌ Укажите темы через запятую")

                elif cmd.startswith("/recursive"):
                    parts = cmd[11:].strip().split()
                    if parts:
                        topic = parts[0]
                        depth = int(parts[1]) if len(parts) > 1 else 2
                        await self.train_recursive(topic, depth)
                    else:
                        print("❌ Укажите тему")

                else:
                    print("❌ Неизвестная команда")

            except KeyboardInterrupt:
                print("\n🛑 Прерывание...")
                break
            except Exception as e:
                print(f"❌ Ошибка: {e}")


async def main():
    """Главная функция"""
    parser = argparse.ArgumentParser(description='Тренер мультимодального мозга')
    parser.add_argument('--mode', '-m', choices=['interactive', 'internet', 'image', 'doc', 'audio', 'batch'],
                        default='interactive', help='Режим обучения')
    parser.add_argument('--topic', '-t', help='Тема для обучения')
    parser.add_argument('--depth', '-d', default='medium', choices=['fast', 'medium', 'deep'],
                        help='Глубина обучения')
    parser.add_argument('--path', '-p', help='Путь к файлу')
    parser.add_argument('--brain', '-b', help='Путь к сохраненному мозгу')
    parser.add_argument('--topics', nargs='+', help='Список тем для пакетного обучения')

    args = parser.parse_args()

    # Создаем оркестратор
    trainer = TrainingOrchestrator()
    await trainer.initialize(args.brain)

    try:
        if args.mode == 'interactive':
            await trainer.interactive_mode()

        elif args.mode == 'internet':
            if args.topic:
                await trainer.train_from_internet(args.topic, args.depth)
            else:
                print("❌ Укажите тему с --topic")

        elif args.mode == 'image':
            if args.path:
                await trainer.train_from_image(args.path)
            else:
                print("❌ Укажите путь к изображению с --path")

        elif args.mode == 'doc':
            if args.path:
                await trainer.train_from_document(args.path)
            else:
                print("❌ Укажите путь к документу с --path")

        elif args.mode == 'audio':
            if args.path:
                await trainer.train_from_audio(args.path)
            else:
                print("❌ Укажите путь к аудио с --path")

        elif args.mode == 'batch':
            if args.topics:
                await trainer.train_batch(args.topics, args.depth)
            else:
                print("❌ Укажите темы с --topics")

        # Показываем итоговую статистику
        trainer.show_stats()

    finally:
        await trainer.shutdown()


if __name__ == "__main__":
    asyncio.run(main())