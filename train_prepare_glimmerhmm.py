import sys

# 确保提供了正确的命令行参数
if len(sys.argv) != 4:
    print(f"用法: python {sys.argv[0]} <gff文件> <基因组fasta文件> <cds位置输出文件>")
    sys.exit(1)

# 读取命令行参数
gff_file = sys.argv[1]
genome_file = sys.argv[2]
cds_output_file = sys.argv[3]

scaffold_names = []  # 存储scaffold名称
seq_dict = {}  # 用于存储序列信息（未实际使用）
hash_dict = {}  # 用于存储CDS信息
strand_dict = {}  # 记录每个基因的链信息

# 读取基因组fasta文件，获取scaffold名称
with open(genome_file, 'r') as gf:
    for line in gf:
        line = line.strip()
        if line.startswith('>'):
            scaffold_id = line[1:].split()[0]  # 提取scaffold ID
            scaffold_names.append(scaffold_id)

# 解析GFF文件，提取CDS信息
with open(gff_file, 'r') as gff:
    for line in gff:
        line = line.strip()
        fields = line.split()
        if len(fields) < 9:
            continue  # 跳过格式不完整的行
        
        scaffold_name = fields[0]  # scaffold名称
        feature_type = fields[2]  # GFF记录的类型
        strand = fields[6]  # 链方向
        
        # 仅处理exon类型
        if feature_type == "exon":
            gene_name = None
            for attr in fields[8].split(';'):
                if attr.startswith("Parent="):
                    gene_name = attr.split("=")[1]
                    break
            
            if not gene_name:
                continue  # 如果找不到Parent属性，则跳过
            
            strand_dict[gene_name] = strand  # 记录基因的链方向
            
            # 由于GFF是1-based，而Python是0-based，因此坐标保持一致
            start, end = int(fields[3]), int(fields[4])
            
            if strand == "-":
                cds_entry = [scaffold_name, end, start]  # 负链：高坐标在前
            else:
                cds_entry = [scaffold_name, start, end]  # 正链：低坐标在前
            
            if scaffold_name not in hash_dict:
                hash_dict[scaffold_name] = {}
            if gene_name not in hash_dict[scaffold_name]:
                hash_dict[scaffold_name][gene_name] = []
            
            hash_dict[scaffold_name][gene_name].append(cds_entry)

# 将提取的信息写入cds_output_file
with open(cds_output_file, 'w') as output:
    for scaffold_name in scaffold_names:
        if scaffold_name in hash_dict:
            for gene_name in sorted(hash_dict[scaffold_name], key=lambda g: hash_dict[scaffold_name][g][0][1]):
                
                if gene_name not in strand_dict:
                    print(f"基因 {gene_name} 在GFF文件中没有链信息", file=sys.stderr)
                    sys.exit(1)
                
                cds_list = hash_dict[scaffold_name][gene_name]
                if strand_dict[gene_name] == "-":
                    cds_list.sort(key=lambda x: x[1], reverse=True)  # 负链按坐标降序
                else:
                    cds_list.sort(key=lambda x: x[1])  # 正链按坐标升序
                
                for cds in cds_list:
                    output.write("\t".join(map(str, cds)) + "\n")
                
                output.write("\n")  # 每个基因之间留空行

