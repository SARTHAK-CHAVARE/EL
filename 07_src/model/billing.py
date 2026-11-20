"""Model B: PARTIAL monthly KERC HT-2(a) bill estimate for a scheduled shift (post-hoc; never inside the solver).

Source: 03_tariff/tariff_reference.md (KERC Tariff Order 2025, HT-2(a), FY 2026-27):
    demand charge INR 350 per kVA per month of billing demand;  BD = max(MD, 0.90 x CD).
The energy cost of the shift (EC) already uses the instance's time-of-day tariff vector.

What this estimate IS: (energy cost of the scheduled shift) x (shift-days per month) + 350 x BD,
assuming (i) the same schedule runs on every counted day, (ii) this shift sets the month's maximum demand,
(iii) MD [kVA] = peak [kW] / PF with a constant power factor, and (iv) the shift's ToD prices apply.

What it is NOT: a full bill. Excluded: fixed/other charges, taxes and duties, other shifts and loads, PF surcharge
or incentive, ToD applicability rules (compulsory only for CD >= 500 kVA, optional below), the metering interval of
MD (UNKNOWN relative to our 15-minute slots), rebates and all other billing items. Every result carries this label.

Contract-demand scenarios:
    "renegotiated": CD is lowered to the schedule's own MD, so BD = MD (best case for peak reduction).
    "fixed":        CD stays at a given value (normally the reference schedule's MD), so BD = max(MD, 0.90 CD):
                    a peak cut below 0.90 CD earns nothing until CD is renegotiated.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, Optional, Union

from .tariff import scaled_to_inr

DEMAND_CHARGE_INR_PER_KVA_MONTH = Fraction(350)
BILLING_DEMAND_FLOOR = Fraction(9, 10)
PARTIAL_BILL_LABEL = ("PARTIAL MONTHLY BILL ESTIMATE (KERC HT-2(a) demand charge + energy of the scheduled shift only; "
                      "excludes fixed charges, taxes, other loads/shifts, PF surcharge/incentive, ToD applicability "
                      "rules and other billing items; assumes the same schedule every counted day and that this shift "
                      "sets the monthly MD)")
SCENARIOS = ("renegotiated", "fixed")

Number = Union[int, Fraction]


@dataclass(frozen=True)
class BillingAssumptions:
    days_per_month: int = 26                       # shift-days per billing month
    power_factor: Fraction = Fraction(1)           # MD[kVA] = peak[kW] / PF
    demand_charge_inr_per_kva: Fraction = DEMAND_CHARGE_INR_PER_KVA_MONTH
    bd_floor: Fraction = BILLING_DEMAND_FLOOR

    def __post_init__(self):
        if not isinstance(self.days_per_month, int) or self.days_per_month <= 0:
            raise ValueError("days_per_month must be a positive integer")
        pf = Fraction(self.power_factor)
        if not (0 < pf <= 1):
            raise ValueError("power_factor must be in (0, 1]")
        object.__setattr__(self, "power_factor", pf)
        object.__setattr__(self, "demand_charge_inr_per_kva", Fraction(self.demand_charge_inr_per_kva))
        object.__setattr__(self, "bd_floor", Fraction(self.bd_floor))


@dataclass(frozen=True)
class PartialMonthlyBill:
    scenario: str
    energy_inr: Fraction
    md_kva: Fraction
    cd_kva: Fraction
    billing_demand_kva: Fraction
    demand_charge_inr: Fraction
    total_inr: Fraction
    floor_binding: bool                 # BD set by the 0.90 x CD floor, not by MD
    label: str = PARTIAL_BILL_LABEL


def md_kva(peak_w: int, a: BillingAssumptions) -> Fraction:
    return Fraction(peak_w, 1000) / a.power_factor


def rho_equivalent_inr_per_kw(a: BillingAssumptions) -> Fraction:
    """Per-shift demand-charge intensity (Model A's rho, INR/kW) equivalent to the KERC monthly charge under the
    stated assumptions AND the renegotiated scenario: rho_eq = 350 / (days x PF). Under a fixed CD the marginal value
    of a peak cut is 0 below the floor, so no single rho is equivalent."""
    return a.demand_charge_inr_per_kva / (a.days_per_month * a.power_factor)


def partial_monthly_bill(ec_int: int, peak_w: int, a: BillingAssumptions, scenario: str,
                         cd_kva: Optional[Number] = None) -> PartialMonthlyBill:
    if scenario not in SCENARIOS:
        raise ValueError(f"scenario must be one of {SCENARIOS}")
    md = md_kva(peak_w, a)
    if scenario == "renegotiated":
        if cd_kva is not None:
            raise ValueError("renegotiated scenario sets CD = MD; do not pass cd_kva")
        cd = md
    else:
        if cd_kva is None:
            raise ValueError("fixed scenario requires cd_kva (normally the reference schedule's MD)")
        cd = Fraction(cd_kva)
        if cd <= 0:
            raise ValueError("cd_kva must be positive")
    floor = a.bd_floor * cd
    bd = max(md, floor)
    energy = scaled_to_inr(ec_int) * a.days_per_month
    demand = a.demand_charge_inr_per_kva * bd
    return PartialMonthlyBill(scenario, energy, md, cd, bd, demand, energy + demand, floor > md)


@dataclass(frozen=True)
class BillComparison:
    scenario: str
    reference: PartialMonthlyBill
    candidate: PartialMonthlyBill
    saving_inr: Fraction                # reference total - candidate total (negative => candidate costs more)
    label: str = PARTIAL_BILL_LABEL


def compare_bills(cand_ec_int: int, cand_peak_w: int, ref_ec_int: int, ref_peak_w: int,
                  a: BillingAssumptions) -> Dict[str, BillComparison]:
    """Both scenarios. Under 'fixed', CD = the reference schedule's MD for both schedules."""
    out = {}
    ref_r = partial_monthly_bill(ref_ec_int, ref_peak_w, a, "renegotiated")
    cand_r = partial_monthly_bill(cand_ec_int, cand_peak_w, a, "renegotiated")
    out["renegotiated"] = BillComparison("renegotiated", ref_r, cand_r, ref_r.total_inr - cand_r.total_inr)
    cd = md_kva(ref_peak_w, a)
    ref_f = partial_monthly_bill(ref_ec_int, ref_peak_w, a, "fixed", cd)
    cand_f = partial_monthly_bill(cand_ec_int, cand_peak_w, a, "fixed", cd)
    out["fixed"] = BillComparison("fixed", ref_f, cand_f, ref_f.total_inr - cand_f.total_inr)
    return out
