import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# --- Pin Definitions ---
# Room RGB LEDs
PIN_MAP = {
    'A': {'R': 17, 'Y': 27, 'G': 22},
    'B': {'R': 5,  'Y': 6,  'G': 13},
    'C': {'R': 19, 'Y': 26, 'G': 21},
}

# Shared sensors
DHT_PIN = 4
IR_PIN = 23
US_TRIG = 18
US_ECHO = 24

# --- Setup GPIOs ---
for room_pins in PIN_MAP.values():
    for pin in room_pins.values():
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

GPIO.setup(IR_PIN, GPIO.IN)
GPIO.setup(US_TRIG, GPIO.OUT)
GPIO.setup(US_ECHO, GPIO.IN)

# --- DHT11 Without Adafruit ---
def read_dht11(pin):
    data = []
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.02)  # 20ms
    GPIO.output(pin, GPIO.HIGH)
    GPIO.setup(pin, GPIO.IN)

    count = 0
    last = -1
    while GPIO.input(pin) == GPIO.LOW:
        continue

    while GPIO.input(pin) == GPIO.HIGH:
        continue

    for i in range(40):
        while GPIO.input(pin) == GPIO.LOW:
            continue
        t = time.time()
        while GPIO.input(pin) == GPIO.HIGH:
            continue
        if time.time() - t > 0.00005:
            data.append(1)
        else:
            data.append(0)

    # Convert bits to bytes
    humidity = int("".join(str(bit) for bit in data[0:8]), 2)
    humidity_dec = int("".join(str(bit) for bit in data[8:16]), 2)
    temperature = int("".join(str(bit) for bit in data[16:24]), 2)
    temperature_dec = int("".join(str(bit) for bit in data[24:32]), 2)
    checksum = int("".join(str(bit) for bit in data[32:40]), 2)

    calc_checksum = (humidity + humidity_dec + temperature + temperature_dec) & 0xFF
    if checksum == calc_checksum:
        return temperature, humidity
    else:
        return None, None

# --- Other Sensors ---
def read_ir(pin):
    return GPIO.input(pin) == GPIO.HIGH

def read_ultrasonic(trig, echo):
    GPIO.output(trig, False)
    time.sleep(0.05)

    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    pulse_start = time.time()
    timeout = pulse_start + 0.04
    while GPIO.input(echo) == 0 and time.time() < timeout:
        pulse_start = time.time()

    pulse_end = time.time()
    timeout = pulse_end + 0.04
    while GPIO.input(echo) == 1 and time.time() < timeout:
        pulse_end = time.time()

    duration = pulse_end - pulse_start
    distance = duration * 17150
    return round(distance, 2)

def set_light(room, color):
    pins = PIN_MAP[room]
    for c in ['R', 'Y', 'G']:
        GPIO.output(pins[c], GPIO.LOW)
    GPIO.output(pins[color], GPIO.HIGH)

def room_logic(temp, humidity, motion, distance):
    print(f"\nSensor Readings: Temp={temp}°C | Humidity={humidity}% | Motion={motion} | Distance={distance} cm")

    # Room A: temperature
    if temp is not None and temp > 28:
        print("Room A: Hot - GREEN")
        set_light('A', 'G')
    elif temp is not None and temp < 20:
        print("Room A: Cold - YELLOW")
        set_light('A', 'Y')
    else:
        set_light('A', 'R')

    # Room B: motion
    if motion:
        print("Room B: Motion detected - GREEN")
        set_light('B', 'G')
    else:
        set_light('B', 'R')

    # Room C: distance
    if distance < 100:
        print("Room C: Object close - GREEN")
        set_light('C', 'G')
    else:
        set_light('C', 'R')

# --- Main Loop ---
def main():
    try:
        while True:
            temp, humidity = read_dht11(DHT_PIN)
            motion = read_ir(IR_PIN)
            distance = read_ultrasonic(US_TRIG, US_ECHO)

            room_logic(temp, humidity, motion, distance)
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nExiting. Cleaning up GPIO...")
    finally:
        for room in PIN_MAP:
            set_light(room, 'R')
        GPIO.cleanup()

if __name__ == "__main__":
    main()