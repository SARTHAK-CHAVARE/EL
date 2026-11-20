"""Model B partial monthly bill (model/billing.py): hand-checked examples, scenario semantics, labelling."""
from fractions import Fraction as F

import pytest

from model.billing import (PARTIAL_BILL_LABEL, BillingAssumptions, compare_bills, md_kva, partial_monthly_bill,
                           rho_equivalent_inr_per_kw)

INR = 6_000_000                       # ec_int units per rupee
B_EC, B_PK = 78560 * INR // 100, 37000     # benchmark energy-only: INR 785.60, 37 kW
C_EC, C_PK = 91260 * INR // 100, 27000     # benchmark peak-aware:  INR 912.60, 27 kW


def test_rho_equivalent():
    assert rho_equivalent_inr_per_kw(BillingAssumptions(26)) == F(350, 26)           # 13.46...
    assert rho_equivalent_inr_per_kw(BillingAssumptions(30)) == F(35, 3)             # 11.67
    assert rho_equivalent_inr_per_kw(BillingAssumptions(26, F(9, 10))) == F(350, 26) / F(9, 10)


def test_renegotiated_benchmark_by_hand():
    a = BillingAssumptions(26)
    b = partial_monthly_bill(B_EC, B_PK, a, "renegotiated")
    c = partial_monthly_bill(C_EC, C_PK, a, "renegotiated")
    assert b.energy_inr == F("20425.6") and b.demand_charge_inr == 350 * 37 and b.total_inr == F("33375.6")
    assert c.total_inr == F("23727.6") + 350 * 27 == F("33177.6")
    cmp = compare_bills(C_EC, C_PK, B_EC, B_PK, a)
    assert cmp["renegotiated"].saving_inr == F(198)
    # consistency with Model A: per-shift saving at rho_eq times days equals the monthly saving
    rho = rho_equivalent_inr_per_kw(a)
    per_shift = (F(B_EC - C_EC, INR)) + rho * F(B_PK - C_PK, 1000)
    assert per_shift * 26 == F(198)


def test_fixed_contract_demand_floor_can_reverse_the_result():
    cmp = compare_bills(C_EC, C_PK, B_EC, B_PK, BillingAssumptions(26))["fixed"]
    assert cmp.candidate.cd_kva == 37 and cmp.candidate.billing_demand_kva == F("33.3") and cmp.candidate.floor_binding
    assert not cmp.reference.floor_binding
    assert cmp.saving_inr == F("33375.6") - (F("23727.6") + 350 * F("33.3")) == F(-2007)


def test_47_to_32_kva_example_from_roadmap():
    a = BillingAssumptions(26)
    fixed = partial_monthly_bill(0, 32000, a, "fixed", 47)
    reneg = partial_monthly_bill(0, 32000, a, "renegotiated")
    assert fixed.billing_demand_kva == F("42.3") and fixed.demand_charge_inr == F(14805)
    assert reneg.billing_demand_kva == 32 and reneg.demand_charge_inr == 11200
    full = partial_monthly_bill(0, 47000, a, "fixed", 47).demand_charge_inr
    assert (full - fixed.demand_charge_inr) / (full - reneg.demand_charge_inr) == F(47 - F("42.3"), 15)   # ~31 %


def test_power_factor_converts_kw_to_kva():
    a = BillingAssumptions(26, F(9, 10))
    assert md_kva(27000, a) == 30
    assert partial_monthly_bill(0, 27000, a, "renegotiated").demand_charge_inr == 350 * 30


def test_label_and_input_validation():
    a = BillingAssumptions()
    bill = partial_monthly_bill(B_EC, B_PK, a, "renegotiated")
    assert bill.label == PARTIAL_BILL_LABEL and "PARTIAL" in bill.label and "excludes" in bill.label
    with pytest.raises(ValueError):
        partial_monthly_bill(B_EC, B_PK, a, "fixed")
    with pytest.raises(ValueError):
        partial_monthly_bill(B_EC, B_PK, a, "renegotiated", 40)
    with pytest.raises(ValueError):
        partial_monthly_bill(B_EC, B_PK, a, "monthly")
    for bad in (dict(days_per_month=0), dict(power_factor=F(0)), dict(power_factor=F(11, 10)), dict(days_per_month=2.5)):
        with pytest.raises(ValueError):
            BillingAssumptions(**bad)
