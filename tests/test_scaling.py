from fractions import Fraction

import pytest

from model import SCALE_INR, format_inr, inr_to_paise, kw_to_w, scaled_to_inr, evaluate_schedule, Operation
from model.tariff import tier_at_minute, tou_vector_paise
from benchmark_instance import benchmark_instance


def test_exact_conversions():
    assert kw_to_w("37") == 37000 and kw_to_w(0.1) == 100 and kw_to_w(2.005) == 2005
    assert inr_to_paise(5.6) == 560 and inr_to_paise("12.70") == 1270 and inr_to_paise(15) == 1500


@pytest.mark.parametrize("bad", ["0.0005", 1.0001])
def test_kw_not_representable_is_rejected(bad):
    with pytest.raises(ValueError):
        kw_to_w(bad)


def test_inr_not_representable_is_rejected():
    with pytest.raises(ValueError):
        inr_to_paise("5.601")


def test_scale_constant_and_hand_value():
    assert SCALE_INR == 6_000_000
    # slot 1 of Schedule B: 5.60 INR/kWh * 37 kW * 1 h = INR 207.20
    assert scaled_to_inr(560 * 60 * 37000) == Fraction(20720, 100)
    assert format_inr(4_713_600_000) == "785.60"


def test_energy_cost_integer_values_match_hand_calc():
    inst = benchmark_instance()
    b = [Operation("J1", 1, 1, 2), Operation("J2", 1, 3, 5), Operation("J4", 1, 6, 8), Operation("J3", 2, 1, 1)]
    m = evaluate_schedule(inst, b, 1500)
    assert m.ec_int == 4_713_600_000          # INR 785.60
    assert m.dc_int == 60 * 1500 * 37000 == 3_330_000_000  # INR 555.00
    assert m.energy_kwh == Fraction(121)       # hand_calculations.md: 121 kWh


def test_dt_15_min_scaling():
    # 1 kW for one 15-min slot at INR 8/kWh = INR 2.00
    from model import make_instance
    inst = make_instance(machines=[1], jobs=[("J", {1: 1}, {1: "1"})], T=1, delta_t_min=15,
                         base_kw=0, tariff_inr_per_kwh=["8"])
    m = evaluate_schedule(inst, [Operation("J", 1, 1, 1)], 0)
    assert m.ec_inr == 2


def test_tou_clock():
    assert tier_at_minute(5 * 60) == "off" and tier_at_minute(6 * 60) == "peak"
    assert tier_at_minute(9 * 60) == "normal" and tier_at_minute(18 * 60) == "peak"
    assert tier_at_minute(22 * 60) == "off" and tier_at_minute(23 * 60 + 59) == "off"
    v = tou_vector_paise(16, 60, 8, 560, 660, 760)
    assert v == (660, 660, 760, 760, 760, 760, 560, 560)
    with pytest.raises(ValueError):
        tou_vector_paise(16, 25, 4, 1, 2, 3)
