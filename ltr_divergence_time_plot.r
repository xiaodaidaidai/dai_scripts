library("tidyverse")
library("ggplot2")
library('argparse')
p="argparse"
parser <- ArgumentParser(description='ltr_divergence_time_plot analysis')

parser$add_argument( "-i", "--input_ltr_time", type="character",required=T,
                     help="input the ltr time file [required]",
                     metavar="filepath")
parser$add_argument( "-p", "--outFilePrefix", type="character",required=F,default="ltr_div_time",
                     help="output file prefix [default %(default)s]",
                     metavar="filepath")
parser$add_argument( "-o", "--outdir", type="character", default=getwd(),
                     help="output file directory [default %(default)s]",
                     metavar="outdir")
parser$add_argument( "-H", "--height", type="double", default=5,required=F,
                     help="the height of pic   inches  [default %(default)s]",
                     metavar="height")
parser$add_argument("-W", "--width", type="double", default=5,required=F,
                    help="the width of pic   inches [default %(default)s]",
                    metavar="width")
opt <- parser$parse_args()
if( !file.exists(opt$outdir) ){
  dir.create(opt$outdir, showWarnings = FALSE, recursive = TRUE)
}


# ————————————————————————————————————————————————————————————————————
# line pic
# ————————————————————————————————————————————————————————————————————
time_d = read.table(opt$input_ltr_time,header = F,sep="\t",comment.char = "#" )

colnames(time_d)<-c("LTR_loc","Category","Motif",   "TSD",     "5_TSD", "3_TSD", 
                    "Internal",        "Identity"  ,    "Strand" , "SuperFamily"  ,"TE_type",
                    "Insertion_Time")


time_d=time_d[which(time_d$TE_type == 'LTR'),]
time_d$Insertion_Time=time_d$Insertion_Time/1000000

head(time_d)
gra_3<-ggplot(time_d,aes(Insertion_Time))+
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) +
  geom_density(stat = "bin",bins = 50, col = 'red3')+
  labs(x = "time(million years)", fill = NULL) +
  theme_bw()+
  theme(panel.grid=element_blank())

ggsave(gra_3,filename = paste0(opt$outdir,'/',opt$outFilePrefix,'.png'),width = opt$width,height = opt$height)
ggsave(gra_3,filename = paste0(opt$outdir,'/',opt$outFilePrefix,'.pdf'),width = opt$width,height = opt$height)
