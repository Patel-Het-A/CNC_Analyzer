class Logger:

    @staticmethod
    def log(message):
        print(f"[INFO] {message}")

    @staticmethod
    def warning(message):
        print(f"[WARNING] {message}")

    @staticmethod
    def error(message):
        print(f"[ERROR] {message}")