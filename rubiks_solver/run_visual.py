import pygame

from rubiks_solver.config import SCREEN_WIDTH, SCREEN_HEIGHT, SHUFFLE_SEQUENCE
from rubiks_solver.render import render_cube_perspective, render_cube_orthographic, draw_button
from rubiks_solver.cube import Cube
from rubiks_solver.controls import handle_keyboard

def main():
    # --- Initialize pygame ---
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  
    pygame.display.set_caption("Rubik's Cube")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 30)

    # --- Cube state ---
    cube = Cube()

    # --- Main loop ---
    running = True
    perspective_view = True

    while running:
        screen.fill("white")

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        # --- UI buttons ---
        draw_button(screen, font, "Shuffle", (50, 30), events, on_click=lambda: cube.shuffle(None))
        draw_button(screen, font, "Shuffle GA", (160, 30), events, on_click=lambda: [cube.reset(), cube.shuffle(SHUFFLE_SEQUENCE)])
        draw_button(screen, font, "Reset", (262, 30), events, on_click=cube.reset)

        view_text = "Switch to orthographic" if perspective_view else "Switch to perspective"
        if draw_button(screen, font, view_text, (423, 30), events):
            perspective_view = not perspective_view

        # --- Handle keyboard input ---
        handle_keyboard(cube, events)

        # --- Render cube ---
        if perspective_view:
            render_cube_perspective(screen, cube)
        else:
            render_cube_orthographic(screen, cube)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
