from log import get_logger
from config import *

logger = get_logger(__name__)

# Initialize the gunicorn variables
bind = f"{HOST}:{PORT}"
timeout = 240
workers = 2
threads = 4


# noinspection PyUnusedLocal
def post_fork(server, worker):
    """
    This method is to initialize all workers.
    :return: None
    """
    logger.info("Worker Started")
