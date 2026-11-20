"""Peak-aware energy-cost production scheduling: CP-SAT engine (SPEC-001)."""
from .evaluate import Metrics, ScheduleError, check_schedule, evaluate_schedule, rho_star_pair
from .formulation import InfeasibleInstance, build_formulation, placements
from .instance import Instance, Job, Operation, make_instance
from .solver import (InternalConsistencyError, SolveStatus, SolverConfig, Stage, StrategyResult,
                     combine_status, run_lexicographic, solve_min_peak, solve_strategy_a,
                     solve_strategy_b, solve_strategy_c)
from .tariff import SCALE_INR, format_inr, inr_to_paise, kw_to_w, scaled_to_inr
from .validation import InstanceError, validate_instance
