# agent/generation.py

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from logging import getLogger
from mylogging.error_logger import error_logger
from mylogging.research_logger import research_logger
from monitoring.metrics import REQUEST_COUNT, ERROR_COUNT

MODEL_PATH = "./hf_models/phi3/Phi-3-mini-4k-instruct"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True,
    attn_implementation="eager"
)
model.eval()

def generate_response(
    prompt: str,
    max_new_tokens: int = 50,
    temperature: float = 0.5,
    top_p: float = 0.9
) -> str:
    REQUEST_COUNT.inc()
    if not prompt.strip():
        ERROR_COUNT.inc()
        error_logger.error("Prompt is empty.")
        return "[Error] Prompt is empty. Please provide a meaningful request."
    try:
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=temperature,
                top_p=top_p,
                eos_token_id=tokenizer.eos_token_id
            )
        output = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        # Remove echoed prompt if present
        if output.startswith(prompt.strip()):
            output = output[len(prompt.strip()):].strip()
        output_lower = output.lower()
        meta_starts = [
            "write", "create", "include", "generate", "describe", "your task",
            "the prompt should", "you are tasked to"
        ]
        if not output or any(output_lower.startswith(p) for p in meta_starts):
            ERROR_COUNT.inc()
            error_logger.error("Generated output insufficient or unclear for prompt: %s", prompt)
            return "[Error] Insufficient or unclear prompt content. Please rephrase or provide more specific details."
        if len(output) < 25 and output_lower in prompt.strip().lower():
            ERROR_COUNT.inc()
            error_logger.error("Generated output too similar to input: %s", prompt)
            return "[Error] Generated output too similar to input. Add more detail."
        research_logger.info("Generated response for prompt: %s", prompt)
        return output
    except Exception as e:
        ERROR_COUNT.inc()
        error_logger.error("Exception in generate_response: %s", str(e))
        return "[Error] Exception during generation."

