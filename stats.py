import pygame
pygame.init()
pygame.key.set_repeat()

#This somewhat works for starting and stopping the timer with the spacebar. There is some bug with how it loops where itll trigger multiple stages at once, not starting/stopping the timer correctly, but I can fix that
#My thinking is that for each run it will initialize a new iteration of the class and the leaderboard will display a sorted list of the iterations. 

class statis():
    def __init__(self):
        self.BLACK = (0, 0, 0)
        self.font = pygame.font.Font(None, 25)
        self.start_time = 0
        self.end_time = 0
        self.flip = 1
        self.val_out = 0
        self.end_time = 0

    def timer(self,dimen):
        time = self.clock()
        ms = time % 1000
        seconds = (time // 1000) % 60
        minutes = (time//60000)
        output_string = "Time: {0:02}:{1:02}:{2:02}".format(minutes, seconds, ms)
        text = self.font.render(output_string, True, self.BLACK)
        dimen.blit(text, [20, 20])

    def clock(self):
        total_time = pygame.time.get_ticks()
        output_time = total_time - self.start_time 
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN) & (self.flip == 0):
                    self.end_time = output_time
                    self.val_out = 1
                    print("h")
            elif (event.type == pygame.KEYUP) & (self.flip == 1): 
                    self.flip = 0
                    self.start_time = total_time
                    output_time = total_time - self.start_time
                    self.val_out = 2
                    print("f")
            elif (event.type == pygame.KEYUP) & (self.flip == 0):
                    self.flip = 1
                    self.val_out = 0
                    print("l")
        if self.val_out == 1:
            return(int(self.end_time))
        elif self.val_out == 2:
            return(int(output_time))
        else:
            return(int(0))
            
