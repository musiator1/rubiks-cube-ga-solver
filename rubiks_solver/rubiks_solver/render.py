import pygame

from rubiks_solver.config import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS


def render_cube_perspective(screen, cube):
    """
    Render cube in perspective view.
    """
    size = min(SCREEN_HEIGHT, SCREEN_WIDTH) * 0.5 
    skew = size / 3
    tile_size = size / 3
    tile_skew = skew / 3

    # --- Front face ---
    v1_front = (SCREEN_WIDTH * 0.15, SCREEN_HEIGHT * 0.35)
    v2_front = (v1_front[0] + size, v1_front[1])
    v3_front = (v1_front[0] + size, v1_front[1] + size)
    v4_front = (v1_front[0], v1_front[1] + size)

    for iy, row in enumerate(cube.faces["F"]):
        for ix, tile in enumerate(row):
            x = v1_front[0] + ix * tile_size
            y = v1_front[1] + iy * tile_size
            color = COLORS[tile]
            v1, v2, v3, v4 = (x, y), (x + tile_size, y), (x + tile_size, y + tile_size), (x, y + tile_size)
            pygame.draw.polygon(screen, color, [v1, v2, v3, v4])

    pygame.draw.polygon(screen, "black", [v1_front, v2_front, v3_front, v4_front], 3)
    pygame.draw.line(screen, "black", (v1_front[0] + tile_size, v1_front[1]), (v4_front[0] + tile_size, v4_front[1]), 3)
    pygame.draw.line(screen, "black", (v1_front[0] + tile_size * 2, v1_front[1]), (v4_front[0] + tile_size * 2, v4_front[1]), 3)
    pygame.draw.line(screen, "black", (v1_front[0], v1_front[1] + tile_size), (v2_front[0], v2_front[1] + tile_size), 3)
    pygame.draw.line(screen, "black", (v1_front[0], v1_front[1] + tile_size * 2), (v2_front[0], v2_front[1] + tile_size * 2), 3)

    # --- Up face ---
    v1_up = (v1_front[0] + skew, v1_front[1] - skew)
    v2_up = (v1_up[0] + size, v1_up[1])
    v3_up = (v1_up[0] + size - skew, v1_up[1] + skew)
    v4_up = (v1_up[0] - skew, v1_up[1] + skew)

    for iy, row in enumerate(cube.faces["U"]):
        for ix, tile in enumerate(row):
            x = v1_up[0] + tile_size * ix - tile_skew * iy
            y = v1_up[1] + tile_skew * iy
            color = COLORS[tile]
            v1, v2, v3, v4 = (x, y), (x + tile_size, y), (x + tile_size - tile_skew, y + tile_skew), (x - tile_skew, y + tile_skew)
            pygame.draw.polygon(screen, color, [v1, v2, v3, v4])

    pygame.draw.polygon(screen, "black", [v1_up, v2_up, v3_up, v4_up], 3)
    pygame.draw.line(screen, "black", (v4_up[0] + tile_size, v4_up[1]), (v4_up[0] + tile_size + skew, v4_up[1] - skew), 3)
    pygame.draw.line(screen, "black", (v4_up[0] + tile_size * 2, v4_up[1]), (v4_up[0] + tile_size * 2 + skew, v4_up[1] - skew), 3)
    pygame.draw.line(screen, "black", (v4_up[0] + tile_skew, v4_up[1] - tile_skew), (v3_up[0] + tile_skew, v3_up[1] - tile_skew), 3)
    pygame.draw.line(screen, "black", (v4_up[0] + tile_skew * 2, v4_up[1] - tile_skew * 2), (v3_up[0] + tile_skew * 2, v3_up[1] - tile_skew * 2), 3)

    # --- Right face ---
    v1_right = (v1_front[0] + size, v1_front[1])
    v2_right = (v1_right[0] + skew, v1_right[1] - skew)
    v3_right = (v1_right[0] + skew, v1_right[1] + size - skew)
    v4_right = (v1_right[0], v1_right[1] + size)

    for iy, row in enumerate(cube.faces["R"]):
        for ix, tile in enumerate(row):
            x = v1_right[0] + ix * tile_skew
            y = v1_right[1] + iy * tile_size - ix * tile_skew
            color = COLORS[tile]
            v1, v2, v3, v4 = (x, y), (x + tile_skew, y - tile_skew), (x + tile_skew, y - tile_skew + tile_size), (x, y + tile_size)
            pygame.draw.polygon(screen, color, [v1, v2, v3, v4])

    pygame.draw.polygon(screen, "black", [v1_right, v2_right, v3_right, v4_right], 3)
    pygame.draw.line(screen, "black", (v4_right[0], v4_right[1] - tile_size), (v3_right[0], v3_right[1] - tile_size), 3)
    pygame.draw.line(screen, "black", (v4_right[0], v4_right[1] - tile_size * 2), (v3_right[0], v3_right[1] - tile_size * 2), 3)
    pygame.draw.line(screen, "black", (v4_right[0] + tile_skew, v4_right[1] - tile_skew), (v1_right[0] + tile_skew, v1_right[1] - tile_skew), 3)
    pygame.draw.line(screen, "black", (v4_right[0] + tile_skew * 2, v4_right[1] - tile_skew * 2), (v1_right[0] + tile_skew * 2, v1_right[1] - tile_skew * 2), 3)


def render_cube_orthographic(screen, cube):
    """
    Render cube in orthographic (flat net) view.
    """
    size = min(SCREEN_HEIGHT, SCREEN_WIDTH) / 5

    # Top-left corner coordinates for each face
    x_left = SCREEN_WIDTH / 2 - size * 2
    y_left = SCREEN_HEIGHT / 2 - size / 2

    x_front = x_left + size
    y_front = y_left

    x_right = x_front + size
    y_right = y_front

    x_back = x_right + size
    y_back = y_right

    x_up = x_front
    y_up = y_front - size

    x_down = x_front
    y_down = y_front + size

    _draw_face(screen, cube.faces["L"], x_left, y_left, size)
    _draw_face(screen, cube.faces["F"], x_front, y_front, size)
    _draw_face(screen, cube.faces["R"], x_right, y_right, size)
    _draw_face(screen, cube.faces["B"], x_back, y_back, size)
    _draw_face(screen, cube.faces["U"], x_up, y_up, size)
    _draw_face(screen, cube.faces["D"], x_down, y_down, size)


def _draw_face(screen, face, x, y, size):
    """Helper: draw a single 3×3 face."""
    tile_size = size / 3
    tile_offset = 3
    pygame.draw.rect(screen, "black", (x - tile_offset, y - tile_offset, size + tile_offset, size + tile_offset))
    for i, row in enumerate(face):
        for j, tile in enumerate(row):
            pygame.draw.rect(
                screen,
                COLORS[tile],
                (x + j * tile_size, y + i * tile_size, tile_size - tile_offset, tile_size - tile_offset),
            )


def draw_button(screen, font, text, center_pos, events, on_click=None):
    """
    Draw a clickable button with text.
    Returns True if clicked.
    """
    mouse_pos = pygame.mouse.get_pos()
    writing = font.render(text, True, (0, 0, 0))
    rect = writing.get_rect(center=center_pos)
    button_rect = rect.inflate(20, 10)

    bg_color = (200, 200, 200) if button_rect.collidepoint(mouse_pos) else (170, 170, 170)
    pygame.draw.rect(screen, bg_color, button_rect)
    pygame.draw.rect(screen, (0, 0, 0), button_rect, 2)
    screen.blit(writing, rect)

    clicked = False
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_rect.collidepoint(event.pos):
                clicked = True
                if on_click:
                    on_click()
                break

    return clicked