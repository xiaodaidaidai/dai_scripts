#!/usr/bin/env Rscript
library(argparse)
library(ggplot2)

# 1. 设置参数解析
parser <- ArgumentParser(description='专业版：基因结构（含 UTR 比例）与 SNP 标注工具')
parser$add_argument("-i", "--input", required=TRUE, help="输入的 GFF3 文件路径")
parser$add_argument("-o", "--output", default="gene_plot_final.pdf", help="输出文件名")
parser$add_argument("-c", "--color", default="#2A9D8F", help="CDS 区域的颜色")
parser$add_argument("-u", "--utr_color", default="#E9C46A", help="UTR 区域的颜色")
parser$add_argument("-s", "--snps", help="可选：SNP 位点位置，用逗号隔开")
parser$add_argument("-t", "--title", help="自定义图表标题")

# 比例与长宽控制
parser$add_argument("--cds_h", type="double", default=0.15, help="CDS 厚块的高度一半")
parser$add_argument("--utr_h_ratio", type="double", default=0.6, help="UTR 高度相对于 CDS 的比例 [0-1.0]")
parser$add_argument("--img_w", type="double", default=10, help="输出图片的宽度")
parser$add_argument("--img_h", type="double", default=3, help="输出图片的高度")

args <- parser$parse_args()

# 2. 读取与处理数据
gff <- read.table(args$input, sep="\t", header=F, stringsAsFactors = FALSE)
colnames(gff) <- c("chr", "source", "type", "start", "end", "score", "strand", "phase", "attributes")

gene_range <- gff[gff$type == "gene", ]
cds_regions <- gff[gff$type == "CDS", ]
utr_regions <- gff[gff$type %in% c("five_prime_UTR", "three_prime_UTR"), ]

title_name <- ifelse(is.null(args$title), gsub(".gff", "", basename(args$input)), args$title)

# 3. 计算坐标边界
y_min_cds <- 1 - args$cds_h
y_max_cds <- 1 + args$cds_h

# 计算 UTR 高度
utr_h <- args$cds_h * args$utr_h_ratio
y_min_utr <- 1 - utr_h
y_max_utr <- 1 + utr_h

label_y_pos <- min(y_min_cds, y_min_utr) - 0.05 
y_upper_limit <- if (!is.null(args$snps)) 1.6 else max(y_max_cds, y_max_utr) + 0.1

# 4. 构建图层
p <- ggplot() +
  # A. 内含子线
  geom_segment(aes(x = gene_range$start, xend = gene_range$end, y = 1, yend = 1), 
               linewidth = 0.8, color = "black") +
  
  # B. UTR 矩形
  geom_rect(data = utr_regions, aes(xmin = start, xmax = end, ymin = y_min_utr, ymax = y_max_utr),
            fill = args$utr_color, color = "black", linewidth = 0.3) +
  
  # C. CDS 矩形
  geom_rect(data = cds_regions, aes(xmin = start, xmax = end, ymin = y_min_cds, ymax = y_max_cds),
            fill = args$color, color = "black", linewidth = 0.3) +
  
  # D. 基因起始终止坐标
  annotate("text", x = gene_range$start, y = label_y_pos, label = gene_range$start, 
           size = 3, vjust = 1, fontface = "italic") +
  annotate("text", x = gene_range$end, y = label_y_pos, label = gene_range$end, 
           size = 3, vjust = 1, fontface = "italic")

# 5. SNP 标注
if (!is.null(args$snps) && args$snps != "") {
  snp_list <- as.numeric(unlist(strsplit(gsub(" ", "", args$snps), ",")))
  if (!any(is.na(snp_list))) {
    p <- p + geom_vline(xintercept = snp_list, color = "red", linetype = "dashed", alpha = 0.5) +
             annotate("text", x = snp_list, y = max(y_max_cds, y_max_utr) + 0.05, 
                      label = snp_list, color = "red", size = 3, angle = 90, 
                      hjust = 0, fontface = "bold")
  }
}

# 6. 纯净主题
p <- p + scale_y_continuous(limits = c(0.4, y_upper_limit)) +
  coord_cartesian(clip = "off") +
  theme_minimal() +
  theme(
    axis.text = element_blank(),
    axis.ticks = element_blank(),
    panel.grid = element_blank(),
    plot.margin = unit(c(1, 1, 1, 1), "lines"),
    plot.title = element_text(hjust = 0.5, face = "bold", size = 14),
    axis.title.x = element_text(size = 12, margin = margin(t = 15))
  ) +
  labs(x = paste("Chromosome Position (", gene_range$chr[1], ")", sep=""), 
       y = "", title = title_name)

# 7. 保存
ggsave(args$output, p, width = args$img_w, height = args$img_h)
cat(paste("绘图完成！图片保存至:", args$output, "\n"))
