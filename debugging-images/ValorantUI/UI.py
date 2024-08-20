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
    user_text = ""
    print("slow")
    font = pygame.font.SysFont('jetbrainsmonoregular', 25)
    print("cunt")
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
    inputboxActivated = False
    while running:
        input_rect = pygame.Rect(WINDOW_WIDTH // 2 - 300 // 2,
                                 WINDOW_HEIGHT // 2 + 250,
                                 300,
                                 32)



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
                    print(event.key)
                    if event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()
                    elif event.key == 96:
                        if not inputboxActivated:
                            inputboxActivated = True
                            print("active input box")

                    else:

                        if inputboxActivated:
                            if event.key == pygame.K_BACKSPACE:
                                user_text = user_text[:-1]
                            elif event.key == pygame.K_RETURN:

                                try:
                                    agentImage = pygame.image.load(str(agentPNGs[int(user_text)-1])).convert_alpha() # fix this
                                    if len(agents) >= 5:
                                        agentImage = pygame.transform.flip(agentImage, True, False)
                                    agents.append(AgentImage(agentImage, (446 if len(agents) < 5 else 839)+(66*len(agents)), 30)) # TODO: Second team isnt registered properly, FIX!
                                    user_text = ""
                                except:
                                    print("Invalid agent number")
                                inputboxActivated = False
                            else:
                                if event.unicode.isdigit():
                                    user_text += event.unicode


                        # agentAdder = int(input("Add an agent: (1-24 "))
                        # try:
                        #     agentImage = pygame.image.load(str(agentPNGs[agentAdder-1])).convert_alpha() # fix this
                        #     agents.append(AgentImage(agentImage, 446+(66*len(agents)), 30))
                        # except IndexError:
                        #     print("Invalid agent number")

                case pygame.KEYUP:
                    print(event.key) # debug statement, not necessary but I like it


        for agent in agents:
            screen.blit(agent.image, (agent.x, agent.y))


        if inputboxActivated:
            color = pygame.Color('lightskyblue3')
            pygame.draw.rect(screen, color, input_rect)
            text_surface = font.render(user_text, True, (255, 255, 255))
            screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        pygame.display.flip()

        dt = clock.tick(30) / 1000

    pygame.quit()

main()