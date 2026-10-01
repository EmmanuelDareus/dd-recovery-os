"""
Core Engine Module
Handles the primary business logic and operational loop for the application.
"""

class CoreEngine:
    def __init__(self, name: str = "CreatorOS-Engine"):
        self.name = name
        self.is_running = False

    def start(self):
        """Initializes and starts the core execution loop."""
        self.is_running = True
        print(f"[{self.name}] Engine initialized and running successfully.")

    def process(self, data: any) -> any:
        """Process incoming tasks or data."""
        if not self.is_running:
            raise RuntimeError("Engine is not running. Call start() first.")
        
        # TODO: Implement core data processing logic here
        print(f"[{self.name}] Processing data: {data}")
        return {"status": "success", "processed_data": data}

    def stop(self):
        """Stops the core execution loop gracefully."""
        self.is_running = False
        print(f"[{self.name}] Engine shut down safely.")

if __name__ == "__main__":
    # Test the engine directly if run as a script
    engine = CoreEngine()
    engine.start()
    engine.process("Sample Test Payload")
    engine.stop()