import yaml
import os

DEFAULT_CONFIG = {
    'api_keys': {
        'openai': 'DEFAULT_KEY_PLACEHOLDER'
    },
    'timeouts': {
        'step': 10,
        'total': 120
    }
}

def load_config(config_path='config/settings.yaml'):
    """Loads configuration from a YAML file."""
    if os.path.exists(config_path):
        try:
            with open(config_path, 'rt') as f:
                config = yaml.safe_load(f.read())
            return config
        except Exception as e:
            print(f"Error loading settings config {config_path}: {e}. Using default.")
            return DEFAULT_CONFIG
    else:
        print(f"Warning: {config_path} not found. Using default config.")
        return DEFAULT_CONFIG
