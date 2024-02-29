from openai import OpenAI
import pandas as pd

def llm_get_scores(question, true_answer, model_answer):
	response = client.completions.create(
  		model="qwen-14b",
  		prompt= (
			"请你按照以下评分标准对模型回答进行打分，满分10分，顺便给出理由。\n"
                        "评分标准：比较给出的模型回答和标准回答，如果标准回答中最终的确认故障原因能与模型回答中的某条故障原因匹配，则给分为满分10分，否则给0分。\n\n"
			"这有一个例子，问题是：'故障现象：某配套FANUC6M的立式加工中心，在长期停用后首次开机，出现电源无法接通的故障。'标准回答是：'分析及处理过程对照以上原理图4–1，经测量电源输入单元TP1，输入U/V为200V正常，但检查U1、V1端无AC200V。由图4–1可见，其故障原因应为F1、F2熔断，经测量确认F1、F2已经熔断。进一步检查发现，输入单元的TP3上200A/200B间存在短路。为了区分故障部位，取下TP3上的200A、200B连线，进行再次测量，确认故障在输入单元的外部。检查线路发现200A、200B电缆绝缘破损。在更换电缆、熔断器F1、F2，排除短路故障后，机床恢复正常。'\n给出的模型回答是：'根据提供的信息，故障现象描述为：在长期停用后首次开机，出现电源无法接通的故障。根据这个故障现象，我们可以考虑以下几种可能的问题：1. 输入单元的发光二极管 PIL 不亮，内部无 DC24V 电压：这种情况下，可以检查 Q1、DS1、C1 与 F3 等元器件是否良好。如果其中某个元器件出现问题，则需要更换相应的元器件。2. 输入单元的 F3 已经熔断：如果输入单元的 F3 已经熔断，则需要更换新的 F3 元件。3. 偶然性的过电流引起：如果上述两种情况都排除了，则可能是由于偶然性的过电流引起的问题。这种情况下，建议检查电路是否有短路或其他异常情况，并进行相应的维修。因此，根据已知的故障现象相关问题，可能的问题和解决方案如下：1.熔断问题；2.输入单元的发光二极管PI不亮；3.内部无 DC24V 电压问题；4. 偶然性的过电流引起问题'\n。所以能够得到10分。原因如下：由于最终原因是输入单元的TP3上200A/200B间存在短路，而模型回答中给出的原因有1. 输入单元的发光二极管 PIL 不亮，内部无 DC24V 电压；2.输入单元的 F3 已经熔断；3.偶然性的过电流引起。因为第3种情况提到了短路，能够匹配TP3上200A/200B间存在短路的故障现象，所以得分为10。\n\n"
			 f"现在，需要你评判的问题是：{question}\n"
			 f"标准回答是：{true_answer}\n"
			 f"模型回答是：{model_answer}\n"
			  "根据评分标准和例子，你的输出是：\n得分："
			),
  		max_tokens=4096,
  		temperature=1.0)
	
	response = response.choices[0].text
	print(response,"\n")
	return response

client = OpenAI(api_key="none", base_url="http://127.0.0.1:8000/v1")

data = pd.read_csv('机床维修例子_output.csv')
model_data = pd.read_csv('qwen_questions_answers_property_300.csv')
test_questions = data['故障现象']
true_answers = data['分析过程']
model_answers = model_data['answers']
    
print(len(test_questions))
answers = []
for question, true_answer, model_answer in zip(test_questions, true_answers, model_answers):
    #print(question)
    answer = llm_get_scores(question, true_answer, model_answer)
    answers.append(answer)

data = pd.DataFrame({'questions': test_questions, 'ture_answers': true_answers, 'model_answers': model_answers, 'scores': answers})
data.to_csv('qwen_scores_300.csv', index=False)



#print(completion.choices[0].message)

