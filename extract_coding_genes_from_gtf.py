#!/usr/bin/env python3
import sys

# 检查输入参数数量，要求提供两个输入文件（GTF文件和ID文件）
if len(sys.argv) != 3:
    print(f"Usage: python {sys.argv[0]} <gtf> <id.txt(transcript_id\\tgene_id)>")
    sys.exit(1)

# 获取输入文件名
gtf_file = sys.argv[1]
id_file = sys.argv[2]

# 定义两个集合（set），分别用于存储 transcript_id 和 gene_id
tid = set()
gid = set()

# 读取ID文件，提取 transcript_id 和 gene_id
with open(id_file) as f:
    for line in f:
        line = line.strip().split()  # 去除首尾空格并按空格或制表符分割
        if len(line) < 2:
            continue  # 如果当前行字段少于两个，跳过
        tid.add(line[0])  # 第一个字段为 transcript_id，存入tid集合
        gid.add(line[1])  # 第二个字段为 gene_id，存入gid集合

# 打开GTF文件，逐行读取和筛选
with open(gtf_file) as f:
    for line in f:
        line = line.strip()  # 去除首尾空格
        fields = line.split('\t')  # 按制表符分割成列表
        if len(fields) != 9:
            continue  # 如果字段数量不等于9（不符合GTF格式），跳过

        flag = False  # 标记变量，表示是否输出该行
        attributes = fields[8]  # 第9列为属性信息

        # 检查gene_id
        if 'gene_id' in attributes:
            # 使用split提取gene_id的值
            gene_id = attributes.split('gene_id "')[1].split('"')[0]
            # 如果当前行为基因行（第3列为gene），且gene_id在ID列表中，设置标记为True
            if fields[2] == 'gene' and gene_id in gid:
                flag = True

        # 检查transcript_id
        if 'transcript_id' in attributes:
            # 使用split提取transcript_id的值
            transcript_id = attributes.split('transcript_id "')[1].split('"')[0]
            # 如果transcript_id存在于ID列表中，设置标记为True
            if transcript_id in tid:
                flag = True

        # 如果flag为True，输出该行（表示gene_id或transcript_id匹配）
        if flag:
            print(line)

