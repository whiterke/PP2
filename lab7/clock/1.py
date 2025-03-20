import pygame
from datetime import datetime

pygame.init()

w, h = 829, 836
center = w/2, h/2

screen = pygame.display.set_mode((w,h))

clock = pygame.time.Clock()
mainclock = pygame.image.load('main-clock.png')
left = pygame.image.load('left-hand.png')
right = pygame.image.load('right-hand.png')
hours = pygame.image.load('hours.png')


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    time = datetime.now()
    seconds = (time.second / 60) * 360
    minutes = (time.minute / 60) * 360 + (time.second / 60) * (360 / 60)
    hour = (time.hour / 12) * 360 + (time.minute / 60) * (360/12)

    rotateleft = pygame.transform.rotate(left, -seconds)
    left_rect = rotateleft.get_rect(center=center)
    rotateright = pygame.transform.rotate(right, -minutes)
    right_rect = rotateright.get_rect(center=center)
    rotatehours = pygame.transform.rotate(hours, -hour)
    hours_rect = rotatehours.get_rect(center=center)

    screen.fill("white")
    screen.blit(mainclock, (0, 0))
    screen.blit(rotateleft, left_rect)
    screen.blit(rotateright, right_rect)
    screen.blit(rotatehours, hours_rect)
    pygame.display.flip()