import os

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

    agentPNGs = []
    # if this doesnt work, set working directory in pycharm to ValorantUI
    for file in os.listdir("Correct Agents"):
        f = os.path.join("Correct Agents", file)
        if not ".png" in f:
            continue
        agentPNGs.append(f)
    print(len(agentPNGs))

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
                        agentAdder = int(input("Add an agent: (1-24 "))
                        try:
                            agentImage = pygame.image.load(str(agentPNGs[agentAdder-1])).convert_alpha() # fix this
                            agents.append(AgentImage(agentImage, 446+(66*len(agents)), 30))
                        except IndexError:
                            print("Invalid agent number")
                case pygame.KEYUP:
                    print(event.key) # debug statement, not necessary but I like it


        for agent in agents:
            screen.blit(agent.image, (agent.x, agent.y))
        pygame.display.flip()


        dt = clock.tick(30) / 1000

    pygame.quit()

main()