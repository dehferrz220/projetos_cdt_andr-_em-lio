import pygame
import random
import time

pygame.init()
tela = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Snake Run Deluxe")

# ========================
# CONFIGURAÇÕES
# ========================

VEL = 10
clock = pygame.time.Clock()

# Ranking em RAM
ranking = []

# Cores da cobra
cores_cobra = [
    (0, 255, 0),
    (0, 200, 255),
    (255, 0, 200),
    (255, 255, 0),
    (255, 100, 0)
]
cor_index = 0

# ========================
# FUNÇÕES
# ========================

def gerar_comida():
    return (random.randrange(0, 59) * 10, random.randrange(0, 39) * 10)

def desenhar(corpo_cobra, comida, pontuacao, tempo, cor_cobra):
    tela.fill((0, 0, 0))

    # desenha cobra
    for parte in corpo_cobra:
        pygame.draw.rect(tela, cor_cobra, (*parte, 10, 10))

    # desenha comida
    pygame.draw.rect(tela, (255, 0, 0), (*comida, 10, 10))

    # pontuação e tempo
    fonte = pygame.font.SysFont(None, 28)
    texto_pontos = fonte.render(f"Pontos: {pontuacao}", True, (255, 255, 255))
    texto_tempo = fonte.render(f"Tempo: {int(tempo)}s", True, (255, 255, 255))
    tela.blit(texto_pontos, (10, 10))
    tela.blit(texto_tempo, (10, 35))

    pygame.display.update()

def jogar():
    global cor_index

    corpo_cobra = [(90, 100)]
    direcao = (10, 0)
    comida = gerar_comida()
    pontuacao = 0
    inicio_tempo = time.time()

    rodando = True

    while rodando:
        tempo_atual = time.time() - inicio_tempo

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP and direcao != (0, 10):
                    direcao = (0, -10)
                elif evento.key == pygame.K_DOWN and direcao != (0, -10):
                    direcao = (0, 10)
                elif evento.key == pygame.K_LEFT and direcao != (10, 0):
                    direcao = (-10, 0)
                elif evento.key == pygame.K_RIGHT and direcao != (-10, 0):
                    direcao = (10, 0)

        # Movimento
        nova_cabeca = (corpo_cobra[0][0] + direcao[0], corpo_cobra[0][1] + direcao[1])
        corpo_cobra.insert(0, nova_cabeca)

        # Comeu comida
        if nova_cabeca == comida:
            pontuacao += 10
            comida = gerar_comida()

            # troca de cor da cobra
            cor_index = (cor_index + 1) % len(cores_cobra)

        else:
            corpo_cobra.pop()

        # colisão com corpo
        if nova_cabeca in corpo_cobra[1:]:
            rodando = False

        # colisão com parede
        if nova_cabeca[0] < 0 or nova_cabeca[0] >= 600 or nova_cabeca[1] < 0 or nova_cabeca[1] >= 400:
            rodando = False

        # desenhar
        desenhar(corpo_cobra, comida, pontuacao, tempo_atual, cores_cobra[cor_index])

        clock.tick(15)

    # Ao perder, registra ranking e reinicia
    ranking.append(pontuacao)
    ranking.sort(reverse=True)

    jogar()  # reinicia automaticamente


# ========================
# INICIAR JOGO
# ========================
jogar()
