import pygame
import ctypes
ctypes.windll.user32.SetProcessDPIAware()
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
# Pygame setup
pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE, display=0)
clock = pygame.time.Clock()

class AgentImage:
    def __init__(self, image, x, y):
        self.image = pygame.transform.scale(image, (40, 40))

        self.x = x
        self.y = y


def main():
    global running
    global active
    global win
    global user_text
    global dt
    global currentMessage

    running = True
    fullscreen = False
    img = pygame.image.load("img.png").convert()
    agents = []
    screen.fill("purple")
    while running:
        # scale image to window size
        img_scaled = pygame.transform.scale(img, (screen.get_width(), screen.get_height()))
        screen.blit(img_scaled, (0, 0))
        for event in pygame.event.get():
            match event.type:
                case pygame.MOUSEBUTTONDOWN:
                    pass

                case pygame.QUIT:
                    running = False
                case pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()
                    elif event.key == pygame.K_a:
                        agentAdder = input("Add an agent: (1-17")
                        agentImage = pygame.image.load("Original Agent Icons/Skye_icon.png").convert() # fix this
                        agents.append(AgentImage(agentImage, 710, 30))
                case pygame.KEYUP:
                    print(event.key) # debug statement, not necessary but I like it


        for agent in agents:
            screen.blit(agent.image, (agent.x, agent.y))
        pygame.display.flip()


        dt = clock.tick(60) / 1000

    pygame.quit()

main()