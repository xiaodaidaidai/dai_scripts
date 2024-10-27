import sys
import os
import pandas as pd

def merge_txt_to_excel(file_list, output_prefix):
    # 创建一个新的Excel文件
    with pd.ExcelWriter(f"{output_prefix}_merged.xlsx") as writer:
        # 遍历指定的txt文件
        for file_path in file_list:
            # 读取txt文件
            df = pd.read_csv(file_path, sep="\t")
            # 使用文件名（不含路径和扩展名）作为sheet名称
            sheet_name = os.path.basename(file_path).replace('.txt', '')
            # 写入Excel的sheet
            df.to_excel(writer, sheet_name=sheet_name, index=False)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python merge_txt_to_excel.py <输出文件前缀> <文件1> <文件2> ...")
        sys.exit(1)

    output_prefix = sys.argv[1]
    file_list = sys.argv[2:]

    merge_txt_to_excel(file_list, output_prefix)
