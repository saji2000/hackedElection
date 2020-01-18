from uagame import Window
import pygame, time
from pygame.locals import *

def main():
    window = Window('Pong', 500, 500)
    window.set_auto_update(False)   
    game = Game(window)
    
    game.play()
    window.close() 
    

class Game:
    
    def __init__(self, window):
        # Initialize a Game.
        # - self is the Game to initialize
        # - window is the uagame window object
        pygame.key.set_repeat(20, 20)
        height = window.get_height()//6
        width =  window.get_height()//30
        radius = window.get_height()//60
        self.window = window
        self.bg_color = pygame.Color('black')
        self.pause_time = 0.01 # smaller is faster game
        self.close_clicked = False
        self.continue_game = True
        self.ball = Ball('white', radius, [window.get_width()//2, window.get_height()//2], [-15,5], window.get_surface())
        self.left_paddle = Paddle(self.window.get_surface(),'white',[self.window.get_width()//9,(self.window.get_height()//2)-self.window.get_width()//9],[width, height])
        self.right_paddle = Paddle(self.window.get_surface(),'white',[self.window.get_width()-((self.window.get_width()//9)+width),(self.window.get_height()//2)-self.window.get_width()//9],[width, height]) 
        self.left_score = 0
        self.right_score = 0
    
        #
        
    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.
    
        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_event()
            self.draw()   
            if self.continue_game:
                self.update()
                self.decide_continue()
            time.sleep(self.pause_time) # set game velocity by pausing
            
            
    def handle_event(self):
        # Handle each user event by changing the game state
        # appropriately.
        # - self is the Game whose events will be handled
            
        event = pygame.event.poll()
        key_list = []
        key_list = pygame.key.get_pressed()
        if event.type == QUIT:
            self.close_clicked = True
        if key_list[K_q] and self.continue_game:
            self.left_paddle.paddle_up()
        elif key_list[K_a] and self.continue_game:
            self.left_paddle.paddle_down()
        if key_list[K_p] and self.continue_game:
            self.right_paddle.paddle_up()
        elif key_list[K_l] and self.continue_game:
            self.right_paddle.paddle_down()        
        
    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw
                  
        self.window.clear()        
        self.left_paddle.draw()
        self.right_paddle.draw()
        self.draw_left_score()
        self.draw_right_score()        
        self.ball.draw()

        self.window.update()
   
    def update_right_score(self):
       
        # update the right score
        window_width = self.window.get_width()
        ball_radius = self.ball.radius
        self.right_score == 0
        if self.ball.center[0] <= ball_radius:
            self.right_score += 1    
        return self.right_score
    
    def update_left_score(self):
        
        # update the right score
        window_width = self.window.get_width()
        ball_radius = self.ball.radius
        self.left_score == 0 
        if self.ball.center[0] >= window_width - ball_radius:
            self.left_score += 1  
        return self.left_score
    
    def draw_right_score(self):
        # Draws right score
        window_width = self.window.get_width()
        string_x = window_width-20 
        if self.right_score >= 10:
            string_x -= 20         
        score_string = str(self.right_score)
        self.window.set_font_size(50)
        self.window.draw_string(score_string, string_x, 0)
    def draw_left_score(self):
        # Draws left score
        score_string = str(self.left_score)
        self.window.set_font_size(50)
        self.window.draw_string(score_string,0,0 )         

            
    def update(self):
        # Update the game objects.
        # - self is the Game to update
        self.ball.move(self.left_paddle,self.right_paddle)
        self.update_left_score()
        self.update_right_score()
        #self.left_paddle.update_paddle()
        #self.right_paddle.update_paddle()
    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check
        end_score = 11
        if self.left_score == end_score or self.right_score == end_score:
            self.continue_game = False

class Ball:
    # An object in this class represents a colored circle.
    def __init__(self, color, radius, center, velocity, surface):
        # Initialize a Cirlcle.
        # - self is the Circle to initialize
        # - center is a list containing the x and y int
        # coords of the center of the Circle
        # - radius is the int pixel radius of the Circle
        # - color is the pygame.Color of the Circle
        # - window is the uagame window object

        self.center = center
        self.radius = radius
        self.color = pygame.Color(color)
        self.surface = surface
        self.velocity = velocity
        
    def draw(self):
        # Draw the Circle.
        # - self is the Circle to draw            
        pygame.draw.circle(self.surface, self.color, self.center, self.radius)
   
    def move(self, left_paddle, right_paddle):
        # Change the location and the velocity of the Ball so it
        # remains on the surface by bouncing from its edges.
        # - self is the Ball
        size = self.surface.get_size()
        for coordinate in range(0, 2):
            self.center[coordinate] = (self.center[coordinate] + self.velocity[coordinate]) 
            if  self.center[coordinate]  <= self.radius or self.center[coordinate] + self.radius >= size[coordinate]:
                self.velocity[coordinate] = - self.velocity[coordinate]  
            if coordinate == 0:
                if left_paddle.collision_check_left_paddle(self.center, self.velocity, self.radius):
                    self.velocity[coordinate] = - self.velocity[coordinate]
                if right_paddle.collision_check_right_paddle(self.center, self.velocity, self.radius):
                    self.velocity[coordinate] = - self.velocity[coordinate]                    
           
    
    
class Paddle:
    def __init__(self, surface, color, coordinates, dimensions):
       
        self.surface = surface
        self.color = pygame.Color(color)
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.width = dimensions[0]
        self.height = dimensions[1]

    def draw(self):
        #draws a rectangle with the current coordinates and dimensions
        pygame.draw.rect(self.surface,self.color,pygame.Rect((self.x, self.y), (self.width, self.height)))
    
    def collision_check_left_paddle(self, center, velocity, radius):
        # Checks collision for front of left paddle
        edge = center[0] - radius       
        if pygame.Rect((self.x, self.y), (self.width, self.height)).collidepoint(edge,center[1]) and velocity[0]<0:
            return True
    def collision_check_right_paddle(self, center, velocity, radius):
        edge = center[0] + radius 
        # Checks collision for front of left paddle
        if pygame.Rect((self.x, self.y), (self.width, self.height)).collidepoint(edge,center[1]) and velocity[0]>0:
            return True 
    def paddle_up(self):
        if self.y > 0:
            self.y -= 25
    def paddle_down(self):
        if self.y < self.surface.get_height() - self.height:
            self.y += 25    
main()