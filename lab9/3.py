import pygame
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
screen.fill((255, 255, 255))

C_WHITE = (255, 255, 255)
C_BLACK = (0, 0, 0)
C_RED = (255, 0, 0)
C_BLUE = (0, 0, 255)
C_GREEN = (0, 255, 0)

color = C_BLACK
saved_color = color  
radius = 5
clock = pygame.time.Clock()

drawing = False
last_pos = None
shape = "circle"
eraser_mode = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Shape selection keys:
            if event.key == pygame.K_PLUS:
                shape = "circle"
            elif event.key == pygame.K_MINUS:
                shape = "rect"
            elif event.key == pygame.K_SPACE:
                shape = "line"
            elif event.key == pygame.K_4:
                shape = "square"
            elif event.key == pygame.K_5:
                shape = "right_triangle"
            elif event.key == pygame.K_6:
                shape = "equilateral_triangle"
            elif event.key == pygame.K_7:
                shape = "rhombus"
            elif event.key == pygame.K_1:
                color = C_RED
                saved_color = color
                eraser_mode = False
            elif event.key == pygame.K_2:
                color = C_GREEN
                saved_color = color
                eraser_mode = False
            elif event.key == pygame.K_3:
                color = C_BLUE
                saved_color = color
                eraser_mode = False
            elif event.key == pygame.K_0:
                color = C_WHITE
                saved_color = color
                eraser_mode = False
            elif event.key == pygame.K_9:
                color = C_BLACK
                saved_color = color
                eraser_mode = False
            elif event.key == pygame.K_e:
                color = C_WHITE
                eraser_mode = True
            elif event.key == pygame.K_b:
                color = saved_color
                eraser_mode = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            last_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                current_pos = event.pos
                if shape == "circle":
                    center = ((last_pos[0] + current_pos[0]) // 2,
                              (last_pos[1] + current_pos[1]) // 2)
                    radius_circle = max(abs(current_pos[0] - last_pos[0]) // 2,
                                        abs(current_pos[1] - last_pos[1]) // 2)
                    pygame.draw.circle(screen, color, center, radius_circle)
                elif shape == "rect":
                    rect = pygame.Rect(min(last_pos[0], current_pos[0]),
                                       min(last_pos[1], current_pos[1]),
                                       abs(current_pos[0] - last_pos[0]),
                                       abs(current_pos[1] - last_pos[1]))
                    pygame.draw.rect(screen, color, rect)
                elif shape == "line":
                    pygame.draw.line(screen, color, last_pos, current_pos, radius)
                elif shape == "square":
                    dx = current_pos[0] - last_pos[0]
                    dy = current_pos[1] - last_pos[1]
                    side = min(abs(dx), abs(dy))
                    start_x, start_y = last_pos
                    if dx >= 0 and dy >= 0:
                        rect = pygame.Rect(start_x, start_y, side, side)
                    elif dx < 0 and dy >= 0:
                        rect = pygame.Rect(start_x - side, start_y, side, side)
                    elif dx >= 0 and dy < 0:
                        rect = pygame.Rect(start_x, start_y - side, side, side)
                    else: 
                        rect = pygame.Rect(start_x - side, start_y - side, side, side)
                    pygame.draw.rect(screen, color, rect)
                elif shape == "right_triangle":
                    pygame.draw.polygon(screen, color, [last_pos, 
                                                          (current_pos[0], last_pos[1]), 
                                                          (last_pos[0], current_pos[1])])
                elif shape == "equilateral_triangle":
                    x1, y1 = last_pos
                    x2, y2 = current_pos
                    side_length = math.hypot(x2 - x1, y2 - y1)
                    mid = ((x1 + x2) / 2, (y1 + y2) / 2)
                    height = (math.sqrt(3) / 2) * side_length
                    dx, dy = x2 - x1, y2 - y1
                    perp = (-dy, dx)
                    length = math.hypot(perp[0], perp[1])
                    if length != 0:
                        perp = (perp[0] / length, perp[1] / length)
                    else:
                        perp = (0, 0)
                    third_vertex = (mid[0] + perp[0] * height, mid[1] + perp[1] * height)
                    pygame.draw.polygon(screen, color, [last_pos, current_pos, third_vertex])
                elif shape == "rhombus":
                    x1, y1 = last_pos
                    x2, y2 = current_pos
                    left = min(x1, x2)
                    right = max(x1, x2)
                    top = min(y1, y2)
                    bottom = max(y1, y2)
                    mid_top = ((left + right) / 2, top)
                    mid_bottom = ((left + right) / 2, bottom)
                    mid_left = (left, (top + bottom) / 2)
                    mid_right = (right, (top + bottom) / 2)
                    pygame.draw.polygon(screen, color, [mid_top, mid_right, mid_bottom, mid_left])
            drawing = False
            last_pos = None

    if drawing and shape == "line":
        mouse_pos = pygame.mouse.get_pos()
        if last_pos:
            pygame.draw.line(screen, color, last_pos, mouse_pos, radius)
        last_pos = mouse_pos

    pygame.display.update()
    clock.tick(120)

pygame.quit()
