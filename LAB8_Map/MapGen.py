from PIL import Image, ImageDraw
import math
import serial
import time
import matplotlib.pyplot as plt
import numpy as np

class Map2D:
    def _init_(self, width=500, height=500, scale=10):
        self.width = width
        self.height = height
        self.scale = scale  # e.g. 1 pixel = 1 cm
        self.image = Image.new("RGB", (width, height), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.origin = (width // 2, height // 2)  # Center as (0,0)

    def draw_robot(self, x, y, color="blue"):
        px = self.origin[0] + int(x * self.scale)
        py = self.origin[1] - int(y * self.scale)
        self.draw.ellipse((px-2, py-2, px+2, py+2), fill=color)

    def draw_obstacle(self, x, y, color="black"):
        px = self.origin[0] + int(x * self.scale)
        py = self.origin[1] - int(y * self.scale)
        self.draw.rectangle((px, py, px+1, py+1), fill=color)

    def get_image_array(self):
        return np.array(self.image)

    def save(self, filename="map.png"):
        self.image.save(filename)

map2d = Map2D(width=500, height=500, scale=1)  # 1cm per pixel
map2d.draw_robot(0,0)
# Suppose the robot is at (0,0), facing 0° (upward)
robot_x = 0
robot_y = 0

plt.ion()
fig, ax = plt.subplots()
img_display = ax.imshow(map2d.get_image_array())
plt.title("Live Map")
plt.axis('off')

SERIAL_PORT = 'COM13'       # or '/dev/ttyUSB0' or '/dev/ttyACM0'
BAUD_RATE = 9600

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Wait for Arduino to reset
    print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.\n")

    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            try:
                angle_str, dis_str = line.split(',')
                angle = int(angle_str.strip())
                distance = int(dis_str.strip())
                print(angle,distance)

                obs_x = robot_x + distance * math.cos(math.radians(angle))
                obs_y = robot_x + distance * math.sin(math.radians(angle))
                if distance != -1 and distance > 2 and distance < 100: #real distance within a range gets mapped
                   map2d.draw_obstacle(obs_x,obs_y)

                img_display.set_data(map2d.get_image_array())
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


# Save the map
map2d.save("simple_map.png")