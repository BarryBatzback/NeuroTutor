class CriticalMind:
    """Модуль критического мышления"""

    def analyze_information(self, information: str, sources: List[Dict] = None) -> Dict:
        """
        Анализирует информацию на достоверность

        Args:
            information: анализируемая информация
            sources: источники информации

        Returns:
            Dict: результат анализа
        """
        analysis = {
            'information': information[:100],
            'confidence': 0.5,
            'contradictions': [],
            'verifications': [],
            'conclusion': '',
            'action': 'analyze_more'
        }

        # Шаг 1: Разбиваем информацию на ключевые слова
        keywords = information.lower().split()

        # Шаг 2: Ищем в мозге похожие знания
        found_neurons = self.brain.search_knowledge(information)
        print(f"DEBUG: Ищем: '{information[:50]}...'")
        print(f"DEBUG: Найдено нейронов: {len(found_neurons)}")
        if found_neurons:
            for n in found_neurons:
                print(f"DEBUG:   • {n.content[:50]}...")

        if found_neurons:
            # Проверяем каждое найденное знание
            for neuron in found_neurons:
                # Простая проверка на противоречие
                if self.is_contradictory(information, neuron.content):
                    analysis['contradictions'].append({
                        'existing': neuron.content[:100],
                        'confidence': neuron.activation_level
                    })
                else:
                    analysis['verifications'].append({
                        'knowledge': neuron.content[:100],
                        'confidence': neuron.activation_level
                    })

        # Шаг 3: Корректируем уверенность на основе подтверждений/противоречий
        if analysis['verifications']:
            # Чем больше подтверждений, тем выше уверенность
            verification_boost = min(0.3, len(analysis['verifications']) * 0.15)
            analysis['confidence'] += verification_boost

        if analysis['contradictions']:
            # Чем больше противоречий, тем ниже уверенность
            contradiction_penalty = min(0.4, len(analysis['contradictions']) * 0.2)
            analysis['confidence'] -= contradiction_penalty

        # Шаг 4: Анализ источников (если есть)
        if sources:
            source_reliability = self.analyze_sources(sources)
            analysis['source_reliability'] = source_reliability
            analysis['confidence'] = (analysis['confidence'] + source_reliability) / 2

        # Шаг 5: Поиск логических ошибок
        fallacies = self.detect_logical_fallacies(information)
        if fallacies:
            analysis['fallacies'] = fallacies
            analysis['confidence'] -= len(fallacies) * 0.15

        # Шаг 6: Формируем вывод
        if analysis['contradictions']:
            analysis['conclusion'] = "Обнаружены противоречия с существующими знаниями"
        elif analysis['verifications']:
            analysis['conclusion'] = "Информация подтверждается существующими знаниями"
            # Если есть подтверждения, повышаем уверенность еще
            analysis['confidence'] = min(0.95, analysis['confidence'] + 0.1)
        elif analysis.get('source_reliability', 0) > 0.7:
            analysis['conclusion'] = "Источники надежны, но информация новая"
        else:
            analysis['conclusion'] = "Требуется дополнительная проверка"

        # Шаг 7: Определяем действие
        analysis['action'] = self.determine_action(analysis)

        # Сохраняем в историю
        self.decision_history.append({
            'timestamp': datetime.now(),
            'information': information[:50],
            'confidence': analysis['confidence'],
            'conclusion': analysis['conclusion']
        })

        return analysis

    def question_assumptions(self, topic: str) -> List[Dict]:
        """
        Ставит под сомнение существующие знания по теме
        """
        # Используем search_knowledge вместо think
        knowledge = self.brain.search_knowledge(topic)

        print(f"DEBUG: question_assumptions для '{topic}' нашла {len(knowledge)} нейронов")

        assumptions = []

        for neuron in knowledge:
            # Генерируем альтернативы
            alternatives = self.generate_alternatives(neuron.content)

            first_word = neuron.content.split()[0] if neuron.content.split() else 'это'

            assumptions.append({
                'original': neuron.content[:100],
                'alternatives': alternatives,
                'challenge': f"А точно ли {first_word}?",
                'verification_needed': True
            })

        return assumptions