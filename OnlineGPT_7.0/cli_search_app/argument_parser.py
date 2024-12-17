# cli_search_app/argument_parser.py
# 负责日志配置。

import argparse

def parse_arguments():
    """
    解析命令行参数。

    返回:
    - args: 解析后的命令行参数对象
    """
    parser = argparse.ArgumentParser(
        description='命令行搜索应用',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-k', '--keywords',
        nargs='+',
        required=False,
        help='搜索关键词。如果未提供，将会提示输入。'
    )
    parser.add_argument(
        '-e', '--engine',
        choices=['Google', 'Bing', '百度'],
        default='Google',
        help='选择搜索引擎。'
    )
    parser.add_argument(
        '-n', '--num',
        type=int,
        default=5,
        help='每个关键词的搜索结果数量。'
    )
    parser.add_argument(
        '-a', '--advanced',
        action='store_true',
        help='启用进阶模式，允许自定义问题。'
    )
    parser.add_argument(
        '-q', '--question',
        type=str,
        default='',
        help='自定义问题，仅在启用进阶模式时使用。'
    )
    parser.add_argument(
        '-s', '--save',
        type=str,
        default='',
        help='将搜索结果保存到指定的文件路径。默认保存到 Downloads/search_results.txt。'
    )
    parser.add_argument(
        '-l', '--language',
        choices=['en', 'zh'],
        default='en',
        help='选择界面语言。'
    )

    args = parser.parse_args()
    return args