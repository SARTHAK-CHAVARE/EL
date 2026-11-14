# KERC TARIFF REFERENCE

## Source

Karnataka Electricity Regulatory Commission
Tariff Order 2025 — All ESCOMs
Annexure 9

## Tariff Category

HT-2(a) — Industrial

## Study Year

FY 2026–27

## Effective Date

1 April 2026

## Energy Charge

₹6.60/kWh

## Demand Charge

₹350/kVA/month of billing demand

## Billing Demand

BD = max(MD, 0.90 × CD)

where:

MD = maximum demand recorded during the month
CD = contract demand

## December–June ToD

06:00–09:00 → +₹1.00/kWh
09:00–18:00 → ₹0.00/kWh
18:00–22:00 → +₹1.00/kWh
22:00–06:00 → −₹1.00/kWh

With the ₹6.60/kWh base rate:

06:00–09:00 → ₹7.60/kWh
09:00–18:00 → ₹6.60/kWh
18:00–22:00 → ₹7.60/kWh
22:00–06:00 → ₹5.60/kWh

## July–November

The tariff-order table gives zero ToD adjustment in the listed periods.

## ToD Applicability

The tariff order states compulsory ToD for relevant HT-2 categories with contract
demand of 500 kVA and above, while optional ToD continues below 500 kVA.

The exact experimental scenario must be stated explicitly.

## Power Factor

The tariff order contains an average PF requirement and surcharge provisions for
PF below 0.90.

The DC testbed does not reproduce industrial AC PF behavior.

## Important Modelling Distinction

Actual KERC demand billing is:

₹350/kVA/month

The experimental sensitivity parameter ρ is NOT the KERC tariff.

A normalized research model may use:

Cρ(S) = EC(S) + ρ Ppeak(S)

This is an experimental sensitivity model, not an actual monthly electricity bill.

## kW vs kVA

Scheduling model:
Ppeak,kW

KERC billing:
MD,kVA

They must not be silently equated.

A kW ≈ kVA mapping requires an explicit PF≈1 assumption.

## Billing Horizon

KERC demand charge is monthly.

A short physical testbed experiment does not represent a monthly industrial bill.

Physical experiments validate power/energy model behavior.

Normalized tariff experiments study economic sensitivity.

## Exclusions for Core Model

Unless specifically studied:

- discounted energy rate scheme
- detailed industrial billing extras
- AC power-factor behavior
- real monthly aggregation

must remain outside the core optimization model.