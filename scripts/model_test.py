from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_PATH = "models/final_csharp_cs_model"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.float16,
    device_map="auto",
)

model.eval()

prompt = """
질문: 왜 LinkedList<T>가 이론상 삽입 O(1)인데 실무에서는 List<T>가 더 빠른 경우가 많아?
답변:
"""

inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        do_sample=True,
        temperature=0.5,
        top_p=0.85,
        repetition_penalty=1.15
    )

print(tokenizer.decode(outputs[0], skip_special_tokens=True))