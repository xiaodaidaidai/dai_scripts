import argparse

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='生成基因存在-缺失矩阵文件')
    parser.add_argument('--pangenel', required=True, help='泛基因组基因列表文件')
    parser.add_argument('--spid', required=True, help='物种ID列表文件')
    parser.add_argument('--unigenel', required=True, help='物种特有基因列表文件')
    parser.add_argument('--fam', required=True, help='家族名称前缀')
    return parser.parse_args()

def read_file(filename):
    """读取文件内容并返回去除空行的列表"""
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def process_pangenes(pangenel_file):
    """处理泛基因文件，返回按家族分类的基因字典"""
    pangene_dict = {}
    for line in read_file(pangenel_file):
        parts = line.split('\t')
        if len(parts) >= 2:
            fam = parts[0]
            gene = parts[1]
            pangene_dict.setdefault(fam, []).append(gene)
    return pangene_dict

def generate_pav_gene(pangene_dict, species_ids, unique_genes, fam_prefix):
    """生成PAV_gene.list文件内容"""
    output = []
    # 构建表头
    output.append("Fam_N\t" + "\t".join(species_ids))
    
    m = 0
    # 处理泛基因家族
    for fam in sorted(pangene_dict.keys()):
        m += 1
        row = [f"{fam_prefix}{m}"]
        genes = pangene_dict[fam]
        # 按物种顺序匹配基因
        for sp in species_ids:
            matches = [gene for gene in genes if f"_{sp}" in gene]
            # 基因列表用分号连接，末尾保留分号
            row.append(";".join(matches) + (";" if matches else ""))
        output.append("\t".join(row))
    
    # 处理特有基因
    for gene in unique_genes:
        m += 1
        row = [f"{fam_prefix}{m}"]
        for sp in species_ids:
            # 每个物种列只保留对应物种的基因
            cell = f"{gene};" if f"_{sp}" in gene else ""
            row.append(cell)
        output.append("\t".join(row))
    
    return output

def generate_pav_draw(pav_gene_content):
    """生成PAV_draw.list文件内容，统计各物种基因数量"""
    output = []
    if not pav_gene_content:
        return output
    
    # 添加表头
    output.append(pav_gene_content[0])
    
    # 处理数据行
    for line in pav_gene_content[1:]:
        parts = line.split('\t')
        fam = parts[0]
        counts = []
        # 统计每个物种列的分号数量（基因数量）
        for cell in parts[1:]:
            count = cell.count(';') if cell else 0
            counts.append(str(count))
        # 构建结果行
        output.append(f"{fam}\t" + "\t".join(counts))
    
    return output

def main():
    """主函数"""
    args = parse_arguments()
    
    # 读取输入文件
    species_ids = read_file(args.spid)
    unique_genes = read_file(args.unigenel)
    pangene_dict = process_pangenes(args.pangenel)
    
    # 生成PAV_gene.list内容
    pav_gene = generate_pav_gene(pangene_dict, species_ids, unique_genes, args.fam)
    with open('PAV_gene.list', 'w') as f:
        f.write("\n".join(pav_gene) + "\n")
    
    # 生成PAV_draw.list内容
    pav_draw = generate_pav_draw(pav_gene)
    with open('PAV_draw.list', 'w') as f:
        f.write("\n".join(pav_draw) + "\n")

if __name__ == "__main__":
    main()
