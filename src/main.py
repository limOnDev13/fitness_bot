import logging
import logging.config

from config.config import load_config
from config.log_config import dict_config


logging.config.dictConfig(dict_config)
logger = logging.getLogger("main")
