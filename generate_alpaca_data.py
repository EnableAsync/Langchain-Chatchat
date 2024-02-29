import pandas as pd
from tqdm import tqdm
import os
import json
import random


from server.knowledge_base.kb_service import faiss_kb_service
from server.knowledge_base.utils import KnowledgeFile, get_kb_path, get_vs_path
from pprint import pprint

knowledge_base_name = "test_book_data"
top_k = 3
score_threshold = 1.0
prompt_name = "default"
max_tokens = 4096

# 获取文件路径函数
def get_files(dir_path):
    # args：dir_path，目标文件夹路径
    file_list = []
    for filepath, dirnames, filenames in os.walk(dir_path):
        # os.walk 函数将递归遍历指定文件夹
        for filename in filenames:
            # 通过后缀名判断文件类型是否满足要求
            if filename.endswith(".csv"):
                # 如果满足要求，将其绝对路径加入到结果列表
                file_list.append(os.path.join(filepath, filename))

    return file_list

# 获取文件路径函数
def get_files_name(dir_path):
    # args：dir_path，目标文件夹路径
    file_list = []
    for filepath, dirnames, filenames in os.walk(dir_path):
        # os.walk 函数将递归遍历指定文件夹
        for filename in filenames:
            # 通过后缀名判断文件类型是否满足要求
                # 如果满足要求，将其绝对路径加入到结果列表
            file_list.append(filename)

    return file_list

def get_all_df(dir_path):
    # args：dir_path，目标文件夹路径
    # 首先调用上文定义的函数得到目标文件路径列表
    file_lst = get_files(dir_path)
    # docs 存放所有 df
    docs = pd.DataFrame({'questions': [], 'answers': []})
    # 遍历所有目标文件
    for one_file in tqdm(file_lst):
        file_type = one_file.split('.')[-1]
        if file_type == 'csv':
            csv_data = pd.read_csv(one_file)
        else:
            # 如果是不符合条件的文件，直接跳过
            continue
        docs = pd.concat([docs, csv_data], ignore_index=True)
    return docs

def load_files():
    # 目标文件夹
    tar_dir = [
        "tuning_data/cleaned_data"
    ]

    # 加载目标文件
    docs = pd.DataFrame({'questions': [], 'answers': []})
    for dir_path in tar_dir:
        docs = pd.concat([docs, get_all_df(dir_path)], ignore_index=True)
    return docs


def df_to_alpaca(df):
    alpaca_data = []
    for index, row in df.iterrows():
        # print(f'Index: {index}, A: {row["A"]}, B: {row["B"]}')
        question = f"{row['questions']}"
        answer = f"{row['answers']}"
        data = {
            "instruction": "你是一个专业的机床维修工人,你需要帮我分析出问题中的故障现象的故障原因、故障原因的解决方案和排查手段",
            "input": question,
            "output": answer
        }
        alpaca_data.append(data)
    return alpaca_data

def df_to_qwen(df):
    qwen_data = []
    for index, row in df.iterrows():
        question = f"{row['questions']}"
        faissService = faiss_kb_service.FaissKBService(knowledge_base_name)
        docs = faissService.search_docs(question, top_k, score_threshold)
        context = "\n".join([doc[0].page_content for doc in docs])
        # pprint(context)
        answer = f"{row['answers']}"
        data = {
            "id": f"identity_{index}",
            "conversations": [
              {
                "from": "user",
                "value": f"已知信息：{context}\n\n问题：{question}"
              },
              {
                "from": "assistant",
                "value": answer
              }
            ]
        }
        qwen_data.append(data)
    return qwen_data

def generate_qwen_kb_json():
    df = load_files()
    print(df.head())
    print(df.shape)
    # data = df_to_alpaca(df)
    data = df_to_qwen(df)
    data = random.sample(data, len(data))
    # print(data)
    with open('9720-book-data-shuffle-qwen-kb.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)

def create_kb():
    faissService = faiss_kb_service.FaissKBService(knowledge_base_name)
    # 取到所有文件
    files = get_files_name("/home/kdzlys/data-disk/sjj/Langchain-Chatchat/knowledge_base/test_book_data/content")
    pprint(files)
    for file in files:
        faissService.add_doc(KnowledgeFile(file, knowledge_base_name))




if __name__ == "__main__":
    # create_kb()
    generate_qwen_kb_json()
