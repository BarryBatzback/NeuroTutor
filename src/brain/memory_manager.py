# src/brain/memory_manager.py

import pickle
import json
import os
import time
from pathlib import Path
from datetime import datetime


class MemoryManager:
    """
    Класс для сохранения и загрузки состояния мозга
    Управляет долговременной памятью
    """

    def __init__(self, save_dir: str = "data/models"):
        """
        Инициализация менеджера памяти

        Args:
            save_dir: директория для сохранения
        """
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir = self.save_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)

    def save_brain(self, cortex, filename: str = None) -> str:
        """
        Сохранить состояние мозга в файл

        Args:
            cortex: объект Cortex для сохранения
            filename: имя файла (если None, создается автоматически)

        Returns:
            str: путь к сохраненному файлу
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"brain_{timestamp}.pkl"

        # Убедимся, что у filename нет расширения .pkl дважды
        if not filename.endswith('.pkl'):
            filename += '.pkl'

        filepath = self.save_dir / filename

        # Подготавливаем данные для сохранения
        save_data = {
            'graph': cortex.graph,
            'config': {
                'learning_rate': cortex.learning_rate,
                'forgetting_rate': cortex.forgetting_rate,
                'hebbian_factor': cortex.hebbian_factor
            },
            'stats': {
                'neuron_count': cortex.graph.number_of_nodes(),
                'synapse_count': cortex.graph.number_of_edges(),
                'thought_count': cortex.thought_count
            },
            'timestamp': time.time(),
            'version': '1.0'
        }

        # Сохраняем основной файл
        with open(filepath, 'wb') as f:
            pickle.dump(save_data, f)

        # Создаем резервную копию
        backup_path = self.backup_dir / f"backup_{filename}"
        with open(backup_path, 'wb') as f:
            pickle.dump(save_data, f)

        print(f"💾 Мозг сохранен: {filepath}")
        print(f"   Нейронов: {save_data['stats']['neuron_count']}, Синапсов: {save_data['stats']['synapse_count']}")
        print(f"   Резервная копия: {backup_path}")

        return str(filepath)

    def load_brain(self, filepath: str = None):
        """
        Загрузить состояние мозга из файла

        Args:
            filepath: путь к файлу (если None, загружается последний)

        Returns:
            dict: загруженные данные или None если файл не найден
        """
        if filepath is None:
            # Ищем самый последний файл
            files = list(self.save_dir.glob("brain_*.pkl"))
            if not files:
                # Пробуем поискать в backups
                files = list(self.backup_dir.glob("backup_brain_*.pkl"))

            if not files:
                print("📂 Нет сохраненных файлов мозга")
                return None

            # Берем самый новый файл
            filepath = max(files, key=os.path.getctime)
            print(f"📂 Найден последний файл: {filepath.name}")

        filepath = Path(filepath)
        if not filepath.exists():
            print(f"❌ Файл не найден: {filepath}")
            return None

        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)

            print(f"📂 Мозг загружен: {filepath}")
            print(f"   Нейронов: {data.get('stats', {}).get('neuron_count', '?')}")
            print(f"   Синапсов: {data.get('stats', {}).get('synapse_count', '?')}")
            print(f"   Версия: {data.get('version', 'unknown')}")

            return data

        except Exception as e:
            print(f"❌ Ошибка загрузки: {e}")
            return None

    def export_knowledge(self, cortex, format: str = 'json', filepath: str = None):
        """
        Экспортировать знания в читаемый формат

        Args:
            cortex: объект Cortex
            format: формат экспорта ('json' или 'txt')
            filepath: путь для сохранения
        """
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = self.save_dir / f"knowledge_export_{timestamp}.{format}"

        # Собираем все знания
        knowledge = []
        for node_id, node_data in cortex.graph.nodes(data=True):
            if 'neuron' in node_data:
                neuron = node_data['neuron']

                # Собираем связи этого нейрона
                connections = []
                for successor in cortex.graph.successors(node_id):
                    edge_data = cortex.graph.get_edge_data(node_id, successor)
                    if edge_data and 'synapse' in edge_data:
                        synapse = edge_data['synapse']
                        post_neuron = cortex.graph.nodes[successor]['neuron']
                        connections.append({
                            'to': post_neuron.content[:50],
                            'weight': synapse.weight
                        })

                knowledge.append({
                    'id': neuron.uid,
                    'content': neuron.content,
                    'category': neuron.category,
                    'firing_count': neuron.firing_count,
                    'created': time.ctime(neuron.created_at),
                    'connections': connections[:5]  # Топ-5 связей
                })

        if format == 'json':
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(knowledge, f, ensure_ascii=False, indent=2)
        else:
            with open(filepath, 'w', encoding='utf-8') as f:
                for k in knowledge:
                    f.write(f"\n{'=' * 50}\n")
                    f.write(f"[{k['category']}] {k['content']}\n")
                    f.write(f"ID: {k['id']}\n")
                    f.write(f"Срабатываний: {k['firing_count']}\n")
                    if k['connections']:
                        f.write("Связи:\n")
                        for conn in k['connections']:
                            f.write(f"  → {conn['to']} (вес: {conn['weight']:.2f})\n")

        print(f"📤 Экспортировано {len(knowledge)} знаний в {filepath}")

    def list_saved_brains(self) -> list:
        """
        Список всех сохраненных состояний мозга

        Returns:
            list: список файлов с датами
        """
        files = list(self.save_dir.glob("brain_*.pkl"))
        result = []

        for f in sorted(files, key=os.path.getmtime, reverse=True):
            stat = f.stat()
            size_kb = stat.st_size / 1024
            result.append({
                'filename': f.name,
                'size': f"{size_kb:.1f} KB",
                'modified': datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            })

        return result

    def cleanup_old_backups(self, keep_last: int = 5):
        """
        Очистка старых резервных копий

        Args:
            keep_last: сколько последних копий оставить
        """
        backups = list(self.backup_dir.glob("backup_brain_*.pkl"))
        backups.sort(key=os.path.getmtime, reverse=True)

        # Удаляем старые, оставляя только keep_last
        for old_backup in backups[keep_last:]:
            old_backup.unlink()
            print(f"🗑 Удалена старая резервная копия: {old_backup.name}")

    def get_brain_info(self, filepath: str) -> dict:
        """
        Получить информацию о сохраненном мозге без загрузки

        Args:
            filepath: путь к файлу

        Returns:
            dict: информация о мозге
        """
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)

            file_stat = Path(filepath).stat()

            return {
                'filename': Path(filepath).name,
                'size': f"{file_stat.st_size / 1024:.1f} KB",
                'created': datetime.fromtimestamp(file_stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
                'neurons': data.get('stats', {}).get('neuron_count', '?'),
                'synapses': data.get('stats', {}).get('synapse_count', '?'),
                'version': data.get('version', 'unknown')
            }
        except Exception as e:
            return {'error': str(e)}