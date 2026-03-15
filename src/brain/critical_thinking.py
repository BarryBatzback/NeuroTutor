# src/brain/critical_thinking.py
from typing import List, Dict
from datetime import datetime
import numpy as np


class CriticalThinking:
    """Модуль критического мышления"""

    def __init__(self, brain):
        self.brain = brain
        self.confidence_threshold = 0.7
        self.decision_history = []
        print("🧠 Модуль критического мышления инициализирован")

    def analyze_information(self, information: str, sources: List[Dict] = None) -> Dict:
        """Анализ информации"""
        analysis = {
            'information': information[:100],
            'confidence': 0.5,
            'contradictions': [],
            'verifications': [],
            'conclusion': '',
            'action': 'analyze_more'
        }

        found_neurons = self.brain.search_knowledge(information)

        for neuron in found_neurons:
            if self._is_contradictory(information, neuron.content):
                analysis['contradictions'].append({
                    'existing': neuron.content[:100],
                    'confidence': neuron.activation_level
                })
            else:
                analysis['verifications'].append({
                    'knowledge': neuron.content[:100],
                    'confidence': neuron.activation_level
                })

        if analysis['verifications']:
            analysis['confidence'] += min(0.3, len(analysis['verifications']) * 0.15)

        if analysis['contradictions']:
            analysis['confidence'] -= min(0.4, len(analysis['contradictions']) * 0.2)

        if sources:
            source_reliability = self._analyze_sources(sources)
            analysis['confidence'] = (analysis['confidence'] + source_reliability) / 2

        if analysis['contradictions']:
            analysis['conclusion'] = "Обнаружены противоречия"
        elif analysis['verifications']:
            analysis['conclusion'] = "Информация подтверждается"
            analysis['confidence'] = min(0.95, analysis['confidence'] + 0.1)
        else:
            analysis['conclusion'] = "Требуется проверка"

        analysis['action'] = self._determine_action(analysis)

        self.decision_history.append({
            'timestamp': datetime.now(),
            'information': information[:50],
            'confidence': analysis['confidence']
        })

        return analysis

    def _is_contradictory(self, text1: str, text2: str) -> bool:
        opposite_pairs = [
            ('притягивает', 'отталкивает'),
            ('да', 'нет'),
            ('верно', 'неверно')
        ]
        t1, t2 = text1.lower(), text2.lower()
        for w1, w2 in opposite_pairs:
            if (w1 in t1 and w2 in t2) or (w2 in t1 and w1 in t2):
                return True
        return False

    def _analyze_sources(self, sources: List[Dict]) -> float:
        if not sources:
            return 0.5
        scores = []
        for s in sources:
            score = 0.5
            if s.get('type') in ['academic', 'textbook']:
                score += 0.3
            scores.append(max(0, min(1, score)))
        return float(np.mean(scores))

    def _determine_action(self, analysis: Dict) -> str:
        confidence = analysis.get('confidence', 0.5)
        contradictions = analysis.get('contradictions', [])
        verifications = analysis.get('verifications', [])

        if confidence > 0.8 and not contradictions:
            return 'accept'
        elif confidence > 0.7 and verifications:
            return 'accept_with_caution'
        elif confidence < 0.3 or (contradictions and confidence < 0.6):
            return 'reject'
        elif confidence < 0.6:
            return 'verify_further'
        else:
            return 'consider'

    def question_assumptions(self, topic: str) -> List[Dict]:
        """Оспаривание предположений"""
        knowledge = self.brain.search_knowledge(topic)
        assumptions = []
        for neuron in knowledge:
            assumptions.append({
                'original': neuron.content[:100],
                'challenge': f"А точно ли {neuron.content.split()[0] if neuron.content.split() else 'это'}?",
                'alternatives': [
                    f"Возможно, {neuron.content} не совсем точно",
                    f"С другой стороны, это может быть ошибочным"
                ]
            })
        return assumptions

    def get_statistics(self) -> Dict:
        return {
            'total_analyses': len(self.decision_history),
            'average_confidence': float(
                np.mean([d['confidence'] for d in self.decision_history])) if self.decision_history else 0
        }