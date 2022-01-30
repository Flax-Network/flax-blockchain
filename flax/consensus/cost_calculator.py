from dataclasses import dataclass
from typing import List, Optional

from flax.types.blockchain_format.program import SerializedProgram
from flax.types.name_puzzle_condition import NPC
from flax.util.ints import uint16, uint64
from flax.util.streamable import Streamable, streamable


@dataclass(frozen=True)
@streamable
class NPCResult(Streamable):
    error: Optional[uint16]
    npc_list: List[NPC]
    cost: uint64  # The total cost of the block, including CLVM cost, cost of
    # conditions and cost of bytes


def calculate_cost_of_program(program: SerializedProgram, npc_result: NPCResult, cost_per_byte: int) -> uint64:
    """
    This function calculates the total cost of either a block or a spendbundle
    """
    return npc_result.cost
