import random
import sys
import time
import keyboard
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
    def __init__(self, game_board):
        self.head = (5, 5)
        self.body = [(5, 5)]
        self.direction = Direction.RIGHT
        self.alive = True
        self.game_board = game_board

    def move(self):
        if not self.alive:
            return

        current_x, current_y = self.head
        dx, dy = self.direction
        new_head = (current_x + dx, current_y + dy)
        if new_head in self.body or not self.game_board.is_within_bounds(new_head):
            self.alive = False
        else:
            self.head = new_head
            self.body.insert(0, new_head)
            if new_head == self.game_board.food_position:
                self.game_board.place_food()
            else:
                self.body.pop()

    def change_direction(self, new_direction):
        opposite_direction = (-self.direction[0], -self.direction[1])
        if new_direction != opposite_direction:
            self.direction = new_direction


class GameBoard:
    def __init__(self, width, height, snake):
        self.width = width
        self.height = height
        self.snake = snake
        self.food_position = None
        self.place_food()

    def is_within_bounds(self, position):
        x, y = position
        return 0 <= x < self.width and 0 <= y < self.height

    def place_food(self):
        while True:
            position = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            if position not in self.snake.body:
                self.food_position = position
                break

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) == self.snake.head:
                    print('S', end='')
                elif (x, y) in self.snake.body:
                    print('s', end='')
                elif (x, y) == self.food_position:
                    print('F', end='')
                else:
                    print('.', end='')
            print()
        print()


class SnakeGame:
    def __init__(self, width, height):
        self.snake = Snake(None)  # Temporarily no game board
        self.game_board = GameBoard(width, height, self.snake)
        self.snake.game_board = self.game_board  # Link back the game board

    def update(self):
        self.snake.move()
        if not self.snake.alive:
            print("Game Over!")
            sys.exit()

    def run(self):
        while self.snake.alive:
            self.game_board.render()
            self.update()
            time.sleep(0.5)

            if keyboard.is_pressed('up'):
                self.snake.change_direction(Direction.UP)
            elif keyboard.is_pressed('down'):
                self.snake.change_direction(Direction.DOWN)
            elif keyboard.is_pressed('left'):
                self.snake.change_direction(Direction.LEFT)
            elif keyboard.is_pressed('right'):
                self.snake.change_direction(Direction.RIGHT)


if __name__ == '__main__':
    game = SnakeGame(20, 10)
    game.run()
