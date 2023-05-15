import logging


_LOGGER: logging.Logger = logging.getLogger('root')
_IS_DEBUG: bool = False


class ServiceLogger:
    def __init__(
            self,
            sv_name: str = "root",
            is_debug: bool = False
    ):
        logging.basicConfig(
            level=logging.DEBUG if is_debug else logging.INFO,
            format="%(asctime)s  %(name)s  [%(levelname)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            )
        global _LOGGER
        _LOGGER = logging.getLogger(sv_name)
        self.lg = logging.getLogger(sv_name)


def configure(sv_name: str = "root", is_debug: bool = False):
    logging.basicConfig(
        level=logging.DEBUG if is_debug else logging.INFO,
        format="%(asctime)s  %(name)s  [%(levelname)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        )
    global _LOGGER
    _LOGGER = logging.getLogger(sv_name)


def info(msg: str):
    global _LOGGER
    _LOGGER.info(msg)


def debug(msg: str):
    global _LOGGER
    _LOGGER.debug(msg)


def warning(msg: str):
    global _LOGGER
    _LOGGER.warning(msg)


def fatal(msg: str):
    global _LOGGER
    _LOGGER.fatal(msg)
