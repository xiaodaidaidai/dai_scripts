#!/usr/bin/env Rscript

# ==============================================================================
# 功能：根据 motif 数据生成绘图区域 BED 文件，可自定义筛选列
library(readr)
library(dplyr)
library(argparse)

# --------------------------- 创建命令行参数解析器 ---------------------------
parser <- ArgumentParser(description = "根据 motif 数据生成绘图区域 BED 文件")

# 输入文件参数
parser$add_argument("--overview_file", required = TRUE, help = "单个 motif 的概览文件")

# 输出文件参数
parser$add_argument("--output_file", required = TRUE, help = "输出 BED 文件路径，用于绘图")

# 筛选参数
parser$add_argument("--motif_name", required = TRUE, help = "motif 名称，可以自由指定")
parser$add_argument("--score_columns", nargs=2, required = TRUE, help = "用于筛选的两列名称")
parser$add_argument("--score_order_column", required = TRUE, help = "用于排序的列名称")
parser$add_argument("--top_n", type = "integer", default = 20, help = "选择的 top N 个位点（默认 20）")
parser$add_argument("--flank", type = "integer", default = 1000, help = "在 peak 两侧扩展的碱基数（默认 1000 bp）")

# 解析命令行参数
args <- parser$parse_args()

# --------------------------- 读取数据 ---------------------------
motif_overview <- read_delim(args$overview_file, delim = "\t", escape_double = FALSE, trim_ws = TRUE)


# --------------------------- 筛选 top N 位点 ---------------------------
score_col1 <- args$score_columns[1]
score_col2 <- args$score_columns[2]

# 筛选：两列加和为2，排序：根据用户指定列，选前 top_n
motif_selected <- filter(motif_overview, .data[[score_col1]] + .data[[score_col2]] == 2) %>%
  arrange(desc(.data[[args$score_order_column]])) %>%
  slice(1:args$top_n)

# --------------------------- 生成绘图区域 ---------------------------
plot_regions <- mutate(motif_selected,
                       peak_chr,
                       plot_start = peak_start - args$flank,
                       plot_end = peak_end + args$flank) %>%
  select(peak_chr, plot_start, plot_end)

# --------------------------- 输出 BED 文件 ---------------------------
write.table(plot_regions,
            file = args$output_file,
            sep = "\t",
            row.names = FALSE,
            col.names = FALSE,
            quote = FALSE)

cat("已生成绘图区域 BED 文件：", args$output_file, "\n")

