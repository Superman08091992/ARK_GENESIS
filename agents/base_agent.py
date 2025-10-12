class BaseAgent:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.logger = None  # Should be set externally, or in subclass

    async def process(self, input_data):
        raise NotImplementedError("Subclasses must implement process()")