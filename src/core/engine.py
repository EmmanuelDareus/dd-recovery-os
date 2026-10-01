class CoreEngine:
    def __init__(self, name: str = "CoreEngine"):
        self.name = name
        self.is_running = False

    def start(self):
        self.is_running = True
        return f"{self.name} started successfully."

    def stop(self):
        self.is_running = False
        return f"{self.name} stopped."

    def process(self, data: str):
        if not self.is_running:
            raise RuntimeError(f"{self.name} is not running!")
        return {
            "input": data,
            "processed": data[::-1],
            "engine": self.name
        }
