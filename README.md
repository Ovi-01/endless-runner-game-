# endless-runner-game-
Code Breakdown:

Initialization: Sets up Pygame, creates the screen, defines colors, fonts, and game variables.<br>
Player Class: Manages the player character, including its position, size, jumping physics (gravity, jump strength), drawing, and updating its state.<br>
Obstacle Class: Manages obstacles, including their position, size, movement (scrolling left), and drawing.<br>
Game Loop: The main part of the game.<br>
Handles user input (jumping, quitting).<br>
Updates the player's position (applying gravity/jump).<br>
Updates obstacle positions and removes off-screen obstacles.<br>
Spawns new obstacles periodically.<br>
Checks for collisions between the player and obstacles.
Increases the score and game speed over time.
Draws everything onto the screen (background, player, obstacles, score).
Controls the game's frame rate.
Game Over Loop: Displays the game over message and final score, waiting for the user to restart or quit.<br>
Main Function: Initializes the game and runs the main game loop, handling restarts.<br>
