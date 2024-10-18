import sys

# 读取ID文件，提取需要的列名
def read_id_file(id_file):
    ids = []
    with open(id_file, 'r') as f:
        for line in f:
            ids.append(line.strip())
    return ids

# 处理基因型文件，提取前4列和指定的列
def filter_genotype(geno_file, id_list, output_file):
    with open(geno_file, 'r') as infile, open(output_file, 'w') as outfile:
        # 读取文件的第一行，提取列标题
        header = infile.readline().strip().split('\t')
        # 提取前4列和ID.txt中指定的列的索引
        selected_cols = [0, 1, 2, 3]  # 前四列
        selected_cols += [header.index(id_) for id_ in id_list if id_ in header]

        # 写入新的表头，包含前4列和指定的ID列
        outfile.write('\t'.join([header[i] for i in selected_cols]) + '\n')

        # 处理数据行，提取对应列
        for line in infile:
            row = line.strip().split('\t')
            outfile.write('\t'.join([row[i] for i in selected_cols]) + '\n')

# 主函数，处理输入输出
def main():
    # 检查命令行参数数量
    if len(sys.argv) != 4:
        print("用法: python extract_columns_by_ID.py <基因型文件> <ID文件> <输出文件>")
        sys.exit(1)  # 退出程序，返回非零状态表示错误

    # sys.argv获取命令行参数，输入基因型文件，ID文件和输出文件
    geno_file = sys.argv[1]  # 基因型文件
    id_file = sys.argv[2]    # ID.txt文件
    output_file = sys.argv[3]  # 输出文件名称

    # 读取ID文件
    id_list = read_id_file(id_file)

    # 过滤并输出基因型文件
    filter_genotype(geno_file, id_list, output_file)

# 判断脚本是否直接运行
if __name__ == "__main__":
    main()
