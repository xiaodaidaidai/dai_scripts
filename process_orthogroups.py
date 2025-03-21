import sys

def process_orthogroups(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # 写入表头
        outfile.write("panIDtrans\ttransChr_transStrand\n")
        
        # 读取并处理文件内容
        header = infile.readline().strip().split('\t')
        species_labels = ['Bau', 'Bsh', 'Bsy', 'Btu', 'Bva']  # 你可以根据需要修改标签
        
        for line in infile:
            fields = line.strip().split('\t')
            orthogroup = fields[0]
            
            for i, genes in enumerate(fields[1:], start=1):
                if genes:
                    gene_list = genes.split(', ')
                    for gene in gene_list:
                        outfile.write(f"{orthogroup}\t{gene}_{species_labels[i-1]}\n")

if __name__ == "__main__":
    # 确保命令行参数正确
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    process_orthogroups(input_file, output_file)

