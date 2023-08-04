import pygame
import time
import random
import pickle


pygame.init()

# Configuración del juego
width = 800
height = 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Colores
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
gray = (128, 128, 128)  
green_dark = (0, 128, 0)
red_dark = (128, 0, 0)

# Variables 
block_size = 20
fps = 10
border_color = gray  # Color del borde (puedes cambiarlo a tu elección)
border_thickness = block_size  # Grosor del borde en píxeles
font = pygame.font.SysFont(None, 40)

def guardar_high_score(puntos):
    with open("high_score.pkl", "wb") as archivo:
        pickle.dump(puntos, archivo)

def cargar_high_score():
    try:
        with open("high_score.pkl", "rb") as archivo:
            return pickle.load(archivo)
    except FileNotFoundError:
        return 0

def message(msg, color, posx, posy):
    screen_text = font.render(msg, True, color)
    text_width, text_height = screen_text.get_size()
    x = ((width - text_width) / 2) + posx
    y = ((height - text_height) / 2) + posy
    display.blit(screen_text, (x, y))

def draw_borders():
    # Dibuja los bordes superiores e inferiores
    pygame.draw.rect(display, border_color, (0, 0, width, border_thickness))  # Borde superior
    pygame.draw.rect(display, border_color, (0, height - border_thickness, width, border_thickness))  # Borde inferior

    # Dibuja los bordes izquierdo y derecho (restando el grosor de los bordes superior e inferior)
    pygame.draw.rect(display, border_color, (0, 0, border_thickness, height))  # Borde izquierdo
    pygame.draw.rect(display, border_color, (width - border_thickness, 0, border_thickness, height))  # Borde derecho


clock = pygame.time.Clock()

def gameLoop():
    game_over = False
    game_lose = False

    high_score = cargar_high_score()  # Cargar la high score almacenada

    #puntuacion inciail
    puntos = 0

    # Posición inicial de la serpiente
    x = width / 2
    y = height / 2
    x_change = 0
    y_change = 0

    snake_list = []
    length_of_snake = 1

    # Posición aleatoria para la comida
    foodx = round(random.randrange(border_thickness, width - block_size - border_thickness) / block_size) * block_size
    foody = round(random.randrange(border_thickness, height - block_size - border_thickness) / block_size) * block_size

    while not game_over:

        #Perdiste
        while game_lose == True:
            display.fill(black)
            message("Perdiste! Presiona Esc para salir o C para jugar de nuevo", red, 0, 0)
            message("Tu puntuación: " + str(puntos), red, 0, -80)
            message("High Score: " + str(high_score), red, 0, -40)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: #Si el usuario intento cerrar la ventana, se cierra el juego
                    game_over = True
                    game_lose = False                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_over = True
                        game_lose = False
                    if event.key == pygame.K_c:
                        gameLoop()
       
        #juego en curso
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Si el usuario intento cerrar la ventana, se cierra el juego
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True
                    game_lose = False
                elif event.key == pygame.K_LEFT and x_change != block_size:
                    x_change = -block_size
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change != -block_size:
                    x_change = block_size
                    y_change = 0
                elif event.key == pygame.K_UP and y_change != block_size:
                    y_change = -block_size
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change != -block_size:
                    y_change = block_size
                    x_change = 0

        
        #condicion para perder por bordes
        if x < border_thickness or x > (width - block_size -border_thickness) or y < border_thickness or y > (height -block_size - border_thickness):
                game_lose = True

        x += x_change
        y += y_change
        display.fill(black)
       
       # Dibuja los bordes alrededor de la pantalla
        draw_borders()  
            
        pygame.draw.rect(display, green, [foodx, foody, block_size, block_size])
        for segment in snake_list:
            pygame.draw.rect(display, green_dark, [segment[0], segment[1], block_size, block_size])

        pygame.draw.rect(display, red_dark, [foodx, foody, block_size, block_size])

        snake_head = []
        snake_head.append(x)
        snake_head.append(y)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_lose = True

        for segment in snake_list:
            pygame.draw.rect(display, green_dark, [segment[0], segment[1], block_size, block_size])

        pygame.display.update()

        if x == foodx and y == foody:
            foodx = round(random.randrange(0, width - 2*border_thickness) / block_size) * block_size
            foody = round(random.randrange(0, height - 2*border_thickness) / block_size) * block_size
            length_of_snake += 1
            puntos += 1

        clock.tick(fps)

        if puntos > high_score:
            high_score = puntos
            guardar_high_score(high_score)

    pygame.quit()
    quit()

gameLoop()
