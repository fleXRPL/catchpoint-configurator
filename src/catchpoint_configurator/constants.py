"""Constants for the Catchpoint Configurator."""

from typing import FrozenSet

# API endpoints
API_BASE_URL = "https://api.catchpoint.com/v2"
API_TOKEN_URL = "https://api.catchpoint.com/v2/token"
API_TEST_URL = "https://api.catchpoint.com/v2/tests"
API_DASHBOARD_URL = "https://api.catchpoint.com/v2/dashboards"

# Test types
TEST_TYPE_WEB = "web"
TEST_TYPE_API = "api"
TEST_TYPE_TRANSACTION = "transaction"
TEST_TYPE_DNS = "dns"
TEST_TYPE_TRACEROUTE = "traceroute"

VALID_TEST_TYPES: FrozenSet[str] = frozenset(
    [
        TEST_TYPE_WEB,
        TEST_TYPE_API,
        TEST_TYPE_TRANSACTION,
        TEST_TYPE_DNS,
        TEST_TYPE_TRACEROUTE,
    ]
)

# Metrics
METRIC_RESPONSE_TIME = "response_time"
METRIC_AVAILABILITY = "availability"
METRIC_THROUGHPUT = "throughput"
METRIC_DNS_TIME = "dns_time"
METRIC_CONNECT_TIME = "connect_time"
METRIC_SSL_TIME = "ssl_time"
METRIC_WAIT_TIME = "wait_time"
METRIC_LOAD_TIME = "load_time"

VALID_METRICS: FrozenSet[str] = frozenset(
    [
        METRIC_RESPONSE_TIME,
        METRIC_AVAILABILITY,
        METRIC_THROUGHPUT,
        METRIC_DNS_TIME,
        METRIC_CONNECT_TIME,
        METRIC_SSL_TIME,
        METRIC_WAIT_TIME,
        METRIC_LOAD_TIME,
    ]
)

ALERT_METRICS = VALID_METRICS

# Alert operators
OPERATOR_GT = ">"
OPERATOR_LT = "<"
OPERATOR_GTE = ">="
OPERATOR_LTE = "<="
OPERATOR_EQ = "=="
OPERATOR_NEQ = "!="

VALID_CONDITIONS: FrozenSet[str] = frozenset(
    [
        OPERATOR_GT,
        OPERATOR_LT,
        OPERATOR_GTE,
        OPERATOR_LTE,
        OPERATOR_EQ,
        OPERATOR_NEQ,
    ]
)

# Widget types
WIDGET_TYPE_METRIC = "metric"
WIDGET_TYPE_CHART = "chart"
WIDGET_TYPE_TABLE = "table"
WIDGET_TYPE_TEXT = "text"

VALID_WIDGET_TYPES: FrozenSet[str] = frozenset(
    [
        WIDGET_TYPE_METRIC,
        WIDGET_TYPE_CHART,
        WIDGET_TYPE_TABLE,
        WIDGET_TYPE_TEXT,
    ]
)

# Node types
VALID_NODES: FrozenSet[str] = frozenset(
    [
        "US-East",
        "US-West",
        "EU-West",
        "EU-Central",
        "AP-Southeast",
        "AP-Northeast",
    ]
)

# Recipient types
RECIPIENT_TYPE_EMAIL = "email"
RECIPIENT_TYPE_WEBHOOK = "webhook"
RECIPIENT_TYPE_SLACK = "slack"

VALID_RECIPIENT_TYPES: FrozenSet[str] = frozenset(
    [
        RECIPIENT_TYPE_EMAIL,
        RECIPIENT_TYPE_WEBHOOK,
        RECIPIENT_TYPE_SLACK,
    ]
)

# File paths
CONFIG_FILE = "catchpoint.yaml"
LOG_FILE = "catchpoint.log"

# Logging
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"

# Environment variables
REQUIRED_VARS = [
    "CATCHPOINT_CLIENT_ID",
    "CATCHPOINT_CLIENT_SECRET",
]

# Frequency Settings
DEFAULT_FREQUENCY = 300  # 5 minutes
MIN_FREQUENCY = 60  # 1 minute
MAX_FREQUENCY = 86400  # 24 hours

# Retry Settings
DEFAULT_RETRIES = 3
MIN_RETRIES = 1
MAX_RETRIES = 5

# File Settings
TEMPLATE_DIR = "templates"
CACHE_DIR = ".cache"
CACHE_TTL = 3600  # 1 hour
