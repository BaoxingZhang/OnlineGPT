# cli_search_app/logging_setup.py
# 负责日志配置。

import logging
import sys

def setup_logging(log_level=logging.INFO, log_file='cli_search_app.log'):
    """
    设置日志记录，输出到控制台和日志文件。

    参数:
    - log_level: 日志级别，默认为 logging.INFO
    - log_file: 日志文件路径，默认为 'cli_search_app.log'
    """
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # 防止重复添加处理器
    if not logger.handlers:
        # 创建控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)

        # 创建文件处理器
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(log_level)
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)

        # 添加处理器到logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        logging.info(f"日志记录已设置，输出到控制台和文件: {log_file}")