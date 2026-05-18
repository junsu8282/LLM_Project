import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

BASE_MODEL_PATH = "/llm_project/outputs/phase1_merged"
ADAPTER_PATH = "/llm_project/outputs/phase2_csharp_cs_adapter"
FINAL_SAVE_PATH = "/llm_project/models/final_csharp_cs_model"

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_PATH)

base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL_PATH,
    torch_dtype=torch.float16,
    device_map="auto",
)

model = PeftModel.from_pretrained(
    base_model,
    ADAPTER_PATH,
)

merged_model = model.merge_and_unload()

merged_model.save_pretrained(
    FINAL_SAVE_PATH,
    safe_serialization=True,
    max_shard_size="2GB"
)

tokenizer.save_pretrained(FINAL_SAVE_PATH)

print("최종 모델 저장 완료")