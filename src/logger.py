import logging
import time

logger = logging.getLogger("mysql.connector")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Log to console
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

# Also log to a file
file_handler = logging.FileHandler(f"/usr/local/app/logs/cpy-{time.time()}.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler) 
