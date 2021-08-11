from dataclasses import dataclass

from blspy import G2Element
from flax.types.blockchain_format.proof_of_space import ProofOfSpace
from flax.types.blockchain_format.sized_bytes import bytes32
from flax.util.ints import uint64
from flax.util.streamable import streamable, Streamable


@dataclass(frozen=True)
@streamable
class PartialPayload(Streamable):
    proof_of_space: ProofOfSpace
    sp_hash: bytes32
    end_of_sub_slot: bool
    payout_address: str  # The farmer can choose where to send the rewards. This can take a few minutes


@dataclass(frozen=True)
@streamable
class SubmitPartial(Streamable):
    payload: PartialPayload
    partial_aggregate_signature: G2Element  # Sig of partial by plot key and pool key
    difficulty: uint64
