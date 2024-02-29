import re
import pandas as pd

def get_score(sentence):
    score_pattern = re.compile(r'得分：(\d+)|得分为(\d+)分|得(\d+)分|得分(\d+)分|答案：(\d+)分')
    
    # 以句号划分句子
    sentences = re.split(r'[。.！？]', sentence)
    # 去除空字符串
    sentences = [s.strip() for s in sentences if s.strip()]
    # 取得最后一句
    if sentences:
        last_sentence = sentences[-1]

    score_match = score_pattern.search(f"" + last_sentence)
    if score_match:
        score = next(group for group in score_match.groups() if group is not None)
        #print(f"匹配到得分： {score}")
        return score
    else:
        #print("未匹配到得分")
        return "-1"

model_data = pd.read_csv('/home/kdzlys/data-disk/sjj/Langchain-Chatchat/kb_qwen_questions_answers_property_100_top5_scores_book.csv')
model_scores = model_data['scores']
total_score = 0
total_epoch = 0

for model_score in model_scores:
    result = get_score(model_score)
    if result != "-1":
        total_score += int(result)
        total_epoch += 1

print("轮次为：", total_epoch, "\n")
print("总分为：", total_score, "\n")
print("均分为：", total_score/ total_epoch, "\n")