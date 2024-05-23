import logging


def init_logger(pathname: str, filename: str):
    logger = logging.getLogger(pathname)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s:%(lineno)s :: %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(filename=filename, mode="w", encoding="utf-8"), logging.StreamHandler()],
    )
    logger.info("Initialization logger")
