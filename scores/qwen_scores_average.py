import pandas as pd
import re

data = pd.read_csv("qwen_scores_200.csv")
socres = data['scores']
print(len(socres))
all_socres = []

for score in socres:
    match = re.search(r"\d+", score)
    if match:
        current_score = match.group()
        # print(f"{current_score} --- {score[:10]}")
        all_socres.append(int(current_score))
    else:
        print(score)

if len(all_socres) != len(socres):
    print("Size error!")
else:
    print(f"Average accuracy: {sum(all_socres)/len(all_socres)*10.0:.2f}%")


# 42 59.76%
# 200 69.80%
    
# s1 / (42 * 100) = a1
# s2 / (200 * 100) = a2
    
# s1 = a1 * 42 * 100
# s2 = a2 * 200 * 100
    
# all average = (s1+s2) / (42*100 + 200*100)
# (a1 * 42 * 100 + a2 * 200 * 100) / (42*100 + 200*100)
# (a1 * 42 + a2 * 200) / (42 + 200)

print(f"All average accuracy: {(42*0.5976+200*0.698)/(42+200)*100:.2f}%")