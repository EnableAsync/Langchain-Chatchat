from openai import OpenAI
import pandas as pd

def count_correct_and_wrong(string):
    correct_count = string.count("正确")
    wrong_count = string.count("错误")
    return correct_count > wrong_count

def llm_get_scores(question, true_answer, model_answer):
	completion1 = client.chat.completions.create(
 		 model="qwen-7b",
  		messages=[
     		{"role": "user", "content": f"现在你是一名阅卷老师，请你按照以下标准对模型回答进行正误判断，顺便给出理由。标准：比较给出的模型回答和标准回答，如果模型回答给出的解决方案中有能和标准回答给出的解决方案基本一致的，判断结果为正确，否则为错误，判断到此结束，最后输出判断结果。\n现在，给出的问题是：'故障现象：某配套FANUC6M的立式加工中心，在加工过程中，车间突然断电，恢复供电后，无法重新起动机床。'\n给出的标准回答是：'分析及处理过程对照以上原理图4–1，经测量电源输入单元TP1，输入U/V/?为200V正常，但检查U1、V1端无AC200V。由图4–1可见，其故障原因应为F1、F2熔断，经测量确认F1、F2已经熔断。进一步检查发现，输入单元的TP3上200A/200B间存在短路。为了区分故障部位，取下TP3上的200A、200B连线，进行再次测量，确认故障在输入单元的外部。检查线路发现200A、200B电缆绝缘破损。在更换电缆、熔断器F1、F2，排除短路故障后，机床恢复正常。'\n给出的模型回答是：'根据提供的信息，故障现象描述为：在长期停用后首次开机，出现电源无法接通的故障。根据这个故障现象，我们可以考虑以下几种可能的问题：1. 输入单元的发光二极管 PIL 不亮，内部无 DC24V 电压：这种情况下，可以检查 Q1、DS1、C1 与 F3 等元器件是否良好。如果其中某个元器件出现问题，则需要更换相应的元器件。2. 输入单元的 F3 已经熔断：如果输入单元的 F3 已经熔断，则需要更换新的 F3 元件。3. 偶然性的过电流引起：如果上述两种情况都排除了，则可能是由于偶然性的过电流引起的问题。这种情况下，建议检查电路是否有短路或其他异常情况，并进行相应的维修。因此，根据已知的故障现象相关问题，可能的问题和解决方案如下：1.熔断问题；2.输入单元的发光二极管PI不亮；3.内部无 DC24V 电压问题；4. 偶然性的过电流引起问题'\n。经过对标准，模型问答，标准问答的分析后，你应该有如下输出：'\n检查标准：由于标准回答中给出的解决方案是更换电缆、熔断器F1、F2，排除短路故障后，机床恢复正常，而模型回答中的解决方案：1.更换相应的元器件。2.更换新的 F3 元件。3.检查电路是否有短路或其他异常情况，并进行相应的维修。三者和标准回答中的解决方案虽有相似性，但不够准确，不能算基本一致，因此判断结果为错误，判断到此结束，最后输出判断结果：错误。'\n现在，给出的标准回答是：{true_answer}\n给出的模型回答是：{model_answer}\n，请你按照例子的格式输出答案："},       
   		]
	)

	sentence1 = completion1.choices[0].message.content
	if count_correct_and_wrong(sentence1):
		response = "该例按评分标准1进行评分："+sentence1+"由于判断正确，评分结束，不再往下检查标准，输出得分：10分。"
		print(response ,"\n")
		return response
	else:
		completion2 = client.chat.completions.create(
 			model="qwen-7b",
  			messages=[
     			{"role": "user", "content": f"现在你是一名阅卷老师，请你按照以下标准对模型回答进行正误判断，顺便给出理由。标准：比较给出的模型回答和标准回答，如果标准回答中最终的确认故障原因能与模型回答里给出的所有故障原因中的某一条基本一致的话，判断结果为正确，否则为错误，判断到此结束，最后输出判断结果。\n现在，给出的问题是：'故障现象：某配套FANUC6M的立式加工中心，在加工过程中，车间突然断电，恢复供电后，无法重新起动机床。'\n给出的标准回答是：'分析及处理过程对照以上原理图4–1，经测量电源输入单元TP1，输入U/V/?为200V正常，但检查U1、V1端无AC200V。由图4–1可见，其故障原因应为F1、F2熔断，经测量确认F1、F2已经熔断。进一步检查发现，输入单元的TP3上200A/200B间存在短路。为了区分故障部位，取下TP3上的200A、200B连线，进行再次测量，确认故障在输入单元的外部。检查线路发现200A、200B电缆绝缘破损。在更换电缆、熔断器F1、F2，排除短路故障后，机床恢复正常。'\n给出的模型回答是：'根据提供的信息，故障现象描述为：在长期停用后首次开机，出现电源无法接通的故障。根据这个故障现象，我们可以考虑以下几种可能的问题：1. 输入单元的发光二极管 PIL 不亮，内部无 DC24V 电压：这种情况下，可以检查 Q1、DS1、C1 与 F3 等元器件是否良好。如果其中某个元器件出现问题，则需要更换相应的元器件。2. 输入单元的 F3 已经熔断：如果输入单元的 F3 已经熔断，则需要更换新的 F3 元件。3. 偶然性的过电流引起：如果上述两种情况都排除了，则可能是由于偶然性的过电流引起的问题。这种情况下，建议检查电路是否有短路或其他异常情况，并进行相应的维修。因此，根据已知的故障现象相关问题，可能的问题和解决方案如下：1.熔断问题；2.输入单元的发光二极管PI不亮；3.内部无 DC24V 电压问题；4. 偶然性的过电流引起问题'\n。经过对标准，模型问答，标准问答的分析后，你应该有如下输出：'\n检查标准：由于最终原因是输入单元的TP3上200A/200B间存在短路，而模型回答中的故障原因有1.输入单元的发光二极管 PIL 不亮，内部无 DC24V 电压。2.输入单元的 F3 已经熔断。3.偶然性的过电流引起。三者虽然和最终故障原因虽然相似，但是不够准确，不能算基本一致，因此判断结果为错误，判断到此结束，最后输出判断结果：错误。'\n现在，给出的标准回答是：{true_answer}\n给出的模型回答是：{model_answer}\n，请你按照例子的格式输出答案："},       
   			]
		)
		sentence2 = completion2.choices[0].message.content
		if count_correct_and_wrong(sentence2):
			response = "该例按评分标准2进行评分："+sentence2+"由于判断正确，评分结束，不再往下检查标准，虽然匹配最终故障原因，但给出的解决方案未匹配，因此需要扣1分，输出得分：9分。"
			print(response ,"\n")
			return response
		else:
			completion4 = client.chat.completions.create(
 				model="qwen-7b",
  				messages=[
     				{"role": "user", "content": f"现在你是一名阅卷老师，请你按照评分标准对模型回答进行打分，满分8分，顺便给出理由。评分标准：按照故障原因的命中率来给分。比较给出的模型回答和标准回答，只要模型回答中的某1条故障原因能和标准回答中出现的某个故障现象产生的原因有一定关联性，则至少给分在5分以上。在已有基础分5分的条件下，如果模型回答中还有其他故障原因也能和标准回答中出现的某个故障现象产生的原因有一定关联性，则从5分开始加分，按出现1条加1分做加法运算：例如关联到1条加到6分后，继续检查后又关联到1条，则继续加1分到7分，以此类推，注意加分加到最后，得分不能超过满分8分，若超过则得8分，评分结束，不再往下检查标准，输出得分。如果未得到基础分5分，评分结束，则得0分，不再往下检查标准，输出得分。\n现在，给出的问题是：'故障现象：某配套FANUC6M的立式加工中心，在加工过程中，车间突然断电，恢复供电后，无法重新起动机床。'\n给出的标准回答是：'分析及处理过程对照以上原理图4–1，经测量电源输入单元TP1，输入U/V/?为200V正常，但检查U1、V1端无AC200V。由图4–1可见，其故障原因应为F1、F2熔断，经测量确认F1、F2已经熔断。进一步检查发现，输入单元的TP3上200A/200B间存在短路。为了区分故障部位，取下TP3上的200A、200B连线，进行再次测量，确认故障在输入单元的外部。检查线路发现200A、200B电缆绝缘破损。在更换电缆、熔断器F1、F2，排除短路故障后，机床恢复正常。'\n给出的模型回答是：'根据提供的信息，故障现象描述为：在长期停用后首次开机，出现电源无法接通的故障。根据这个故障现象，我们可以考虑以下几种可能的问题：1. 输入单元的发光二极管 PIL 不亮，内部无 DC24V 电压：这种情况下，可以检查 Q1、DS1、C1 与 F3 等元器件是否良好。如果其中某个元器件出现问题，则需要更换相应的元器件。2. 输入单元的 F3 已经熔断：如果输入单元的 F3 已经熔断，则需要更换新的 F3 元件。3. 偶然性的过电流引起：如果上述两种情况都排除了，则可能是由于偶然性的过电流引起的问题。这种情况下，建议检查电路是否有短路或其他异常情况，并进行相应的维修。因此，根据已知的故障现象相关问题，可能的问题和解决方案如下：1.熔断问题；2.输入单元的发光二极管PI不亮；3.内部无 DC24V 电压问题；4. 偶然性的过电流引起问题'\n。经过对标准，模型问答，标准问答的分析后，你应该有如下输出：'\n检查评分标准，标准回答中的故障原因有F1、F2熔断，TP3上200A/200B间存在短路，200A、200B电缆绝缘破损。而模型回答中的第三个原因：偶然性的过电流引起提到了短路，与标准答案中的TP3上200A/200B间存在短路有关联，因为模型回答虽未提及具体的短路部件，但也未随便给出一个和标准回答不同的错误短路部件，而且从故障范围来看，前者的范围包含了后者，由此可知二者存在关联性，因此按评分标准，模型回答中的某1条故障原因能和标准回答中出现的某个故障现象产生的原因有一定关联性的条件，则先得到基础分5分；继续检查发现模型回答的第二个原因中提到了输入单元F3熔断，标准问答中是输入单元F1、F2熔断，虽然熔断的具体部件不同，但是二者都提到了是输入单元这一部分发生熔断，从更大范围来说二者的说法具有一定关联性，因此按评分标准，模型回答中还有1个故障原因与标准问答某个故障现象产生的原因有关联，所以需要在基础分上加1分，通过加分运算5+1=6。继续检查，没有发现还有其他能关联的故障原因，所以不再继续加分，最终通过评分标准后检查得分为6分，评分结束，不再往下检查标准，输出得分：6分。'\n现在，给出的标准回答是：{true_answer}\n给出的模型回答是：{model_answer}\n，请你按照例子的格式输出答案："},       
   				]
			)
			response  = "该例按评分标准3进行评分："+completion4.choices[0].message.content
			print(response ,"\n")
			return response

	return "由于不满足标准1，标准2，标准3，所以该例的得分为0分。"

client = OpenAI(api_key="none", base_url="http://127.0.0.1:8000/v1")

def score_csv_200(column):
	# model_data = pd.read_csv(f'scores/kb_qwen_questions_answers_property_200_new_{column}.csv')
	model_data = pd.read_csv(f'kb_qwen_questions_answers_property_200_tuning_book.csv')
	data = pd.read_csv('scores/机床维修案例_200.csv')

	test_questions = model_data['questions']
	true_answers = data['分析过程']
	model_answers = model_data['answers']
		
	print(len(test_questions))
	answers = []
	for question, true_answer, model_answer in zip(test_questions, true_answers, model_answers):
		#print(question)
		answer = llm_get_scores(question, true_answer, model_answer)
		answers.append(answer)

	data = pd.DataFrame({'questions': test_questions, 'true_answers': true_answers, 'model_answers': model_answers, 'scores': answers})
	data.to_csv(f'kb_qwen_questions_answers_property_200_top5_scores_{column}.csv', index=False)

def score_csv_100(column):
	model_data = pd.read_csv(f'kb_qwen_questions_answers_property_100_tuning_book.csv')
	data = pd.read_csv('scores/机床维修案例_100.csv')

	test_questions = model_data['questions']
	true_answers = data['分析过程']
	model_answers = model_data['answers']
		
	print(len(test_questions))
	answers = []
	for question, true_answer, model_answer in zip(test_questions, true_answers, model_answers):
		#print(question)
		answer = llm_get_scores(question, true_answer, model_answer)
		answers.append(answer)

	data = pd.DataFrame({'questions': test_questions, 'true_answers': true_answers, 'model_answers': model_answers, 'scores': answers})
	data.to_csv(f'kb_qwen_questions_answers_property_100_top5_scores_{column}.csv', index=False)

if __name__ == "__main__":
	score_csv_200("rewrite1")
	score_csv_100("rewrite1")

	score_csv_200("rewrite2")
	score_csv_100("rewrite2")

	score_csv_200("rewrite3")
	score_csv_100("rewrite3")



#print(completion.choices[0].message)

