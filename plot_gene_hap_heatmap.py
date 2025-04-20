import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
from haplot.chart import GeneWithHapHeatmap

# 从命令行获取文件路径和图片前缀
if len(sys.argv) != 4:
    print("Usage: python script.py <gene_structure_file> <genotype_data_file> <output_prefix>")
    sys.exit(1)

gene_structure_file = sys.argv[1]
genotype_data_file = sys.argv[2]
output_prefix = sys.argv[3]

# 从 gene_structure_file 读取基因结构数据
df1 = pd.read_csv(gene_structure_file, sep='\t')
print(df1)

# 从 genotype_data_file 读取基因型数据
df2 = pd.read_csv(genotype_data_file, sep='\t', header=[0, 1, 2, 3], index_col=0)
print(df2)

# 绘制基因结构和基因型热图
fig = plt.figure(figsize=(7, 8))
GeneWithHapHeatmap(df1, df2, fig=fig)

# 保存图片为 PDF 文件
output_file = f"{output_prefix}_gene_hap_heatmap.pdf"
plt.savefig(output_file)
print(f"图片已保存为 {output_file}")
plt.close()

