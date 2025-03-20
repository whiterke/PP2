import pygame
import os
pygame.init()

w, h = 300, 300
screen = pygame.display.set_mode((w,h))


songs = []
for f in os.listdir(os.getcwd()):
    if os.path.isfile(os.path.join(os.getcwd(), f)) and f.endswith(".mp3"):
        songs.append(f)
song = 0
pygame.mixer.music.load(songs[song])
pygame.mixer.music.play()

paused = False
resongs =[]
o = 1
for i in songs:
    resongs.append(songs[len(songs)-o])
    o += 1 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                paused = not paused
                if paused:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

            elif event.key == pygame.K_RIGHT:
                song = (song + 1) % len(songs)
                pygame.mixer.music.load(songs[song])
                pygame.mixer.music.play()

            elif event.key == pygame.K_LEFT:
                song = (song - 1) % len(songs)
                pygame.mixer.music.load(songs[song])
                pygame.mixer.music.play()

    f = pygame.font.Font(None, 36)
    text = f.render(songs[song], 1, (255, 255, 255))
    screen.fill((0,0,0))
    screen.blit(text, (30, 100))
    pygame.display.update()
                