import os
from pathlib import Path

DEFAULT_ROOT_PATH = Path(os.path.expanduser(os.getenv("FLAX_ROOT", "~/.flax/mainnet"))).resolve()
STANDALONE_ROOT_PATH = Path(
    os.path.expanduser(os.getenv("FLAX_STANDALONE_WALLET_ROOT", "~/.flax/standalone_wallet"))
).resolve()

DEFAULT_KEYS_ROOT_PATH = Path(os.path.expanduser(os.getenv("FLAX_KEYS_ROOT", "~/.flax_keys"))).resolve()
