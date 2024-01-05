from server.knowledge_base.kb_service import faiss_kb_service
from server.knowledge_base.utils import KnowledgeFile, get_kb_path, get_vs_path
from pprint import pprint

knowledge_base_name = "test_200"
top_k = 3
score_threshold = 0.8
prompt_name = "default"
max_tokens = 16384

def process_csv():
    import pandas as pd
    df = pd.read_csv('/home/kdzlys/data-disk/sjj/Baichuan2/机床维修例子_output.csv')
    pprint(df.head())
    # 选择特定的几列
    selected_columns = ['故障现象', '分析过程']
    # 提取特定的几列，保存到新的 DataFrame 中
    df = df.loc[:, selected_columns]
    # 随机选择 200 行数据
    random_rows = df.sample(n=200, random_state=42)
    # 将结果保存到新的文件或者进行进一步处理
    random_rows.to_csv(f'knowledge_base/{knowledge_base_name}/content/机床维修案例_200.csv', index=False)  # 将数据保存到 CSV 文件中，不保存行索引

    # 从剩下的数据中随机选择 100 条数据
    remaining_data = df.drop(random_rows.index)  # 剩下的数据
    remaining_data.to_csv(f'knowledge_base/{knowledge_base_name}/content/机床维修案例_100.csv', index=False)

def process_kb():
    faissService = faiss_kb_service.FaissKBService(knowledge_base_name)
    faissService.add_doc(KnowledgeFile("机床维修案例_200.csv", knowledge_base_name))
    # faissService.delete_doc(KnowledgeFile("README.md", "test"))
    # faissService.do_drop_kb()

def delete_kb():
    faissService = faiss_kb_service.FaissKBService(knowledge_base_name)
    # faissService.add_doc(KnowledgeFile("机床维修案例_200.csv", "test_200"))
    faissService.do_drop_kb()

def search_kb(query = "开机时系统出现报警ALM950：FUSEBREAK"):
    faissService = faiss_kb_service.FaissKBService(knowledge_base_name)
    pprint(faissService.search_docs(query, top_k, score_threshold))

def generate_answer(query):
    from openai import OpenAI

    client = OpenAI(api_key="none", base_url="http://127.0.0.1:8000/v1")

    faissService = faiss_kb_service.FaissKBService(knowledge_base_name)
    docs = faissService.search_docs(query, top_k, score_threshold)
    # pprint(docs)
    context = "\n".join([doc[0].page_content for doc in docs])
    if len(docs) == 0:  # 如果没有找到相关文档，使用empty模板
        prompt_template = ('你是一个专业的机床维修工人,你需要帮我分析出问题中的故障现象的故障原因、故障原因的解决方案和排查手段\n\n'
        '例如用户输入：某配套FANUC6M的立式加工中心，开机时发现系统电源无法正常接通。你的输出为：分析及处理过程：经检查，该机床输人单元的发光二极管PIL不亮，内部无DC24V电压，对照原理图4–2可知，可能的原因为Q1、DS1、C1与F3等元器件不良。逐一检查以上元器件，发现输入单元的F3已经熔断，其他元器件均无故障。更换F3后开机试验，机床随即恢复正常，证明故障是偶然性的过电流引起的。\n\n'
        f'现在用户的问题是：{query}，你可以尽可能详细地说出原因，并给出详细的解决方案，并按可能性顺序输出可能的原因和解决方案，所以你的输出是：')
    else:
        prompt_template = ('你是一个专业的机床维修工人,你需要根据已知信息帮我分析出问题中的故障现象的故障原因、故障原因的解决方案和排查手段\n\n'
                           f'已知信息：{context}\n\n'
        '例如用户输入：某配套FANUC6M的立式加工中心，开机时发现系统电源无法正常接通。你的输出为：分析及处理过程：经检查，该机床输人单元的发光二极管PIL不亮，内部无DC24V电压，对照原理图4–2可知，可能的原因为Q1、DS1、C1与F3等元器件不良。逐一检查以上元器件，发现输入单元的F3已经熔断，其他元器件均无故障。更换F3后开机试验，机床随即恢复正常，证明故障是偶然性的过电流引起的。\n\n'
        f'现在用户的问题是：{query}，你可以参照已知信息尽可能详细地说出原因，并给出详细的解决方案，并按可能性顺序输出可能的原因和解决方案，所以你的输出是：')
    pprint(prompt_template)

    response = client.completions.create(
        model="qwen-14b",
        prompt=prompt_template,
        max_tokens=4096,
        temperature=1.0
    )
    source_documents = []
    for inum, doc in enumerate(docs):
        doc = doc[0]
        filename = doc.metadata.get("source")
        text = f"""出处 [{inum + 1}] [{filename}] \n\n{doc.page_content}\n\n"""
        source_documents.append(text)
    if len(source_documents) == 0:  # 没有找到相关文档
        source_documents.append(f"未找到相关文档,该回答为大模型自身能力解答！")
    pprint(source_documents)
    all_context = "\n\n".join([doc for doc in source_documents])
    print(response.choices[0].text)
    # pprint(all_context)
    return response.choices[0].text, all_context

def test_config():
    from configs.model_config import ONLINE_LLM_MODEL, MODEL_PATH
    print(ONLINE_LLM_MODEL.get("openai-api", {}))

# def test_llm():
#     from langchain_community.llms.openai import OpenAI
#     from langchain_community.chat_models import ChatOpenAI
#     from langchain.schema import HumanMessage

#     model = OpenAI(
#         streaming=False,
#         verbose=True,
#         openai_api_key="EMPTY",
#         openai_api_base="http://127.0.0.1:8000/v1",
#         model_name="qwen-14b",
#         temperature=1.0,
#         max_tokens=max_tokens,
#     )

#     pprint(model)
#     text = "你好，我是"
#     pprint(model.invoke(text))

def generate_csv():
    import pandas as pd
    data = pd.read_csv('机床维修案例_200.csv')
    # print(data)
    # cleaned_data = data.dropna(subset=['故障现象'])
    # print(cleaned_data)

    test_questions = data['故障现象']
    print(len(test_questions))
    answers = []
    contexts = []
    for question in test_questions:
        print(question)
        answer, context = generate_answer(question)
        answers.append(answer)
        contexts.append(context)

    data = pd.DataFrame({'questions': test_questions, 'answers': answers, 'contexts': contexts})
    data.to_csv('kb_qwen_questions_answers_property_200.csv', index=False)

def generate_csv2():
    import pandas as pd
    data = pd.read_csv('机床维修案例_100.csv')
    # print(data)
    # cleaned_data = data.dropna(subset=['故障现象'])
    # print(cleaned_data)

    test_questions = data['故障现象']
    print(len(test_questions))
    answers = []
    contexts = []
    for question in test_questions:
        print(question)
        answer, context = generate_answer(question)
        answers.append(answer)
        contexts.append(context)

    data = pd.DataFrame({'questions': test_questions, 'answers': answers, 'contexts': contexts})
    data.to_csv('kb_qwen_questions_answers_property_100.csv', index=False)

def get_answer(prompt):
    from openai import OpenAI
    client = OpenAI(api_key="none", base_url="http://127.0.0.1:8000/v1")
    response = client.completions.create(
        model="qwen-14b",
        prompt=prompt,
        max_tokens=4096,
        temperature=1.0
    )
    return response.choices[0].text


def llm_get_scores(question, true_answer, model_answer):
    prompt = ('你是一个阅卷老师，请针对模型回答给出得分，满分10分，顺便给出理由。\n'
              f'问题：{question}\n'
              f'标准回答：{true_answer}\n\n'
              f'模型回答：{model_answer}\n\n'
              '所以你的输出是：\n得分：')
    answer = get_answer(prompt)
    print(answer, "\n")
    return answer

def score_csv_100():
    import pandas as pd
    data = pd.read_csv('机床维修案例_100.csv')
    model_data = pd.read_csv('kb_qwen_questions_answers_property_100.csv')
    test_questions = data['故障现象']
    true_answers = data['分析过程']
    model_answers = model_data['answers']
    
    print(len(test_questions))
    answers = []
    for question, true_answer, model_answer in zip(test_questions, true_answers, model_answers):
        print(question)
        answer = llm_get_scores(question, true_answer, model_answer)
        answers.append(answer)

    data = pd.DataFrame({'questions': test_questions, 'ture_answers': true_answers, 'model_answers': model_answers, 'scores': answers})
    data.to_csv('qwen_scores_100.csv', index=False)

def score_csv_200():
    import pandas as pd
    data = pd.read_csv('机床维修案例_200.csv')
    model_data = pd.read_csv('kb_qwen_questions_answers_property_200.csv')
    test_questions = data['故障现象']
    true_answers = data['分析过程']
    model_answers = model_data['answers']
    
    print(len(test_questions))
    answers = []
    for question, true_answer, model_answer in zip(test_questions, true_answers, model_answers):
        print(question)
        answer = llm_get_scores(question, true_answer, model_answer)
        answers.append(answer)

    data = pd.DataFrame({'questions': test_questions, 'ture_answers': true_answers, 'model_answers': model_answers, 'scores': answers})
    data.to_csv('qwen_scores_200.csv', index=False)


if __name__ == '__main__':
    # process_csv()
    # process_kb()
    # delete_kb()
    # search_kb()

    # test_config()
    # generate_answer("手动操作Z轴时有振动和异常响声")
    # generate_csv()
    # generate_csv2()
    score_csv_100()
    score_csv_200()
    pass


