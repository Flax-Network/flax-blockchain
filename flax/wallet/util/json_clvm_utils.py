from __future__ import annotations

from typing import Any

from flax.types.blockchain_format.program import Program


def json_to_flaxlisp(json_data: Any) -> Any:
    list_for_flaxlisp = []
    if isinstance(json_data, list):
        for value in json_data:
            list_for_flaxlisp.append(json_to_flaxlisp(value))
    else:
        if isinstance(json_data, dict):
            for key, value in json_data:
                list_for_flaxlisp.append((key, json_to_flaxlisp(value)))
        else:
            list_for_flaxlisp = json_data
    return Program.to(list_for_flaxlisp)
