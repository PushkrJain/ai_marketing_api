# agent/optimization.py

from mylogging.research_logger import research_logger
from mylogging.error_logger import error_logger
from monitoring.metrics import ERROR_COUNT
from db.feedback import get_feedback_for_product

def optimize_prompt(
    original_prompt: str,
    feedback: dict,
    strategy: str = "engagement_boost",
    product: str = None  # New: Accept product for feedback-based optimization
) -> str:
    try:
        # Use current feedback
        if not feedback:
            research_logger.info("No feedback provided, returning base prompt.")
            return original_prompt + " [Consider adding more personalization.]"

        click_rate = feedback.get("click_rate", 0.0)
        open_rate = feedback.get("open_rate", 0.0)
        engagement = feedback.get("engagement", 0.0)
        new_prompt = original_prompt.strip()

        # Use historical feedback if product is provided
        if product:
            past_feedbacks = get_feedback_for_product(product)
            if any("short" in fb.lower() for fb in past_feedbacks):
                new_prompt = new_prompt[:70] + " [Shortened based on feedback]"
            if any("personal" in fb.lower() for fb in past_feedbacks):
                new_prompt += " [Personalized based on feedback]"

        if click_rate < 0.2:
            new_prompt += " Click here to learn more or claim your offer!"
        if open_rate < 0.3:
            new_prompt = "📬 Important Update: " + new_prompt
        if engagement < 0.3:
            new_prompt += " We’d love to hear your thoughts-reply now!"

        new_prompt += f" [optimized with strategy={strategy}]"
        research_logger.info("Optimized prompt based on feedback: %s", feedback)
        return new_prompt

    except Exception as e:
        ERROR_COUNT.inc()
        error_logger.error("Exception in optimize_prompt: %s", str(e))
        return original_prompt

