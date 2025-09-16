#!/usr/bin/env Rscript

# 加载需要的包
suppressMessages(library(tidyverse))
suppressMessages(library(argparse))

# -------------------------------
# 参数解析
# -------------------------------
parser <- ArgumentParser(description = "统计 ChIP-seq peak 注释的相对位置，并绘制饼图 + 输出统计表")
parser$add_argument("-i", "--input", required=TRUE, help="输入文件 (peak_annotation.txt)")
parser$add_argument("-o", "--output", required=TRUE, help="输出图文件 (pdf/png/jpg)")
parser$add_argument("-t", "--table", required=TRUE, help="输出统计表文件 (tsv/csv)")
args <- parser$parse_args()

# -------------------------------
# 读取输入文件
# -------------------------------
input_data <- read_delim(
  args$input,
  delim = "\t",
  escape_double = FALSE,
  trim_ws = TRUE
)

# -------------------------------
# 统计分布
# -------------------------------
summary_data <- input_data %>%
  group_by(relative_location) %>%
  summarise(count = n()) %>%
  mutate(
    fraction = count / sum(count),
    label = paste0(round(fraction * 100, 2), "%")  # 百分比标签
  )

# -------------------------------
# 绘图
# -------------------------------
p <- ggplot(summary_data,
       aes(x = "", y = fraction, fill = relative_location)) +
  geom_bar(stat = "identity", width = 1, color = "white") +
  coord_polar("y", start = 0) +
  theme_void() +
  scale_fill_brewer(palette = "Set1") +
  theme(legend.title = element_blank()) +
  labs(fill = "Relative Location") +
  geom_text(aes(label = label), 
            position = position_stack(vjust = 0.5), 
            color = "black", size = 5)

# -------------------------------
# 输出结果
# -------------------------------
ggsave(filename = args$output, plot = p, width = 6, height = 6)

# 导出统计表
write_delim(
  summary_data %>% select(relative_location, count),
  args$table,
  delim = "\t"
)

