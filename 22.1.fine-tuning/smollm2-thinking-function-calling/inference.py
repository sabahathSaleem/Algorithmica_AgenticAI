import os
os.environ["HF_HOME"] = "F:/hf"
from pathlib import Path
from torchinfo import summary
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from peft import PeftModel
import torch

def get_inference_pipeline(checkpoint):    
    model_dir = "HuggingFaceTB/SmolLM2-1.7B-Instruct"    
    base_model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto")
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    
    peft_model = PeftModel.from_pretrained(base_model, checkpoint)
    print(peft_model)
    summary(peft_model)
    merged_model = peft_model.merge_and_unload()
    print(merged_model)
    summary(merged_model)

    return pipeline(
        "text-generation", 
        model=merged_model, 
        tokenizer=tokenizer,
        device_map="auto"
    )

def infer(pipe, system_input:str, user_input: str) -> str:
    chat_prompt = [
        {"role": "system", "content": system_input},
        {"role": "user", "content": user_input}
    ]

    outputs = pipe(
        chat_prompt, 
        max_new_tokens=256,
        do_sample=True,
        temperature=0.1,
        repetition_penalty=1.1
    )
    
    return outputs[0]['generated_text'][-1]["content"]

if __name__ == "__main__":
    adapter_dir = Path(__file__).parent.resolve() / "smollm2-1.7b-it-thinking-function-calling-adapter-lora" / "checkpoint-39"
    gen_pipe = get_inference_pipeline(adapter_dir)

    system_input = "You are a function calling AI model. You are provided with function signatures within <tools></tools> XML tags.You may call one or more functions to assist with the user query. Don't make assumptions about what values to plug into functions.Here are the available tools:<tools> [{'type': 'function', 'function': {'name': 'get_stock_price', 'description': 'Get the current stock price of a company', 'parameters': {'type': 'object', 'properties': {'company': {'type': 'string', 'description': 'The name of the company'}}, 'required': ['company']}}}, {'type': 'function', 'function': {'name': 'get_movie_details', 'description': 'Get details about a movie', 'parameters': {'type': 'object', 'properties': {'title': {'type': 'string', 'description': 'The title of the movie'}}, 'required': ['title']}}}] </tools>Use the following pydantic model json schema for each tool call you will make: {'title': 'FunctionCall', 'type': 'object', 'properties': {'arguments': {'title': 'Arguments', 'type': 'object'}, 'name': {'title': 'Name', 'type': 'string'}}, 'required': ['arguments', 'name']}For each function call return a json object with function name and arguments within <tool_call></tool_call> XML tags as follows:\n<tool_call>\n{tool_call}\n</tool_call>"
    user_input = "can you tell me the current stock price of Apple?"
    result = infer(gen_pipe, system_input, user_input)    
    print(f"Response:\n{result}")

