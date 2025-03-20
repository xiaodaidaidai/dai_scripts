#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

# 检查命令行参数数量
if len(sys.argv) != 2:
    print("Usage: {} <gff_file> > out.gff3".format(sys.argv[0]))
    sys.exit(1)

# 获取输入的 GFF 文件名
gff_file = sys.argv[1]

# 定义一个字典，用于记录每个 ID 的出现次数
id_count = {}

try:
    # 打开输入文件
    with open(gff_file, 'r') as infile:
        for line in infile:
            line = line.strip()  # 去除行首尾的空格和换行符
            # 如果是注释行（以 # 开头），直接输出
            if line.startswith('#'):
                print(line)
                continue
            
            # 按制表符（\t）拆分每一行，生成字段列表
            fields = line.split('\t')
            
            # 第 9 列（即索引为 8）中包含注释信息，提取 ID 信息
            if len(fields) > 8 and 'ID=' in fields[8]:
                attributes = fields[8]
                # 使用正则表达式提取 ID= 后面的内容，直到遇到分号（;）
                id_start = attributes.find('ID=') + 3
                id_end = attributes.find(';', id_start) if ';' in attributes[id_start:] else len(attributes)
                gene_id = attributes[id_start:id_end]

                # 记录 ID 的出现次数
                id_count[gene_id] = id_count.get(gene_id, 0) + 1

                # 如果 ID 出现超过一次，修改为 ID_x 的格式
                if id_count[gene_id] > 1:
                    new_id = f"{gene_id}_{id_count[gene_id]}"
                    # 替换原 ID 为新的 ID
                    attributes = attributes.replace(f"ID={gene_id}", f"ID={new_id}")
                    fields[8] = attributes
            
            # 重新拼接为 GFF 格式输出
            print('\t'.join(fields))

except FileNotFoundError:
    print(f"Error: Cannot open file '{gff_file}'")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

