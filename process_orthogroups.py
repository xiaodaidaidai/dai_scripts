import sys
import argparse

def process_orthogroups(input_file, output_file, species_labels):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # 写入表头
        outfile.write("panIDtrans\ttransChr_transStrand\n")
        
        # 读取并处理文件内容
        header = infile.readline().strip().split('\t')

        for line in infile:
            fields = line.strip().split('\t')
            orthogroup = fields[0]

            for i, genes in enumerate(fields[1:], start=0):
                if genes:
                    gene_list = genes.split(', ')
                    for gene in gene_list:
                        if i < len(species_labels):
                            outfile.write(f"{orthogroup}\t{gene}_{species_labels[i]}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process Orthogroups file")
    parser.add_argument("input_file", help="Input file path")
    parser.add_argument("output_file", help="Output file path")
    parser.add_argument("--species_labels", required=True,
                        help="Comma-separated list of species labels (e.g., 'Bau,Bsh,Bsy,Btu,Bva')")

    args = parser.parse_args()

    # 将逗号分隔的字符串转换为列表
    species_labels = args.species_labels.split(',')

    process_orthogroups(args.input_file, args.output_file, species_labels)
