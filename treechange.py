#!/usr/bin/env python3
"""
用法: python treechange.py hash.type treefile
参数:
    hash.type: 包含键值对的文本文件，每行格式为 "key\tvalue"
    treefile: 树结构文件，包含需要替换的标识符

此脚本会根据 hash.type 文件中的映射关系，替换 treefile 中的标识符
"""

import sys

def main():
    # 检查命令行参数数量是否正确
    if len(sys.argv) != 3:
        print("错误: 参数数量不正确")
        print(__doc__)
        sys.exit(1)

    hash_type_file = sys.argv[1]
    tree_file = sys.argv[2]

    # 读取哈希类型文件并构建字典
    hash_type = {}
    try:
        with open(hash_type_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:  # 忽略空行
                    parts = line.split('\t')
                    if len(parts) == 2:
                        hash_type[parts[0]] = parts[1]
                    else:
                        print(f"警告: 行 '{line}' 格式不正确，应为 'key\tvalue'")
    except FileNotFoundError:
        print(f"错误: 无法找到文件 {hash_type_file}")
        sys.exit(1)

    # 读取树文件
    try:
        with open(tree_file, 'r', encoding='utf-8') as f:
            tree_lines = [line.rstrip('\n') for line in f]
    except FileNotFoundError:
        print(f"错误: 无法找到文件 {tree_file}")
        sys.exit(1)

    # 将读取的行连接成一个字符串
    tree_content = ''.join(tree_lines)

    # 根据哈希表替换树内容中的标识符
    # 首先替换形如 "key_key" 的模式
    for key in hash_type:
        # 创建正则表达式模式，匹配 "key_key"
        pattern = f"{key}_{key}"
        # 替换为对应的值
        tree_content = tree_content.replace(pattern, hash_type[key])

    # 然后替换单独的 "key"
    for key in hash_type:
        tree_content = tree_content.replace(key, hash_type[key])

    # 创建输出文件名，在原文件名后添加 .newtree 后缀
    output_file = f"{tree_file}.newtree"

    # 写入处理后的树内容
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(tree_content + '\n')

    print(f"处理完成，结果已保存到 {output_file}")

if __name__ == "__main__":
    main()
