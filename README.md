# test-flagsmith

Flagsmith server-side SDK integration for Python.

## Installation

```bash
uv pip install -e .
```

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Required environment variables:

| Variable | Description |
|----------|-------------|
| `FLAGSMITH_SERVER_SIDE_ENVIRONMENT_KEY` | Your Flagsmith server-side environment key (required) |

Optional environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `FLAGSMITH_ENABLE_LOCAL_EVALUATION` | `false` | Enable local flag evaluation (requires server key starting with `ser.`) |
| `FLAGSMITH_API_URL` | `https://edge.api.flagsmith.com/api/v1/` | Custom API URL for self-hosted Flagsmith |
| `FLAGSMITH_REQUEST_TIMEOUT_SECONDS` | `10` | Request timeout in seconds |
| `FLAGSMITH_ENV_REFRESH_INTERVAL_SECONDS` | `60` | Environment document refresh interval (local evaluation) |
| `FLAGSMITH_CUSTOM_HEADERS` | `null` | Custom headers as JSON string |
| `FLAGSMITH_OFFLINE_MODE` | `false` | Run in fully offline mode |
| `FLAGSMITH_ENVIRONMENT_DOCUMENT_PATH` | `null` | Path to environment document for offline mode |

## Usage

### Basic Usage

```python
from dotenv import load_dotenv
load_dotenv()  # loads .env

from test_flagsmith import is_enabled, get_flag, get_flags, get_flag_object

identity = "user@example.com"
traits = {"plan": "premium", "beta_tester": True}

# Check if feature is enabled
if is_enabled(identity, "new_checkout_flow", traits=traits):
    print("Feature enabled!")

# Get flag value (for multivariate flags)
color = get_flag(identity, "button_color", default="blue", traits=traits)

# Get all flags
all_flags = get_flags(identity, traits)

# Get full flag object (variant, reason, metadata)
flag = get_flag_object(identity, "new_checkout_flow", traits=traits)
```

### Direct Client Access

```python
from test_flagsmith import flagsmith

flags = flagsmith.get_identity_flags(identifier="user@example.com", traits={"plan": "premium"})
```

### Local Evaluation Mode

For better performance (no network call per evaluation):

```bash
# In .env
FLAGSMITH_ENABLE_LOCAL_EVALUATION=true
```

### Offline Mode

Run completely offline with cached environment document:

```bash
# Generate once: flagsmith pull-environment --environment-key YOUR_KEY --output environment.json
# In .env
FLAGSMITH_OFFLINE_MODE=true
FLAGSMITH_ENVIRONMENT_DOCUMENT_PATH=./environment.json
```

### Custom Configuration

```python
from test_flagsmith.config import FlagsmithConfig, create_flagsmith_client

config = FlagsmithConfig(
    environment_key="your_key",
    enable_local_evaluation=True,
    api_url="https://api.your-selfhosted-flagsmith.com/api/v1/",
    request_timeout_seconds=30,
)

client = create_flagsmith_client(config)
```

## API

| Function | Returns |
|----------|---------|
| `is_enabled(identity, feature, default=False, traits=None)` | `bool` |
| `get_flag(identity, feature, default=None, traits=None)` | `Any` |
| `get_flags(identity, traits=None)` | `dict[str, Any]` |
| `get_flag_object(identity, feature, traits=None)` | `Flag \| None` |
| `flagsmith` (lazy) | `Flagsmith` client |