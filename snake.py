import pygame
import random

# Inicializar Pygame
pygame.init()

# Definir colores
WHITE = (255, 255, 255)
GREEN_LIGHT = (144, 238, 144)
GREEN_DARK = (34, 139, 34)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Definir dimensiones de la pantalla
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20

# Definir la velocidad de cambio de color de fondo
BACKGROUND_CHANGE_SPEED = 5

class Snake:
    def __init__(self):
        """Inicializa la serpiente con una posición y dirección inicial."""
        self.body = [(WIDTH / 2, HEIGHT / 2)]
        self.direction = (1, 0)
        self.color_index = 0  # Índice para alternar entre los colores de la serpiente

    def move(self, apple):
        """Mueve la serpiente en la dirección actual y maneja la lógica de colisión con la manzana."""
        x, y = self.body[0]
        dx, dy = self.direction
        new_head = ((x + dx * CELL_SIZE) % WIDTH, (y + dy * CELL_SIZE) % HEIGHT)
        if new_head in self.body[1:]:
            return False  # El juego termina si la serpiente choca consigo misma
        self.body.insert(0, new_head)
        if new_head != apple.position:
            self.body.pop()  
        return True

    def change_direction(self, direction):
        """Cambia la dirección de la serpiente, evitando cambios de 180 grados."""
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def draw(self, surface):
        """Dibuja la serpiente en la pantalla."""
        for i, segment in enumerate(self.body):
            color = (GREEN_LIGHT if i % 2 == 0 else GREEN_DARK)  # Alternar entre los colores definidos
            pygame.draw.rect(surface, color, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

class Apple:
    def __init__(self):
        """Inicializa una manzana con una posición aleatoria."""
        self.position = self.randomize_position()

    def randomize_position(self):
        """Genera una posición aleatoria para la manzana."""
        x = random.randrange(0, WIDTH, CELL_SIZE)
        y = random.randrange(0, HEIGHT, CELL_SIZE)
        return x, y

    def draw(self, surface):
        """Dibuja la manzana en la pantalla."""
        pygame.draw.rect(surface, RED, (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))

def menu_dificultad(screen):
    """Muestra la pantalla de inicio para seleccionar la dificultad."""
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 48)
    text_intro = font.render("Pulse el numero de la dificultad escogida", True, BLACK)
    text_credit = font.render("Hecho por Diego Jurado", True, BLACK)

    text_easy = font.render("Fácil (1)", True, BLACK)
    text_medium = font.render("Medio (2)", True, BLACK)
    text_hard = font.render("Difícil (3)", True, BLACK)

    screen.blit(text_intro, (WIDTH/2 - text_intro.get_width()/2, HEIGHT/2 - 150))
    screen.blit(text_credit, (WIDTH - text_credit.get_width() - 10, HEIGHT - text_credit.get_height() - 10))

    screen.blit(text_easy, (WIDTH/2 - text_easy.get_width()/2, HEIGHT/2 - 100))
    screen.blit(text_medium, (WIDTH/2 - text_medium.get_width()/2, HEIGHT/2))
    screen.blit(text_hard, (WIDTH/2 - text_hard.get_width()/2, HEIGHT/2 + 100))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "easy"
                elif event.key == pygame.K_2:
                    return "medium"
                elif event.key == pygame.K_3:
                    return "hard"

def calculate_background_color(score):
    """Calcula el color de fondo basado en la puntuación."""
    if score <= 51:
        r = max(0, 255 - 5 * score)
        g = max(0, 255 - 5 * score)
        b = 255
    else:
        r = min(255, (score - 50) * 5)
        g = min(255, (score - 50) * 5)
        b = 255
    return (r, g, b)

# Función principal del juego
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")

    clock = pygame.time.Clock()  # Define el reloj antes de utilizarlo

    # Pantalla de inicio para seleccionar dificultad
    difficulty = menu_dificultad(screen)

    # Definir las variables de dificultad según la selección
    if difficulty == "easy":
        apple_count = 10
        snake_speed = 5
    elif difficulty == "medium":
        apple_count = 3
        snake_speed = 10
    else:
        apple_count = 1
        snake_speed = 15

    # Inicializar la serpiente, las manzanas, la puntuación, los sonidos y otras variables del juego
    snake = Snake()
    apples = [Apple() for _ in range(apple_count)]
    score = 0
    eat_sound = pygame.mixer.Sound("eat_sound.wav")
    game_over = False
    font = pygame.font.SysFont(None, 36)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((1, 0))

        # Mover serpiente
        if not snake.move(apples[0]):  # Pasar una instancia de Apple como argumento
            game_over = True

        # Comprobar si la serpiente come alguna manzana
        for apple in apples[:]:
            if snake.body[0] == apple.position:
                eat_sound.play()
                score += 1
                # Añadir una nueva posición al final del cuerpo de la serpiente
                snake.body.append(snake.body[-1])
                # Remover la manzana comida
                apples.remove(apple)
                # Añadir una nueva manzana
                apples.append(Apple())

        # Dibujar todo en la pantalla
        screen.fill(calculate_background_color(score))  # Cambiar el color de fondo
        snake.draw(screen)
        for apple in apples:
            apple.draw(screen)

        # Mostrar puntuación
        text = font.render("Score: " + str(score), True, GREEN_DARK)
        screen.blit(text, (10, 10))

        # Actualizar pantalla
        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()

if __name__ == "__main__":
    main()




"""@diegojura en github"""
