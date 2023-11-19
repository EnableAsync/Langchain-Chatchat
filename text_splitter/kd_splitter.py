from langchain.text_splitter import CharacterTextSplitter
import json
from typing import List


class KDTextSplitter():
    def __init__(self, pdf: bool = False, **kwargs):
        pass

    def split_text(self, text: str) -> List[str]:
        print("text****************", text)
        result = []
        data = json.loads(text)
        sample = ""
        for item in data:
            sample = f"问题：{item['question']}，答案：{item['answer']}"
            result.append(sample)
        print("result***************************", result)
        return result
