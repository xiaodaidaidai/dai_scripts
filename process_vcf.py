import sys

# 处理 VCF 文件的函数
def process_vcf(input_file, output_file):
    # 打开输入文件和输出文件
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # 读取文件的所有行
        lines = infile.readlines()

        # 遍历每一行
        for line in lines:
            # 跳过注释行（以 '##' 开头）
            if line.startswith("##"):
                continue
            # 处理标题行（以 '#CHROM' 开头），只保留第1列、第2列、第4列和第5列
            elif line.startswith("#CHROM"):
                # 将标题行按制表符分隔成列
                columns = line.strip().split("\t")
                # 输出标题行：第1列、第2列、第4列和第5列，以及所有样本列（从第9列开始）
                outfile.write("\t".join([columns[0], columns[1], columns[3], columns[4]] + columns[9:]) + "\n")
            else:
                # 处理数据行，去掉不需要的列
                columns = line.strip().split("\t")
                # 输出数据行：第1列、第2列、第4列和第5列，以及所有样本列（从第9列开始）
                outfile.write("\t".join([columns[0], columns[1], columns[3], columns[4]] + columns[9:]) + "\n")

# 主函数：从命令行获取输入输出文件路径
if __name__ == "__main__":
    # 检查命令行参数是否正确
    if len(sys.argv) != 3:
        print("Usage: python process_vcf.py <input_file> <output_file>")
        sys.exit(1)  # 如果参数不对，退出程序并提示用法
    
    # 获取输入文件和输出文件路径
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # 调用处理函数来处理文件
    process_vcf(input_file, output_file)
    print(f"Processing complete. Output written to {output_file}")

