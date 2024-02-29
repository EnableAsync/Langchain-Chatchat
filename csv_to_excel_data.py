import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import Workbook

# 读取 UTF-8 编码的 CSV 文件
data = pd.read_csv('kb_qwen_questions_answers_property_100_tuning_book.csv', encoding='utf-8')

# 创建一个新的 Excel workbook 对象
workbook = Workbook()

# 创建一个 Excel sheet
sheet = workbook.active

# 将 DataFrame 转换为 rows，并写入 Excel sheet
for row in dataframe_to_rows(data, index=False, header=True):
    sheet.append(row)

# 保存为 GBK 编码的 Excel 文件
workbook.save('kb_qwen_questions_answers_property_100_tuning_book.csv.xlsx')