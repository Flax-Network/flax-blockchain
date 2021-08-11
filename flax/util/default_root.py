import os
from pathlib import Path

DEFAULT_ROOT_PATH = Path(os.path.expanduser(os.getenv("FLAX_ROOT", "~/.flax/mainnet"))).resolve()
