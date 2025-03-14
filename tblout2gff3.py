#!/usr/bin/env python3
import sys

if len(sys.argv) != 3:
    sys.exit(f"Usage: {sys.argv[0]} <family_file> <tblout_file>\n")

family_file = sys.argv[1]
tblout_file = sys.argv[2]

# 从family文件中读取rfam_id和family信息
rfam_to_family = {}
with open(family_file, 'r') as fam:
    for line in fam:
        fields = line.strip().split('\t')
        rfam_id = fields[0]
        family = fields[18]
        rfam_to_family[rfam_id] = family

print("##gff-version 3")

with open(tblout_file, 'r') as tbl:
    for line in tbl:
        if line.startswith('#'):  # 跳过注释行
            continue
        fields = line.strip().split()
        seqid = fields[3]
        rfam_name = fields[1]
        start = fields[9]
        end = fields[10]
        strand = fields[11]
        rfam_id = fields[2]
        score = fields[16]
        evalue = fields[17]
        family = rfam_to_family.get(rfam_id, "NA")  # 如果没有找到family信息，则默认为"NA"
        print(f"{seqid}\tcmscan\tncRNA\t{start}\t{end}\t{score}\t{strand}\t.\tID={rfam_id};Name={rfam_name};Evalue={evalue};Family=\"{family}\"")
