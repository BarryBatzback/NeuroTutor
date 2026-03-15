# src/knowledge/educational_loader.py
import asyncio
import aiohttp
from typing import List, Dict, Optional
from pathlib import Path
import json
import time
from datetime import datetime


class EducationalLoader:
    """
    Загрузчик учебных знаний по всем предметам
    Школа + Университет
    """

    def __init__(self, brain, multilingual, api_learner):
        self.brain = brain
        self.ml = multilingual
        self.api = api_learner

        # Школьные предметы (5-11 класс)
        self.school_subjects = {
            'mathematics': {
                'name_ru': 'Математика',
                'name_en': 'Mathematics',
                'grades': {
                    '5': ['дроби', 'проценты', 'уравнения', 'геометрия основы'],
                    '6': ['отрицательные числа', 'координаты', 'пропорции', 'круг'],
                    '7': ['алгебра начала', 'геометрия треугольник', 'функции'],
                    '8': ['квадратные уравнения', 'теорема пифагора', 'неравенства'],
                    '9': ['прогрессии', 'тригонометрия', 'вероятность', 'векторы'],
                    '10': ['производная', 'интегралы', 'логарифмы', 'стереометрия'],
                    '11': ['пределы', 'комплексные числа', 'матанализ', 'комбинаторика']
                }
            },
            'physics': {
                'name_ru': 'Физика',
                'name_en': 'Physics',
                'grades': {
                    '7': ['механика основы', 'плотность', 'давление', 'сила'],
                    '8': ['тепловые явления', 'электричество основы', 'оптика'],
                    '9': ['законы ньютона', 'колебания', 'волны', 'магнетизм'],
                    '10': ['молекулярная физика', 'термодинамика', 'электростатика'],
                    '11': ['электродинамика', 'квантовая физика', 'ядерная физика', 'относительность']
                }
            },
            'chemistry': {
                'name_ru': 'Химия',
                'name_en': 'Chemistry',
                'grades': {
                    '8': ['атомы', 'молекулы', 'химические реакции', 'периодическая таблица'],
                    '9': ['металлы', 'неметаллы', 'кислоты', 'основания'],
                    '10': ['органическая химия', 'углеводороды', 'спирты'],
                    '11': ['белки', 'жиры', 'углеводы', 'полимеры', 'биохимия']
                }
            },
            'biology': {
                'name_ru': 'Биология',
                'name_en': 'Biology',
                'grades': {
                    '6': ['клетка', 'растения', 'бактерии', 'грибы'],
                    '7': ['животные', 'эволюция', 'экология основы'],
                    '8': ['анатомия человека', 'физиология', 'здоровье'],
                    '9': ['генетика', 'размножение', 'наследственность'],
                    '10': ['цитология', 'биохимия', 'метаболизм'],
                    '11': ['молекулярная биология', 'биотехнологии', 'эволюция современная']
                }
            },
            'informatics': {
                'name_ru': 'Информатика',
                'name_en': 'Computer Science',
                'grades': {
                    '5': ['алгоритмы основы', 'компьютер устройство'],
                    '6': ['программы', 'файлы', 'интернет'],
                    '7': ['программирование scratch', 'логика'],
                    '8': ['python основы', 'алгоритмизация', 'данные'],
                    '9': ['базы данных', 'сети', 'безопасность'],
                    '10': ['объектно ориентированное программирование', 'классы'],
                    '11': ['искусственный интеллект', 'большие данные', 'машинное обучение']
                }
            }
        }

        # Университетские предметы
        self.university_subjects = {
            'higher_mathematics': {
                'name_ru': 'Высшая математика',
                'name_en': 'Higher Mathematics',
                'topics': [
                    'математический анализ',
                    'дифференциальные уравнения',
                    'интегральное исчисление',
                    'ряды',
                    'векторный анализ',
                    'тензорное исчисление',
                    'функциональный анализ',
                    'комплексный анализ',
                    'теория вероятностей',
                    'математическая статистика'
                ]
            },
            'geodesy': {
                'name_ru': 'Геодезия',
                'name_en': 'Geodesy',
                'topics': [
                    'геодезические системы координат',
                    'картографические проекции',
                    'gps технологии',
                    'лазерное сканирование',
                    'фотограмметрия',
                    'геодезические сети',
                    'нивелирование',
                    'теодолитная съемка',
                    'спутниковая геодезия',
                    'гравиметрия'
                ]
            },
            'construction': {
                'name_ru': 'Строительство',
                'name_en': 'Construction Engineering',
                'topics': [
                    'сопротивление материалов',
                    'строительные конструкции',
                    'строительные материалы',
                    'технология строительства',
                    'проектирование зданий',
                    'геотехническая инженерия',
                    'управление строительством',
                    'физика зданий',
                    'ремонт и реконструкция',
                    'устойчивое строительство'
                ]
            },
            'automotive': {
                'name_ru': 'Автомобилестроение',
                'name_en': 'Automotive Engineering',
                'topics': [
                    'динамика транспортных средств',
                    'проектирование двигателей',
                    'трансмиссионные системы',
                    'аэродинамика автомобилей',
                    'автомобильная электроника',
                    'альтернативные двигатели',
                    'безопасность автомобилей',
                    'производственные процессы',
                    'контроль качества',
                    'электромобили'
                ]
            }
        }

        print("📚 EducationalLoader инициализирован")
        print(f"   Школьных предметов: {len(self.school_subjects)}")
        print(f"   Университетских предметов: {len(self.university_subjects)}")

    # src/knowledge/educational_loader.py

    async def load_school_subject(self, subject_key: str, grade: str, topic: str) -> Dict:
        """Загрузка знаний по школьному предмету"""
        subject = self.school_subjects.get(subject_key)
        if not subject:
            return {'error': f'Предмет {subject_key} не найден'}

        print(f"\n📖 Загрузка: {subject['name_ru']} {grade} класс - {topic}")

        # Загружаем из Wikipedia
        wiki_stats = self.api.learn_from_wikipedia(topic, language='ru', depth=1)

        # Создаем итоговый нейрон
        knowledge_text = f"{subject['name_ru']} {grade} класс: {topic}. "
        knowledge_text += f"Это важная тема школьной программы по {subject['name_ru']}."

        # ✅ ИСПРАВЛЕНО: не передаем self.brain
        neurons = self.ml.create_multilingual_neuron(
            knowledge_text,
            category=f"School_{subject_key}_Grade{grade}"
        )

        # Добавляем метаданные
        for neuron in neurons.values():
            self.brain.graph.nodes[neuron.uid]['subject'] = subject_key
            self.brain.graph.nodes[neuron.uid]['grade'] = grade
            self.brain.graph.nodes[neuron.uid]['topic'] = topic
            self.brain.graph.nodes[neuron.uid]['level'] = 'school'

        return {
            'subject': subject_key,
            'grade': grade,
            'topic': topic,
            'neurons_created': len(neurons),
            'wiki': wiki_stats
        }

    async def load_university_subject(self, subject_key: str, topic: str) -> Dict:
        """Загрузка знаний по университетскому предмету"""
        subject = self.university_subjects.get(subject_key)
        if not subject:
            return {'error': f'Предмет {subject_key} не найден'}

        print(f"\n🎓 Загрузка: {subject['name_ru']} - {topic}")

        # Загружаем из научных источников
        wiki_stats = self.api.learn_from_wikipedia(topic, language='ru', depth=2)
        arxiv_stats = self.api.learn_from_arxiv(topic, max_results=2)

        # Создаем итоговый нейрон
        knowledge_text = f"{subject['name_ru']}: {topic}. "
        knowledge_text += f"Это тема университетского уровня по {subject['name_ru']}."

        # ✅ ИСПРАВЛЕНО: не передаем self.brain
        neurons = self.ml.create_multilingual_neuron(
            knowledge_text,
            category=f"University_{subject_key}"
        )

        # Добавляем метаданные
        for neuron in neurons.values():
            self.brain.graph.nodes[neuron.uid]['subject'] = subject_key
            self.brain.graph.nodes[neuron.uid]['topic'] = topic
            self.brain.graph.nodes[neuron.uid]['level'] = 'university'

        return {
            'subject': subject_key,
            'topic': topic,
            'neurons_created': len(neurons),
            'wiki': wiki_stats,
            'arxiv': arxiv_stats
        }

    async def load_all_school_mathematics(self):
        """Загрузить всю школьную математику"""
        print("\n" + "=" * 70)
        print("📐 ЗАГРУЗКА ШКОЛЬНОЙ МАТЕМАТИКИ (5-11 класс)")
        print("=" * 70)

        results = []
        math = self.school_subjects['mathematics']

        for grade, topics in math['grades'].items():
            for topic in topics:
                result = await self.load_school_subject('mathematics', grade, topic)
                results.append(result)
                await asyncio.sleep(0.5)

        total_neurons = sum(r.get('neurons_created', 0) for r in results)
        print(f"\n✅ Загружено: {len(results)} тем, {total_neurons} нейронов")
        return results

    async def load_all_school_physics(self):
        """Загрузить всю школьную физику"""
        print("\n" + "=" * 70)
        print("⚡ ЗАГРУЗКА ШКОЛЬНОЙ ФИЗИКИ (7-11 класс)")
        print("=" * 70)

        results = []
        physics = self.school_subjects['physics']

        for grade, topics in physics['grades'].items():
            for topic in topics:
                result = await self.load_school_subject('physics', grade, topic)
                results.append(result)
                await asyncio.sleep(0.5)

        total_neurons = sum(r.get('neurons_created', 0) for r in results)
        print(f"\n✅ Загружено: {len(results)} тем, {total_neurons} нейронов")
        return results

    async def load_all_university_higher_math(self):
        """Загрузить всю высшую математику"""
        print("\n" + "=" * 70)
        print("📊 ЗАГРУЗКА ВЫСШЕЙ МАТЕМАТИКИ")
        print("=" * 70)

        results = []
        higher_math = self.university_subjects['higher_mathematics']

        for topic in higher_math['topics']:
            result = await self.load_university_subject('higher_mathematics', topic)
            results.append(result)
            await asyncio.sleep(0.5)

        total_neurons = sum(r.get('neurons_created', 0) for r in results)
        print(f"\n✅ Загружено: {len(results)} тем, {total_neurons} нейронов")
        return results

    async def load_all_university_geodesy(self):
        """Загрузить всю геодезию"""
        print("\n" + "=" * 70)
        print("🗺️ ЗАГРУЗКА ГЕОДЕЗИИ")
        print("=" * 70)

        results = []
        geodesy = self.university_subjects['geodesy']

        for topic in geodesy['topics']:
            result = await self.load_university_subject('geodesy', topic)
            results.append(result)
            await asyncio.sleep(0.5)

        total_neurons = sum(r.get('neurons_created', 0) for r in results)
        print(f"\n✅ Загружено: {len(results)} тем, {total_neurons} нейронов")
        return results

    async def load_full_curriculum(self, subjects: List[str] = None):
        """Загрузить полную учебную программу"""
        print("\n" + "=" * 70)
        print("🎓 ЗАГРУЗКА ПОЛНОЙ УЧЕБНОЙ ПРОГРАММЫ")
        print("=" * 70)

        start_time = time.time()
        all_results = []

        # Школьные предметы
        if subjects is None or 'school_math' in subjects:
            results = await self.load_all_school_mathematics()
            all_results.extend(results)

        if subjects is None or 'school_physics' in subjects:
            results = await self.load_all_school_physics()
            all_results.extend(results)

        # Университетские предметы
        if subjects is None or 'higher_math' in subjects:
            results = await self.load_all_university_higher_math()
            all_results.extend(results)

        if subjects is None or 'geodesy' in subjects:
            results = await self.load_all_university_geodesy()
            all_results.extend(results)

        elapsed = time.time() - start_time
        total_neurons = sum(r.get('neurons_created', 0) for r in all_results)

        print("\n" + "=" * 70)
        print("📊 ИТОГИ ЗАГРУЗКИ УЧЕБНОЙ ПРОГРАММЫ:")
        print(f"   Загружено тем: {len(all_results)}")
        print(f"   Создано нейронов: {total_neurons}")
        print(f"   Время загрузки: {elapsed:.2f} сек ({elapsed / 60:.2f} мин)")
        print("=" * 70)

        # Сохраняем мозг
        self.brain.save("educational_brain.pkl")

        return all_results

    def get_educational_stats(self) -> Dict:
        """Статистика образовательных знаний"""
        school_count = 0
        university_count = 0

        for node_id, data in self.brain.graph.nodes(data=True):
            level = data.get('level', '')
            if level == 'school':
                school_count += 1
            elif level == 'university':
                university_count += 1

        return {
            'school_neurons': school_count,
            'university_neurons': university_count,
            'total_educational': school_count + university_count,
            'school_subjects': len(self.school_subjects),
            'university_subjects': len(self.university_subjects)
        }