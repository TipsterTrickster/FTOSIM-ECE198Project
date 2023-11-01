import pygame
import pandas
pygame.init()
pygame.key.set_repeat(200,100)
import os
import math




class statis():
    def __init__(self):
        self.BLACK = (0, 0, 0)
        self.font = pygame.font.Font(None, 40)
        #triggers when an attempt is started to grab the current time as a 0 point
        self.start_time = 0
        #triggers when a solve is completed as the difference between current time and start time
        self.end_time = 0
        #used to flip between the timer running and timer stopped states
        self.flip = 1
        #based on the the flip state, dictates what is actually returned from the clock method
        self.val_out = 0
        #list of times from previous solves
        self.sorted_time = []
        self.rawtimes = []
        self.averaged_values = []
        self.formatted_avg = 0
        #iterates through for the number of items in the sorted_time list, determines how they're displayed on the screen
        self.item = 0
        #counts how many items are in the completed run list to keep that at 10 or below
        self.counter = 0
        self.avgof12 = 0
        #counts the number of attempts for every time a new one is added to the list and numbers the times on the display
        self.index = 0
        self.movecount = 0
        self.data_array = {"Time":[],"Moves":[]}
    #this method tracks the overall time in the background to use when the spacebar is pressed to start and stop the timer
    def clock(self,move,dimen):
        total_time = pygame.time.get_ticks()
        output_time = total_time - self.start_time
        for event in pygame.event.get():
            if (pygame.key.get_pressed()[pygame.K_SPACE]) & (self.flip == 0) & (event.type == pygame.KEYDOWN):
                self.end_time = output_time
                self.counter += 1
                if self.counter > 10:
                    self.counter = 10
                self.avgof12 += 1
                if self.avgof12 > 12:
                    self.avgof12 = 12
                self.leaderboard(self.end_time,self.movecount)
                self.average(self.end_time,self.movecount)
                self.val_out = 1
                self.flip = 1
            elif (pygame.key.get_pressed()[pygame.K_SPACE]) & (self.flip == 1) & (event.type == pygame.KEYDOWN): 
                self.flip = 0
                self.start_time = total_time
                output_time = total_time - self.start_time
                self.val_out = 2
        if self.val_out == 1:
            self.movecount = 0
            return(int(self.end_time))
        elif self.val_out == 2:
            return(int(output_time))
        else:
            return(int(0))
    #this method puts the time returned from the clock method into the correct formatting and displays it on the screen  
    def timer(self,move,dimen):
        time = self.clock(move,dimen)
        ms = time % 1000
        seconds = (time // 1000) % 60
        minutes = (time//60000)
        output_string = "Time: {0:02}:{1:02}.{2:03}".format(minutes, seconds, ms)
        text = self.font.render(output_string, True, self.BLACK)
        dimen.blit(text, [20, 20])
        pass
    #this method takes the time from a solve, which is received through the clock method when the timer is stopped, and puts it in the right formatting to put in the past times log
    def leaderboard(self,solve_time,movecount):
        ms = solve_time % 1000
        seconds = (solve_time // 1000) % 60
        minutes = (solve_time//60000)
        self.index+=1
        time_format = "{0:02}:{1:02}.{2:03}".format(minutes,seconds,ms)
        self.data_array["Time"].append(time_format)
        self.data_array["Moves"].append(movecount)
        df = pandas.DataFrame(self.data_array)
        df.to_csv(os.path.join(r'solve_data.csv')) 
        printed = "{3:01}. {0:02}:{1:02}.{2:03} | {4:01} Moves".format(minutes,seconds,ms,self.index,movecount)
        self.movecount = 0
        self.sorted_time.append(printed) 
        pass
    
    #this method takes the list of previous times from the leaderboard method and actually renders them on the screen. I didn't combine the two because
    #I wanted a shorter method for actually rendering them since this has to be called hundreds of times per second to refresh it on the screen since the screen has to be refreshed
    #I assumed a longer method might take longer to run through and there could be other issues with running through certain lines so many times, especially if no new time is being input
    def print(self,dimen):
        self.item = 0
        if len(self.sorted_time) > 0:
            text = self.font.render("Average of 12", True, self.BLACK)
            dimen.blit(text, [20, 475])
            if self.avgof12 == 12:
                text = self.font.render(self.formatted_avg, True, self.BLACK)
                dimen.blit(text, [20, 500])
            else:
                text = self.font.render("N/A", True, self.BLACK)
                dimen.blit(text, [20, 500])
            for items in range(self.counter,0,-1):
                self.item+=1
                text = self.font.render(self.sorted_time[self.index - self.item], True, self.BLACK)
                dimen.blit(text, [960, (self.item*25)])
                if self.item > 10:
                    self.item = 10 
        pass
    def average(self,solve_time,movecount):
        self.rawtimes.append(solve_time)
        avgtotal = 0
        if self.avgof12 == 12:
            print(self.rawtimes[:])
            for solves in range(self.avgof12):
                avgtotal = avgtotal + self.rawtimes[-solves]
                self.averaged_values.append(self.rawtimes[-solves])
            self.averaged_values = sorted(self.averaged_values)
            maxmin = self.averaged_values[0]+self.averaged_values[11]
            avgtotal = avgtotal - maxmin
            avgtotal = avgtotal/10
            avgtotal = math.ceil(avgtotal)
            ms = avgtotal % 1000
            seconds = (avgtotal // 1000) % 60
            minutes = (avgtotal//60000)
            self.formatted_avg = "Time: {0:02}:{1:02}.{2:03}".format(minutes, seconds, ms)
        pass
