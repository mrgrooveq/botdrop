# ============================================
# data.py — BotData e persistência
# ============================================

import json
import os

DATA_FILE = 'bot_data.json'

class BotData:
    def __init__(self):
        self.last_drop_time = None
        self.current_question = None
        self.current_answers = []
        self.drop_active = False
        self.drop_channel_id = None
        self.winners = {}
        self.answered_users = set()
        self.drops_paused = False
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
                    self.last_drop_time = data.get('last_drop_time')
                    self.winners = data.get('winners', {})
                    self.drops_paused = data.get('drops_paused', False)
            except:
                pass

    def save_data(self):
        with open(DATA_FILE, 'w') as f:
            json.dump({
                'last_drop_time': self.last_drop_time,
                'winners': self.winners,
                'drops_paused': self.drops_paused,
            }, f)

# Instância global compartilhada entre os módulos
bot_data = BotData()