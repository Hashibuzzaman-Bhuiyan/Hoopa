from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from PIL import Image, ImageOps
from smbus2 import SMBus
import time
import os

# ─── I2C multiplexer ──────────────────────────────────────────────────────────
TCA9548A_ADDRESS = 0x70
TCA9548A_CHANNEL = 5

def select_tca_channel(channel):
    if 0 <= channel <= 7:
        with SMBus(1) as bus:
            bus.write_byte(TCA9548A_ADDRESS, 1 << channel)
    else:
        raise ValueError("Channel must be between 0 and 7")

select_tca_channel(TCA9548A_CHANNEL)

# ─── OLED setup ───────────────────────────────────────────────────────────────
serial = i2c(port=1, address=0x3C)
device = sh1106(serial)

# ─── Helpers ─────────────────────────────────────────────────────────────────
def load_eye(name):
    filepath = f"expressions/{name}.bmp"
    print(f"Loading: {filepath}")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing: {filepath}")
    img = Image.open(filepath).convert("1")
    return ImageOps.invert(img)

def blink_and_show(img, blink=0.1, hold=1.5):
    blank = Image.new("1", (128, 64), color=0)
    device.display(blank)
    time.sleep(blink)
    device.display(img)
    time.sleep(hold)

# ─── Expression loop ─────────────────────────────────────────────────────────
expressions = ["left", "right", "focus", "topLeft", "topRight"]

if __name__ == "__main__":
    last_img = None
    print("Running… Press Ctrl+C to stop.")
    try:
        while True:
            for exp in expressions:
                try:
                    new_img = load_eye(exp)
                    blink_and_show(new_img) if last_img else device.display(new_img)
                    last_img = new_img
                    time.sleep(1)
                except Exception as e:
                    print(f"Error: {e}")
                    device.display(Image.new("1", (128, 64), color=0))
                    break  # Stop the loop on image error
    except KeyboardInterrupt:
        device.display(Image.new("1", (128, 64), color=0))
        print("\nStopped by user (Ctrl+C).")


