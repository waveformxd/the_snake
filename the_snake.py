from abc import abstractmethod
from random import choice

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_SCREEN = (320, 240)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 2.5

# Картинки:
img_apple = './pictures/apple.png'
img_rock = './pictures/rock.png'
img_trash = './pictures/trash.png'
img_snake_head_right = './pictures/snake_head_r.png'
img_snake_head_down = './pictures/snake_head_d.png'
img_snake_head_left = './pictures/snake_head_l.png'
img_snake_head_up = './pictures/snake_head_u.png'
img_snake_body = './pictures/snake_body.png'

# Настройка игрового окна:
screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT),
                                 flags=0,
                                 depth=32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self):
        self.position = CENTER_SCREEN
        self.body_color = SNAKE_COLOR
        self.image = None

    @abstractmethod
    def draw(self, surface):
        """Отрисовывает объект на игровой поверхности."""
        screen.blit(self.image, (self.position[0], self.position[1]))

    @staticmethod
    def _random_positions_generator(from_, to_):
        """Генерирует случайное расположение для объектов
        в случайном количестве из диапазона (от:до].
        """
        result = []
        for i in range(from_, to_ + 1):
            res_1 = choice(
                [i * GRID_SIZE for i in range(1, SCREEN_WIDTH // 20)]
            )
            res_2 = choice(
                [i * GRID_SIZE for i in range(1, SCREEN_HEIGHT // 20)]
            )
            result.append((res_1, res_2))
        return result


class Apple(GameObject):
    """Класс, описывающий объект яблока."""

    def __init__(self, num: int = 1):
        super().__init__()
        self.position = self._random_positions_generator(1, num)
        self.image = pygame.image.load(img_apple).convert_alpha()

    def randomize_position(self, num: int = 1):
        """
        Генерирует случайные координаты на сетке игрового
        поля для расположения на них объекта яблока.
        """
        return self._random_positions_generator(1, num)

    def draw(self, surface):
        """Отрисовывает яблоко на игровой поверхности."""
        screen.blit(self.image, (self.position[0][0], self.position[0][1]))


class Snake(GameObject):
    """Класс, описывающий объект Змейки."""

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.body_image = pygame.image.load(
            img_snake_body).convert_alpha()
        self.head_image_right = pygame.image.load(
            img_snake_head_right).convert_alpha()
        self.head_image_down = pygame.image.load(
            img_snake_head_down).convert_alpha()
        self.head_image_left = pygame.image.load(
            img_snake_head_left).convert_alpha()
        self.head_image_up = pygame.image.load(
            img_snake_head_up).convert_alpha()

    def update_direction(self):
        """Устанавливает новое значение для направления движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Обновляет координаты каждой секции позиций змейки.
        Сначала меняет координаты первой секции(головы),
        затем проходится по всем остальным секциям и меняет
        их координаты по принципу: текущая секция принимает
        координаты предыдущей.
        """
        if len(self.positions) > 1:
            for i in range(-1, -1 * len(self.positions), -1):
                self.positions[i] = self.positions[i - 1]
        self.positions[0] = (
            self.positions[0][0] + self.direction[0] * 20,
            self.positions[0][1] + self.direction[1] * 20,
        )

    def draw(self, surface):
        """Отрисовывает змейку на экране, затирая след."""
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]), (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

        if len(self.positions) > 1:
            for position in self.positions[1:]:
                pygame.draw.rect(
                    surface,
                    BOARD_BACKGROUND_COLOR,
                    pygame.Rect((position[0], position[1]),
                                (GRID_SIZE, GRID_SIZE)),
                )
                screen.blit(self.body_image, (position[0], position[1]))

        # Отрисовка головы змейки
        if self.direction == RIGHT:
            screen.blit(
                self.head_image_right,
                (self.positions[0][0], self.positions[0][1])
            )
        elif self.direction == DOWN:
            screen.blit(
                self.head_image_down,
                (self.positions[0][0], self.positions[0][1])
            )
        elif self.direction == LEFT:
            screen.blit(
                self.head_image_left,
                (self.positions[0][0], self.positions[0][1])
            )
        elif self.direction == UP:
            screen.blit(
                self.head_image_up,
                (self.positions[0][0], self.positions[0][1])
            )
        self.last = (self.positions[-1][0], self.positions[-1][1])

    def eat_trash(self, surface):
        """Обработка съедания мусора змейкой."""
        last_rect = pygame.Rect(
            (self.positions[-1][0],
             self.positions[-1][1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)
        del self.positions[-1]

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает длину змейки и ее координаты до начального значения."""
        for position in self.positions:
            rect = pygame.Rect((position[0], position[1]),
                               (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]


class Rock(GameObject):
    """Класс, описывающий камень."""

    def __init__(self, num: int = 7):
        super().__init__()
        self.image = pygame.image.load(img_rock).convert_alpha()
        self.positions = self.randomize_positions(num)

    def randomize_positions(self, num: int = 7):
        """
        Генерирует случайные координаты на сетке игрового
        поля для расположения на них нескольких объектов мусора.
        """
        return self._random_positions_generator(1, num)

    def draw(self, surface):
        """Отрисовывает камни на игровой поверхности."""
        for position in self.positions:
            screen.blit(self.image, (position[0], position[1]))


class Trash(GameObject):
    """Класс, описывающий мусор."""

    def __init__(self, num: int = 1):
        super().__init__()
        self.positions = self.randomize_positions(num)
        self.image = pygame.image.load(img_trash).convert_alpha()

    def randomize_positions(self, num: int = 1):
        """
        Генерирует случайные координаты на сетке игрового
        поля для расположения на них нескольких объектов мусора.
        """
        return self._random_positions_generator(1, num)

    def draw(self, surface):
        """Отрисовывает мусор на игровой поверхности."""
        for position in self.positions:
            screen.blit(self.image, (position[0], position[1]))


# Функция обработки действий пользователя
def handle_keys(game_object: Snake):
    """Функция-обработчик событий нажатий клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if ((event.key == pygame.K_UP)
                    and (game_object.direction != DOWN)):
                game_object.next_direction = UP
            elif ((event.key == pygame.K_DOWN)
                  and (game_object.direction != UP)):
                game_object.next_direction = DOWN
            elif ((event.key == pygame.K_LEFT)
                  and (game_object.direction != RIGHT)):
                game_object.next_direction = LEFT
            elif ((event.key == pygame.K_RIGHT)
                  and (game_object.direction != LEFT)):
                game_object.next_direction = RIGHT


def go(snake, rocks, apple, trash):
    """Основной процесс игры и обработка событий."""
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        head_position = snake.get_head_position()
        # Проверка, не съела ли голова яблоко.
        if head_position == apple.position[0]:
            apple.position = apple.randomize_position()
            while apple.position in trash.positions + rocks.positions:
                apple.position = apple.randomize_position()
            snake.positions.append((snake.positions[-1][0],
                                    snake.positions[-1][1]))

        elif (
            (  # Проверка:
                # Врезалась ли змейка саму в себя
                # Врезалась ли змейка в камень
                # Съела ли змейка мусор при длине в 1 клетку
                # Если выполняется хоть одно, игра начинается заново.
                head_position
                in snake.positions[3:])
            or (head_position in rocks.positions)
            or ((head_position in trash.positions)
                and (len(snake.positions) == 1))):
            snake.reset()
            rect = pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
            apple.position = apple.randomize_position()
            trash.positions = trash.randomize_positions()
            rocks.positions = rocks.randomize_positions()

        elif (  # Проверка, не съела ли голова мусор.
            head_position in trash.positions
        ) and (len(snake.positions) > 1):
            snake.eat_trash(screen)
            # Удаление мусора из клетки, в которую попала змейка.
            del trash.positions[trash.positions.index(head_position)]

        # Проверки на выход за пределы карты.
        if head_position[0] > SCREEN_WIDTH:
            snake.positions[0] = (0, head_position[1])
        elif head_position[0] < 0:
            snake.positions[0] = (SCREEN_WIDTH - 20, head_position[1])
        elif head_position[1] > SCREEN_HEIGHT:
            snake.positions[0] = (head_position[0], 0)
        elif head_position[1] < 0:
            snake.positions[0] = (head_position[0], SCREEN_HEIGHT - 20)

        snake.draw(screen)
        apple.draw(screen)
        rocks.draw(screen)
        trash.draw(screen)
        pygame.display.update()


def main():
    """Функция, выполняющаяся при запуске программы."""
    snake = Snake()
    rocks = Rock()
    apple = Apple()
    trash = Trash()
    snake.draw(screen)

    all_positions = apple.position + trash.positions + rocks.positions
    while len(set(all_positions)) < len(all_positions):
        # Проверка, не накладываются ли объекты друг на друга.
        # Если где-то накладываются, то их координаты заново
        # рандомизируются.
        apple.randomize_position()
        trash.randomize_positions()
        rocks.randomize_positions()
        all_positions = [apple.position] + trash.positions + rocks.positions

    apple.draw(screen)
    trash.draw(screen)
    rocks.draw(screen)

    go(snake, rocks, apple, trash)


if __name__ == "__main__":
    main()
