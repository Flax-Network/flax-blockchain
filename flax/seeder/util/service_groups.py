from typing import KeysView, Generator

SERVICES_FOR_GROUP = {
    "all": "flax_seeder_crawler flax_seeder_server".split(),
    "crawler": "flax_seeder_crawler".split(),
    "server": "flax_seeder_server".split(),
}


def all_groups() -> KeysView[str]:
    return SERVICES_FOR_GROUP.keys()


def services_for_groups(groups) -> Generator[str, None, None]:
    for group in groups:
        for service in SERVICES_FOR_GROUP[group]:
            yield service
