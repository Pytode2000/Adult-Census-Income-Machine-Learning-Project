import random
import time
import sys
import keyboard

# ANSI escape sequences for terminal control
CLEAR_SCREEN = "\033[2J\033[H"  # Clear screen
MOVE_UP = "\033[1A"  # Move cursor up one line
MOVE_DOWN = "\033[1B"  # Move cursor down one line
MOVE_RIGHT = "\033[1C"  # Move cursor right one column
MOVE_LEFT = "\033[1D"  # Move cursor left one column

def display_game(player_position, obstacle_positions, score):
    game_display = [['🌳'] + (["  "] * 20) + ['🌳'] for _ in range(10)]  # 10x20 game environment
    
    # Place the player in the game display
    game_display[player_position[0]][player_position[1]] = '🚘'
    
    # Place the obstacles in the game display if they're within boundaries
    for pos, size in obstacle_positions:
        for i in range(size[0]):
            for j in range(size[1]):
                if pos[0] + i >= 0 and pos[0] + i < 10 and pos[1] + j >= 0 and pos[1] + j < 20:
                    game_display[pos[0] + i][pos[1] + j] = '🌳'
    
    # Display the game environment and score
    sys.stdout.write(CLEAR_SCREEN)  # Clear the screen
    for row in game_display:
        for char in row:
            sys.stdout.write(char)
        sys.stdout.write("\n")
    sys.stdout.write(f"Score: {score}\n")
    sys.stdout.flush()

def move_player_left(player_position):
    if player_position[1] > 1:
        player_position[1] -= 1

def move_player_right(player_position):
    if player_position[1] < 20:
        player_position[1] += 1

def generate_obstacle():
    size = random.randint(1, 3)  # Random size (1x1 to 3x3)
    pos = [0, random.randint(0, 20 - size)]  # Obstacle starts at top row (0) and a random column
    return (pos, (size, size))  # Return obstacle position and size as tuple

def move_obstacle(obstacle_positions):
    for idx, (pos, size) in enumerate(obstacle_positions):
        pos[0] += 1  # Move obstacles down by one row
        if pos[0] >= 10:  # Remove obstacles that have reached the bottom
            del obstacle_positions[idx]

def check_collision(player_position, obstacle_positions):
    for pos, size in obstacle_positions:
        for i in range(size[0]):
            for j in range(size[1]):
                if pos[0] + i == player_position[0] and pos[1] + j == player_position[1]:
                    return True  # Collision detected
    return False

def endless_runner():
    player_position = [9, 10]  # Initial position of the player [row, column]
    obstacle_positions = []  # List to store obstacle positions
    game_speed = 0.1  # Game speed (lower value for faster speed)
    obstacle_spawn_rate = 0.2  # Rate at which obstacles are generated (lower value for more frequent)
    score = 0  # Player's score
    last_score_update_time = time.time()  # Track the last time the score was updated
    while True:
        # Generate random obstacles
        if random.random() < obstacle_spawn_rate:
            obstacle_positions.append(generate_obstacle())
        
        # Move obstacles and check for collisions
        move_obstacle(obstacle_positions)
        
        if check_collision(player_position, obstacle_positions):
            #sys.stdout.write(CLEAR_SCREEN)  # Clear the screen
            sys.stdout.write(f"Game Over! You collided with an obstacle. Final Score: {score}\n")
            sys.stdout.flush()
            return
        
        # Update score every 1 second
        current_time = time.time()
        if current_time - last_score_update_time >= 1:
            score += 1
            last_score_update_time = current_time
        
        display_game(player_position, obstacle_positions, score)  # Display the updated game state
        time.sleep(game_speed)  # Pause to control game speed

        # Get user input for player movement (using the keyboard library)
        if keyboard.is_pressed('left'):
            move_player_left(player_position)
        elif keyboard.is_pressed('right'):
            move_player_right(player_position)
            



if __name__ == "__main__":
    try:
        endless_runner()
    except KeyboardInterrupt:
        sys.exit(0)
