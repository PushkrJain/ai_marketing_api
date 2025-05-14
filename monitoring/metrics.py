# monitoring/metrics.py

from prometheus_client import Gauge
from prometheus_client import Counter

REQUEST_COUNT = Counter('request_count', 'Total number of requests')
ERROR_COUNT = Counter('error_count', 'Number of errors occurred')
CAMPAIGN_CREATED = Counter('campaign_created', 'Number of campaigns created')


FEEDBACK_RATING_COUNT = Gauge(
    "feedback_rating_count",
    "Count of feedbacks by rating",
    ["rating"]
)

