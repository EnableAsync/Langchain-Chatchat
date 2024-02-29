import pandas as pd

base_path = "tuning_data"
train_path = f"{base_path}/all_data"
output_path = f"{base_path}/cleaned_data"

def get_origin_full_path(filename):
    return f"{train_path}/{filename}"

def get_output_full_path(filename):
    return f"{output_path}/{filename}"

def rename_column(df):
    # 获取前两列的列名
    old_column_names = df.columns[:2]

    # 生成新的列名
    new_column_names = ['questions', 'answers']

    # 使用字典将旧列名映射到新列名，然后使用rename函数
    column_mapping = dict(zip(old_column_names, new_column_names))
    df = df.rename(columns=column_mapping)



def merge_unnamed_column(filename):
    df = pd.read_csv(get_origin_full_path(filename))
    print(df.shape)
    # 打印DataFrame，查看所有列名
    print("DataFrame 列名：", df.columns)

    # 找到未命名的列
    unnamed_columns = [col for col in df.columns if not col]

    # 合并未命名的列成新的列
    df['all_answer'] = df[unnamed_columns].apply(lambda row: ''.join(map(str, row)), axis=1)
    df['分析过程'] = df['分析过程'] + df['all_answer']
    print(df.shape)
    df = df.rename(columns={'故障现象': 'questions', '分析过程': 'answers'})
    df = df[['questions', 'answers']]
    df.to_csv(get_output_full_path(filename), index=False)


def drop_not_full(filename):
    data = pd.read_csv(get_origin_full_path(filename))
    print(data.shape)
    data = data[data['other'].notna()]
    print(data.shape)
    # data.to_csv()
    
def delete_start_char(filename):
    df = pd.read_csv(get_origin_full_path(filename))
    print(df.shape)
    df['questions'] = df['问题'].str.replace("问题:", '', case=False)
    df['answers'] = df['答案'].str.replace("答案:", '', case=False)
    print(df.shape)
    df = df[['questions', 'answers']]
    df.to_csv(get_output_full_path(filename), index=False)

def json_to_csv(filename):
    import json

    with open(get_origin_full_path(filename), 'r', encoding='utf-8') as file:
        data = json.load(file)

    result = "questions,answers\n"

    for i, item in enumerate(data):
        item['question'] = item['question'].replace(",", "，")
        item['answer'] = item['answer'].replace(",", "，")
        sample = f"{item['question']},{item['answer']}\n"
        result += sample
    with open(get_output_full_path(filename), 'w', encoding='utf-8') as file:
        file.write(result)

def execl_to_csv(filename):
    import pandas as pd
    from openpyxl import load_workbook

    # 读取Excel文件
    wb = load_workbook(get_origin_full_path(filename))

    # 选择要读取的表格
    sheet = wb['Sheet1']  # 更改为你的表格名称

    # 从Excel读取数据
    data = sheet.values

    # 将数据转换为pandas DataFrame
    df = pd.DataFrame(data)

    df['questions'] = df['questions'].replace(to_replace='\d', value='', regex=True)
    df['answers'] = df['answers'].str.replace("答：", '', case=False)

    # 将DataFrame保存为CSV文件
    df.to_csv(get_output_full_path(filename), index=False, header=False)  # 可根据需要设置index和header参数

if __name__ == "__main__":
    # drop_not_full("242-机床维修例子_output.csv")
    # merge_unnamed_column("1646-数控机床故障诊断与维修-多条(改).csv")
    # delete_start_char("1648-数控机床维修500例数据.csv")
    # delete_start_char("3601-组合车床设计（第一册）.csv")
    # json_to_csv("500-data.json")
    # execl_to_csv("367-pdf2数据-存在数字.xlsx")
    # delete_start_number() ^(\d|"\\d)

    pass



# bash finetune/finetune_lora_ds.sh --deepspeed finetune/ds_config_zero3.json