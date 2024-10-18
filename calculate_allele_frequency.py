import sys
from collections import Counter

# 计算基因频率和基因型计数的函数
def calculate_allele_frequency(genotypes, ref, alt):
    # 初始化计数器
    genotype_counts = Counter()
    allele_counts = Counter()

    # 遍历每个基因型
    for genotype in genotypes:
        if genotype == "--":
            genotype_counts["--"] += 1
            continue
        genotype_counts[genotype] += 1

    # 计算总个体数（不包括缺失值）
    total_individuals = sum(genotype_counts.values()) - genotype_counts["--"]

    # 计算基因频率
    for genotype, count in genotype_counts.items():
        if genotype == ref + ref:  # AA
            allele_counts[ref] += count * 2
        elif genotype == alt + alt:  # aa
            allele_counts[alt] += count * 2
        elif ref in genotype and alt in genotype:  # Aa
            allele_counts[ref] += count
            allele_counts[alt] += count

    # 计算基因频率
    ref_freq = allele_counts[ref] / (total_individuals * 2) if total_individuals > 0 else 0
    alt_freq = allele_counts[alt] / (total_individuals * 2) if total_individuals > 0 else 0

    return ref_freq, alt_freq, genotype_counts

# 主程序
def main(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        header = infile.readline().strip().split('\t')  # 读取标题行
        outfile.write("#CHROM\tPOS\tAF1\tpercentage1\tAF2\tpercentage2\t" +
                      "genotype1\tcount1\tgenotype2\tcount2\tgenotype3\tcount3\tgenotype4\tcount4\n")  # 输出文件标题

        for line in infile:
            if not line.strip():  # 忽略空行
                continue
            
            columns = line.strip().split('\t')
            
            # 确保至少有足够的列来进行处理
            if len(columns) < 4:
                print(f"警告: {line.strip()} 行数据格式不正确，已跳过")
                continue

            chrom = columns[0]
            pos = columns[1]
            ref = columns[2]
            alt = columns[3]
            genotypes = columns[4:]  # 从第5列开始是个体的基因型

            # 计算基因频率和基因型计数
            ref_freq, alt_freq, genotype_counts = calculate_allele_frequency(genotypes, ref, alt)

            # 确保频率的和为1
            if round(ref_freq + alt_freq, 2) != 1.0:
                print(f"警告: {chrom}:{pos} 的基因频率不正确: {ref_freq:.2f} + {alt_freq:.2f} != 1")

            # 输出结果到文件，保留四位小数
            output_line = f"{chrom}\t{pos}\t{ref}\t{ref_freq:.4f}\t{alt}\t{alt_freq:.4f}"

            # 动态添加基因型和计数
            for genotype, count in genotype_counts.items():
                output_line += f"\t{genotype}\t{count}"

            outfile.write(output_line + "\n")

    print("基因频率和基因型计数计算完成，结果已输出到", output_file)

# 检查参数
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python script.py <输入文件> <输出文件>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)
