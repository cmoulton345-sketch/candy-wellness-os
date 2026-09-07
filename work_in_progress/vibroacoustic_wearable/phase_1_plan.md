# Vibroacoustic Vest - Phase 1: Firmware Skeleton

We are moving from concept to execution. Before we can build the mobile app, we must engineer the brain of the vest: the ESP32 firmware.

This plan focuses on setting up the structural codebase for the microcontroller that will listen for Bluetooth commands and trigger the DRV2605L motor drivers.

## Proposed Changes

We will create a new directory for the hardware codebase at `work_in_progress/vibroacoustic_wearable/firmware/`.

### [NEW] `src/main.cpp`
The main execution loop for the ESP32. It will:
1. Initialize the I2C bus to communicate with the haptic motor drivers.
2. Initialize the BLE (Bluetooth Low Energy) server and begin advertising as "SOMA_VEST".
3. Expose a BLE Characteristic that the mobile app can write to.

### [NEW] `src/HapticController.h`
A modular class to manage the DRV2605L drivers.
- Handles setting the specific vibration modes, frequencies, and amplitudes.
- Maps the incoming byte commands to specific anatomical nodes (e.g., Node 1 = Sacral, Node 5 = Vagus).

### [NEW] `platformio.ini`
The configuration file for PlatformIO (the industry standard for ESP32 development), defining the board type (`esp32dev`) and the required external libraries (such as the Adafruit DRV2605 Library).

## Open Questions

> [!IMPORTANT]
> **Motor Addressing:** A single I2C bus can only support one DRV2605L out of the box because they all have the same hardcoded I2C address (0x5A). To run 5-7 distinct motors along the spine simultaneously, we will need an I2C Multiplexer (like the TCA9548A). Do you want me to include the multiplexer logic in this initial firmware draft, or should we start simple with just a single-motor test script for your first physical bench test?

## Verification Plan
- Compile the code structure mentally/virtually to ensure zero syntax or library errors.
- Verify the BLE architecture is correctly structured to receive byte arrays from a mobile app.
