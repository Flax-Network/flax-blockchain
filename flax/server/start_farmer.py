import pathlib
from typing import Dict, Optional

from flax.consensus.constants import ConsensusConstants
from flax.consensus.default_constants import DEFAULT_CONSTANTS
from flax.farmer.farmer import Farmer
from flax.farmer.farmer_api import FarmerAPI
from flax.rpc.farmer_rpc_api import FarmerRpcApi
from flax.server.outbound_message import NodeType
from flax.server.start_service import run_service
from flax.types.peer_info import PeerInfo
from flax.util.config import load_config_cli
from flax.util.default_root import DEFAULT_ROOT_PATH
from flax.util.keychain import Keychain

# See: https://bugs.python.org/issue29288
"".encode("idna")

SERVICE_NAME = "farmer"


def service_kwargs_for_farmer(
    root_path: pathlib.Path,
    config: Dict,
    config_pool: Dict,
    consensus_constants: ConsensusConstants,
    keychain: Optional[Keychain] = None,
) -> Dict:

    connect_peers = []
    fnp = config.get("full_node_peer")
    if fnp is not None:
        connect_peers.append(PeerInfo(fnp["host"], fnp["port"]))

    overrides = config["network_overrides"]["constants"][config["selected_network"]]
    updated_constants = consensus_constants.replace_str_to_bytes(**overrides)

    farmer = Farmer(root_path, config, config_pool, consensus_constants=updated_constants, local_keychain=keychain)
    peer_api = FarmerAPI(farmer)
    network_id = config["selected_network"]
    kwargs = dict(
        root_path=root_path,
        node=farmer,
        peer_api=peer_api,
        node_type=NodeType.FARMER,
        advertised_port=config["port"],
        service_name=SERVICE_NAME,
        server_listen_ports=[config["port"]],
        connect_peers=connect_peers,
        auth_connect_peers=False,
        on_connect_callback=farmer.on_connect,
        network_id=network_id,
    )
    if config["start_rpc_server"]:
        kwargs["rpc_info"] = (FarmerRpcApi, config["rpc_port"])
    return kwargs


def main() -> None:
    config = load_config_cli(DEFAULT_ROOT_PATH, "config.yaml", SERVICE_NAME)
    config_pool = load_config_cli(DEFAULT_ROOT_PATH, "config.yaml", "pool")
    kwargs = service_kwargs_for_farmer(DEFAULT_ROOT_PATH, config, config_pool, DEFAULT_CONSTANTS)
    return run_service(**kwargs)


if __name__ == "__main__":
    main()
