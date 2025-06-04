import time
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_bus_device.i2c_device import I2CDevice

# ========== CONFIGURATION ==========
BODY_TCA_CHANNEL = 0  # PCA9685 for upper body, neck, arms
LEG_TCA_CHANNEL = 6   # PCA9685 for legs, hips, knees, feet
TCA_ADDR = 0x70       # TCA9548A I2C multiplexer address

# ========== I2C SETUP ==========
i2c = busio.I2C(board.SCL, board.SDA)

def select_tca_channel(channel):
    """Activate only the specified TCA9548A I2C channel."""
    if 0 <= channel <= 7:
        with I2CDevice(i2c, TCA_ADDR) as dev:
            dev.write(bytes([1 << channel]))

def calculate_duty(angle):
    """Convert angle to PWM duty cycle."""
    min_pulse = 500
    max_pulse = 2500
    pulse = min_pulse + (max_pulse - min_pulse) * angle / 180
    duty = int(pulse / 1_000_000 * 50 * 65535)
    return duty

def set_multiple_servo_angles(tca_channel, servo_angles):
    """Select TCA channel and set multiple servo angles on the corresponding PCA9685."""
    select_tca_channel(tca_channel)
    time.sleep(0.01)
    
    pca = PCA9685(i2c)
    pca.frequency = 50

    for channel, angle in servo_angles.items():
        duty = calculate_duty(angle)
        pca.channels[channel].duty_cycle = duty
        print(f"[TCA {tca_channel}] PCA channel {channel} -> {angle}°")
        time.sleep(0.05)

def initialize_body_servos():
    set_multiple_servo_angles(BODY_TCA_CHANNEL, {
        9: 90,    # Neck Y (Back 80°, Base 90°, Front 110°)
        10: 100,   # Neck X (Left 0°, Base 85°, Right 175°)
        8: 90,    # Chest-Arm Left (Down 180°, Base 90°, Up 0°)
        11: 90,   # Chest-Arm Right (Down 0°, Base 90°, Up 180°)
        0: 175,   # Shoulder Left (Inside 180°, Base 180°, Outside 0°)
        4: 0,     # Shoulder Right (Inside 0°, Base 0°, Outside 180°)
        1: 70,    # Bicep Left (Inside 180°, Base 90°, Outside 0°)
        5: 90,    # Bicep Right (Inside 0°, Base 90°, Outside 180°)
        2: 180,   # Elbow Left (Down 180°, Base 180°, Up 0°)
        6: 5,     # Elbow Right (Down 5°, Base 5°, Up 180°)
        3: 70,    # Gripper Left (Close 70°, Base 70°, Open 180°)
        7: 120,   # Gripper Right (Close 120°, Base 120°, Open 10°)
        12: 93,   # Chest Left-Right (Right 70°, Base 90°, Left 110°)
        14: 75,   # Chest Up-Down (up 70°, Base 90°, down 110°)
        13: 100   # Spinal X (Left 60°, Base 100°, Right 140°)
    })

def initialize_leg_servos():
    set_multiple_servo_angles(LEG_TCA_CHANNEL, {
        8: 95,    # Lumbar Left-Right (Left 110°, Base 90°, Right 70°)
        11: 90,   # Lumbar Up-Down (Back 110°, Base 90°, Front 40°)
        9: 160,   # Pelvic Left (Out 170°, Base 155°, In 140°)
        10: 15,   # Pelvic Right (Out 5°, Base 15°, In 30°)
        2: 173,   # Pubis Left X (Inside 180°, Base 170°, Outside 160°)
        7: 7,    # Pubis Right X (Inside 0°, Base 10°, Outside 20°)
        3: 90,    # Femur Left (Up 50°, Base 90°, Down 130°)
        6: 95,    # Femur Right (Up 130°, Base 90°, Down 50°)
        0: 5,     # Patella Left (Up 5°, Base 5°, Down 50°)
        4: 180,   # Patella Right (Up 180°, Base 180°, Down 135°)
        1: 70,    # Tarsal Left (Up 0°, Base 40°, Down 90°)
        5: 135    # Tarsal Right (Up 180°, Base 140°, Down 90°)
    })

if __name__ == "__main__":
    print("Initializing Body Servos to Base Positions...")
    initialize_body_servos()
    print("Initializing Leg Servos to Base Positions...")
    initialize_leg_servos()
    print("Initialization complete.")




