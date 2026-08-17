class ShortTermMemory:

    def __init__(self, max_items=5):

        self.max_items = max_items
        self.history = []

    def add_conversation(self, role, message):

        self.history.append({
            "role": role,
            "message": message
        })

        self._evict_if_needed()

    def _evict_if_needed(self):

        if len(self.history) > self.max_items:

            self.history = self.history[-self.max_items:]

    def get_conversation_history(self):

        return self.history