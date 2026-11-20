"""Exact unit conversions and the KERC time-of-day clock (SPEC-001 section 4).

All optimisation arithmetic in this project is integer:
    power  -> watts (int)            price -> paise/kWh (int)
    slot   -> minutes (int)          rho   -> paise/kW (int)

Conversions from kW / rupees use ``decimal.Decimal`` built from ``str(x)`` so that
inputs such as 5.6 or 0.1 are converted exactly, and anything that is not exactly
representable at the target resolution is rejected instead of silently rounded.
"""
from __future__ import annotations

from decimal import Decimal, InvalidOperation
from fractions import Fraction
from typing import Union

Number = Union[int, float, str, Decimal]

#: EC_int, DC_int and TEC_int are expressed in units of 1/SCALE_INR rupees (SPEC-001 section 4).
#: 6_000_000 = 100 (paise per rupee) * 1000 (W per kW) * 60 (minutes per hour).
SCALE_INR: int = 100 * 1000 * 60
MINUTES_PER_HOUR: int = 60


def _exact_int(value: Number, factor: int, what: str) -> int:
    try:
        d = Decimal(str(value)) * factor
    except InvalidOperation as exc:  # pragma: no cover - defensive
        raise ValueError(f"{what}: cannot parse {value!r} as a number") from exc
    if d != d.to_integral_value():
        raise ValueError(
            f"{what}: {value!r} is not exactly representable at the engine resolution "
            f"(x{factor}); would require rounding"
        )
    return int(d)


def kw_to_w(kw: Number) -> int:
    """kW -> integer watts (exact at 1 W)."""
    return _exact_int(kw, 1000, "power (kW)")


def inr_to_paise(inr: Number) -> int:
    """Rupees (per kWh or per kW) -> integer paise (exact at 1 paise)."""
    return _exact_int(inr, 100, "money (INR)")


def scaled_to_inr(value_int: int) -> Fraction:
    """Convert an EC_int / DC_int / TEC_int value to exact rupees."""
    return Fraction(value_int, SCALE_INR)


def format_inr(value_int: int) -> str:
    """Human readable rupees with 2 decimals (display only)."""
    return f"{float(scaled_to_inr(value_int)):.2f}"


# --- KERC HT-2(a) time-of-day clock (03_tariff/tariff_reference.md, Dec-June) ---------
#: (start_hour, end_hour, tier) with end exclusive; tier in {"peak","normal","off"}.
KERC_TOD_CLOCK = (
    (0, 6, "off"),      # 22:00-06:00 wraps midnight
    (6, 9, "peak"),
    (9, 18, "normal"),
    (18, 22, "peak"),
    (22, 24, "off"),
)


def tier_at_minute(minute_of_day: int) -> str:
    """Tier of the KERC ToD clock at a given minute of the day (0..1439)."""
    h = (minute_of_day // 60) % 24
    for start, end, tier in KERC_TOD_CLOCK:
        if start <= h < end:
            return tier
    raise AssertionError("unreachable: clock covers 24 h")  # pragma: no cover


def tou_vector_paise(start_hour: int, delta_t_min: int, n_slots: int,
                     off_paise: int, normal_paise: int, peak_paise: int) -> tuple:
    """Per-slot tariff (paise/kWh) for a shift starting at ``start_hour``.

    A slot takes the tier at its *first* minute (slots must not straddle a tier boundary:
    delta_t_min must divide 60).
    """
    if 60 % delta_t_min != 0:
        raise ValueError("delta_t_min must divide 60 so that slots never straddle a tier boundary")
    rates = {"off": off_paise, "normal": normal_paise, "peak": peak_paise}
    out = []
    for s in range(n_slots):
        minute = start_hour * 60 + s * delta_t_min
        out.append(rates[tier_at_minute(minute % (24 * 60))])
    return tuple(out)
