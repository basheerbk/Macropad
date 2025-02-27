
import board
import digitalio
import usb_hid
import time
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Define button GPIO pins
button_pins = [board.GP15, board.GP7, board.GP0]

# Initialize buttons with pull-up resistors
buttons = []
for pin in button_pins:
    button = digitalio.DigitalInOut(pin)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
    buttons.append(button)

# Define built-in LED (optional for feedback)
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT

# Initialize USB Keyboard
keyboard = Keyboard(usb_hid.devices)

# Key mappings
key_mappings = [
    [Keycode.CONTROL, Keycode.C],  # Button 1 → Copy (Ctrl + C)
    [Keycode.CONTROL, Keycode.Z],  # Button 2 → Undo (Ctrl + Z)
    [Keycode.CONTROL, Keycode.V]   # Button 3 → Paste (Ctrl + V)  **No Enter**
]

# Debounce settings
DEBOUNCE_TIME = 0.2  # 200ms debounce
last_pressed = [0] * len(button_pins)
pressed_flag = [False] * len(button_pins)

print("Macropad ready...")

while True:
    current_time = time.monotonic()  # Get current time
    
    for i, button in enumerate(buttons):
        if not button.value:  # Button pressed (LOW)
            if not pressed_flag[i] and (current_time - last_pressed[i] > DEBOUNCE_TIME):
                keyboard.press(*key_mappings[i])  # Send key combination
                keyboard.release_all()  # Release keys
                led.value = True  # LED on (feedback)
                
                print(f"Pressed: {key_mappings[i]}")  # Debug message
                pressed_flag[i] = True  # Mark button as pressed
                last_pressed[i] = current_time  # Update last press time
        else:
            if pressed_flag[i]:  # Button released
                keyboard.release_all()  # Ensure all keys are released
                pressed_flag[i] = False  # Reset flag
                led.value = False  # LED off (feedback)
    
    time.sleep(0.01)  # Small delay to reduce CPU usage
