from __future__ import annotations

import time
from dataclasses import dataclass
from secrets import token_bytes
from typing import Optional

from flax.farmer.farmer import Farmer
from flax.harvester.harvester import Harvester
from flax.plot_sync.sender import Sender
from flax.protocols.harvester_protocol import PlotSyncIdentifier
from flax.server.start_service import Service
from flax.server.ws_connection import Message, NodeType
from flax.simulator.time_out_assert import time_out_assert
from flax.types.blockchain_format.sized_bytes import bytes32
from flax.types.peer_info import PeerInfo
from flax.util.ints import uint64


@dataclass
class WSFlaxConnectionDummy:
    connection_type: NodeType
    peer_node_id: bytes32
    peer_host: str = "localhost"
    peer_port: int = 0
    last_sent_message: Optional[Message] = None

    async def send_message(self, message: Message) -> None:
        self.last_sent_message = message


def get_dummy_connection(node_type: NodeType, peer_id: Optional[bytes32] = None) -> WSFlaxConnectionDummy:
    return WSFlaxConnectionDummy(node_type, bytes32(token_bytes(32)) if peer_id is None else peer_id)


def plot_sync_identifier(current_sync_id: uint64, message_id: uint64) -> PlotSyncIdentifier:
    return PlotSyncIdentifier(uint64(int(time.time())), current_sync_id, message_id)


async def start_harvester_service(harvester_service: Service[Harvester], farmer_service: Service[Farmer]) -> Harvester:
    # Set the `last_refresh_time` of the plot manager to avoid initial plot loading
    harvester: Harvester = harvester_service._node
    harvester.plot_manager.last_refresh_time = time.time()
    await harvester_service.start()
    harvester_service.add_peer(PeerInfo(str(farmer_service.self_hostname), farmer_service._server.get_port()))
    harvester.plot_manager.stop_refreshing()

    assert harvester.plot_sync_sender._sync_id == 0
    assert harvester.plot_sync_sender._next_message_id == 0
    assert harvester.plot_sync_sender._last_sync_id == 0
    assert harvester.plot_sync_sender._messages == []

    def wait_for_farmer_connection(plot_sync_sender: Sender) -> bool:
        return plot_sync_sender._connection is not None

    await time_out_assert(10, wait_for_farmer_connection, True, harvester.plot_sync_sender)

    return harvester
