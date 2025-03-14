import argparse
import re

def parse_args():
    """定义命令行参数解析器。"""
    parser = argparse.ArgumentParser(description="统计 RNA 类型信息")
    parser.add_argument("-in", "--input", required=True, help="输入文件 (genome.tblout.final.xls)")
    parser.add_argument("-o", "--output", required=True, help="输出文件 (noncoding.stat.xls)")
    return parser.parse_args()

def process_file(input_file):
    """读取输入文件，统计不同 RNA 类型的信息。"""
    stat = {}

    with open(input_file, 'r') as infile:
        for line in infile:
            line = line.strip()
            if line.startswith("#"):  # 跳过注释行
                continue

            fields = line.split("\t")
            if len(fields) < 9:  # 确保行有足够的列
                continue

            rna_type = fields[2]
            if rna_type == "gene":  # 跳过基因行
                continue

            length = abs(int(fields[4]) - int(fields[3])) + 1  # 计算长度

            # 统计 tRNA
            if rna_type == "tRNA":
                stat.setdefault("tRNA", [0, 0])
                stat["tRNA"][0] += 1
                stat["tRNA"][1] += length

            # 统计 rRNA 及其子类型
            elif rna_type == "rRNA":
                stat.setdefault("rRNA", [0, 0])
                stat["rRNA"][0] += 1
                stat["rRNA"][1] += length

                # 匹配 rRNA 子类型，包括 5_8s
                subtype_match = re.search(r'ID=(.+?)_rRNA|ID=(5_8s)', fields[8])
                if subtype_match:
                    subtype = subtype_match.group(1) or subtype_match.group(2)
                    if subtype:
                        stat.setdefault(subtype, [0, 0])
                        stat[subtype][0] += 1
                        stat[subtype][1] += length

    # 计算平均长度
    for key in stat:
        if stat[key][0] > 0:
            stat[key].append(round(stat[key][1] / stat[key][0], 2))
        else:
            stat[key].append(0)

    return stat

def write_output(stat, output_file):
    """将统计结果输出到指定文件中。"""
    order = ["tRNA", "rRNA", "5s", "5_8s", "8s", "18s", "28s"]  # 输出顺序

    with open(output_file, 'w') as outfile:
        outfile.write("Type\tClass\tNumber\tTotal length(bp)\tAverage length(bp)\n")

        for rna_type in order:
            if rna_type not in stat:
                continue

            class_type = rna_type if rna_type in ["tRNA", "rRNA"] else ""  # 分类信息

            num = f"{stat[rna_type][0]:,}"
            total_length = f"{stat[rna_type][1]:,}"
            avg_length = f"{stat[rna_type][2]:,}"

            outfile.write(f"{rna_type}\t{class_type}\t{num}\t{total_length}\t{avg_length}\n")

def main():
    args = parse_args()
    stat = process_file(args.input)
    write_output(stat, args.output)

if __name__ == "__main__":
    main()
