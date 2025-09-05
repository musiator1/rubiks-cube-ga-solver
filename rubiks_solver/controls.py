import pygame

def handle_keyboard(cube, events):
    """
    Map keyboard events to cube moves.
    Shift + key = counterclockwise.
    """
    for event in events:
        if event.type != pygame.KEYDOWN:
            continue

        shift = pygame.key.get_mods() & pygame.KMOD_SHIFT

        # --- Face turns ---
        if event.key == pygame.K_f:
            cube.F_() if shift else cube.F()
        if event.key == pygame.K_r:
            cube.R_() if shift else cube.R()
        if event.key == pygame.K_u:
            cube.U_() if shift else cube.U()
        if event.key == pygame.K_d:
            cube.D_() if shift else cube.D()
        if event.key == pygame.K_l:
            cube.L_() if shift else cube.L()
        if event.key == pygame.K_b:
            cube.B_() if shift else cube.B()

        # --- Whole cube rotations ---
        if event.key == pygame.K_x:
            cube.rotate_x()
        if event.key == pygame.K_y:
            cube.rotate_y()
        if event.key == pygame.K_z:
            cube.rotate_z()
