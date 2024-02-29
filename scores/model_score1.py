from openai import OpenAI
import pandas as pd
import re

def count_correct_and_wrong(string):
    correct_count = string.count("true")
    wrong_count = string.count("false")
    return correct_count > wrong_count

def check_for_number(string):
    pattern = r'得分: (\d+)|得分：(\d+)|得分为(\d+)分|得(\d+)分|得分(\d+)分|答案：(\d+)分'
    if re.search(pattern, string):
        return True
    else:
        return False
def check_for_correct_and_wrong(sentence):
    # 检查是否包含"true"或"false"
    if "true" in sentence or "false" in sentence:
        return True
    else:
        return False

def llm_get_scores(question, true_answer, model_answer):
	completion1 = client.chat.completions.create(
 		 model="qwen-14b",
  		messages=[
     		{"role": "user", "content": f"现在你是一名阅卷老师，请你按照以下标准对模型回答进行正误判断，顺便给出理由。标准：比较给出的模型回答和标准回答，如果模型回答给出的解决方案中有能和标准回答给出的解决方案基本一致的，判断结果为true，否则为false，判断到此结束，最后输出判断结果。\n现在，给出的问题是：'故障现象：某配套FANUC6M的立式加工中心，在加工过程中，车间突然断电，恢复供电后，无法重新起动机床。'\n给出的标准回答是：'分析及处理过程对照以上原理图4–1，经测量电源输入单元TP1，输入U/V/?为200V正常，但检查U1、V1端无AC200V。由图4–1可见，其故障原因应为F1、F2熔断，经测量确认F1、F2已经熔断。进一步检查发现，输入单元的TP3上200A/200B间存在短路。为了区分故障部位，取下TP3上的200A、200B连线，进行再次测量，确认故障在输入单元的外部。检查线路发现200A、200B电缆绝缘破损。在更换电缆、熔断器F1、F2，排除短路故障后，机床恢复正常。'\n给出的模型回答是：'根据提供的信息，故障现象描述为：在长期停用后首次开机，出现电源无法接通的故障。根据这个故障现象，我们可以考虑以下几种可能的问题：1. 输入单元的发光二极管 PIL 不亮，内部无 DC24V 电压：这种情况下，可以检查 Q1、DS1、C1 与 F3 等元器件是否良好。如果其中某个元器件出现问题，则需要更换相应的元器件。2. 输入单元的 F3 已经熔断：如果输入单元的 F3 已经熔断，则需要更换新的 F3 元件。3. 偶然性的过电流引起：如果上述两种情况都排除了，则可能是由于偶然性的过电流引起的问题。这种情况下，建议检查电路是否有短路或其他异常情况，并进行相应的维修。因此，根据已知的故障现象相关问题，可能的问题和解决方案如下：1.熔断问题；2.输入单元的发光二极管PI不亮；3.内部无 DC24V 电压问题；4. 偶然性的过电流引起问题'\n。经过对标准，模型问答，标准问答的分析后，你应该有如下输出：'\n检查标准：由于标准回答中给出的解决方案是更换电缆、熔断器F1、F2，排除短路故障后，机床恢复正常，而模型回答中的解决方案：1.更换相应的元器件。2.更换新的 F3 元件。3.检查电路是否有短路或其他异常情况，并进行相应的维修。三者和标准回答中的解决方案虽有相似性，但不够准确，不能算基本一致，因此判断结果为false，判断到此结束，最后输出判断结果：false。'\n现在，给出的标准回答是：{true_answer}\n给出的模型回答是：{model_answer}\n，请你按照例子的格式输出答案："},       
   		]
	)

	sentence1 = completion1.choices[0].message.content
	if count_correct_and_wrong(sentence1):
		response = "该例按评分标准1进行评分："+sentence1+"由于判断正确，评分结束，不再往下检查标准，输出得分：10分。"
		print(response ,"\n")
		return response
	else:
		completion2 = client.chat.completions.create(
 			model="qwen-14b",
  			messages=[
     			{"role": "user", "content": f"现在你是一名阅卷老师，请你按照以下标准对模型回答进行正误判断，顺便给出理由。标准：比较给出的模型回答和标准回答，如果标准回答中最终的确认故障原因能与模型回答里给出的所有故障原因中的某一条基本一致的话，判断结果为true，否则为false，判断到此结束，最后输出判断结果。\n现在，给出的问题是：'故障现象：某配套FANUC6M的立式加工中心，在加工过程中，车间突然断电，恢复供电后，无法重新起动机床。'\n给出的标准回答是：'分析及处理过程对照以上原理图4–1，经测量电源输入单元TP1，输入U/V/?为200V正常，但检查U1、V1端无AC200V。由图4–1可见，其故障原因应为F1、F2熔断，经测量确认F1、F2已经熔断。进一步检查发现，输入单元的TP3上200A/200B间存在短路。为了区分故障部位，取下TP3上的200A、200B连线，进行再次测量，确认故障在输入单元的外部。检查线路发现200A、200B电缆绝缘破损。在更换电缆、熔断器F1、F2，排除短路故障后，机床恢复正常。'\n给出的模型回答是：'根据提供的信息，故障现象描述为：在长期停用后首次开机，出现电源无法接通的故障。根据这个故障现象，我们可以考虑以下几种可能的问题：1. 输入单元的发光二极管 PIL 不亮，内部无 DC24V 电压：这种情况下，可以检查 Q1、DS1、C1 与 F3 等元器件是否良好。如果其中某个元器件出现问题，则需要更换相应的元器件。2. 输入单元的 F3 已经熔断：如果输入单元的 F3 已经熔断，则需要更换新的 F3 元件。3. 偶然性的过电流引起：如果上述两种情况都排除了，则可能是由于偶然性的过电流引起的问题。这种情况下，建议检查电路是否有短路或其他异常情况，并进行相应的维修。因此，根据已知的故障现象相关问题，可能的问题和解决方案如下：1.熔断问题；2.输入单元的发光二极管PI不亮；3.内部无 DC24V 电压问题；4. 偶然性的过电流引起问题'\n。经过对标准，模型问答，标准问答的分析后，你应该有如下输出：'\n检查标准：由于最终原因是输入单元的TP3上200A/200B间存在短路，而模型回答中的故障原因有1.输入单元的发光二极管 PIL 不亮，内部无 DC24V 电压。2.输入单元的 F3 已经熔断。3.偶然性的过电流引起。三者虽然和最终故障原因虽然相似，但是不够准确，不能算基本一致，因此判断结果为false，判断到此结束，最后输出判断结果：false。'\n现在，给出的标准回答是：{true_answer}\n给出的模型回答是：{model_answer}\n，请你按照例子的格式输出答案："},       
   			]
		)
		sentence2 = completion2.choices[0].message.content
		if count_correct_and_wrong(sentence2):
			response = "该例按评分标准2进行评分："+sentence2+"由于判断正确，评分结束，不再往下检查标准，虽然匹配最终故障原因，但给出的解决方案未匹配，因此需要扣1分，输出得分：9分。"
			print(response ,"\n")
			return response
		else:
			completion3 = client.chat.completions.create(
 				model="qwen-14b",
  				messages=[
     				{"role": "user", "content": f"现在你是一名阅卷老师，请你按照以下标准对模型回答进行正误判断，顺便给出理由。标准：比较给出的模型回答和标准回答，如果标准回答中某一条故障原因能与模型回答里给出的所有故障原因中的某一条基本有一定关联性的话，判断结果直接为true，判断结束，直接输出判断结果:true，不再继续检查标准；若不关联的话，则接着检查未检查过的故障原因，直到所有的故障原因都检查过后仍是不关联，则判断结果为false，判断结束，输出判断结果:false，不再继续检查标准。\n现在，给出的问题是：'故障现象：某配套FANUC6M的立式加工中心，在加工过程中，车间突然断电，恢复供电后，无法重新起动机床。'\n给出的标准回答是：'分析及处理过程对照以上原理图4–1，经测量电源输入单元TP1，输入U/V/?为200V正常，但检查U1、V1端无AC200V。由图4–1可见，其故障原因应为F1、F2熔断，经测量确认F1、F2已经熔断。进一步检查发现，输入单元的TP3上200A/200B间存在短路。为了区分故障部位，取下TP3上的200A、200B连线，进行再次测量，确认故障在输入单元的外部。检查线路发现200A、200B电缆绝缘破损。在更换电缆、熔断器F1、F2，排除短路故障后，机床恢复正常。'\n给出的模型回答是：'根据提供的信息，故障现象描述为：在长期停用后首次开机，出现电源无法接通的故障。根据这个故障现象，我们可以考虑以下几种可能的问题：1. 输入单元的发光二极管 PIL 不亮，内部无 DC24V 电压：这种情况下，可以检查 Q1、DS1、C1 与 F3 等元器件是否良好。如果其中某个元器件出现问题，则需要更换相应的元器件。2. 输入单元的 F3 已经熔断：如果输入单元的 F3 已经熔断，则需要更换新的 F3 元件。3. 偶然性的过电流引起：如果上述两种情况都排除了，则可能是由于偶然性的过电流引起的问题。这种情况下，建议检查电路是否有短路或其他异常情况，并进行相应的维修。因此，根据已知的故障现象相关问题，可能的问题和解决方案如下：1.熔断问题；2.输入单元的发光二极管PI不亮；3.内部无 DC24V 电压问题；4. 偶然性的过电流引起问题'\n。经过对标准，模型问答，标准问答的分析后，你应该有如下输出：'\n检查标准，标准回答中的故障原因有1.F1、F2熔断，2.TP3上200A/200B间存在短路，3.200A、200B电缆绝缘破损。依次检查模型回答中是否有能与标准回答关联的故障原因：1.输入单元的发光二极管 PIL 不亮，内部无 DC24V 电压，2.输入单元的 F3 已经熔断，3.偶然性的过电流引起，电路可能有短路中提到了短路：模型回答的第1个原因中，发光二极管 PIL 、DC24V 电压、 Q1、DS1、C1 与 F3 等元器件根本没出现过，因此二者之间不存在关联性；由于这里是不关联，所以还要检查其他未检查的故障原因，模型回答的第2个原因中提到了输入单元F3熔断，标准问答中是输入单元F1、F2熔断，虽然熔断的具体部件不同，但是二者都提到了是输入单元这一部分发生熔断，从更大范围来说二者的说法具有一定关联性，因此按标准，这里找到了一条关联性原因，判断结果为true，判断结束，输出判断结果：true，不再继续检查标准。'\n现在，给出的标准回答是：{true_answer}\n给出的模型回答是：{model_answer}\n，请你按照例子的格式输出答案："},       
   				]
			)
			sentence3 = completion3.choices[0].message.content
			while True:
				if not check_for_correct_and_wrong(sentence3):
					completion3_1 = client.chat.completions.create(
 						model="qwen-14b",
  						messages=[
     						{"role": "user", "content": f"已知标准：比较给出的模型回答和标准回答，如果标准回答中某一条故障原因能与模型回答里给出的所有故障原因中的某一条基本有一定关联性的话，判断结果直接为true，直接输出判断结果:true，不再接着检查标准；若不关联的话，则接着检查未检查过的故障原因，直到所有的故障原因都检查过后仍是不关联，则判断结果为false，输出判断结果:false，不再接着检查标准。你已按照评分标准输出了你的部分分析，但尚未分析完成，给出的标准回答是：{true_answer}\n给出的模型回答是：{model_answer}\n给出的上文为："+sentence3+"\n请你根据上文自行判断已经进行到了标准的哪一个步骤，并从该步骤往后完成后续的输出，并在最后输出最终判断结果："},
   						]
					)
					sentence3 = sentence3+completion3_1.choices[0].message.content
				else:
					break
			if not count_correct_and_wrong(sentence3):
				response  = "该例按评分标准3进行评分："+sentence3+"由于判断错误，则模型回答中没有一条故障原因能和标准回答有关联，输出得分：0分。"
				print(response ,"\n")
				return response
			else:
				completion4 = client.chat.completions.create(
 					model="qwen-14b",
  					messages=[
     					{"role": "user", "content": f"现在你是一名阅卷老师，请你按照评分标准对模型回答进行打分，基础分为4分，满分8分，顺便给出理由。评分标准：按照故障原因的命中率来给分。比较给出的模型回答和标准回答，从开始一条条检查模型回答中的出现的故障原因，如果该条故障原因能和标准回答中出现的某个故障现象产生的原因有一定关联性，则按1条加1分做加法运算：例如关联到1条加到5分后，继续检查后又关联到1条，则继续加1分到6分，以此类推，注意加分加到最后，得分不能超过满分8分，若超过则得8分，评分结束，不再往下检查标准，输出得分。\n现在，给出的问题是：'故障现象：某配套FANUC6M的立式加工中心，在加工过程中，车间突然断电，恢复供电后，无法重新起动机床。'\n给出的标准回答是：'分析及处理过程对照以上原理图4–1，经测量电源输入单元TP1，输入U/V/?为200V正常，但检查U1、V1端无AC200V。由图4–1可见，其故障原因应为F1、F2熔断，经测量确认F1、F2已经熔断。进一步检查发现，输入单元的TP3上200A/200B间存在短路。为了区分故障部位，取下TP3上的200A、200B连线，进行再次测量，确认故障在输入单元的外部。检查线路发现200A、200B电缆绝缘破损。在更换电缆、熔断器F1、F2，排除短路故障后，机床恢复正常。'\n给出的模型回答是：'根据提供的信息，故障现象描述为：在长期停用后首次开机，出现电源无法接通的故障。根据这个故障现象，我们可以考虑以下几种可能的问题：1. 输入单元的发光二极管 PIL 不亮，内部无 DC24V 电压：这种情况下，可以检查 Q1、DS1、C1 与 F3 等元器件是否良好。如果其中某个元器件出现问题，则需要更换相应的元器件。2. 输入单元的 F3 已经熔断：如果输入单元的 F3 已经熔断，则需要更换新的 F3 元件。3. 偶然性的过电流引起：如果上述两种情况都排除了，则可能是由于偶然性的过电流引起的问题。这种情况下，建议检查电路是否有短路或其他异常情况，并进行相应的维修。因此，根据已知的故障现象相关问题，可能的问题和解决方案如下：1.熔断问题；2.输入单元的发光二极管PI不亮；3.内部无 DC24V 电压问题；4. 偶然性的过电流引起问题'\n。经过对标准，模型问答，标准问答的分析后，你应该有如下输出：'\n检查评分标准，已有基础分4分，且标准回答中的故障原因有1.F1、F2熔断，2.TP3上200A/200B间存在短路，3.200A、200B电缆绝缘破损。依次检查模型回答中是否有能与标准回答关联的故障原因：1.输入单元的发光二极管 PIL 不亮，内部无 DC24V 电压，2.输入单元的 F3 已经熔断，3.偶然性的过电流引起，电路可能有短路中提到了短路。模型回答的第1个原因中的发光二极管 PIL 、DC24V、 Q1、DS1、C1 与 F3 等元器件在标准回答中根本没出现过，因此不存在关联性，所以这一条故障原因不加分，现有分数为：4分；还有其他未检查的原因，因此继续往下检查，模型回答的第2个原因中提到了输入单元F3熔断，标准问答中是输入单元F1、F2熔断，虽然熔断的具体部件不同，但是二者都提到了是输入单元这一部分发生熔断，从更大范围来说二者的说法具有一定关联性，因此按评分标准，该条故障原因能和标准回答中出现的某个故障现象产生的原因有一定关联性的条件，在现有的分数4分上加1分，通过加分运算4+1=5，现有的分数为：5分；还有其他未检查的原因，因此继续往下检查；往下检查，模型回答的第3个原因中提到了短路，与标准答案中的TP3上200A/200B间存在短路有关联，因为模型回答虽未提及具体的短路部件，但也未随便给出一个和标准回答不同的错误短路部件，而且从故障范围来看，前者的范围包含了后者，由此可知二者存在关联性，因此按评分标准，该条故障原因与标准问答某个故障现象产生的原因有关联，在现有的分数上加1分，现在的分数5分上加1分，通过加分运算5+1=6，现有分数为：6分。继续检查，没有发现还有其他能关联的故障原因，所以不再继续加分，最终通过评分标准后检查得分为6分，评分结束，不再往下检查标准，由于最终分数6分未超过评分标准的满分8分，因此可以直接输出，输出得分：6分。'\n现在，给出的标准回答是：{true_answer}\n给出的模型回答是：{model_answer}\n，请你按照例子的格式输出答案："},
   					]
				)
				sentence4 = completion4.choices[0].message.content
				if check_for_number(sentence4):
					response  = "该例按评分标准4进行评分："+ sentence4
					print(response ,"\n")
					return response
				else:
					string1 = sentence4
					i = 0
					while True:
						completion5 = client.chat.completions.create(
 							model="qwen-14b",
  							messages=[
     							{"role": "user", "content": f"请你找到上文中出现的最后一个现有分数，1.若给出的最后一句话的最后几个字与'现有的分数为：5分'类似，则现有分数为5分，输出：现有分数：5分，结束输出。2.若给出的最后一句话的最后几个字与'通过加分运算4+1=5'类似，则现有分数为'='后的数字：5，输出现有分数：5分，结束输出。3.若给出的最后一句话的最后几个字与'现有的分数4分上加1分'类似，则做加法运算：4+1=5，算出现有分数为5，输出：现有分数：5分，结束输出。4.若1、2、3都不满足，则现有分数为：基础分4分。现在，上文为："+string1+"\n请你输出现有分数："},
   							]
						)
						string2 = completion5.choices[0].message.content
						if bool(re.search(r'\d', string2)):
							completion6 = client.chat.completions.create(
 								model="qwen-14b",
  								messages=[
     								{"role": "user", "content": f"已知评分标准：基础分4分，满分8分，按照故障原因的命中率来给分。比较给出的模型回答和标准回答，从开始一条条检查模型回答中的出现的故障原因，如果该条故障原因能和标准回答中出现的某个故障现象产生的原因有一定关联性，则按1条加1分做加法运算：例如从基础分4分开始加法运算，关联到1条，加1分到5分，现有分数为：5分，继续检查后又关联到1条，则继续加1分到6分，现有分数为：6分，以此类推，注意加分加到最后，得分不能超过满分8分，若超过则得8分，评分结束，不再往下检查标准，输出得分。\n现在请记住，你已按照评分标准输出了你的部分分析，但尚未分析完成，给出的标准回答是：{true_answer}\n给出的模型回答是：{model_answer}\n给出的上文为："+string1+"\n现有分数为："+string2+"\n请你根据现有分数及上文自行判断已经进行到了评分标准的哪一个步骤，并从该步骤往后完成后续的输出，并在最后输出最终得分："},
   								]
							)
							string1 = string1+ completion6.choices[0].message.content
						if check_for_number(string1):
							break
						i+=1
						if i>5:
							response  =  "该例按评分标准4进行评分：按照平均分给分，输出得分：6.5分。"
							print(response ,"\n")
							return response
					response  =  "该例按评分标准4进行评分："+string1
					print(response ,"\n")
					return response

	return "由于不满足标准1，标准2，标准3，标准4，所以该例的得分为0分。"

client = OpenAI(api_key="none", base_url="http://127.0.0.1:8000/v1")

# 实际上调用的是 72B 的模型，因为名字改不了，所以写的是 14B

# 这里是调用 Chat 模

def score_csv_200(column):
	# model_data = pd.read_csv(f'scores/kb_qwen_questions_answers_property_200_new_{column}.csv')
	model_data = pd.read_csv(f'kb_qwen_questions_answers_property_200_tuning.csv')
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
	model_data = pd.read_csv(f'kb_qwen_questions_answers_property_100_tuning.csv')
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


# model_data = pd.read_csv('kb_qwen_questions_answers_property_200.csv')
# true_data = pd.read_csv('机床维修案例_200.csv')
# test_questions = model_data['questions']
# true_answers = true_data['分析过程']
# model_answers = model_data['answers']
    
# print(len(test_questions))
# answers = []
# for question, true_answer, model_answer in zip(test_questions, true_answers, model_answers):
#     #print(question)
#     answer = llm_get_scores(question, true_answer, model_answer)
#     answers.append(answer)

# data = pd.DataFrame({'questions': test_questions, 'true_answers': true_answers, 'model_answers': model_answers, 'scores': answers})
# data.to_csv('kb_qwen_scores_300_panduan.csv', index=False)



#print(completion.choices[0].message)

