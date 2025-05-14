# agents/segmentation.py

from mylogging.research_logger import research_logger
from mylogging.error_logger import error_logger
from monitoring.metrics import REQUEST_COUNT, ERROR_COUNT

def segment_user(data: dict) -> list:
    REQUEST_COUNT.inc()
    try:
        segments = []
        age = data.get("age", 0)
        interests = data.get("interests", [])
        location = data.get("location", "").lower()
        if age < 25:
            segments.append("GenZ")
        elif 25 <= age < 40:
            segments.append("Millennial")
        else:
            segments.append("GenX+")
        interests_lower = [i.lower() for i in interests]
        if any(i in interests_lower for i in ["fashion", "beauty", "style"]):
            segments.append("Fashion Enthusiast")
        if any(i in interests_lower for i in ["fitness", "wellness", "gym", "health"]):
            segments.append("Fitness Enthusiast")
        if any(i in interests_lower for i in ["tech", "gadgets", "ai", "machine learning"]):
            segments.append("Tech Savvy")
        if any(i in interests_lower for i in ["reading", "books", "literature"]):
            segments.append("Book Lover")
        if location == "urban":
            segments.append("Urban Dweller")
        elif location == "suburban":
            segments.append("Suburban Resident")
        elif location == "rural":
            segments.append("Rural Explorer")
        research_logger.info("Segmented user: %s -> %s", data, segments)
        return segments
    except Exception as e:
        ERROR_COUNT.inc()
        error_logger.error("Exception in segment_user: %s", str(e))
        return []

