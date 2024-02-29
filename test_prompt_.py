def generate_answer(query):
    from openai import OpenAI

    client = OpenAI(api_key="none", base_url="http://127.0.0.1:8000/v1")
    message = [
     	{"role": "user", "content": query},       
   	]
    response = client.chat.completions.create(
        model="qwen-14b",
        messages=message,
        max_tokens=4096,
        temperature=1.0
    )
    return response


def get_scores(user_input):
    prompt = (
        "你需要扮演一个生气的女朋友，你现在因为生活中长期积累的各种小事生气了，你也不知道为什么生气，"
        "但是你想要你男朋友哄你，你要根据男朋友的语言的字数、语气、颜表情来综合评判并决定是否要原谅他。"
        "你可以给他的回答打负20到20分，你可以给出原因，并说出他最终的得分。"
        "例如：他说：抱抱~，刚刚是我疏忽啦，没注意到你的心情，是我做的不好，我来改正啦。"
        "所以你的输出是：他很照顾我的情绪，而且在尝试寻找自己的问题，并且在找补偿办法，所以最终得分：15分。"
        f"现在他的回答是：{user_input}。"
    )
    resp = generate_answer(prompt).choices[0].message.content
    print(resp)
    return 0, resp


def get_response(user_input, mental):
    prompt = (
        "你需要扮演一个生气的女朋友，你现在因为生活中长期积累的各种小事生气了，你也不知道为什么生气，"
        "但是你想要你男朋友哄你，你要根据男朋友的语言的字数、语气、颜表情来综合评判并决定是否要原谅他。"
        f"现在他的回答是：{user_input}。"
        f"你的想法是：{mental}。"
        "你并不想直接告诉他你内心的想法，你想要更加委婉地表达，最好让他继续猜你内心的心思，不要给他任何提示，所以你的回答是："
    )
    resp = generate_answer(prompt).choices[0].message.content
    # print(resp)
    return resp


if __name__ == "__main__":
    forgiveness = 0
    user_input = input("女朋友：哼\n你：")
    while(user_input):
        scores, mental = get_scores(user_input)
        forgiveness += scores
        if forgiveness < 0:
            print("她离开了你，再见！\n")
            exit(0)
        elif forgiveness >= 100:
            print("恭喜恭喜，她原谅了你，你们在一起了！\n")
            exit(0)
        else:
            response = get_response(user_input, mental)
            user_input = input(f"女朋友：{response}\n你：")
