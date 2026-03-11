#!/usr/bin/env Rscript

# 检查并加载必要的库
if (!require("argparse")) install.packages("argparse", repos='http://cran.us.r-project.org')
if (!require("ggplot2")) install.packages("ggplot2", repos='http://cran.us.r-project.org')

library(argparse)
library(ggplot2)

# 1. 设置参数解析
parser <- ArgumentParser(description='专业版：基因结构绘图工具（支持 UTR 比例、正负链标注与 SNP 映射）')
parser$add_argument("-i", "--input", required=TRUE, help="输入的 GFF3 文件路径")
parser$add_argument("-o", "--output", default="gene_structure_plot.pdf", help="输出文件名")
parser$add_argument("-c", "--color", default="#2A9D8F", help="CDS 区域的颜色")
parser$add_argument("-u", "--utr_color", default="#E9C46A", help="UTR 区域的颜色")
parser$add_argument("-s", "--snps", help="可选：SNP 位点位置，用逗号隔开 (如: 3762,5175)")
parser$add_argument("-t", "--title", help="自定义图表标题")

# 比例与长宽控制
parser$add_argument("--cds_h", type="double", default=0.15, help="CDS 厚块的高度一半")
parser$add_argument("--utr_h_ratio", type="double", default=0.6, help="UTR 高度相对于 CDS 的比例 [0-1.0]")
parser$add_argument("--img_w", type="double", default=12, help="输出图片的宽度")
parser$add_argument("--img_h", type="double", default=4, help="输出图片的高度")

args <- parser$parse_args()

# 2. 读取与预处理数据
gff <- read.table(args$input, sep="\t", header=F, stringsAsFactors = FALSE)
colnames(gff) <- c("chr", "source", "type", "start", "end", "score", "strand", "phase", "attributes")

# 提取关键结构
gene_data <- gff[gff$type == "gene", ][1, ] # 取第一行基因信息
cds_regions <- gff[gff$type == "CDS", ]
utr_regions <- gff[gff$type %in% c("five_prime_UTR", "three_prime_UTR"), ]

# 标题处理
title_name <- ifelse(is.null(args$title), paste("Gene Structure:", basename(args$input)), args$title)

# 3. 计算坐标与方向
# 5' 和 3' 方向逻辑
if (gene_data$strand == "-") {
  label_left <- "3'"
  label_right <- "5'"
} else {
  label_left <- "5'"
  label_right <- "3'"
}

# 高度计算
y_min_cds <- 1 - args$cds_h
y_max_cds <- 1 + args$cds_h
utr_h <- args$cds_h * args$utr_h_ratio
y_min_utr <- 1 - utr_h
y_max_utr <- 1 + utr_h

# 设置绘图上界（为 SNP 标签留出空间）
y_upper_limit <- if (!is.null(args$snps)) 1.7 else 1.3

# 4. 构建可视化图层


p <- ggplot() +
  # A. 内含子线 (背景线)
  geom_segment(aes(x = gene_data$start, xend = gene_data$end, y = 1, yend = 1), 
               linewidth = 1, color = "black") +
  
  # B. UTR 矩形 (较窄)
  geom_rect(data = utr_regions, 
            aes(xmin = start, xmax = end, ymin = y_min_utr, ymax = y_max_utr, fill = "UTR"),
            color = "black", linewidth = 0.3) +
  
  # C. CDS 矩形 (较宽)
  geom_rect(data = cds_regions, 
            aes(xmin = start, xmax = end, ymin = y_min_cds, ymax = y_max_cds, fill = "CDS"),
            color = "black", linewidth = 0.3) +
  
  # D. 方向标注 (5' 和 3')
  annotate("text", x = gene_data$start, y = 1, label = label_left, 
           hjust = 1.5, size = 5, fontface = "bold") +
  annotate("text", x = gene_data$end, y = 1, label = label_right, 
           hjust = -0.5, size = 5, fontface = "bold") +
  
  # E. 物理位置标注 (基因起始与终止)
  annotate("text", x = gene_data$start, y = 0.75, label = gene_data$start, size = 3.5, fontface = "italic") +
  annotate("text", x = gene_data$end, y = 0.75, label = gene_data$end, size = 3.5, fontface = "italic")

# 5. 添加 SNP 位点 (如果有)
if (!is.null(args$snps) && args$snps != "") {
  snp_list <- as.numeric(unlist(strsplit(gsub(" ", "", args$snps), ",")))
  if (!any(is.na(snp_list))) {
    p <- p + 
      geom_vline(xintercept = snp_list, color = "red", linetype = "dashed", alpha = 0.6) +
      annotate("text", x = snp_list, y = 1.4, label = snp_list, 
               color = "red", size = 3, angle = 90, vjust = -0.5, fontface = "bold")
  }
}

# 6. 样式美化与图例
p <- p +
  scale_fill_manual(name = "Structure", 
                    values = c("CDS" = args$color, "UTR" = args$utr_color)) +
  scale_y_continuous(limits = c(0.6, y_upper_limit)) +
  theme_minimal() +
  theme(
    axis.text = element_blank(),
    axis.title.y = element_blank(),
    panel.grid = element_blank(),
    legend.position = "bottom",
    plot.title = element_text(hjust = 0.5, size = 16, face = "bold"),
    axis.title.x = element_text(size = 12, margin = margin(t = 20))
  ) +
  labs(title = title_name, x = paste("Chromosome Position (", gene_data$chr, ")", sep=""))

# 7. 保存结果
ggsave(args$output, p, width = args$img_w, height = args$img_h)
cat(paste("成功！图片已保存至:", args$output, "\n"))
