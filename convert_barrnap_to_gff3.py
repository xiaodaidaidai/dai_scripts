#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
脚本名称:
    convert_barrnap_to_gff3.py - 将 barrnap 输出的 GFF2 文件转换为标准 GFF3 格式

使用方法:
    python convert_barrnap_to_gff3.py --input /path/to/some_file.out --log output.log

参数:
    --input, -i      输入 barrnap 的输出文件
    --log, -l        日志文件（可选）
    --help, -h       显示帮助信息

输出:
    将标准 GFF3 文件输出到标准输出（stdout）
"""

import argparse
import sys

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="将 barrnap 输出的 GFF2 文件转换为 GFF3 格式"
    )
    parser.add_argument(
        '-i', '--input', required=True, help="输入文件路径 (barrnap 输出的 GFF2 文件)"
    )
    parser.add_argument(
        '-l', '--log', help="日志文件路径（可选）"
    )
    return parser.parse_args()

def write_log(log_file, message):
    """写入日志文件"""
    if log_file:
        with open(log_file, 'a') as log:
            log.write(message + "\n")

def convert_barrnap_to_gff3(input_file, log_file):
    """转换 barrnap 的 GFF2 文件为 GFF3 格式"""
    try:
        with open(input_file, 'r') as infile:
            i = 1  # ID 计数器
            print("##gff-version 3")  # 输出 GFF3 文件头

            for line in infile:
                if line.startswith('#'):
                    # 跳过注释行
                    continue

                # 使用制表符分割行
                cols = line.strip().split('\t')
                if len(cols) < 9:
                    continue

                contig = cols[0]    # 序列名
                start = int(cols[3]) # 起始位点
                stop = int(cols[4])  # 终止位点
                score = cols[5]      # 评分值
                strand = cols[6]     # 链（正链或负链）
                target = cols[8]     # 特征信息

                # 生成唯一的 ID
                feature_id = f"{target}_{i}"

                if strand == "+":
                    # 正链
                    print(f"{contig}\tbarrnap\tgene\t{start}\t{stop}\t{score}\t+\t.\tID={feature_id}")
                    print(f"{contig}\tbarrnap\trRNA\t{start}\t{stop}\t{score}\t+\t.\tID={feature_id}_rRNA;Parent={feature_id}")
                    print(f"{contig}\tbarrnap\texon\t{start}\t{stop}\t{score}\t+\t.\tID={feature_id}_exon;Parent={feature_id}_rRNA")
                elif strand == "-":
                    # 负链
                    print(f"{contig}\tbarrnap\tgene\t{start}\t{stop}\t{score}\t-\t.\tID={feature_id}")
                    print(f"{contig}\tbarrnap\trRNA\t{start}\t{stop}\t{score}\t-\t.\tID={feature_id}_rRNA;Parent={feature_id}")
                    print(f"{contig}\tbarrnap\texon\t{start}\t{stop}\t{score}\t-\t.\tID={feature_id}_exon;Parent={feature_id}_rRNA")

                i += 1

            write_log(log_file, f"成功转换文件: {input_file}")

    except Exception as e:
        # 输出错误信息
        write_log(log_file, f"处理文件 {input_file} 时出错: {e}")
        sys.exit(f"ERROR: 处理文件 {input_file} 时出错: {e}")

def main():
    """主函数"""
    args = parse_args()

    # 检查输入文件是否存在
    try:
        with open(args.input, 'r'):
            pass
    except FileNotFoundError:
        sys.exit(f"ERROR: 输入文件 {args.input} 不存在！")

    # 运行转换函数
    convert_barrnap_to_gff3(args.input, args.log)

if __name__ == "__main__":
    main()

