from __future__ import annotations

import os
import sys

from setuptools import setup

dependencies = [
    "aiofiles==22.1.0",  # Async IO for files
    "blspy==1.0.16",  # Signature library
    "chiavdf==1.0.8",  # timelord and vdf verification
    "chiabip158==1.2",  # bip158-style wallet filters
    "chiapos==1.0.11",  # proof of space
    "clvm==0.9.7",
    "clvm_tools==0.4.6",  # Currying, Program.to, other conveniences
    "chia_rs==0.2.0",
    "clvm-tools-rs==0.1.30",  # Rust implementation of clvm_tools' compiler
    "aiohttp==3.8.3",  # HTTP server for full node rpc
    "aiosqlite==0.17.0",  # asyncio wrapper for sqlite, to store blocks
    "bitstring==3.1.9",  # Binary data management library
    "colorama==0.4.5",  # Colorizes terminal output
    "colorlog==6.7.0",  # Adds color to logs
    "concurrent-log-handler==0.9.20",  # Concurrently log and rotate logs
    "cryptography==38.0.3",  # Python cryptography library for TLS - keyring conflict
    "filelock==3.8.0",  # For reading and writing config multiprocess and multithread safely  (non-reentrant locks)
    "keyring==23.9.3",  # Store keys in MacOS Keychain, Windows Credential Locker
    "PyYAML==6.0",  # Used for config file format
    "setproctitle==1.2.3",  # Gives the flax processes readable names
    "sortedcontainers==2.4.0",  # For maintaining sorted mempools
    "click==8.1.3",  # For the CLI
    "dnspython==2.2.1",  # Query DNS seeds
    "watchdog==2.2.0",  # Filesystem event watching - watches keyring.yaml
    "dnslib==0.9.23",  # dns lib
    "typing-extensions==4.4.0",  # typing backports like Protocol and TypedDict
    "zstd==1.5.2.6",
    "packaging==21.3",
    "psutil==5.9.4",
]

upnp_dependencies = [
    "miniupnpc==2.2.2",  # Allows users to open ports on their router
]

dev_dependencies = [
    "anyio",
    "build",
    "coverage",
    "diff-cover",
    "pre-commit",
    "py3createtorrent",
    "pylint",
    "pytest",
    "pytest-asyncio>=0.18.1",  # require attribute 'fixture'
    "pytest-cov",
    "pytest-monitor; sys_platform == 'linux'",
    "pytest-xdist",
    "twine",
    "isort",
    "flake8",
    # TODO: remove this pin after fixing the new complaints
    "mypy<1",
    "black==22.10.0",
    "aiohttp_cors",  # For blackd
    "ipython",  # For asyncio debugging
    "pyinstaller==5.6.2",
    "types-aiofiles",
    "types-cryptography",
    "types-pkg_resources",
    "types-pyyaml",
    "types-setuptools",
]

legacy_keyring_dependencies = [
    "keyrings.cryptfile==1.3.9",
]

kwargs = dict(
    name="flax-blockchain",
    description="Flax blockchain full node, farmer, timelord, and wallet.",
    url="https://flaxnetwork.org/",
    license="Apache License",
    python_requires=">=3.7, <4",
    keywords="flax blockchain node",
    install_requires=dependencies,
    extras_require=dict(
        dev=dev_dependencies,
        upnp=upnp_dependencies,
        legacy_keyring=legacy_keyring_dependencies,
    ),
    packages=[
        "build_scripts",
        "flax",
        "flax.cmds",
        "flax.clvm",
        "flax.consensus",
        "flax.daemon",
        "flax.data_layer",
        "flax.full_node",
        "flax.timelord",
        "flax.farmer",
        "flax.harvester",
        "flax.introducer",
        "flax.plot_sync",
        "flax.plotters",
        "flax.plotting",
        "flax.pools",
        "flax.protocols",
        "flax.rpc",
        "flax.seeder",
        "flax.server",
        "flax.simulator",
        "flax.types.blockchain_format",
        "flax.types",
        "flax.util",
        "flax.wallet",
        "flax.wallet.db_wallet",
        "flax.wallet.puzzles",
        "flax.wallet.cat_wallet",
        "flax.wallet.did_wallet",
        "flax.wallet.nft_wallet",
        "flax.wallet.settings",
        "flax.wallet.trading",
        "flax.wallet.util",
        "flax.ssl",
        "mozilla-ca",
    ],
    entry_points={
        "console_scripts": [
            "flax = flax.cmds.flax:main",
            "flax_daemon = flax.daemon.server:main",
            "flax_wallet = flax.server.start_wallet:main",
            "flax_full_node = flax.server.start_full_node:main",
            "flax_harvester = flax.server.start_harvester:main",
            "flax_farmer = flax.server.start_farmer:main",
            "flax_introducer = flax.server.start_introducer:main",
            "flax_crawler = flax.seeder.start_crawler:main",
            "flax_seeder = flax.seeder.dns_server:main",
            "flax_timelord = flax.server.start_timelord:main",
            "flax_timelord_launcher = flax.timelord.timelord_launcher:main",
            "flax_full_node_simulator = flax.simulator.start_simulator:main",
            "flax_data_layer = flax.server.start_data_layer:main",
            "flax_data_layer_http = flax.data_layer.data_layer_server:main",
        ]
    },
    package_data={
        "flax": ["pyinstaller.spec"],
        "": ["*.clvm", "*.clvm.hex", "*.clib", "*.clinc", "*.clsp", "py.typed"],
        "flax.util": ["initial-*.yaml", "english.txt"],
        "flax.ssl": ["flax_ca.crt", "flax_ca.key", "dst_root_ca.pem"],
        "mozilla-ca": ["cacert.pem"],
    },
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    zip_safe=False,
    project_urls={
        "Source": "https://github.com/Flax-Network/flax-blockchain/",
        "Changelog": "https://github.com/Flax-Network/flax-blockchain/blob/main/CHANGELOG.md",
    },
)

if "setup_file" in sys.modules:
    # include dev deps in regular deps when run in snyk
    dependencies.extend(dev_dependencies)

if len(os.environ.get("FLAX_SKIP_SETUP", "")) < 1:
    setup(**kwargs)  # type: ignore
