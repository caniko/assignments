import os

TEST_ENDPOINT_PATH = "/tibber-developer-test/enter-path"
EXAMPLE_REQUEST_TOWARDS_TEST_ENDPOINT = {
    "start": {"x": 10, "y": 10},
    "commands": [{"direction": "north", "steps": 5}],
}

MODEL_PATH = "tibber.models"
POSTGRES_URL = os.getenv("POSTGRES_URL")
TORTOISE_CONFIG = {
    "connections": {"default": POSTGRES_URL},
    "apps": {
        "models": {
            "models": [MODEL_PATH, "aerich.models"],
            "default_connection": "default",
        },
    },
}

aerich_config = {
    "connections": {
        "default": "postgres://postgres:this_is_bad_very_bad@0.0.0.0:5432/postgres"
    },
    "apps": {
        "models": {
            "models": [MODEL_PATH, "aerich.models"],
            "default_connection": "default",
        },
    },
}
