import logging


class App:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def run(self):
        self.logger.info("App started")
        print("Running main app logic...")
        self.logger.info("App finished")
