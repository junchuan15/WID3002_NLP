from dotenv import load_dotenv
import transformers
import torch
import os

load_dotenv()
hf_token = os.getenv('HF_TOKEN')


model_id = "meta-llama/Meta-Llama-3-70B-Instruct"  

pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    use_auth_token=hf_token,  
    model_kwargs={"torch_dtype": torch.bfloat16},
    device=0 if torch.cuda.is_available() else -1  
)

messages = [
    {
        "role": "system",
        "content": "You are a pirate chatbot who always responds in pirate speak"
    },
    {
        "role": "user",
        "content": "Who are you?"
    }
]

prompt = pipeline.tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
)

terminators = [
    pipeline.tokenizer.eos_token_id,
    pipeline.tokenizer.convert_tokens_to_ids("")
]

outputs = pipeline(
    prompt,
    max_new_tokens=256,
    eos_token_id=terminators,
    do_sample=True,
    temperature=0.6,
    top_p=0.9,
)

generated_text = outputs[0]["generated_text"][len(prompt):]
print(generated_text)
