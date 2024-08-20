import os
import pygame
import ctypes

ctypes.windll.user32.SetProcessDPIAware()
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE, display=0)
clock = pygame.time.Clock()

class AgentImage:
    def __init__(self, image, x, y):
        self.image = pygame.transform.scale(image, (40, 40))
        self.x = x
        self.y = y

    def is_clicked(self, pos):
        return self.x <= pos[0] <= self.x + 40 and self.y <= pos[1] <= self.y + 40

def main():
    global running
    global active
    global win
    global user_text
    user_text = ""
    font = pygame.font.SysFont('jetbrainsmonoregular', 25)
    agentPNGs = []
    for file in os.listdir("Correct Agents"):
        f = os.path.join("Correct Agents", file)
        if not ".png" in f:
            continue
        agentPNGs.append(f)

    running = True
    fullscreen = False
    img = pygame.image.load("img.png").convert()
    agentsL = []
    agentsR = []
    screen.fill("purple")
    inputboxActivated = False

    while running:
        input_rect = pygame.Rect(WINDOW_WIDTH // 2 - 300 // 2, WINDOW_HEIGHT // 2 + 250, 300, 32)
        img_scaled = pygame.transform.scale(img, (screen.get_width(), screen.get_height()))
        screen.blit(img_scaled, (0, 0))

        for event in pygame.event.get():
            match event.type:
                case pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for agent in agentsL:
                        if agent.is_clicked(pos):
                            agentsL.remove(agent)
                            for idx, agent in enumerate(agentsL):
                                agent.x = 710 - (66 * idx)
                            break
                    for agent in agentsR:
                        if agent.is_clicked(pos):
                            agentsR.remove(agent)
                            for idx, agent in enumerate(agentsR):
                                agent.x = 1171 + (66 * idx)
                            break

                case pygame.QUIT:
                    running = False
                case pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()
                    elif event.key == 96:
                        if not inputboxActivated:
                            inputboxActivated = True
                    else:
                        if inputboxActivated:
                            if event.key == pygame.K_BACKSPACE:
                                user_text = user_text[:-1]
                            elif event.key == pygame.K_RETURN:
                                try:
                                    agentImage = pygame.image.load(str(agentPNGs[int(user_text) - 1])).convert_alpha()
                                    if len(agentsL) >= 5:
                                        agentImage = pygame.transform.flip(agentImage, True, False)
                                        agentsR.append(AgentImage(agentImage, 1171 + (66 * len(agentsR)), 30))
                                    else:
                                        agentsL.append(AgentImage(agentImage, 710 - (66 * len(agentsL)), 30))
                                except:
                                    print("Invalid agent number")
                                inputboxActivated = False
                                user_text = ""
                            else:
                                if event.unicode.isdigit():
                                    user_text += event.unicode

                case pygame.KEYUP:
                    pass

        for agent in agentsL:
            screen.blit(agent.image, (agent.x, agent.y))
        for agent in agentsR:
            screen.blit(agent.image, (agent.x, agent.y))

        if inputboxActivated:
            color = pygame.Color('lightskyblue3')
            pygame.draw.rect(screen, color, input_rect)
            text_surface = font.render(user_text, True, (255, 255, 255))
            screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        pygame.display.flip()

        clock.tick(30)

    pygame.quit()

main()