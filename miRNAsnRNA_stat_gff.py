#!/usr/bin/env python3
import sys
import re

def parse_gff(gff_file):
    data = {
        'miRNA': {'miRNA': {'count': 0, 'total_length': 0}},
        'snRNA': {
            'CD-box': {'count': 0, 'total_length': 0},
            'HACA-box': {'count': 0, 'total_length': 0},
            'splicing': {'count': 0, 'total_length': 0}
        }
    }

    with open(gff_file, 'r') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue

            fields = line.strip().split('\t')
            if len(fields) < 9:
                continue

            start = int(fields[3])
            end = int(fields[4])
            strand = fields[6]
            attributes = fields[8]

            # 计算序列长度
            length = abs(end - start) + 1

            # 用正则表达式提取 Family 字段（匹配引号内的内容）
            match = re.search(r'Family="([^"]+)"', attributes)
            family_info = match.group(1) if match else None

            # 打印调试信息，确认提取到的 Family 字段
            # print(f"Line: {line.strip()}")
            # print(f"Extracted Family: {family_info}")

            # 如果未找到 Family 字段，跳过该行
            if not family_info:
                print("No Family info found, skipping line.")
                continue

            # 分类并统计
            if 'miRNA' in family_info:
                # print(f"Found miRNA: Length={length}")
                data['miRNA']['miRNA']['count'] += 1
                data['miRNA']['miRNA']['total_length'] += length
            elif 'CD-box' in family_info:
                # print(f"Found CD-box: Length={length}")
                data['snRNA']['CD-box']['count'] += 1
                data['snRNA']['CD-box']['total_length'] += length
            elif 'HACA-box' in family_info:
                # print(f"Found HACA-box: Length={length}")
                data['snRNA']['HACA-box']['count'] += 1
                data['snRNA']['HACA-box']['total_length'] += length
            elif 'splicing' in family_info:
                # print(f"Found splicing: Length={length}")
                data['snRNA']['splicing']['count'] += 1
                data['snRNA']['splicing']['total_length'] += length

    return data

def write_output(output_file, data):
    with open(output_file, 'w') as out:
        # 输出表头
        out.write('Type\tClass\tNumber\tTotal length(bp)\tAverage length(bp)\n')

        # 处理 miRNA
        miRNA_count = data['miRNA']['miRNA']['count']
        miRNA_total_length = data['miRNA']['miRNA']['total_length']
        if miRNA_count > 0:
            miRNA_avg_length = round(miRNA_total_length / miRNA_count, 2)
            out.write(f"miRNA\tmiRNA\t{miRNA_count}\t{miRNA_total_length}\t{miRNA_avg_length}\n")

        # 统计 snRNA 总类
        snRNA_count = sum(data['snRNA'][subclass]['count'] for subclass in data['snRNA'])
        snRNA_total_length = sum(data['snRNA'][subclass]['total_length'] for subclass in data['snRNA'])
        if snRNA_count > 0:
            snRNA_avg_length = round(snRNA_total_length / snRNA_count, 2)
            # ✅ 提前输出 snRNA 总类统计行
            out.write(f"snRNA\tsnRNA\t{snRNA_count}\t{snRNA_total_length}\t{snRNA_avg_length}\n")

        # 输出 snRNA 子类统计行
        for subclass in ['CD-box', 'HACA-box', 'splicing']:
            count = data['snRNA'][subclass]['count']
            total_length = data['snRNA'][subclass]['total_length']
            if count > 0:
                avg_length = round(total_length / count, 2)
                out.write(f"snRNA\t{subclass}\t{count}\t{total_length}\t{avg_length}\n")

def main():
    if len(sys.argv) != 3:
        print("用法: python stat_gff.py <输入文件> <输出文件>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # 解析 GFF 文件
    data = parse_gff(input_file)

    # 输出统计结果
    write_output(output_file, data)

    print(f"统计结果已输出到 {output_file}")

if __name__ == "__main__":
    main()

