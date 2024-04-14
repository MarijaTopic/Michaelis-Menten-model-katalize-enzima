import pygame
import sys
import random
import math
import matplotlib.pyplot as plt
import numpy as np

# inicijalizacija Pygame-a
pygame.init()

# postavljanje početnog prozora
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Michaelis-Menten Simulacija')

class Button:
    def __init__(self, text_input, text_size, text_color, rectangle_width_and_height, rectangle_color, rectangle_hovering_color, position):
        self.text_input = text_input
        # rectangle ispod teksta
        self.rectangle = pygame.Rect((position[0]-(rectangle_width_and_height[0]/2), position[1]-(rectangle_width_and_height[1]/2)), rectangle_width_and_height)
        self.rectangle_color, self.rectangle_hovering_color = rectangle_color, rectangle_hovering_color
        # tekst u gumbu
        self.font = pygame.font.Font(None, text_size)
        self.text_surface = self.font.render(text_input, False, text_color)
        self.text_rectangle = self.text_surface.get_rect(center = self.rectangle.center)
    def update(self, screen):
        pygame.draw.rect(screen, self.rectangle_color, self.rectangle)
        screen.blit(self.text_surface, self.text_rectangle)
    def checkForCollision(self, mouse_position):
        if mouse_position[0] in range(self.rectangle.left, self.rectangle.right) and mouse_position[1] in range(self.rectangle.top, self.rectangle.bottom):
            return True
        return False
    def changeButtonColor(self):
        self.rectangle_color = self.rectangle_hovering_color

# postavljanje svih gumbova
gumb1 = Button("Povećaj!", 24, "white", (120, 50), "green", "pink", (670, 500))
gumb_simulacija = Button("Simulacija", 30, "white", (130, 50), "pink", "pink", (270, 300))
gumb_povratak = Button("Natrag", 24, "white", (120,50), "red", "pink", (130, 500))
gumb_graf = Button("Grafovi", 30, "white", (130,50), "pink", "pink", (530, 300))
mouse_pos = pygame.mouse.get_pos()
for btn in [gumb1,gumb_simulacija,gumb_povratak,gumb_graf]:
            if btn.checkForCollision(mouse_pos):
                btn.changeButtonColor()
            btn.update(screen)

# definicija boja
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (173, 216, 230)  # svijetloplava boja
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PINK = (255, 182, 193) # svijetloroza boja
substrate_concentrations = []
reaction_rates = []

# postavljanje početnih vrijednosti za simulaciju
Km = 20.0  # Michaelisova konstanta u molovima
Vm = 40.0  # maksimalna brzina reakcije u molovima po sekundi
enzyme_concentration = 1.0 # broj enzima
substrate_concentration = 0.01  # početna koncentracija supstrata u molovima

# definicija fontova
title_font = pygame.font.Font(None, 50)
menu_font = pygame.font.Font(None, 40)

# funkcija za izračunavanje brzine reakcije prema Michaelis-Mentenovoj jednadžbi
def calculate_reaction_rate(substrate_concentration, Km, Vm):
    return (Vm * substrate_concentration) / (Km + substrate_concentration)

# funkcija za crtanje simulacije
def draw_simulation():
    global mouse_pos, substrate_concentration
    sim_screen_active = True
    while sim_screen_active:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if gumb1.checkForCollision(mouse_pos):
                    substrate_concentration += 1 # povećavanje koncentracije za jedan klikom na gumb za povećavanje
                    substrate_concentrations.append(substrate_concentration) 
                    reaction_rate = calculate_reaction_rate(substrate_concentration, Km, Vm) # računa se brzina reakcije prema formuli
                    reaction_rates.append(reaction_rate)
                if gumb_povratak.checkForCollision(mouse_pos):
                    sim_screen_active = False
                    main()

        # stvaranje površine za dvostruki bafer
        back_buffer = screen.copy()

        # bijela pozadina
        back_buffer.fill(WHITE)

        # veličine varijabli u simulaciji
        variables_font = pygame.font.SysFont(None, 30)
        v0_text = variables_font.render(f'V0: {calculate_reaction_rate(substrate_concentration, Km, Vm):.2f} mol/s', True, BLACK)
        vmax_text = variables_font.render(f'Vm: {Vm} mol/s', True, BLACK)
        km_text = variables_font.render(f'Km: {Km} mol/s', True, BLACK)
        substrate_text = variables_font.render(f'[s]: {substrate_concentration} mol', True, BLACK)

        back_buffer.blit(v0_text, (50, height // 8))
        back_buffer.blit(vmax_text, (50, height // 8 + 40))
        back_buffer.blit(km_text, (50, height // 8 + 80))
        substrate_rect = back_buffer.blit(substrate_text, (50, height // 8 + 120))

        # crtanje kvadrata koji predstavlja posudu
        square_rect = pygame.Rect((width - 400) // 2, (height - 400) // 2, 400, 400)
        pygame.draw.rect(back_buffer, BLUE, square_rect)

        # crtanje enzima
        enzyme_pos = (width // 2, height // 2)
        pygame.draw.circle(back_buffer, BLACK, enzyme_pos, 50)

        # nasumično pomicanje supstrata u posudi
        for _ in range(int(substrate_concentration * 100)):
            x = random.randint(square_rect.left, square_rect.right)
            y = random.randint(square_rect.top, square_rect.bottom)
            substrate_pos = (x, y)

            # provjera udaljenosti između supstrata i enzima
            distance = math.sqrt((substrate_pos[0] - enzyme_pos[0]) ** 2 + (substrate_pos[1] - enzyme_pos[1]) ** 2)
            if distance <= 55:  # radijus enzima je 50, dodajemo 5 za sigurnosni razmak
                # supstrat se odbija od enzima
                dx = substrate_pos[0] - enzyme_pos[0]
                dy = substrate_pos[1] - enzyme_pos[1]
                substrate_pos = (substrate_pos[0] + dx, substrate_pos[1] + dy)
                # promjena boje supstrata u crvenu kada dotakne enzim
                pygame.draw.circle(back_buffer, RED, substrate_pos, 3)
            else:
                pygame.draw.circle(back_buffer, GREEN, substrate_pos, 3)

        # crtanje površine za dvostruki bafer na zaslon
        screen.blit(back_buffer, (0, 0))
        gumb1.update(screen)
        gumb_povratak.update(screen)

        # ažuriranje zaslona
        pygame.display.flip()

    return


# funkcija za crtanje kontrole simulacije
def draw_simulation_controls():
    # gumb natrag na početni zaslon
    back_button = pygame.Rect(20, height - 80, 100, 50)
    pygame.draw.rect(screen, BLUE, back_button)
    back_text = menu_font.render("Natrag", True, WHITE)
    screen.blit(back_text, (30, height - 70))

    return back_button


# crtanje grafova
def graf(substrate_concentrations, reaction_rates):
    plt.figure(figsize=(15, 5))

    #crtanje grafa ovisnosti V0 o [s]
    plt.subplot(1, 3, 1)
    plt.plot(substrate_concentrations, reaction_rates)
    plt.title('Brzina reakcije (V0) vs. koncentracija supstrata ([s])')
    plt.xlabel('Koncentracija supstrata ([s])/[mol]') # x-os
    plt.ylabel('Brzina reakcije (V0)/[mol/s]') #y-os
    plt.grid(True)

    #crtanje grafa ovisnosti V0 0 Km
    plt.subplot(1, 3, 2)
    plt.plot([Km] * len(substrate_concentrations), reaction_rates)
    plt.title('Brzina reakcije (V0) vs. Michaelisova konstanta (Km)')
    plt.xlabel('Michaelisova konstanta (Km)/[mol/s]') # x-os
    plt.ylabel('Brzina reakcije (V0)/[mol/s]') #y-os
    plt.grid(True)

    # crtanje grafa ovisnosti [s] o Km
    plt.subplot(1, 3, 3)
    plt.plot([Km] * len(substrate_concentrations), substrate_concentrations)
    plt.title('Koncentracija supstrata ([s]) vs. Michaelisova konstanta (Km)')
    plt.xlabel('Michaelisova konstanta (Km)/[mol/s]')
    plt.ylabel('Koncentracija supstrata ([s])/[mol]')
    plt.grid(True)

    plt.tight_layout()
    plt.show()


# glavna petlja igre
def main():

    running = True
    screen.fill("white")
    while running:
        mouse_pos = pygame.mouse.get_pos()  # ažurirajte poziciju miša u svakoj iteraciji petlje
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if gumb_simulacija.checkForCollision(mouse_pos):
                    draw_simulation()
                    running = False
                if gumb_graf.checkForCollision(mouse_pos):
                    graf(substrate_concentrations, reaction_rates)
        gumb_simulacija.update(screen)
        gumb_graf.update(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()