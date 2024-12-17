# cli_search_app/cli_app.py
# 主启动文件，负责执行搜索任务。    

import sys
import logging
import os
from cli_worker import CLIWorker
from utils import save_results_to_txt, generate_txt_content
from language_manager import LanguageManager
from logging_setup import setup_logging
from argument_parser import parse_arguments

def main():
    """
    主函数，执行搜索任务。
    """
    # 设置日志记录
    setup_logging()

    # 解析命令行参数
    args = parse_arguments()

    # 初始化语言管理器
    language_manager = LanguageManager()
    language_manager.set_language(args.language)
    logging.info(f"当前语言设置为: {'English' if args.language == 'en' else '中文'}")

    # 获取搜索关键词
    if args.keywords:
        queries = args.keywords
    else:
        # 交互式输入关键词
        try:
            input_keywords = input(language_manager.tr('请输入搜索关键词，多个关键词用空格分隔: ')).strip()
            if not input_keywords:
                logging.error(language_manager.tr('未提供搜索关键词。'))
                print(language_manager.tr('错误: 未提供搜索关键词。'))
                sys.exit(1)
            queries = input_keywords.split()
        except KeyboardInterrupt:
            logging.info("用户中断输入。")
            print("\n" + language_manager.tr('搜索已取消。'))
            sys.exit(0)

    # 获取其他参数
    engine_display = args.engine
    engine = engine_display  # 假设 engines 字典在 GUI 中对应直接使用
    num_results = args.num
    is_advanced = args.advanced
    custom_question = args.question if is_advanced else None

    # 如果启用进阶模式但未提供自定义问题，提示输入
    if is_advanced and not custom_question:
        try:
            custom_question = input(language_manager.tr('请输入自定义问题: ')).strip()
            if not custom_question:
                logging.error(language_manager.tr('进阶模式下未提供自定义问题。'))
                print(language_manager.tr('错误: 进阶模式下未提供自定义问题。'))
                sys.exit(1)
        except KeyboardInterrupt:
            logging.info("用户中断输入自定义问题。")
            print("\n" + language_manager.tr('搜索已取消。'))
            sys.exit(0)

    logging.info(f"搜索参数 - 关键词: {queries}, 引擎: {engine}, 结果数量: {num_results}, 进阶模式: {is_advanced}")

    # 修改 main 函数中的搜索执行部分
    try:
        # 执行搜索
        worker = CLIWorker(queries, num_results, engine, custom_question)
        worker.start()
        
        try:
            # 等待搜索完成
            worker.wait_until_finished()
            
            # 检查是否有结果
            if worker.results and worker.filename:
                # 展示结果
                for idx, result in enumerate(worker.results, start=1):
                    print(f"结果 {idx}:")
                    print(f"标题: {result['title']}")
                    print(f"URL: {result['link']}")
                    print(f"摘要: {result['snippet']}\n")

                print(language_manager.tr('搜索结果已保存到: ') + worker.filename)
            else:
                print(language_manager.tr('未找到搜索结果。'))

        except KeyboardInterrupt:
            worker.stop()
            logging.info("用户中断搜索任务。")
            print("\n" + language_manager.tr('搜索已取消。'))
            sys.exit(0)
        except Exception as e:
            logging.error(f"搜索过程中发生错误: {e}")
            print(language_manager.tr('错误: 搜索过程中发生错误: ') + str(e))
            sys.exit(1)

    except Exception as e:
        logging.error(f"搜索过程中发生错误: {e}")
        print(language_manager.tr('错误: 搜索过程中发生错误: ') + str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()