import pygame
import random
import math

pygame.init()
tela = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Snake Run Deluxe')

# --- ÁUDIO ---
pygame.mixer.music.load("Move With Me.mp3")    # coloque um mp3 na mesma pasta
pygame.mixer.music.play(-1)                    # loop infinito

som_comer = pygame.mixer.Sound("comer.wav")    # efeitos sonoros
som_gameover = pygame.mixer.Sound("gameover.wav")

# --- VARIÁVEIS DO JOGO ---
corpo_cobra = [(90, 100)]
direcao = (10, 0)
comida = (300, 200)
contador_frames = 0

# --- FUNÇÃO: fundo animado ---
def fundo_animado():
    global contador_frames
    contador_frames += 1

    for y in range(400):
        cor = (
            (math.sin((y + contador_frames) * 0.02) * 100 + 155),
            (math.sin((y + contador_frames) * 0.02 + 2) * 100 + 155),
            (math.sin((y + contador_frames) * 0.02 + 4) * 100 + 155)
        )
        pygame.draw.line(tela, cor, (0, y), (600, y))

# --- FUNÇÃO: desenhar ---
def desenhar():
    fundo_animado()

    # Corpo da cobra muda a cor conforme cresce
    tamanho = len(corpo_cobra)
    for i, parte in enumerate(corpo_cobra):
        intensidade = 100 + i * 3
        cor_cobra = (intensidade % 255, 255 - (i * 2 % 255), 80)
        pygame.draw.rect(tela, cor_cobra, (*parte, 10, 10))

    # Comida com brilho
    brilho = abs(math.sin(contador_frames * 0.1)) * 120 + 100
    pygame.draw.rect(tela, (255, brilho, brilho), (*comida, 10, 10))

    pygame.display.update()

rodando = True
relogio = pygame.time.Clock()

# --- LOOP PRINCIPAL ---
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP and direcao != (0, 10):
                direcao = (0, -10)
            elif evento.key == pygame.K_DOWN and direcao != (0, -10):
                direcao = (0, 10)
            elif evento.key == pygame.K_LEFT and direcao != (10, 0):
                direcao = (-10, 0)
            elif evento.key == pygame.K_RIGHT and direcao != (-10, 0):
                direcao = (10, 0)

    nova_cabeca = (corpo_cobra[0][0] + direcao[0], corpo_cobra[0][1] + direcao[1])
    corpo_cobra.insert(0, nova_cabeca)

    # Comer comida
    if nova_cabeca == comida:
        som_comer.play()
        comida = (random.randrange(0, 59) * 10, random.randrange(0, 39) * 10)
    else:
        corpo_cobra.pop()

    # Colisão com o corpo
    if nova_cabeca in corpo_cobra[1:]:
        som_gameover.play()
        pygame.time.delay(1200)
        rodando = False

    # Bater na parede
    if nova_cabeca[0] < 0 or nova_cabeca[0] >= 600 or nova_cabeca[1] < 0 or nova_cabeca[1] >= 400:
        som_gameover.play()
        pygame.time.delay(1200)
        rodando = False

    desenhar()
    relogio.tick(15)

pygame.quit()
