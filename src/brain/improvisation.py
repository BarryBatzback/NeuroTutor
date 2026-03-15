# src/brain/improvisation.py
import random
from typing import List, Dict
import numpy as np


class Improvisation:
    """Модуль импровизации"""

    def __init__(self, brain, critical_thinking):
        self.brain = brain
        self.critical = critical_thinking
        self.creativity_level = 0.7
        self.improvisation_history = []
        print("🎭 Модуль импровизации инициализирован")

    def solve_creatively(self, problem: str, domain: str = None) -> Dict:
        """Творческое решение"""
        analysis = self._analyze_problem(problem)
        analogies = self._find_analogies(analysis, domain)
        solution = self._combine_ideas(analogies)

        verification = self.critical.analyze_information(
            solution,
            [{'type': 'creative_solution', 'authority': 0.5, 'year': 2024}]
        )

        result = {
            'problem': problem,
            'analysis': analysis,
            'analogies': analogies,
            'solution': solution,
            'confidence': verification['confidence']
        }

        self.improvisation_history.append(result)
        return result

    def _analyze_problem(self, problem: str) -> Dict:
        related = self.brain.search_knowledge(problem)
        words = [w for w in problem.lower().split() if len(w) > 3]

        type_indicators = {
            'technical': ['как сделать', 'как построить', 'формула'],
            'scientific': ['почему', 'объясни', 'причина'],
            'creative': ['придумай', 'создай', 'новый']
        }

        problem_type = 'general'
        for ptype, indicators in type_indicators.items():
            if any(ind in problem for ind in indicators):
                problem_type = ptype
                break

        return {
            'keywords': words,
            'related_knowledge': len(related),
            'problem_type': problem_type,
            'complexity': min(1.0, len(words) / 5)
        }

    def _find_analogies(self, problem_analysis: Dict, domain: str = None) -> List[Dict]:
        analogy_library = {
            'biology': ['нейронные сети как мозг', 'эволюция как оптимизация'],
            'physics': ['гравитация как притяжение', 'резонанс как созвучие'],
            'engineering': ['обратная связь как контроль', 'усилитель как развитие'],
            'nature': ['дерево как иерархия', 'река как поток']
        }

        sources = list(analogy_library.keys()) if not domain else [domain]
        selected = random.sample(sources, min(3, len(sources)))

        analogies = []
        for source in selected:
            if source in analogy_library:
                analogies.append({
                    'source': source,
                    'analogy': random.choice(analogy_library[source]),
                    'relevance': random.uniform(0.5, 0.9)
                })

        return analogies

    def _combine_ideas(self, analogies: List[Dict]) -> str:
        if not analogies:
            return "Не найдено аналогий"

        templates = [
            f"Предлагаю объединить {analogies[0]['source']} ({analogies[0]['analogy']}) "
            f"с {analogies[1]['source'] if len(analogies) > 1 else 'другими областями'}",
            f"Вдохновляясь {analogies[0]['analogy']}, можно создать инновационное решение",
            f"Решение основано на метафоре: {analogies[0]['analogy']}"
        ]

        return random.choice(templates)

    def brainstorm(self, topic: str, num_ideas: int = 5) -> List[str]:
        """Мозговой штурм"""
        templates = [
            f"А что если {topic} использовать по-другому?",
            f"Можно ли объединить {topic} с чем-то ещё?",
            f"Как бы {topic} выглядело в будущем?",
            f"Как упростить {topic}?",
            f"Где ещё можно применить {topic}?"
        ]

        ideas = []
        for i in range(num_ideas):
            ideas.append(random.choice(templates).replace(topic, f"'{topic}'"))

        return ideas

    def get_statistics(self) -> Dict:
        return {
            'total_improvisations': len(self.improvisation_history),
            'average_confidence': float(
                np.mean([i['confidence'] for i in self.improvisation_history])) if self.improvisation_history else 0,
            'creativity_level': self.creativity_level
        }