import re
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained(
        "/home/kdzlys/data-disk/sjj/Qwen/Qwen-72B-Chat",
        device_map="auto",
        trust_remote_code=True,
        resume_download=True,
    ).eval()

model_modules = str(model.modules)
print(model_modules)
pattern = r'\((\w+)\): Linear'
linear_layer_names = re.findall(pattern, model_modules)

names = []
# Print the names of the Linear layers
for name in linear_layer_names:
    names.append(name)
target_modules = list(set(names))
print(target_modules)