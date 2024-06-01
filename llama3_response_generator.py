import os
from huggingface_hub import login
import transformers

# Directly set the Hugging Face token here
HUGGINGFACE_TOKEN = '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'

# Login using the token
login(token=HUGGINGFACE_TOKEN)

# Check if the token is set correctly
if not HUGGINGFACE_TOKEN:
    raise ValueError("Hugging Face token not found. Make sure to set it correctly.")

# Explicitly set the token as an environment variable
os.environ['HUGGINGFACE_TOKEN'] = HUGGINGFACE_TOKEN
os.environ['HUGGINGFACEHUB_API_TOKEN'] = HUGGINGFACE_TOKEN

# Use the token for authentication
model_id = "meta-llama/Meta-Llama-3-70B-Instruct"
pipeline = transformers.pipeline(model=model_id, use_auth_token=HUGGINGFACE_TOKEN)

# Test the pipeline with a simple input
result = pipeline("What is a bot?")
print(result)