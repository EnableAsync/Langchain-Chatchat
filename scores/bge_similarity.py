from pprint import pprint

query_instruction = "为这个句子生成表示以用于检索相关文章："

model_path = "/home/kdzlys/data-disk/sjj/bge-large-zh-v1.5"

from sentence_transformers import SentenceTransformer, util

queries = ['query_1', 'query_2', "查询_1"]
passages = ["样例文档-1", "样例文档-2", "document-1"]
instruction = "为这个句子生成表示以用于检索相关文章："

model = SentenceTransformer(model_path)
# Two lists of sentences
sentences1 = ["""G52: PC 执行命令期间出错可能是由于以下原因导致：

1. 控制系统软件或硬件故障：
   原因：控制系统软件存在错误，或者控制器、PLC等硬件部件发生故障。
   解决方案：检查控制系统软件版本是否正确并进行升级；排查硬件故障，如更换有问题的硬件。

2. 通讯问题：
   原因：通讯线缆损坏、接口松动或通信协议不匹配等。
   解决方案：检查通讯线缆连接状态，修复或更换损坏线缆；确保通讯接口正常接触；核实通讯协议设置。

3. 输入数据错误：
   原因：编程过程中输入的数据存在错误，导致执行命令期间出错。
   解决方案：仔细检查程序代码和输入数据，修正错误部分；重新运行程序验证效果。

4. 机械结构或电气设备故障：
   原因：机床机械部件损坏或电气设备（如电机、编码器）发生故障。
   解决方案：检查机床机械部件是否存在磨损或损坏情况，及时修复或更换；检测电气设备工作状态，对有问题的部分进行维修或更换。

5. 系统参数设置不当：
   原因：机床系统的参数设置错误，导致在执行命令期间出现问题。
   解决方案：查阅机床操作手册，核对系统参数设置，调整至正确数值。

6. 刀具、工件或其他配件问题：
   原因：刀具、工件安装不当，或者其他配件质量问题。
   解决方案：重新校准刀具、工件安装；更换质量可靠的配件。

请根据上述原因及解决方案逐一排查问题，找到具体原因后，采取相应的措施解决。同时，确保操作人员具备足够的知识和技能，在使用机床前充分了解操作手册，遵循正确的操作步骤和规程。"""]

sentences2 = ["""故障描述:CNC通过G52功能，在设备自动管理后，执行请求加工服务器。故障原因：PC 未执行从CNC接收到的 G52 命令。故障措施：验证服务器中所定义的加工目录。验证 PC 与 Server 之间是否能正常对话"""]

#Compute embedding for both lists
embeddings1 = model.encode(sentences1, convert_to_tensor=True)
embeddings2 = model.encode(sentences2, convert_to_tensor=True)

#Compute cosine-similarities
cosine_scores = util.cos_sim(embeddings1, embeddings2)

pprint(cosine_scores)

#Output the pairs with their score
for i in range(len(sentences1)):
    print("{} \t\t {} \t\t Score: {:.4f}".format(sentences1[i], sentences2[i], cosine_scores[i][i]))