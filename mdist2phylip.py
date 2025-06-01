#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python脚本功能说明：
本脚本用于将 PLINK 输出的 .mdist 文件转换为 Phylip 格式。
输入文件包括：
1) $prefix.mdist.id（样本ID文件）
2) $prefix.mdist（距离矩阵文件）
输出文件包括：
1) hash.sample（记录新的样本名和原始样本名）
2) $prefix.mdist.phylip（Phylip格式的距离矩阵）
"""

import sys

# 获取输入文件的前缀，例如：如果输入是"plink"，则会使用"plink.mdist.id"和"plink.mdist"两个文件
prefix = sys.argv[1]

# 第一步：处理 $prefix.mdist.id 文件
species = []         # 用于存储新的样本名称
start = 1000         # 起始编号
count = 1            # 样本计数器

# 读取 .mdist.id 文件
with open(f"{prefix}.mdist.id", "r") as infile, open("hash.sample", "w") as outfile:
    for line in infile:
        line = line.strip()                         # 去除行尾换行符
        inf = line.split()                          # 按空格或制表符分割
        number = count + start                      # 生成新的数字标签
        newname = f"S{number}S"                     # 生成新的样本名称，例如：S1001S
        species.append(newname)                     # 存储到 species 列表中
        outfile.write(f"{newname}\t{inf[0]}\n")     # 写入 hash.sample 文件
        count += 1                                  # 样本计数器加一

# 第二步：处理 $prefix.mdist 文件，转换为 Phylip 格式
length = count - 1                                  # 计算样本总数

# 打开 .mdist 文件
with open(f"{prefix}.mdist", "r") as infile, open(f"{prefix}.mdist.phylip", "w") as outfile:
    outfile.write(f"\t{length}\n")                  # 写入样本数量，Phylip 格式要求
    i = 0                                           # 用于 species 索引
    for line in infile:
        line = line.strip()                         # 去除换行符
        len_name = len(species[i])                  # 获取样本名长度
        x = 10 - len_name                           # 计算补齐空格（Phylip要求固定列宽）
        a = " " * x                                 # 生成补齐的空格
        outfile.write(f"{species[i]}{a}\t{line}\n") # 写入 Phylip 格式的矩阵行
        i += 1

# 结束
