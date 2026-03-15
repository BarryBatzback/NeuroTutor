class SituationalAwareness:
    """Понимание контекста и ситуации"""

    def __init__(self):
        self.context = {
            'time': None,
            'place': None,
            'user': None,
            'history': [],
            'mood': None,
            'urgency': None
        }

    def analyze_situation(self, user_input):
        """Анализирует текущую ситуацию"""

        # Определяем контекст
        self.context['time'] = self.get_time_context()
        self.context['user'] = self.identify_user(user_input)
        self.context['history'] = self.get_recent_history()

        # Анализируем настроение пользователя
        self.context['mood'] = self.analyze_mood(user_input)

        # Определяем срочность
        self.context['urgency'] = self.check_urgency(user_input)

        # Адаптируем ответ под ситуацию
        return self.adapt_response(self.context)

    def adapt_response(self, context):
        """Адаптирует ответ под ситуацию"""

        if context['urgency'] > 0.8:
            return {
                'style': 'concise',
                'length': 'short',
                'tone': 'direct'
            }
        elif context['mood'] < 0.3:  # Плохое настроение
            return {
                'style': 'supportive',
                'length': 'medium',
                'tone': 'empathetic'
            }
        elif context['time'] == 'night':
            return {
                'style': 'calm',
                'length': 'short',
                'tone': 'gentle'
            }
        else:
            return {
                'style': 'normal',
                'length': 'detailed',
                'tone': 'neutral'
            }