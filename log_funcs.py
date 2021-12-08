import logging
import sys
import os

FORMAT = """\
LOG:
    asctime: %(asctime)s
    filename: %(filename)s
    funcName: %(funcName)s
    levelname: %(levelname)s
    lineno: %(lineno)d
    message: %(message)s
-------------
"""

def format_exception():
    """Create format for logger out of exception e.
    """
    exc_type, exc_obj, exc_tb = sys.exc_info()
    filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    lineno = exc_tb.tb_lineno
    print(type(filename), type(lineno))

    return f"""\
LOG:
    asctime: %(asctime)s
    filename: {filename}
    levelname: %(levelname)s
    lineno: {str(lineno)}
    message: %(message)s
-------------
"""

def log_error(e):
    """Log e into 'errors.log'
    """
    logging.basicConfig(filename='errors.log', format=format_exception())

    logger = logging.getLogger(__name__)  # or, try changing this to a string
    logger.setLevel(logging.WARNING)

    logging.error(e)

def log_message(message):
    """Log message (string) into 'errors.log'
    """
    logging.basicConfig(filename='errors.log', level=logging.INFO, format=format_exception())

    logger = logging.getLogger(__name__)  # or, try changing this to a string
    logger.setLevel(logging.WARNING)

    logging.info(message)
