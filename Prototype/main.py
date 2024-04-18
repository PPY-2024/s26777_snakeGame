import pytest

def test_snake_initialization():
    snake = Snake()
    assert snake.head == (0, 0)
    assert snake.body == [(0, 0)]
    assert snake.direction == Direction.RIGHT
    assert snake.alive == True

def test_snake_movement():
    snake = Snake()
    snake.move()
    assert snake.head == (1, 0)

def test_snake_grow():
    snake = Snake()
    snake.eat_food()
    assert len(snake.body) == 2

def test_snake_collision():
    snake = Snake()
    snake.move()
    snake.move()
    snake.move()
    snake.change_direction(Direction.UP)
    snake.move()
    assert not snake.alive

def test_game_board():
    board = GameBoard(10, 10)
    assert board.width == 10
    assert board.height == 10
    assert board.food_position is not None
    assert board.is_within_bounds((5, 5))
    assert not board.is_within_bounds((15, 5))

def test_game_logic():
    game = SnakeGame(10, 10)
    assert game.snake.alive
    assert game.game_board.food_position is not None
    game.update()
    assert game.snake.alive


class Direction:
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.head = (0, 0)
        self.body = [(0, 0)]
        self.direction = Direction.RIGHT
        self.alive = True

    def move(self):
        current_x, current_y = self.head
        dx, dy = self.direction
        new_head = (current_x + dx, current_y + dy)

        if new_head in self.body or not self.is_within_bounds(new_head):
            self.alive = False
        else:
            self.head = new_head
            self.body.insert(0, new_head)

    def change_direction(self, new_direction):
        if (new_direction[0] != -self.direction[0] or
                new_direction[1] != -self.direction[1]):
            self.direction = new_direction

    def eat_food(self):
        self.body.append(self.body[-1])

    def is_within_bounds(self, position):
        x, y = position
        return True

class GameBoard:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.food_position = (5, 5)

    def is_within_bounds(self, position):
        x, y = position
        return 0 <= x < self.width and 0 <= y < self.height

class SnakeGame:
    def __init__(self, width, height):
        self.snake = Snake()
        self.game_board = GameBoard(width, height)

    def update(self):
        if self.snake.alive:
            self.snake.move()
