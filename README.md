# Local AI Study Buddy (Flask + Ollama + ESP32)

A 100% local, offline desktop study companion that reads your syllabus via Flask and Ollama, guides you on how to study and solve problems, and syncs status + cute facial expressions to an ESP32 OLED desk buddy with mic, speaker, and haptic feedback.

## Hardware Components
- ESP32 DevKit Board (USB-C)
- 0.96-inch OLED Display (I2C)
- INMP441 Microphone Module
- MAX98357A Amplifier Module
- 8-Ohm 3W Speaker
- Mini Vibration Motor
- 2N2222 NPN Transistor
- 1K Ohm Resistor
- 1N4007 Diode
- 1000µF Electrolytic Capacitor
- Medium Breadboard
- Jumper Wires Pack (Male-to-Female & Male-to-Male)
- 5V / 2A Mobile Charger & USB-C Cable

## Quick Start
1. Run Ollama locally (`ollama serve`) with your local model ready.
2. Start the Flask backend server (`python backend/app.py`).
3. Flash the ESP32 sketch with your local Wi-Fi credentials and PC's local IP address.
