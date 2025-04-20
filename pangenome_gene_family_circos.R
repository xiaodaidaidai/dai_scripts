# 加载所需的包
library(circlize)  # circlize包用于绘制环状基因组图
library(grid)      # grid包用于更好地控制文本的位置

# 读取数据
genome <- read.csv("C:/Users/Lenovo/Desktop/test1/genome.csv", header = TRUE)  # 读取基因组文件
Ath1_four_speed_g <- read.csv("C:/Users/Lenovo/Desktop/test1/Ath1.csv", header = TRUE)  # 读取Ath1数据
Ath2_four_speed_g <- read.csv("C:/Users/Lenovo/Desktop/test1/Ath2.csv", header = TRUE)  # 读取Ath2数据

# 设置输出路径和文件名
output_dir <- "C:/Users/Lenovo/Desktop/test1/"
output_file <- "circos_plot"  # 基础文件名

# 保存为PDF（矢量图，推荐用于论文）
pdf(file = paste0(output_dir, output_file, ".pdf"), width = 8, height = 8)

# 清除之前的circos绘图
circos.clear()

# 设置circos绘图参数
# start.degree = 85：设置 Circos 图的起始角度为 85 度，控制圆环的起始位置。
# track.height = 0.02：设置每个轨道的高度为 0.02，调整轨道的视觉效果。
# cell.padding = c(0,0,0,0)：设置单元格的内边距为 0，即不留任何空隙。
# gap.degree=c(rep(1,9), 5)：设置轨道之间的间隔，其中前 9 个间隔为 1 度，最后一个间隔为 14 度。
circos.par(start.degree = 85, 
    track.height = 0.02, 
    cell.padding = c(0,0,0,0), 
    gap.degree = c(rep(1,9), 14))

# 用ideogram初始化circos绘图（带有坐标轴和标签）
# genome：指定要绘制的基因组数据
# plotType = c("axis", "labels")：设置绘图类型，包括绘制坐标轴（"axis"）和标签（"labels"），用于展示基因组的结构信息。
circos.initializeWithIdeogram(genome, plotType = c("axis", "labels"))

# 定义函数用于创建包含2个组的基因组轨道
# 在基因组区域绘制四组数据的轨道，设置轨道高度和背景边框颜色
# #在 panel.fun 函数中，可以基础图形函数来添加图形，函数接收两个参数 region 和 value：
# region：包含两列起止位置的数据框
# value：其他列信息的数据框，一般从第四列开始的数据
# 其中 region 的数据用于标识 x 轴，value 标识的是 y 轴。
# panel.fun 函数还强制要求传入第三个参数 ...，用于传递用户不可见的变量，并交由其内部的基础绘图函数进行解析，如 circos.genomicPoints
create_genomic_track <- function(four_speed_g_list) {
  circos.genomicTrackPlotRegion(four_speed_g_list, track.height = 0.08, ylim = c(0,1), bg.border = "lightgray",
                                panel.fun = function(region, value, ...) {
                                  i = getI(...)  # 获取组索引
                                  if (i == 1) {
                                    circos.genomicRect(region, value, col = "blue", border = "blue", lwd = 1)  # 蓝色表示group1组
                                  } else if (i == 2) {
                                    circos.genomicRect(region, value, col = "purple", border = "purple", lwd = 1)  # 紫色表示group2组
                                  } else if (i == 3) {
                                    circos.genomicRect(region, value, col = "red", border = "red", lwd = 1)  # 红色表示group3组
                                  } else if (i == 4) {
                                    circos.genomicRect(region, value, col = "orange", border = "orange", lwd = 1)  # 橙色表示group4组
                                  }
                                })
}

# 为每个基因组准备数据列表
Ath1_four_speed_g_list <- list(Ath1_four_speed_g[Ath1_four_speed_g$group == "group1", ],
                              Ath1_four_speed_g[Ath1_four_speed_g$group == "group2", ],
                              Ath1_four_speed_g[Ath1_four_speed_g$group == "group3", ],
                              Ath1_four_speed_g[Ath1_four_speed_g$group == "group4", ])

Ath2_four_speed_g_list <- list(Ath2_four_speed_g[Ath2_four_speed_g$group == "group1", ],
                              Ath2_four_speed_g[Ath2_four_speed_g$group == "group2", ],
                              Ath2_four_speed_g[Ath2_four_speed_g$group == "group3", ],
                              Ath2_four_speed_g[Ath2_four_speed_g$group == "group4", ])

# 绘制每个基因组
create_genomic_track(Ath1_four_speed_g_list)
create_genomic_track(Ath2_four_speed_g_list)

# 添加每个基因组的标签
text(-0.01, 0.85, "Ath1", cex = 1)  # Ath1基因组
text(-0.01, 0.75, "Ath2", cex = 1)  # Ath2基因组


# 在中心添加图例
grid.text("group1", x = 0.5, y = 0.60, gp = gpar(col = "blue", fontsize = 14, fontface = "bold"))      # 蓝色的"group1"标签
grid.text("group2", x = 0.5, y = 0.55, gp = gpar(col = "purple", fontsize = 14, fontface = "bold"))    # 紫色的"group2"标签
grid.text("group3", x = 0.5, y = 0.50, gp = gpar(col = "red", fontsize = 14, fontface = "bold"))       # 红色的"group3"标签
grid.text("group4", x = 0.5, y = 0.45, gp = gpar(col = "orange", fontsize = 14, fontface = "bold"))    # 橙色的"group4"标签

# 关闭PDF设备
dev.off()
