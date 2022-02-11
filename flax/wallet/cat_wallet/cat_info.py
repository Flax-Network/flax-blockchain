from dataclasses import dataclass
from typing import List, Optional, Tuple

from flax.types.blockchain_format.program import Program
from flax.types.blockchain_format.sized_bytes import bytes32
from flax.wallet.lineage_proof import LineageProof
from flax.util.streamable import Streamable, streamable


@dataclass(frozen=True)
@streamable
class CATInfo(Streamable):
    limitations_program_hash: bytes32
    my_tail: Optional[Program]  # this is the program
    lineage_proofs: List[Tuple[bytes32, Optional[LineageProof]]]  # {coin.name(): lineage_proof}
