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
    start_value=1,
    value_range=(0, 10.1),
    manager=manager
)

theta_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((70, 40, 200, 20)),
    start_value=90,
    value_range=(0.001, 360),  # theta range from 0 to pi
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
    relative_rect=pygame.Rect((70, 130, 90, 30)),
    text='+',
    manager=manager
)

decrement_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((180, 130, 90, 30)),
    text='-',
    manager=manager
)

# Create text entry for typing the steps value
steps_entry = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((70, 100, 200, 30)),
    manager=manager
)
steps_entry.set_text('0')  # Initial value for steps

# Set up fonts
font = pygame.font.Font(None, 24)

def render_text(text, position):
    text_surface = font.render(text, True, pygame.Color('black'))
    screen.blit(text_surface, position)

clock = pygame.time.Clock()
running = True

steps = 1  # Initial value for steps
scaler = 400
originVector = Vector2(0, 0)

"""
steps = 2000
positions = []
k_increase = .05
theta_increase = 10
maxK = 5
max_theta = 180
rad_theta_increase = theta_increase*math.pi/180
print(int(max_theta / theta_increase)*int(maxK/k_increase))
for A in range(int(max_theta / theta_increase)):
    positions.append([])
    for s in range(int(maxK/k_increase)):
        avgVec = Vector2(0, 0)
        for n in range(1, steps):
            magnitude = (1 / (steps * (n ** ((s+0.001)*k_increase)))) * (steps - n + 1)

            avgVec = Vector2.addVectors(Vector2(magnitude, (A+1)*rad_theta_increase * (n-1)), avgVec)
        positions[A].append([avgVec.x , avgVec.y])
        #print(f'({round(avgVec.x , 3)}, {round(avgVec.y, 3)})')
    print("Done!!!\n\n")
print(positions)
"""



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

        # Check if the text entry has been updated
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if event.ui_element == steps_entry:
                try:
                    steps = max(0, int(steps_entry.get_text())+1)  # Convert text to int
                except ValueError:
                    steps = 0  # If invalid input, reset to 0

    manager.update(time_delta)

    # Get the values from sliders
    k = k_slider.get_current_value()
    theta = theta_slider.get_current_value()*math.pi/180
    scaler = scaler_slider.get_current_value()

    screen.fill("white")
    vectors = []
    for n in range(1, steps):
        magnitude = scaler * ((1 / (n)**k))

        vectors.append(Vector2(magnitude, theta * (n-1)))
    avgVec = Vector2(0, 0)
    for n in range(1, steps):
        magnitude = scaler * ((1 / (steps * (n) ** k))) * (steps - n+1)

        avgVec = Vector2.addVectors(Vector2(magnitude, theta * (n-1)), avgVec)

    avgVec.drawVector(originVector, screen, [0, 255, 0])
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
    render_text(f'theta: {theta_slider.get_current_value():.2f}', (300, 45))
    render_text(f'Scaler: {scaler:.2f}', (300, 75))
    render_text(f'Steps: {steps-1}', (300, 135))
    render_text(f'Drawn Vector pos: ({round(currentOrigin.x/scaler, 3)}, {round(currentOrigin.y/scaler, 3)})', (screen_size[0] - 300, 350))
    #render_text(f'(for k^n) Final pos: ({round(a,3)}, {round(b,3)})', (screen_size[0]-300, 300))
    render_text(f'Avg Vector pos: ({round(avgVec.x / scaler, 3)}, {round(avgVec.y / scaler, 3)} )',
                (screen_size[0] - 300, 300))
    if avgVec.x != 0:
        render_text(f'slope: {round(avgVec.y / avgVec.x, 3)}',
                (screen_size[0] - 300, 250))
    else:
        render_text(f'Avg Vector Slope: None',
                    (screen_size[0] - 300, 250))



    pygame.display.flip()

pygame.quit()
