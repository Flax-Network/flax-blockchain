from typing import KeysView, Generator

SERVICES_FOR_GROUP = {
    "all": "flax_harvester flax_timelord_launcher flax_timelord flax_farmer flax_full_node flax_wallet".split(),
    "node": "flax_full_node".split(),
    "harvester": "flax_harvester".split(),
    "farmer": "flax_harvester flax_farmer flax_full_node flax_wallet".split(),
    "farmer-no-wallet": "flax_harvester flax_farmer flax_full_node".split(),
    "farmer-only": "flax_farmer".split(),
    "timelord": "flax_timelord_launcher flax_timelord flax_full_node".split(),
    "timelord-only": "flax_timelord".split(),
    "timelord-launcher-only": "flax_timelord_launcher".split(),
    "wallet": "flax_wallet flax_full_node".split(),
    "wallet-only": "flax_wallet".split(),
    "introducer": "flax_introducer".split(),
    "simulator": "flax_full_node_simulator".split(),
}


def all_groups() -> KeysView[str]:
    return SERVICES_FOR_GROUP.keys()


def services_for_groups(groups) -> Generator[str, None, None]:
    for group in groups:
        for service in SERVICES_FOR_GROUP[group]:
            yield service


def validate_service(service: str) -> bool:
    return any(service in _ for _ in SERVICES_FOR_GROUP.values())
