import os, logging, errno
from logging import handlers


def init_logger(
    filename=None,
    level=logging.INFO,
    frmt=None,
    maxbytes=104857600,
    backupcount=5,
):
    log = logging.getLogger(filename)
    log.setLevel(level)

    if frmt is None:
        frmt = "%(asctime)s %(filename)s:%(lineno)s %(levelname)s: %(process)d: %(message)s"

    formatter = logging.Formatter(frmt)
    try:
        handler = handlers.RotatingFileHandler(
            filename, maxBytes=maxbytes, backupCount=backupcount
        )
        log.addHandler(handler)
        handler.setFormatter(formatter)
    except:
        pass

    return log


logger = init_logger(
    filename="logs.log",
    level=logging.DEBUG,
)
