import pygame
import pifacedigitalio as pio
import time as t

piface = pio.PiFaceDigital()

pygame.mixer.init()
sound = pygame.mixer.Sound('spider3.wav')
sound.set_volume(.035)

def lid_up(delay):
    piface.relays[0].turn_on()
    if delay is not None:
        t.sleep(delay)
    
def lid_down(delay):
    piface.relays[0].turn_off()
    if delay is not None:
        t.sleep(delay)


def trigger1():
    sound.play()
    t.sleep(1.5)
    for x in range(3):
        lid_up(.2)
        lid_down(.2)
    t.sleep(.7)
    for x in range(2):
        lid_up(.3)
        lid_down(.3)
    t.sleep(.2)
    lid_up(1.5)
    lid_down(None)
        
def trigger2():
    for x in range(4):
        lid_up(.2)
        lid_down(.2)
        
def trigger3():
    sound.play()
    t.sleep(3)
    
        
 
    
