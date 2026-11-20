import dataclasses

import pytest

from model import InstanceError, Job, SolverConfig, build_formulation, make_instance, solve_strategy_a, validate_instance
from benchmark_instance import benchmark_instance


def _inst(**over):
    base = dict(machines=[1], jobs=[("J", {1: 2}, {1: "1"})], T=4, delta_t_min=60, base_kw=0,
                tariff_inr_per_kwh=["5"] * 4)
    base.update(over)
    return make_instance(**base)


def test_benchmark_valid():
    validate_instance(benchmark_instance())


@pytest.mark.parametrize("mutate,msg", [
    (lambda i: dataclasses.replace(i, T=0), "T must be"),
    (lambda i: dataclasses.replace(i, D=99), "deadline D"),
    (lambda i: dataclasses.replace(i, delta_t_min=0), "delta_t_min"),
    (lambda i: dataclasses.replace(i, tariff_paise=(500, 500)), "tariff has 2 entries"),
    (lambda i: dataclasses.replace(i, base_w=-1), "base_w"),
    (lambda i: dataclasses.replace(i, tariff_paise=(500, 500, 500, -5)), "tariff slot 4"),
    (lambda i: dataclasses.replace(i, jobs=()), "no jobs"),
    (lambda i: dataclasses.replace(i, machines=(1, 1)), "duplicate machine"),
    (lambda i: dataclasses.replace(i, base_w=1.5), "floats are not allowed"),
])
def test_invalid_instances_report_problem(mutate, msg):
    with pytest.raises(InstanceError) as e:
        validate_instance(mutate(_inst()))
    assert msg in str(e.value)


def test_job_level_errors_all_listed():
    i = _inst()
    bad = Job("J", {1: 0, 9: 2}, {1: 5}, release=0)
    i = dataclasses.replace(i, jobs=(bad,))
    with pytest.raises(InstanceError) as e:
        validate_instance(i)
    text = str(e.value)
    assert "same machines" in text and "unknown machine 9" in text and ">= 1" in text and "release" in text
    assert len(e.value.problems) >= 4


def test_float_rho_rejected():
    with pytest.raises(InstanceError):
        build_formulation(_inst(), 1.5)
    with pytest.raises(InstanceError):
        build_formulation(_inst(), -1)


def test_overflow_guard():
    huge = make_instance(machines=[1], jobs=[("J", {1: 1}, {1: "1000000"})], T=4, delta_t_min=60,
                         base_kw=0, tariff_inr_per_kwh=["99999999999"] * 4)
    with pytest.raises(InstanceError) as e:
        validate_instance(huge)
    assert "overflow" in str(e.value) or "int64" in str(e.value)
    with pytest.raises(InstanceError):
        solve_strategy_a(huge, SolverConfig())
