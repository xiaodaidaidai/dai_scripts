import sys

# 检查命令行参数
# 确保脚本接收两个输入参数：family文件和tblout文件
if len(sys.argv) != 3:
    sys.exit(f"Usage: {sys.argv[0]} <family_file> <tblout_file>")

# 获取命令行参数
family_file, tblout_file = sys.argv[1], sys.argv[2]

# 从family文件中读取rfam_id和family信息
# 创建一个字典来存储rfam_id与family之间的对应关系
rfam_to_family = {}
with open(family_file, 'r') as fam:
    for line in fam:
        line = line.strip()  # 去除行首行尾的空白字符（包括换行符）
        fields = line.split('\t')  # 按制表符（TAB）分割每一行
        if len(fields) > 18:  # 确保有足够的列数
            rfam_id, family = fields[0], fields[18]  # 第1列是rfam_id，第19列是family信息
            rfam_to_family[rfam_id] = family  # 将rfam_id与family信息存储到字典中

# 输出GFF文件的版本信息
print("##gff-version 3")

# 处理tblout文件
with open(tblout_file, 'r') as tbl:
    for line in tbl:
        if line.startswith('#'):
            continue  # 跳过以#号开头的注释行
        line = line.strip()  # 去除行首行尾的空白字符
        fields = line.split()  # 按空格或制表符分割每一行

        # 确保行中有足够的列数
        if len(fields) > 17:
            # 提取所需的字段
            seqid = fields[3]      # 第4列：序列ID
            rfam_name = fields[1]  # 第2列：rfam名称
            start = fields[9]      # 第10列：起始位置
            end = fields[10]       # 第11列：结束位置
            strand = fields[11]    # 第12列：链（正链或负链）
            rfam_id = fields[2]    # 第3列：rfam ID
            score = fields[16]     # 第17列：得分
            evalue = fields[17]    # 第18列：e值

            # 通过rfam_id在字典中查找family信息，若未找到，默认为"NA"
            family = rfam_to_family.get(rfam_id, "NA")

            # 格式化输出为GFF格式
            print(f"{seqid}\tcmscan\tncRNA\t{start}\t{end}\t{score}\t{strand}\t.\tID={rfam_id};Name={rfam_name};Evalue={evalue};Family=\"{family}\"")

