import pygame
import pandas
pygame.init()
import os
import math
from FTO import FTO
from pathlib import Path




class statis():
    def __init__(self):
        self.BLACK = (0, 0, 0)
        self.font = pygame.font.Font(None, 40)
        #triggers when an attempt is started to grab the current time as a 0 point
        self.start_time = 0
        #triggers when a solve is completed as the difference between current time and start time
        self.end_time = 0
        #used to flip between the timer running and timer stopped states
        self.started = 2
        #based on the the flip state, dictates what is actually returned from the clock method
        self.val_out = 0
        #list of times from previous solves
        self.sorted_time = []
        self.rawtimes = []
        self.fastestof12 = 0
        self.formatted_avgof12 = 0
        self.fastestof5 = 0
        self.formatted_avgof5 = 0
        #iterates through for the number of items in the sorted_time list, determines how they're displayed on the screen
        self.item = 0
        #counts how many items are in the completed run list to keep that at 10 or below
        self.counter = 0
        self.avgof12 = 0
        self.avgof5 = 0
        #counts the number of attempts for every time a new one is added to the list and numbers the times on the display
        self.index = 0
        self.movecount = 0
        self.data_array = {"Time":[],"Moves":[]}
        self.key_mapping = {}
        p = Path(__file__).with_name("key_binds.txt")
        with p.open('r') as file:
                for line in file:
                    move,  key = line.strip().split(': ')
                    self.key_mapping[key] = move

    def check_solved(self,cube_status):
        for i in range(len(cube_status)):
            for x in range(len(cube_status[i])):
                if cube_status[i][0] != cube_status[i][x]:
                    return False
        return True
    
    #this method tracks the overall time in the background to use when the cube is scrambled
    def clock(self,cube_status,dimen):
        total_time = pygame.time.get_ticks()
        output_time = total_time - self.start_time
        if self.check_solved(cube_status) == True & self.started == 1:
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
                self.started = 0
        elif self.check_solved(cube_status) == True & self.started == 0: 
                self.started = 1
                self.start_time = total_time
                output_time = total_time - self.start_time
                self.val_out = 2
        if self.check_solved(cube_status) == True & self.started == 2:
            self.started = 1
        if self.val_out == 1:
            self.movecount = 0
            return(int(self.end_time))
        elif self.val_out == 2:
            return(int(output_time))
        else:
            return(int(0))
    #this method puts the time returned from the clock method into the correct formatting and displays it on the screen  
    def timer(self,cube_status,dimen):
        time = self.clock(cube_status,dimen)
        ms = time % 1000
        seconds = (time // 1000) % 60
        minutes = (time//60000)
        output_string = "Time: {0:02}:{1:02}.{2:03}".format(minutes, seconds, ms)
        text = self.font.render(output_string, True, self.BLACK)
        dimen.blit(text, [20, 20])
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
        y_height = 450
        if len(self.sorted_time) > 0:
            text = self.font.render("Average of 12", True, self.BLACK)
            dimen.blit(text, [20, y_height])
            text = self.font.render("Fastest of 12", True, self.BLACK)
            dimen.blit(text, [20, y_height + 50])
            if self.avgof12 == 12:
                text = self.font.render(self.formatted_avgof12, True, self.BLACK)
                dimen.blit(text, [20, y_height + 25])
                text = self.font.render(self.fastestof12, True, self.BLACK)
                dimen.blit(text, [20, y_height + 75])
            else:
                text = self.font.render("DNF", True, self.BLACK)
                dimen.blit(text, [20, y_height + 25])
            text = self.font.render("Average of 5", True, self.BLACK)
            dimen.blit(text, [20, y_height + 100])
            text = self.font.render("Fastest of 5", True, self.BLACK)
            dimen.blit(text, [20, y_height + 150])
            if self.avgof12 >= 5:
                text = self.font.render(self.formatted_avgof5, True, self.BLACK)
                dimen.blit(text, [20, y_height + 125])
                text = self.font.render(self.fastestof5, True, self.BLACK)
                dimen.blit(text, [20, y_height + 175])
            else:
                text = self.font.render("DNF", True, self.BLACK)
                dimen.blit(text, [20, y_height + 125])
            for items in range(self.counter,0,-1):
                self.item+=1
                text = self.font.render(self.sorted_time[self.index - self.item], True, self.BLACK)
                dimen.blit(text, [960, (self.item*25)])
                if self.item > 10:
                    self.item = 10 

    def average(self,solve_time,movecount):
        self.rawtimes.append(solve_time)
        if self.avgof12 == 12:
            self.formatted_avgof12 = self.uniform_avg(12)[1]
            self.fastestof12 = self.uniform_avg(12)[0]
        if self.avgof12 >= 5:
            self.formatted_avgof5 = self.uniform_avg(5)[1]
            self.fastestof5 = self.uniform_avg(5)[0]

    def uniform_avg(self,ranges):
        avgtotal = 0
        averaged_values = []
        for solves in range(ranges):
            avgtotal = avgtotal + self.rawtimes[-solves]
            averaged_values.append(self.rawtimes[-solves])
        averaged_values = sorted(averaged_values)
        maxmin = averaged_values[0]+averaged_values[ranges-1]
        fastestinrange ="Time: {2:02}:{1:02}.{0:03}".format(self.time_formatter(averaged_values[0])[0],self.time_formatter(averaged_values[0])[1],self.time_formatter(averaged_values[0])[2])
        averaged_values.clear()
        avgtotal = avgtotal - maxmin
        avgtotal = avgtotal/(ranges-2)
        avgtotal = math.ceil(avgtotal)
        formatted_avg = "Time: {2:02}:{1:02}.{0:03}".format(self.time_formatter(avgtotal)[0],self.time_formatter(avgtotal)[1],self.time_formatter(avgtotal)[2])
        return[fastestinrange,formatted_avg]
    
    def time_formatter(self,time):
        ms = time % 1000
        seconds = (time // 1000) % 60
        minutes = (time//60000)
        return[ms,seconds,minutes]
    
    def movecounter(self, event):
        for key_name, move in self.key_mapping.items():
            key_code = getattr(pygame, key_name)
            if event.key == key_code:
                if "," in move:
                    self.movecount += 1
