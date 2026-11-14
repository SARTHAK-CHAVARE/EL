# CURRENT HARDWARE SPECIFICATION

> STATUS: CURRENT / AUTHORITATIVE
>
> This document supersedes earlier hardware proposals.

## 1. Physical Testbed

The project uses a programmable low-voltage machine-load emulation testbed.

It is NOT a real factory and NOT a real industrial production line.

The testbed uses 12V DC loads to emulate different machine electrical profiles.

## 2. Measurement

### INA226

INA226 DC power-monitoring modules are used to measure:

- voltage
- current
- electrical power

The INA226 communicates with the ESP32 using I²C.

## 3. Controller

### ESP32

Responsibilities:

- read INA226 measurements
- control load switching
- timestamp machine/load states
- communicate with Raspberry Pi
- publish measurements

## 4. Load Control

Candidate switching:

- relay module
- MOSFET-based switching

Final choice depends on actual component ratings and electrical verification.

## 5. Load Emulators

Candidate 12V DC loads:

- DC motor
- DC heater/load
- LED load
- DC fan/pump

These are machine-load emulators, not industrial-machine replicas.

## 6. Raspberry Pi 5

The Raspberry Pi acts as the local optimization and experiment server.

Responsibilities:

- load job data
- load tariff profiles
- construct scheduling model
- run OR-Tools CP-SAT
- run epsilon-constraint workflow
- generate schedules
- send schedules to ESP32
- receive measurements
- log experiment data
- benchmark optimization time

## 7. Communication

Raspberry Pi ↔ Wi-Fi ↔ ESP32

MQTT may be used for:

- schedule commands
- power measurements
- state information
- timestamps
- experiment identifiers

Serial communication can be retained for debugging.

## 8. Current Architecture

Raspberry Pi 5
        ↓
   Wi-Fi / MQTT
        ↓
      ESP32
        ↓
    INA226 sensors
        ↓
Relay / MOSFET switching
        ↓
  12V DC loads

## 9. Superseded Hardware

PZEM-004T was considered in an earlier design.

It is NOT part of the current 12V DC testbed.

The current DC measurement direction is INA226.

## 10. Safety

The core testbed is low-voltage DC.

Do not expose mains wiring on the breadboard.

Use an enclosed commercial AC/DC supply.

Verify:

- supply current capacity
- switching-device ratings
- wire current capacity
- INA226 shunt configuration
- ESP32 I²C compatibility
- load current
- thermal limits

Exact final hardware ratings must be verified from the purchased components.