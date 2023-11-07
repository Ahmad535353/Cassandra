import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# model_path = 'ahxt/llama2_xs_460M_experimental'
# model_path = 'ahxt/llama1_s_1.8B_experimental'
model_path = '"nomic-ai/gpt4all-j"'

# model = AutoModelForCausalLM.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
    "nomic-ai/gpt4all-j", revision="v1.2-jazzy"
)
tokenizer = AutoTokenizer.from_pretrained(model_path)
model.eval()

prompt = "Here is everything you need to know about Roman empire:\n\n"
input_ids = tokenizer(prompt, return_tensors="pt").input_ids
tokens = model.generate(input_ids, max_length=500)
print(tokenizer.decode(tokens[0].tolist(), skip_special_tokens=True))
# Q: What is the largest bird?\nA: The largest bird is the bald eagle.

while True:
    user_input = input("Q: ")
    input_ids = tokenizer(user_input, return_tensors="pt").input_ids
    tokens = model.generate(input_ids, max_length=500)
    print(tokenizer.decode(tokens[0].tolist(), skip_special_tokens=True))
