#!/usr/bin/env Rscript

# 加载必要的库
suppressMessages(library(ggplot2))
suppressMessages(library(gridExtra))

# 获取命令行参数
args <- commandArgs(trailingOnly = TRUE)
if(length(args) != 2){
  cat("Usage: Rscript plot_macs3_cutoff_analysis.R input_file.txt output_file.pdf\n")
  quit(status = 1)
}

input_file <- args[1]
output_file <- args[2]

# 读取数据
df <- read.table(input_file, header = TRUE, sep = "\t")

# 绘图1：npeaks vs qscore (封闭折线)
p1 <- ggplot(df, aes(x = qscore, y = npeaks)) +
  geom_area(fill = "lightblue", alpha = 0.5) +   # 填充颜色
  geom_line(color = "blue", size = 1) +          # 折线
  geom_point(color = "blue") +                   # 点
  labs(title = "npeaks vs qscore", x = "qscore", y = "npeaks") +
  theme_minimal()

# 绘图2：avelpeak vs qscore (封闭折线)
p2 <- ggplot(df, aes(x = qscore, y = avelpeak)) +
  geom_area(fill = "pink", alpha = 0.5) +
  geom_line(color = "red", size = 1) +
  geom_point(color = "red") +
  labs(title = "avelpeak vs qscore", x = "qscore", y = "avelpeak") +
  theme_minimal()

# 左右排列并保存为 PDF
pdf(output_file, width = 12, height = 5)
grid.arrange(p1, p2, ncol = 2)
dev.off()

