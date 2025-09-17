#!/usr/bin/env python3
import sys

# 使用方法: python gtf2bed6.py input.gtf output.bed
if len(sys.argv) != 3:
    print("Usage: python gtf2bed6.py <input.gtf> <output.bed>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for line in infile:
        if line.startswith("#"):
            continue
        fields = line.strip().split("\t")
        if fields[2] == "gene":  # 只提取 gene 条目
            chrom = fields[0]
            start = fields[3]  # GTF 是 1-based，BED 也是可以直接用
            end = fields[4]
            strand = fields[6]
            
            # 在 attributes 字段里提取 gene_id
            attr_field = fields[8]
            gene_id = "."
            for attr in attr_field.split(";"):
                attr = attr.strip()
                if attr.startswith("gene_id"):
                    gene_id = attr.split(" ")[1].replace('"', '')
                    break
            
            # 输出 BED6 格式
            outfile.write(f"{chrom}\t{start}\t{end}\t{gene_id}\t.\t{strand}\n")

