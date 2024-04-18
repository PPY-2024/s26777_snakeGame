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


