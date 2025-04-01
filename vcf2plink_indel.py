import sys
from typing import List, Tuple

def process_header(header: List[str]) -> str:
    """处理VCF头部行，生成新的头部格式"""
    # 保留前2列，插入ID列，保留REF/ALT列，添加固定列，保留样本列
    required_columns = header[:2] + ["ID"] + header[3:5] + ["QUAL", "FILTER", "INFO", "FORMAT"] + header[9:]
    return "\t".join(required_columns) + "\n"

def process_data_line(fields: List[str]) -> str:
    """处理VCF数据行，提取所需信息并格式化"""
    # 提取基本字段
    chrom, pos, ref, alt = fields[0], fields[1], fields[3], fields[4]
    
    # 处理样本基因型数据
    sample_values = []
    for sample in fields[9:]:
        genotype = sample.split(":", 1)[0]  # 只分割第一个冒号，提高效率
        genotype = genotype.replace("|", "/")  # 标准化分隔符
        sample_values.append(genotype)
    
    # 组装固定字段
    fixed_fields = [
        chrom, pos, ".",  # ID设为默认值
        ref, alt, ".",    # QUAL设为默认值
        ".", "PR", "GT"   # FILTER, INFO, FORMAT
    ]
    
    return "\t".join(fixed_fields + sample_values) + "\n"

def extract_vcf_columns(input_vcf: str, output_file: str) -> None:
    """主处理函数，读取输入VCF并写入处理后的输出"""
    with open(input_vcf, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.startswith("#CHROM"):
                header = line.strip().split("\t")
                outfile.write(process_header(header))
            elif not line.startswith("#"):
                fields = line.strip().split("\t")
                outfile.write(process_data_line(fields))

def main() -> None:
    """命令行入口函数"""
    if len(sys.argv) != 3:
        print("Usage: python script.py <input.vcf> <output.vcf>", file=sys.stderr)
        sys.exit(1)
    
    input_vcf, output_file = sys.argv[1], sys.argv[2]
    extract_vcf_columns(input_vcf, output_file)

if __name__ == "__main__":
    main()
