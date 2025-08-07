#!/usr/bin/env Rscript

# 加载必要的库
library(ggplot2)
library(argparse)

# 创建参数解析器
parser <- ArgumentParser(description = "Plot sequencing depth from samtools depth output")
parser$add_argument("-i", "--input", help = "Input CSV file from samtools depth", required = TRUE)
parser$add_argument("-o", "--output", help = "Output image file (e.g., depth_plot.png)", default = "depth_plot.png")
args <- parser$parse_args()

# 读取数据
depth_data <- read.table(args$input, header = FALSE, sep = "\t", col.names = c("Chrom", "Position", "Depth"))

# 绘图
p <- ggplot(depth_data, aes(x = Position, y = Depth)) +
  geom_line(color = "steelblue") +
  labs(title = "Sequencing Depth", x = "Genomic Position", y = "Depth") +
  theme_minimal()

# 保存图片
ggsave(args$output, p, width = 10, height = 5)

