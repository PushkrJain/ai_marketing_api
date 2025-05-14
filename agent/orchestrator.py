# agents/orchestrator.py

from agent.segmentation import segment_user
from agent.generation import generate_response
from agent.optimization import optimize_prompt
from monitoring.metrics import CAMPAIGN_CREATED, ERROR_COUNT
from mylogging.error_logger import error_logger
from mylogging.research_logger import research_logger

def create_campaign(user_profile: dict, campaign_type: str, product: str, offer: str,
                   feedback: dict = None, max_tokens: int = 100, temperature: float = 0.7) -> str:
    try:
        segments = segment_user(user_profile)
        name = user_profile.get("name", "Customer")
        segment_str = ", ".join(segments) if segments else "valued"
        base_prompt = (
            f"Hi {name}, as a {segment_str} customer, you'll love our {product}! "
            f"{offer} just for you. This is part of our {campaign_type} campaign."
        )
        final_prompt = optimize_prompt(base_prompt, feedback or {})
        response = generate_response(
            prompt=final_prompt,
            max_new_tokens=max_tokens,
            temperature=temperature
        )
        CAMPAIGN_CREATED.inc()
        research_logger.info("Campaign created for user: %s, prompt: %s", name, final_prompt)
        return response
    except Exception as e:
        ERROR_COUNT.inc()
        error_logger.error("Exception in create_campaign: %s", str(e))
        return "[Error] Exception during campaign creation."

