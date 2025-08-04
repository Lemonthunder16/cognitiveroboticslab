import RPi.GPIO as GPIO
import time
import random

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define GPIO pins for each lane's LEDs
PIN_MAP = {
    'A': {'R': 17, 'Y': 27, 'G': 22},
    'B': {'R': 5,  'Y': 6,  'G': 13},
    'C': {'R': 19, 'Y': 26, 'G': 21},
}

# Setup all pins as outputs and turn them off initially
for lane_pins in PIN_MAP.values():
    for pin in lane_pins.values():
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

# Queues and ambulance flags
queue = {'A': [], 'B': [], 'C': []}
ambulance_flags = {'A': False, 'B': False, 'C': False}

def set_light(lane, color):
    """Set the specified light color ON, others OFF for the lane."""
    pins = PIN_MAP[lane]
    # Turn all off first
    for c in ['R', 'Y', 'G']:
        GPIO.output(pins[c], GPIO.LOW)
    # Turn the requested color ON
    GPIO.output(pins[color], GPIO.HIGH)

def all_red():
    for lane in ['A', 'B', 'C']:
        set_light(lane, 'R')

def update_ambulance_flags():
    for lane in ['A', 'B', 'C']:
        ambulance_flags[lane] = 'A' in queue[lane]

def add_random_cars():
    for lane in ['A', 'B', 'C']:
        new_cars = random.randint(1, 3)
        PR = random.random()
        if PR < 0.1:
            queue[lane] += ['A'] * new_cars
            print(f"Lane {lane}: Ambulance(s) arrived! Added {new_cars} ambulances.")
        else:
            queue[lane] += ['C'] * new_cars
            print(f"Lane {lane}: Added {new_cars} new cars.")
        print(f"Lane {lane}: Total vehicles now: {len(queue[lane])}")

def pick_ambulance_lane():
    for lane in ['A', 'B', 'C']:
        if ambulance_flags[lane]:
            return lane
    return None

def pick_next_lane():
    ambulance_lane = pick_ambulance_lane()
    if ambulance_lane:
        return ambulance_lane
    max_lane = max(queue, key=lambda x: len(queue[x]))
    return max_lane if queue[max_lane] else None

def simulate_car_movement_with_preemptive(lane, max_duration):
    print(f"\n--- Starting Yellow Light on lane {lane} ---")
    set_light(lane, 'Y')
    time.sleep(2)

    print(f"--- Green Light on lane {lane} for up to {max_duration} seconds (ambulance priority active) ---")
    set_light(lane, 'G')

    seconds_passed = 0
    while seconds_passed < max_duration:
        update_ambulance_flags()
        ambulance_lane = pick_ambulance_lane()

        # Preempt if ambulance in different lane
        if ambulance_lane and ambulance_lane != lane:
            print(f"\n*** Preempting lane {lane} to serve ambulance in lane {ambulance_lane} ***")
            break

        if queue[lane]:
            car = queue[lane].pop(0)
            print(f"Lane {lane}: 1 {'ambulance' if car == 'A' else 'car'} moved out, remaining cars: {len(queue[lane])}")
        else:
            print(f"Lane {lane}: No cars left to move.")
            break

        seconds_passed += 1
        time.sleep(1)

    print(f"--- Ending with Yellow Light on lane {lane} ---")
    set_light(lane, 'Y')
    time.sleep(2)

    print(f"--- Switching to Red Light on lane {lane} ---")
    set_light(lane, 'R')

    return seconds_passed

def main():
    cycle_duration = 30
    simulation_minutes = 3
    total_seconds = simulation_minutes * 60
    start_time = time.time()
    last_car_add_time = time.time()

    add_random_cars()
    update_ambulance_flags()
    all_red()

    try:
        while time.time() - start_time < total_seconds:
            now = time.time()

            # Add new cars every 30 seconds
            if now - last_car_add_time >= 30:
                add_random_cars()
                update_ambulance_flags()
                last_car_add_time = now

            selected_lane = pick_next_lane()

            if selected_lane:
                print(f"\n*** Selected Lane for green light: {selected_lane} ***")
                simulate_car_movement_with_preemptive(selected_lane, cycle_duration)
            else:
                print("No cars in any lane, all lights Red.")
                all_red()
                time.sleep(5)

    except KeyboardInterrupt:
        print("Exiting, cleaning up GPIO...")

    finally:
        all_red()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
