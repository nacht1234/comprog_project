import pygame
import random
import sys
import colorsys
from button import Button

pygame.init()

time_display = 5000
shape_size = 200
shapes = [('circle'), ('square'), ('triangle'), ('diamond'), ('rectangle')]

shapes_colors = [
    ('red', 'circle'), ('red', 'square'), ('red', 'triangle'), ('red', 'diamond'), ('red', 'rectangle'),
    ('orange', 'circle'), ('orange', 'square'), ('orange', 'triangle'), ('orange', 'diamond'), ('orange', 'rectangle'),
    ('yellow', 'circle'), ('yellow', 'square'), ('yellow', 'triangle'), ('yellow', 'diamond'), ('yellow', 'rectangle'),
    ('green', 'circle'), ('green', 'square'), ('green', 'triangle'), ('green', 'diamond'), ('green', 'rectangle'),
    ('blue', 'circle'), ('blue', 'square'), ('blue', 'triangle'), ('blue', 'diamond'), ('blue', 'rectangle'),
    ('violet', 'circle'), ('violet', 'square'), ('violet', 'triangle'), ('violet', 'diamond'), ('violet', 'rectangle')
]

colors = {
    'red': (255, 0, 0),
    'orange': (255, 165, 0),
    'yellow': (255, 255, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'violet': (238, 130, 238)
}

game_window_width = 1300
game_window_height = 750
game_window = pygame.display.set_mode((game_window_width, game_window_height))
pygame.display.set_caption("Pop Me Baby!")

menu_background_image = pygame.image.load("program_resources/main_menu_background.png")
if menu_background_image.get_size() != (game_window_width, game_window_height):
        menu_background_image = pygame.transform.scale(menu_background_image, (game_window_width, game_window_height))
shape_w_color = pygame.image.load("program_resources/shape_with_color_bg.png")
if shape_w_color.get_size() != (game_window_width, game_window_height):
        shape_w_color = pygame.transform.scale(shape_w_color, (game_window_width, game_window_height))
shape_only = pygame.image.load("program_resources/shape_only_bg.png")
if shape_only.get_size() != (game_window_width, game_window_height):
        shape_only = pygame.transform.scale(shape_only, (game_window_width, game_window_height))

play_rect = pygame.image.load("program_resources/play_button.png")
options_rect = pygame.image.load("program_resources/options_button.png")
exit_rect = pygame.image.load("program_resources/exit_button.png")

resized_width, resized_height = 250, 100
resized_play_rect = pygame.transform.scale(play_rect, (resized_width, resized_height))
resized_options_rect = pygame.transform.scale(options_rect, (resized_width, resized_height))
resized_exit_rect = pygame.transform.scale(exit_rect, (resized_width, resized_height))

click_sound = pygame.mixer.Sound("program_resources/mouse_click.wav")
click_sound.set_volume(1.0)
shape_pop_sound = pygame.mixer.Sound("program_resources/shape_pop_sound.wav")
wrong_click1 = pygame.mixer.Sound("program_resources/inccorect_shape_sound.wav")
wrong_click2 = pygame.mixer.Sound("program_resources/hehe_boi.mp3")

pygame.mixer.music.load("program_resources/bg_music.mp3")
pygame.mixer.music.play(-1)

def get_font(size):
    return pygame.font.Font("program_resources/game_font.ttf", size)

def draw_shape_wo_color(screen, shape, x, y):
    if shape == 'circle':
        pygame.draw.circle(screen, (0, 0, 0), (x, y), shape_size // 2, 1)
    elif shape == 'square':
        pygame.draw.rect(screen, (0, 0, 0), (x - shape_size // 2, y - shape_size // 2, shape_size, shape_size), 1)
    elif shape == 'triangle':
        points = [(x, y - shape_size // 2), (x - shape_size // 2, y + shape_size // 2), (x + shape_size // 2, y + shape_size // 2)]
        pygame.draw.polygon(screen, (0, 0, 0), points, 1)
    elif shape == 'diamond':
        points = [(x, y - shape_size // 2), (x - shape_size // 2, y), (x, y + shape_size // 2), (x + shape_size // 2, y)]
        pygame.draw.polygon(screen, (0, 0, 0), points, 1)
    elif shape == 'rectangle':
        pygame.draw.rect(screen, (0, 0, 0), (x - shape_size // 2, y - shape_size // 4, shape_size, shape_size // 2), 1)

def get_new_shapes_wo_color(target_shape):
    other_shapes = [sc for sc in shapes if sc != target_shape]
    random_shapes = random.sample(other_shapes, 2)
    display_shapes = [target_shape] + random_shapes
    random.shuffle(display_shapes)
    return display_shapes

def check_click_wo_color(pos, shape_info):
    x, y = pos
    shape, shape_x, shape_y = shape_info
    if shape == target_shape and show_target_shape_wo:
        return False
    if shape == 'circle':
        distance = ((x - shape_x) ** 2 + (y - shape_y) ** 2) ** 0.5
        return distance <= shape_size // 2
    elif shape == 'square':
        return shape_x - shape_size // 2 <= x <= shape_x + shape_size // 2 and shape_y - shape_size // 2 <= y <= shape_y + shape_size // 2
    elif shape == 'triangle':
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        b1 = sign(pos, (shape_x, shape_y - shape_size // 2), (shape_x - shape_size // 2, shape_y + shape_size // 2)) < 0.0
        b2 = sign(pos, (shape_x - shape_size // 2, shape_y + shape_size // 2), (shape_x + shape_size // 2, shape_y + shape_size // 2)) < 0.0
        b3 = sign(pos, (shape_x + shape_size // 2, shape_y + shape_size // 2), (shape_x, shape_y - shape_size // 2)) < 0.0
        return ((b1 == b2) and (b2 == b3))
    elif shape == 'diamond':
        return shape_x - shape_size // 2 <= x <= shape_x + shape_size // 2 and shape_y - shape_size // 2 <= y <= shape_y + shape_size // 2
    elif shape == 'rectangle':
        return shape_x - shape_size // 2 <= x <= shape_x + shape_size // 2 and shape_y - shape_size // 4 <= y <= shape_y + shape_size // 4

def draw_shape_w_color(screen, shape, color, x, y):
    if shape == 'circle':
        pygame.draw.circle(screen, color, (x, y), shape_size // 2)
    elif shape == 'square':
        pygame.draw.rect(screen, color, (x - shape_size // 2, y - shape_size // 2, shape_size, shape_size))
    elif shape == 'triangle':
        points = [(x, y - shape_size // 2), (x - shape_size // 2, y + shape_size // 2), (x + shape_size // 2, y + shape_size // 2)]
        pygame.draw.polygon(screen, color, points)
    elif shape == 'diamond':
        points = [(x, y - shape_size // 2), (x - shape_size // 2, y), (x, y + shape_size // 2), (x + shape_size // 2, y)]
        pygame.draw.polygon(screen, color, points)
    elif shape == 'rectangle':
        pygame.draw.rect(screen, color, (x - shape_size // 2, y - shape_size // 4, shape_size, shape_size // 2))

def get_new_shapes_w_color(target_shape_color):
    other_shapes = [sc for sc in shapes_colors if sc != target_shape_color]
    random_shapes = random.sample(other_shapes, 2)
    display_shapes = [target_shape_color] + random_shapes
    random.shuffle(display_shapes)
    return display_shapes

def check_click_w_color(pos, shape_info):
    x, y = pos
    shape_color, shape, shape_x, shape_y = shape_info
    if shape == 'circle':
        distance = ((x - shape_x) ** 2 + (y - shape_y) ** 2) ** 0.5
        return distance <= shape_size // 2
    elif shape == 'square':
        return shape_x - shape_size // 2 <= x <= shape_x + shape_size // 2 and shape_y - shape_size // 2 <= y <= shape_y + shape_size // 2
    elif shape == 'triangle':
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        b1 = sign(pos, (shape_x, shape_y - shape_size // 2), (shape_x - shape_size // 2, shape_y + shape_size // 2)) < 0.0
        b2 = sign(pos, (shape_x - shape_size // 2, shape_y + shape_size // 2), (shape_x + shape_size // 2, shape_y + shape_size // 2)) < 0.0
        b3 = sign(pos, (shape_x + shape_size // 2, shape_y + shape_size // 2), (shape_x, shape_y - shape_size // 2)) < 0.0
        return ((b1 == b2) and (b2 == b3))
    elif shape == 'diamond':
        return shape_x - shape_size // 2 <= x <= shape_x + shape_size // 2 and shape_y - shape_size // 2 <= y <= shape_y + shape_size // 2
    elif shape == 'rectangle':
        return shape_x - shape_size // 2 <= x <= shape_x + shape_size // 2 and shape_y - shape_size // 4 <= y <= shape_y + shape_size // 4

def draw_timer(screen, time_left):
    text = get_font(40).render(f"Time left: {time_left} seconds", True, (0, 0, 0))
    screen.blit(text, (game_window_width // 2 - text.get_width() // 2, game_window_height // 2 + shape_size))

def draw_game_over(screen):
    game_over_b2mm_rect = pygame.image.load("program_resources/game_over_b2mm.png")
    game_over_b2mm_rect = pygame.transform.scale(game_over_b2mm_rect, (500, 100))
    game_over_txt = get_font(60).render('Game Over', True, (255, 0, 0))
    screen.blit(game_over_txt, (game_window_width // 2 - game_over_txt.get_width() // 2, game_window_height // 2 - game_over_txt.get_height() // 2))

    button_rect = game_over_b2mm_rect.get_rect(center=(game_window_width // 2, game_window_height // 2 + 100))
    screen.blit(game_over_b2mm_rect, button_rect)

    button_text = get_font(20).render('Back to Main Menu', True, (255, 255, 255))
    screen.blit(button_text, (button_rect.x + (button_rect.width - button_text.get_width()) // 2, button_rect.y + (button_rect.height - button_text.get_height()) // 2))
    
    return button_rect

def play_without_color():
    global target_shape, display_shapes_wo, show_target_shape_wo, start_time, game_over
    target_shape = random.choice(shapes)
    display_shapes_wo = get_new_shapes_wo_color(target_shape)
    show_target_shape_wo = True
    start_time = pygame.time.get_ticks()
    game_over = False
    shapes_on_screen = []
    while True:
        game_window.fill('White')
        game_window.blit(shape_only, (0, 0))
        play_wo_mouse_pos = pygame.mouse.get_pos()
        play_wo_back_btn = Button(image=None, pos=(60, 30), text_input="<<<", font=get_font(30), base_color="black", hovering_color="Green")
        play_wo_back_btn.changeColor(play_wo_mouse_pos)
        play_wo_back_btn.update(game_window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    if play_wo_back_btn.checkForInput(play_wo_mouse_pos):
                        click_sound.play()
                        main_menu()
                    if game_over:
                        button_rect = draw_game_over(game_window)
                        if button_rect.collidepoint(mouse_pos):
                            click_sound.play()
                            main_menu()
                    else:
                        for shape, shape_x, shape_y in shapes_on_screen:
                            if check_click_wo_color(mouse_pos, (shape, shape_x, shape_y)):
                                if shape == target_shape:
                                    shape_pop_sound.play()
                                    target_shape = random.choice(shapes)
                                    display_shapes_wo = get_new_shapes_wo_color(target_shape)
                                    show_target_shape_wo = True
                                    start_time = pygame.time.get_ticks()
                                else:
                                    wrong_click1.play()
                                    game_over = True

        if game_over:
            button_rect = draw_game_over(game_window)
        else:
            current_time = pygame.time.get_ticks()
            if show_target_shape_wo:
                if current_time - start_time < time_display:
                    draw_shape_wo_color(game_window, target_shape, game_window_width // 2, game_window_height // 2)
                    time_left = (time_display - (current_time - start_time)) // 1000
                    draw_timer(game_window, time_left)
                else:
                    show_target_shape_wo = False

            if not show_target_shape_wo:
                shapes_on_screen = []
                for i, shape in enumerate(display_shapes_wo):
                    x = (i + 1) * (game_window_width // 4)
                    y = game_window_height // 2
                    draw_shape_wo_color(game_window, shape, x, y)
                    shapes_on_screen.append((shape, x, y))

        pygame.display.flip()

def play_with_color():
    global target_shape_color, display_shapes_w, show_target_shape_w, start_time, game_over
    target_shape_color = random.choice(shapes_colors)
    display_shapes_w = get_new_shapes_w_color(target_shape_color)
    show_target_shape_w = True
    start_time = pygame.time.get_ticks()
    game_over = False
    shapes_on_screen = []
    while True:
        game_window.fill('White')
        game_window.blit(shape_w_color, (0, 0))
        play_w_mouse_pos = pygame.mouse.get_pos()
        play_w_back_btn = Button(image=None, pos=(60, 30), text_input="<<<", font=get_font(30), base_color="black", hovering_color="Green")
        play_w_back_btn.changeColor(play_w_mouse_pos)
        play_w_back_btn.update(game_window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    if play_w_back_btn.checkForInput(play_w_mouse_pos):
                        click_sound.play()
                        main_menu()
                    if game_over:
                        button_rect = draw_game_over(game_window)
                        if button_rect.collidepoint(mouse_pos):
                            click_sound.play()
                            main_menu()
                    else:
                        if show_target_shape_w:
                            continue

                        for shape_color, shape, shape_x, shape_y in shapes_on_screen:
                            if check_click_w_color(mouse_pos, (shape_color, shape, shape_x, shape_y)):
                                if (shape_color, shape) == target_shape_color:
                                    shape_pop_sound.play()
                                    target_shape_color = random.choice(shapes_colors)
                                    display_shapes_w = get_new_shapes_w_color(target_shape_color)
                                    show_target_shape_w = True
                                    start_time = pygame.time.get_ticks()
                                else:
                                    wrong_click2.play()
                                    game_over = True

        if game_over:
            button_rect = draw_game_over(game_window)
        else:
            current_time = pygame.time.get_ticks()
            if current_time - start_time < time_display:
                if show_target_shape_w:
                    draw_shape_w_color(game_window, target_shape_color[1], colors[target_shape_color[0]], game_window_width // 2, game_window_height // 2)
                    time_left = (time_display - (current_time - start_time)) // 1000
                    draw_timer(game_window, time_left)
                else:
                    show_target_shape_w = False
            else:
                show_target_shape_w = False

            if not show_target_shape_w:
                shapes_on_screen = []
                for i, (color_name, shape) in enumerate(display_shapes_w):
                    color = colors[color_name]
                    x = (i + 1) * (game_window_width // 4)
                    y = game_window_height // 2
                    draw_shape_w_color(game_window, shape, color, x, y)
                    shapes_on_screen.append((color_name, shape, x, y))

        pygame.display.flip()

def play_sub_menu():
    while True:
        sub_menu_mouse_pos = pygame.mouse.get_pos()
        game_window.fill("white")
        sub_menu_back_btn = Button(image=None, pos=(60, 30), text_input="<<<", font=get_font(30), base_color="Black", hovering_color="Yellow")
        sub_menu_back_btn.changeColor(sub_menu_mouse_pos)
        sub_menu_back_btn.update(game_window)

        play_text = get_font(45).render("Select a mode:", True, "Black")
        play_rect = play_text.get_rect(center=(640, 200))
        game_window.blit(play_text, play_rect)
        shapes_only_button = Button(image=None, pos=(640, 300), text_input="Shapes Only", font=get_font(30), base_color="Black", hovering_color="Gray")
        shapes_with_colors_button = Button(image=None, pos=(640, 360), text_input="Shapes with Colors", font=get_font(30), base_color="Black", hovering_color=("Green"))
        shapes_only_button.changeColor(sub_menu_mouse_pos)
        shapes_with_colors_button.changeColor(sub_menu_mouse_pos)
        shapes_only_button.update(game_window)
        shapes_with_colors_button.update(game_window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sub_menu_back_btn.checkForInput(sub_menu_mouse_pos):
                    click_sound.play()
                    main_menu()
                if shapes_only_button.checkForInput(sub_menu_mouse_pos):
                    click_sound.play()
                    play_without_color()
                elif shapes_with_colors_button.checkForInput(sub_menu_mouse_pos):
                    click_sound.play()
                    play_with_color()
        pygame.display.update()

def options():
    while True:
        options_mouse_pos = pygame.mouse.get_pos()

        game_window.fill("white")

        options_text = get_font(45).render("volume ray ibutang nako ani.", True, "Black")
        options_rect = options_text.get_rect(center=(640, 260))
        game_window.blit(options_text, options_rect)

        options_back_btn = Button(image=None, pos=(60, 30), text_input="<<<", font=get_font(30), base_color="Black", hovering_color="Yellow")
        options_back_btn.changeColor(options_mouse_pos)
        options_back_btn.update(game_window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if options_back_btn.checkForInput(options_mouse_pos):
                    click_sound.play()
                    main_menu()

        pygame.display.update()

def main_menu():
    game_logo = pygame.image.load("program_resources/pop-me-bb-logo.png")
    pygame.display.set_icon(game_logo)
    logo_width, logo_height = game_logo.get_size()
    game_window_width, game_window_height = pygame.display.get_surface().get_size()
    original_width, original_height = game_logo.get_size()
    target_width = 600

    inflation_speed = 0.0009  # Adjust the speed of inflation/deflation
    max_scale = 1.4  # Maximum scale factor for inflation
    min_scale = original_width / target_width  # Minimum scale factor based on target size
    scale_direction = 1  # Initial direction of scaling: 1 for inflation, -1 for deflation
    while True:
        game_window.blit(menu_background_image, (0, 0))
        menu_mouse_pos = pygame.mouse.get_pos()

        title_font = pygame.font.Font("program_resources\game_name_font.otf", 100)
        title_font_color = (255, 122, 204)
        title_text = title_font.render("POP ME BABY!", True, title_font_color)
        menu_rect = title_text.get_rect(center=(640, 400))

        scale_factor = min_scale + (max_scale - min_scale) * abs(pygame.time.get_ticks() * inflation_speed % (max_scale * 2) - max_scale)

        # Update scale direction if maximum or minimum scale is reached
        if scale_factor >= max_scale or scale_factor <= min_scale:
            scale_direction *= -1

        # Scale logo image
        scaled_logo_image = pygame.transform.scale(game_logo, (int(original_width * scale_factor), int(original_height * scale_factor)))
        scaled_logo_rect = scaled_logo_image.get_rect(center=game_logo.get_rect(center=(game_window_width // 2, game_window_height - 550)).center)  # Center logo on the screen

        game_window.blit(scaled_logo_image, scaled_logo_rect)
        game_window.blit(title_text, menu_rect)

        play_button = Button(image=resized_play_rect, pos=(640, 510), text_input="PLAY", font=get_font(25), base_color="#d7fcd4", hovering_color="Gray")
        options_button = Button(image=resized_options_rect, pos=(640, 570), text_input="OPTIONS", font=get_font(25), base_color="#d7fcd4", hovering_color="Gray")
        exit_button = Button(image=resized_exit_rect, pos=(640, 630), text_input="EXIT", font=get_font(25), base_color="#d7fcd4", hovering_color="Red")

        for button in [play_button, options_button, exit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(game_window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    click_sound.play()
                    play_sub_menu()
                if options_button.checkForInput(menu_mouse_pos):
                    click_sound.play()
                    options()
                if exit_button.checkForInput(menu_mouse_pos):
                    click_sound.play()
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


pygame.display.update()

main_menu()