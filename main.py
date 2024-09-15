import math
import pygame
import pygame_gui

import Vector
from Vector import Vector2

pygame.init()

# Initialize the Pygame display
screen_size = (Vector.width, Vector.height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Real-time Slider Adjustment')

# Initialize pygame_gui
manager = pygame_gui.UIManager(screen_size)

# Create labels for sliders
k_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((0, 10, 75, 20)),
    text='k:',
    manager=manager
)

theta_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((0, 40, 75, 20)),
    text='theta:',
    manager=manager
)

scaler_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((0, 70, 75, 20)),
    text='Scaler:',
    manager=manager
)

steps_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((0, 100, 75, 20)),
    text='Steps:',
    manager=manager
)

# Create sliders for k and theta
k_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((70, 10, 200, 20)),
    start_value=2,
    value_range=(0.1, 10),
    manager=manager
)

theta_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((70, 40, 200, 20)),
    start_value=1.267,
    value_range=(0.1, 6.28),  # theta range from 0 to 2*pi
    manager=manager
)

scaler_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((70, 70, 200, 20)),
    start_value=400,
    value_range=(10, 1000),
    manager=manager
)

# Create buttons for incrementing and decrementing steps
increment_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((70, 100, 90, 30)),
    text='+',
    manager=manager
)

decrement_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((180, 100, 90, 30)),
    text='-',
    manager=manager
)

# Set up fonts
font = pygame.font.Font(None, 24)

def render_text(text, position):
    text_surface = font.render(text, True, pygame.Color('black'))
    screen.blit(text_surface, position)

clock = pygame.time.Clock()
running = True

steps = 0  # Initial value for steps
scaler = 400
originVector = Vector2(0, 0)

while running:
    time_delta = clock.tick(60) / 1000.0  # Seconds since last frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        manager.process_events(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == increment_button:
                steps += 1
            elif event.ui_element == decrement_button:
                steps = max(0, steps - 1)  # Ensure steps doesn't go below 0

    manager.update(time_delta)

    # Get the values from sliders
    k = k_slider.get_current_value()
    theta = theta_slider.get_current_value()
    scaler = scaler_slider.get_current_value()

    screen.fill("white")
    vectors = []
    for n in range(steps):
        magnitude = scaler * ((1 / k) ** n)
        vectors.append(Vector2(magnitude, theta * n))

    currentOrigin = originVector
    for vector in vectors:
        currentOrigin = vector.drawVector(currentOrigin, screen)

    a = ((k * (k - math.cos(theta))) /
         (k ** 2 - 2 * k * math.cos(theta) + 1))

    b = ((k * math.sin(theta)) /
         (k ** 2 - 2 * k * math.cos(theta) + 1))
    finalPos = pygame.Vector2(a * scaler, Vector.height - b * scaler - Vector2.initialHeight)

    pygame.draw.circle(screen, "red", finalPos, 2)

    # Draw sliders, labels, and buttons
    manager.draw_ui(screen)

    # Render current values to the right of the GUI
    render_text(f'k: {k:.2f}', (300, 15))
    render_text(f'theta: {theta:.2f}', (300, 45))
    render_text(f'Scaler: {scaler:.2f}', (300, 75))
    render_text(f'Steps: {steps}', (300, 105))
    render_text(f'Final pos: ({round(a,3)}, {round(b,3)})', (screen_size[0]-300, 300))

    pygame.display.flip()

pygame.quit()
