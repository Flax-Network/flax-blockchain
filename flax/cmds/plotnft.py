from decimal import Decimal
from typing import Optional

import click


MAX_CMDLINE_FEE = Decimal(0.5)


def validate_fee(ctx, param, value):
    try:
        fee = Decimal(value)
    except ValueError:
        raise click.BadParameter("Fee must be decimal dotted value in XFX (e.g. 0.00005)")
    if fee < 0 or fee > MAX_CMDLINE_FEE:
        raise click.BadParameter(f"Fee must be in the range 0 to {MAX_CMDLINE_FEE}")
    return value


