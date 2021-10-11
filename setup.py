from setuptools import setup

dependencies = [
    "blspy==1.0.6",  # Signature library
    "chiavdf==1.0.3",  # timelord and vdf verification
    "chiabip158==1.0",  # bip158-style wallet filters
    "chiapos==1.0.4",  # proof of space
    "clvm==0.9.7",
    "clvm_rs==0.1.14",
    "clvm_tools==0.4.3",
    "aiohttp==3.7.4",  # HTTP server for full node rpc
    "aiosqlite==0.17.0",  # asyncio wrapper for sqlite, to store blocks
    "bitstring==3.1.9",  # Binary data management library
    "colorama==0.4.4",  # Colorizes terminal output
    "colorlog==5.0.1",  # Adds color to logs
    "concurrent-log-handler==0.9.19",  # Concurrently log and rotate logs
    "cryptography==3.4.7",  # Python cryptography library for TLS - keyring conflict
    "fasteners==0.16.3",  # For interprocess file locking
    "keyring==23.0.1",  # Store keys in MacOS Keychain, Windows Credential Locker
    "keyrings.cryptfile==1.3.4",  # Secure storage for keys on Linux (Will be replaced)
    #  "keyrings.cryptfile==1.3.8",  # Secure storage for keys on Linux (Will be replaced)
    #  See https://github.com/frispete/keyrings.cryptfile/issues/15
    "PyYAML==5.4.1",  # Used for config file format
    "setproctitle==1.2.2",  # Gives the flax processes readable names
    "sortedcontainers==2.4.0",  # For maintaining sorted mempools
    "websockets==8.1.0",  # For use in wallet RPC and electron UI
    "click==7.1.2",  # For the CLI
    "dnspython==2.1.0",  # Query DNS seeds
    "watchdog==2.1.3",  # Filesystem event watching - watches keyring.yaml
]

upnp_dependencies = [
    "miniupnpc==2.2.2",  # Allows users to open ports on their router
]

dev_dependencies = [
    "pytest",
    "pytest-asyncio",
    "flake8",
    "mypy",
    "black",
    "aiohttp_cors",  # For blackd
    "ipython",  # For asyncio debugging
    "types-setuptools",
]

kwargs = dict(
    name="flax-blockchain",
    description="Flax blockchain full node, farmer, timelord, and wallet.",
    url="https://flaxnetwork.org/",
    license="Apache License",
    python_requires=">=3.7, <4",
    keywords="flax blockchain node",
    install_requires=dependencies,
    setup_requires=["setuptools_scm"],
    extras_require=dict(
        uvloop=["uvloop"],
        dev=dev_dependencies,
        upnp=upnp_dependencies,
    ),
    packages=[
        "build_scripts",
        "flax",
        "flax.cmds",
        "flax.clvm",
        "flax.consensus",
        "flax.daemon",
        "flax.full_node",
        "flax.timelord",
        "flax.farmer",
        "flax.farmer.pooling",
        "flax.harvester",
        "flax.introducer",
        "flax.plotting",
        "flax.pools",
        "flax.protocols",
        "flax.rpc",
        "flax.server",
        "flax.simulator",
        "flax.types.blockchain_format",
        "flax.types",
        "flax.util",
        "flax.wallet",
        "flax.wallet.puzzles",
        "flax.wallet.rl_wallet",
        "flax.wallet.cc_wallet",
        "flax.wallet.did_wallet",
        "flax.wallet.settings",
        "flax.wallet.trading",
        "flax.wallet.util",
        "flax.ssl",
        "mozilla-ca",
    ],
    entry_points={
        "console_scripts": [
            "flax = flax.cmds.flax:main",
            "flax_wallet = flax.server.start_wallet:main",
            "flax_full_node = flax.server.start_full_node:main",
            "flax_harvester = flax.server.start_harvester:main",
            "flax_farmer = flax.server.start_farmer:main",
            "flax_introducer = flax.server.start_introducer:main",
            "flax_timelord = flax.server.start_timelord:main",
            "flax_timelord_launcher = flax.timelord.timelord_launcher:main",
            "flax_full_node_simulator = flax.simulator.start_simulator:main",
        ]
    },
    package_data={
        "flax": ["pyinstaller.spec"],
        "": ["*.clvm", "*.clvm.hex", "*.clib", "*.clinc", "*.clsp", "py.typed"],
        "flax.util": ["initial-*.yaml", "english.txt"],
        "flax.ssl": ["flax_ca.crt", "flax_ca.key", "dst_root_ca.pem"],
        "mozilla-ca": ["cacert.pem"],
    },
    version="0.1.3",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    zip_safe=False,
)


if __name__ == "__main__":
    setup(**kwargs)
