import sys
import logging

level = logging.INFO
date_format = '%Y-%m-%d %H:%M:%S'

fmt = '[%(asctime)s] - CAD %(levelname)s - "%(message)s"'

formatter = logging.Formatter(fmt, date_format)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)

logger = logging.getLogger('cad')
logger.addHandler(handler)
logger.setLevel(level)
