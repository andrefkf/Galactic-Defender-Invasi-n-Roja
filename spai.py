import pygame
import random

pygame.init()

# Configuración
ANCHO = 800
ALTO = 600
FPS = 60
COLOR_FONDO = (0, 0, 20)

# Pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Invaders Mejorado")
reloj = pygame.time.Clock()

# Colores
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
BLANCO = (255, 255, 255)
AMARILLO = (255, 255, 0)
NEGRO = (0, 0, 0)

# Fuentes
fuente_grande = pygame.font.SysFont("Arial Black", 64)
fuente_mediana = pygame.font.SysFont("Arial", 32)
fuente_pequena = pygame.font.SysFont("Arial", 24)

# Estrellas para fondo animado
estrellas = [(random.randint(0, ANCHO), random.randint(0, ALTO)) for _ in range(60)]

# Variables de juego globales
puntaje = 0
vidas = 3
game_over = False
victoria = False

# --- Clases ---
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Diseño mejorado: nave triangular con un rectángulo para el cuerpo
        self.image = pygame.Surface((60, 40), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, AZUL, [(0, 40), (30, 0), (60, 40)])  # triángulo superior
        pygame.draw.rect(self.image, (0, 100, 255), (10, 30, 40, 10))  # cuerpo
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 10
        self.velocidad = 6

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.velocidad
        if teclas[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocidad
        if teclas[pygame.K_DOWN] and self.rect.bottom < ALTO:
            self.rect.y += self.velocidad

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((60, 40), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, ROJO, [(0, 40), (30, 0), (60, 40)])  # triángulo superior
        pygame.draw.rect(self.image, (150, 0, 0), (10, 30, 40, 10))  # cuerpo
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direccion = 1
        self.velocidad = 2
        self.disparo_cooldown = random.randint(60, 180)  # frames hasta el próximo disparo

    def update(self):
        self.rect.x += self.velocidad * self.direccion
        if self.rect.right >= ANCHO or self.rect.left <= 0:
            self.direccion *= -1
            self.rect.y += 10
        
        # Manejar cooldown y disparo
        self.disparo_cooldown -= 1
        if self.disparo_cooldown <= 0:
            bala = BalaEnemiga(self.rect.centerx, self.rect.bottom)
            grupo_balas_enemigos.add(bala)
            self.disparo_cooldown = random.randint(90, 240)  # nuevo cooldown

class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.velocidad = -10

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.bottom < 0:
            self.kill()

class BalaEnemiga(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(AMARILLO)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.velocidad = 6

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.top > ALTO:
            self.kill()

# Grupos
jugador = Jugador()
grupo_jugador = pygame.sprite.Group(jugador)
grupo_balas = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()
grupo_balas_enemigos = pygame.sprite.Group()

# Crear enemigos
for fila in range(3):
    for col in range(7):
        enemigo = Enemigo(100 + col * 70, 50 + fila * 60)
        grupo_enemigos.add(enemigo)

# Mostrar texto con sombra para mejor visibilidad
def mostrar_texto(texto, x, y, fuente, color=BLANCO, sombra=True):
    if sombra:
        sombra_render = fuente.render(texto, True, NEGRO)
        pantalla.blit(sombra_render, (x + 2, y + 2))
    render = fuente.render(texto, True, color)
    pantalla.blit(render, (x, y))

# Mostrar opciones para reiniciar o salir
def mostrar_menu_fin(texto_principal):
    pantalla.fill(COLOR_FONDO)
    mostrar_texto(texto_principal, ANCHO//2 - 150, ALTO//3, fuente_grande, AMARILLO)
    mostrar_texto("Presiona R para volver a jugar", ANCHO//2 - 150, ALTO//2, fuente_mediana, BLANCO)
    mostrar_texto("Presiona Q para salir", ANCHO//2 - 150, ALTO//2 + 40, fuente_mediana, BLANCO)
    pygame.display.flip()

def reiniciar_juego():
    global puntaje, vidas, game_over, victoria, grupo_enemigos, grupo_balas, grupo_balas_enemigos, grupo_jugador, jugador

    puntaje = 0
    vidas = 3
    game_over = False
    victoria = False

    grupo_balas.empty()
    grupo_balas_enemigos.empty()
    grupo_enemigos.empty()
    grupo_jugador.empty()

    jugador = Jugador()
    grupo_jugador.add(jugador)

    for fila in range(3):
        for col in range(7):
            enemigo = Enemigo(100 + col * 70, 50 + fila * 60)
            grupo_enemigos.add(enemigo)

# Bucle principal
ejecutando = True
while ejecutando:
    reloj.tick(FPS)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        elif evento.type == pygame.KEYDOWN:
            if not game_over and not victoria:
                if evento.key == pygame.K_SPACE:
                    bala = Bala(jugador.rect.centerx, jugador.rect.top)
                    grupo_balas.add(bala)
            else:
                if evento.key == pygame.K_r:
                    reiniciar_juego()
                elif evento.key == pygame.K_q:
                    ejecutando = False

    if not game_over and not victoria:
        grupo_jugador.update()
        grupo_balas.update()
        grupo_enemigos.update()
        grupo_balas_enemigos.update()

        # Colisiones balas jugador - enemigos
        colisiones = pygame.sprite.groupcollide(grupo_balas, grupo_enemigos, True, True)
        puntaje += len(colisiones) * 10

        # Colisiones balas enemigos - jugador
        if pygame.sprite.spritecollideany(jugador, grupo_balas_enemigos):
            vidas -= 1
            # Eliminar todas las balas que golpearon al jugador
            for bala_enemiga in pygame.sprite.spritecollide(jugador, grupo_balas_enemigos, True):
                pass
            if vidas <= 0:
                game_over = True

        # Enemigos que llegan al fondo
        for enemigo in grupo_enemigos:
            if enemigo.rect.bottom >= ALTO:
                vidas -= 1
                grupo_enemigos.remove(enemigo)
                if vidas <= 0:
                    game_over = True

        # Si ganás
        if len(grupo_enemigos) == 0:
            victoria = True

        # Dibujar fondo y objetos
        pantalla.fill(COLOR_FONDO)
        for i, (x, y) in enumerate(estrellas):
            pygame.draw.circle(pantalla, BLANCO, (x, y), 2)
            estrellas[i] = (x, (y + 1) % ALTO)

        grupo_jugador.draw(pantalla)
        grupo_balas.draw(pantalla)
        grupo_enemigos.draw(pantalla)
        grupo_balas_enemigos.draw(pantalla)

        # HUD
        mostrar_texto(f"Puntaje: {puntaje}", 10, 10, fuente_pequena)
        mostrar_texto(f"Vidas: {vidas}", ANCHO - 150, 10, fuente_pequena)

        pygame.display.flip()

    else:
        if game_over:
            mostrar_menu_fin("GAME OVER")
        elif victoria:
            mostrar_menu_fin("¡VICTORIA!")

pygame.quit()
