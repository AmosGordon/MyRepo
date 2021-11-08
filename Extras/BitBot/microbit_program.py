from cyberbot import *

# moves servos based on direction and speed
def servo(side, speed):
    if side == "left":
        bot(19).servo_speed(speed)
    if side == "right":
        bot(18).servo_speed(speed)

# toggles leds based on direction
def led(side, on_off):
    if side == "left":
        bot(0).write_digital(on_off)
    if side == "right":
        bot(15).write_digital(on_off)
        
def sound(pitch, time):
    bot(22).tone(pitch, time)
        
while True:
    
    # rest if no button is pressed
    if not button_a.is_pressed() and not button_b.is_pressed():
        servo("left", None)
        servo("right", None)
        led("left", 0)
        led("right", 0)
        
    # moves forward and turns on both leds if both buttons are pressed
    if button_a.is_pressed() and button_b.is_pressed():
        servo("left", 75)
        servo("right", -75)
        led("left", 1)
        led("right", 1)
        sound(1500, 150)
        sound(1000, 150)
    
    # moves left and turns on left led when button A is pressed
    elif button_a.is_pressed():
        servo("left", 75)
        servo("right", 75)
        led("left", 1)
        
    # moves right and turns on right led if button A is pressed
    elif button_b.is_pressed():
        servo("left", -75)
        servo("right", -75)
        led("right", 1)
