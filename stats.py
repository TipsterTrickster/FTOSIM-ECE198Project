import pygame
pygame.init()
pygame.key.set_repeat()



class statis():
    def __init__(self):
        self.BLACK = (0, 0, 0)
        self.font = pygame.font.Font(None, 40)
        self.start_time = 0
        self.end_time = 0
        self.flip = 1
        self.val_out = 0
        self.sorted_time = []
        self.item = 0
        self.counter = 0
    #this method tracks the overall time in the background to use when the spacebar is pressed to start and stop the timer
    def clock(self,dimen):
        total_time = pygame.time.get_ticks()
        output_time = total_time - self.start_time 
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN) & (self.flip == 0):
                    self.end_time = output_time
                    #this variable tracks how many times have been added to the past times log on the right and starts removing them when you reach over 10 solves
                    self.counter += 1
                    if self.counter > 10:
                        self.sorted_time.pop(0)
                        self.counter = 10
                    self.leaderboard(self.end_time,dimen)
                    self.val_out = 1
                    self.flip = 1
            elif (event.type == pygame.KEYDOWN) & (self.flip == 1): 
                    self.flip = 0
                    self.start_time = total_time
                    output_time = total_time - self.start_time
                    self.val_out = 2
        if self.val_out == 1:
            return(int(self.end_time))
        elif self.val_out == 2:
            return(int(output_time))
        else:
            return(int(0))
    #this method puts the time returned from the clock method into the correct formatting and renders it on the screen  
    def timer(self,dimen):
        time = self.clock(dimen)
        ms = time % 1000
        seconds = (time // 1000) % 60
        minutes = (time//60000)
        output_string = "Time: {0:02}:{1:02}:{2:03}".format(minutes, seconds, ms)
        text = self.font.render(output_string, True, self.BLACK)
        dimen.blit(text, [20, 20])
        pass
    #this method takes the time from a solve, which is received through the clock method when the timer is stopped, and puts it in the right formatting to put in the past times log
    def leaderboard(self,solve_time,dimen):
        ms = solve_time % 1000
        seconds = (solve_time // 1000) % 60
        minutes = (solve_time//60000)
        printed = "Time: {0:02}:{1:02}:{2:03}".format(minutes,seconds,ms)
        self.sorted_time.append(printed)  
        pass
    #this method takes the list of previous times from the leaderboard method and actually renders them on the screen. I didn't combine the two because
    #I wanted a shorter method for actually rendering them since this has to be called hundreds of times per second to refresh it on the screen since the screen has to be refreshed
    #I assumed a longer method might take longer to run through and there could be other issues with running through certain lines so many times, especially if no new time is being input
    def print(self,dimen):
        self.item = 0
        if len(self.sorted_time) > 0:
            for items in range(self.counter):
                text = self.font.render(self.sorted_time[self.item], True, self.BLACK)
                dimen.blit(text, [1000, 20+(self.item*25)])
                self.item+=1
                if self.item > 10:
                    self.item = 10 
        pass
