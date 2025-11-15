import logging
import logging.config
import yaml
import os

DEFAULT_LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - [%(levelname)s] - %(name)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout'
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    },
    'loggers': {
        'AgentController': {
            'level': 'DEBUG',
            'propagate': False,
            'handlers': ['console']
        },
        'DemoRunner': {
            'level': 'INFO',
            'propagate': False,
            'handlers': ['console']
        }
    }
}

def setup_logging(config_path='config/logging.yaml'):
    """Sets up logging configuration from a YAML file."""
    # Need to check relative path correctly from where run_demo is
    # This logic assumes the script is run from the root, or paths are absolute.
    # Let's make it more robust by checking relative to this file's path.
    
    # This is tricky. Let's assume run_demo.py's sys.path insert
    # makes 'config/logging.yaml' available from the root.
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'rt') as f:
                config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
            print(f"Logging loaded from {config_path}")
        except Exception as e:
            print(f"Error loading logging config {config_path}: {e}. Using default.")
            logging.config.dictConfig(DEFAULT_LOGGING_CONFIG)
    else:
        print(f"Warning: {config_path} not found. Using default logging config.")
        logging.config.dictConfig(DEFAULT_LOGGING_CONFIG)
