# cli_search_app/cli_worker.py

import logging
import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from search_engines import (
    get_google_search_results,
    get_bing_search_results,
    get_baidu_search_results
)
from utils import save_results_to_txt
import threading

class CLIWorker:
    """
    CLI 工作类，用于执行搜索任务。
    """
    def __init__(self, queries, num_results=5, engine='Google', custom_question=None):
        """
        初始化 CLIWorker。

        参数:
        - queries: 搜索关键词列表。
        - num_results: 每个关键词的搜索结果数量。
        - engine: 搜索引擎（'Google', 'Bing', '百度'）。
        - custom_question: 自定义问题，仅在进阶模式下使用。
        """
        self.queries = queries
        self.num_results = num_results
        self.engine = engine
        self.custom_question = custom_question
        self._is_running = False
        self._thread = None
        self._lock = threading.Lock()
        self.results = []
        self.filename = ''

    def start(self):
        """
        启动搜索任务。
        """
        with self._lock:
            if not self._is_running:
                self._is_running = True
                self._thread = threading.Thread(target=self.run)
                self._thread.start()
                logging.info("CLIWorker 已启动。")
            else:
                logging.warning("CLIWorker 已在运行中。")

    def run(self):
        """
        执行搜索任务。
        """
        try:
            all_results = []
            logging.info(
                f"CLIWorker 开始执行搜索任务，关键词: {self.queries}, "
                f"结果数量: {self.num_results}, 搜索引擎: {self.engine}"
            )
            for query in self.queries:
                if not self._is_running:
                    logging.info("搜索任务被中断。")
                    break
                if self.engine == 'Google':
                    results = get_google_search_results(
                        query, self.num_results
                    )
                elif self.engine == 'Bing':
                    results = get_bing_search_results(
                        query, self.num_results
                    )
                elif self.engine == '百度':
                    results = get_baidu_search_results(
                        query, self.num_results
                    )
                else:
                    raise ValueError("不支持的搜索引擎。")
                # 添加查询词到结果中
                for result in results:
                    result['query'] = query
                all_results.append(results)

            if not self._is_running:
                logging.info("搜索任务已被用户中断，停止后续操作。")
                return

            # 展平结果列表
            flat_results = [item for sublist in all_results for item in sublist]

            # 保存结果到文件
            self.filename = save_results_to_txt(
                flat_results,
                ', '.join(self.queries),
                engine=self.engine,
                custom_question=self.custom_question
            )
            self.results = flat_results
            logging.info("CLIWorker 搜索任务完成。")
        except Exception as e:
            logging.error(f"CLIWorker 搜索任务失败：{e}")
        finally:
            with self._lock:
                self._is_running = False

    def stop(self):
        """
        停止搜索任务。
        """
        with self._lock:
            if self._is_running:
                self._is_running = False
                logging.info("CLIWorker 已收到停止信号。")
            else:
                logging.warning("CLIWorker 未在运行中。")

    def wait_until_finished(self):
        """
        等待搜索任务完成。
        """
        if self._thread:
            self._thread.join()
            logging.info("CLIWorker 线程已完成。")
