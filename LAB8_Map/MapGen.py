import math
import serial
import time
import matplotlib.pyplot as plt
import numpy as np
import json

GRID_SIZE = 25  # 25x25 grid
GRID_SCALE = 4  # cm per cell (assuming map 100cm x 100cm)

grid_map = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

robot_grid_x = GRID_SIZE // 2
robot_grid_y = GRID_SIZE // 2

plt.ion()
fig, ax = plt.subplots()
img_display = ax.imshow(grid_map, cmap='Greys', vmin=0, vmax=1)
plt.title("Live Grid Map (25x25)")
plt.axis('off')

SERIAL_PORT = 'COM8'       # Adjust if needed
BAUD_RATE = 9600

def mark_obstacle(distance, angle):
    dx = distance * math.cos(math.radians(angle))
    dy = distance * math.sin(math.radians(angle))

    grid_x = robot_grid_x + int(round(dx / GRID_SCALE))
    grid_y = robot_grid_y - int(round(dy / GRID_SCALE))

    if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
        grid_map[grid_y, grid_x] = 1

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.\n")

    sweep_count = 0
    prev_angle = None

    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            try:
                angle_str, dis_str = line.split(',')
                angle = int(angle_str.strip())
                distance = int(dis_str.strip())
                print(angle, distance)

                # Detect sweep completion: angle wraps around from high to low (e.g., from > 350 to < 10)
                if prev_angle is not None and prev_angle > 350 and angle < 10:
                    sweep_count += 1
                    print(f"Sweep #{sweep_count} completed.")

                    if sweep_count >= 10:
                        print("Completed 10 sweeps. Stopping.")
                        break

                prev_angle = angle

                if distance != -1 and 2 < distance < 100:
                    mark_obstacle(distance, angle)

                img_display.set_data(grid_map)
                plt.draw()
                plt.pause(0.001)

            except ValueError:
                print(f"Invalid line: {line}")

except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
except KeyboardInterrupt:
    print("Interrupted by user. Exiting...")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")

# Save grid map as JSON
with open("grid_map.json", "w") as f:
    json.dump(grid_map.tolist(), f)
print("Grid map saved as grid_map.json")
