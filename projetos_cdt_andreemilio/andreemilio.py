import pygame
import random
import time

pygame.init()
tela = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Snake Run – Minimal Deluxe")

# --- VARIÁVEIS ---
corpo_cobra = [(90, 100)]
direcao = (10, 0)
comida = (300, 200)
pontuacao = 0
pausado = False
timer_inicio = time.time()

fonte = pygame.font.SysFont("arial", 24, True)

# --- Função: cor da cobra mudando ---
def cor_variavel(frame):
    r = (frame * 3) % 255
    g = (frame * 5) % 255
    b = (frame * 7) % 255
    return (r, g, b)

# --- Função: desenhar ---
def desenhar(frame):
    tela.fill((0, 0, 0))  # fundo preto

    cor_cobra = cor_variavel(frame)

    # desenha a cobra
    for parte in corpo_cobra:
        pygame.draw.rect(tela, cor_cobra, (*parte, 10, 10))

    # comida (vermelha)
    pygame.draw.rect(tela, (255, 50, 50), (*comida, 10, 10))

    # pontuação
    texto = fonte.render(f"Score: {pontuacao}", True, (255, 255, 255))
    tela.blit(texto, (10, 10))

    # timer
    tempo_passado = int(time.time() - timer_inicio)
    texto_timer = fonte.render(f"Tempo: {tempo_passado}s", True, (255, 255, 255))
    tela.blit(texto_timer, (470, 10))

    # pausa
    if pausado:
        overlay = fonte.render("PAUSADO", True, (255, 255, 0))
        tela.blit(overlay, (260, 180))

    pygame.display.update()

# --- Loop principal ---
rodando = True
relogio = pygame.time.Clock()
frame = 0

while rodando:
    frame += 1

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_p:
                pausado = not pausado

            if not pausado:
                if evento.key == pygame.K_UP and direcao != (0, 10):
                    direcao = (0, -10)
                elif evento.key == pygame.K_DOWN and direcao != (0, -10):
                    direcao = (0, 10)
                elif evento.key == pygame.K_LEFT and direcao != (10, 0):
                    direcao = (-10, 0)
                elif evento.key == pygame.K_RIGHT and direcao != (-10, 0):
                    direcao = (10, 0)

    if pausado:
        desenhar(frame)
        continue

    # mover cobra
    nova_cabeca = (corpo_cobra[0][0] + direcao[0], corpo_cobra[0][1] + direcao[1])
    corpo_cobra.insert(0, nova_cabeca)

    # comer
    if nova_cabeca == comida:
        pontuacao += 1
        comida = (random.randrange(0, 59) * 10, random.randrange(0, 39) * 10)
    else:
        corpo_cobra.pop()

    # colisão com o corpo
    if nova_cabeca in corpo_cobra[1:]:
        rodando = False

    # colisão com paredes
    if nova_cabeca[0] < 0 or nova_cabeca[0] >= 600 or nova_cabeca[1] < 0 or nova_cabeca[1] >= 400:
        rodando = False

    desenhar(frame)
    relogio.tick(15)

pygame.quit()
