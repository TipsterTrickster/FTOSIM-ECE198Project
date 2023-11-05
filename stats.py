import pygame
import pandas
pygame.init()
import os
import math
from FTO import FTO
from pathlib import Path




class statis():
    def __init__(self, FTO):
        self.fto = FTO

        self.font = pygame.font.Font(None, 40)
        self.start_time = 0 #triggers when an attempt is started to grab the current time as a 0 point
        self.end_time = 0 #triggers when a solve is completed as the difference between current time and start time
        self.started = 0 #used to flip between the timer running and timer stopped states
        self.val_out = 0 #based on the the flip state, dictates what is actually returned from the clock method
        self.sorted_time = [] #list of times from previous solves
        self.rawtimes = []
        self.moveslist = []
        self.fastestof12list = []
        self.movesof12list = []
        self.fastestof12 = 0
        self.formatted_avgof12 = 0
        self.fastestof5 = 0
        self.fastestof5list = []
        self.movesof5list = []
        self.formatted_avgof5 = 0
        self.fastestoverall = 0
        self.item = 0 #iterates through for the number of items in the sorted_time list, determines how they're displayed on the screen
        self.counter = 0 #counts how many items are in the completed run list to keep that at 10 or below
        self.avgof12 = 0
        self.avgof5 = 0
        self.index = 0 #counts the number of attempts for every time a new one is added to the list and numbers the times on the display
        self.movecount = 0
        self.data_array = {"Time":[],"Moves":[],"Reconstruction":[]}


        self.scramble = [] # stores scramble for reconstruction
        self.solution = [] # stores solution for reconstruction
        self.reconstruction = "https://alpha.twizzle.net/explore/?puzzle=FTO&alg="
  

    def check_solved(self,cube_status):
        for i in range(len(cube_status)):
            for x in range(len(cube_status[i])):
                if cube_status[i][0] != cube_status[i][x]:
                    return False
        return True
    
    #this method tracks the overall time in the background to use when the cube is scrambled
    def clock(self,cube_status,dimen):
        # self.fto.scrambled = True # uncomment to test without having to scramble and solve
        total_time = pygame.time.get_ticks()
        output_time = total_time - self.start_time

        if self.started == 0: # controls function will change self.started to 1
            self.start_time = total_time # constantly update starttime
            return self.end_time
        elif self.check_solved(self.fto.state) == False and self.started == 1:
            output_time = total_time - self.start_time 
            return output_time
        elif self.check_solved(self.fto.state) == True and self.started == 1:
                self.end_time = output_time
                self.counter += 1
                if self.counter > 10:
                    self.counter = 10
                self.avgof12 += 1
                if self.avgof12 > 12:
                    self.avgof12 = 12
                self.leaderboard(self.end_time,self.movecount)
                self.average(self.end_time, self.movecount)  
                self.movecount = 0
                self.started = 0
                self.fto.scrambled = False
                return self.end_time
        elif self.started == 2:
                self.fto.size = 3
                self.movecount = 0
                self.started = 0
                self.fto.scrambled = False
                return 0

        else:
            return self.end_time
    
    #this method puts the time returned from the clock method into the correct formatting and displays it on the screen  
    def timer(self,cube_status,dimen):
        time = self.clock(cube_status,dimen)
        ms = time % 1000
        seconds = (time // 1000) % 60
        minutes = (time//60000)
        output_string = "Time: {0:02}:{1:02}.{2:03}".format(minutes, seconds, ms)
        text = self.font.render(output_string, True, "Black")
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
        for move in self.scramble:
            self.reconstruction += move[-1]
            self.reconstruction += move[0].lower()
            if "BR" in move or "BL" in move:
                self.reconstruction += move[1].lower()
            if "p" in move:
                self.reconstruction += "%27"
            self.reconstruction += "+"
        self.reconstruction += "%2F%2F+scramble+%0A%0A"

        for move in self.solution:
            if "T" in move:
                self.reconstruction += move[0]
            elif "o" in move:
                self.reconstruction += move[0]
                self.reconstruction += "v"
            else:
                self.reconstruction += move[-1]
                self.reconstruction += move[0].lower()
                if "BR" in move or "BL" in move:
                    self.reconstruction += move[1].lower()

            if "p" in move:
                self.reconstruction += "%27"
            self.reconstruction += "+"

        self.data_array["Reconstruction"].append(self.reconstruction)
        # self.data_array["Solution"].append(' '.join(self.solution))
        df = pandas.DataFrame(self.data_array)
        df.to_csv(os.path.join(r'solve_data.csv')) 
        printed = "{3:01}. {0:02}:{1:02}.{2:03} | {4:01} Moves".format(minutes,seconds,ms,self.index,movecount)
        self.sorted_time.append(printed) 
        pass
    
    #this method takes the list of previous times from the leaderboard method and actually renders them on the screen. I didn't combine the two because
    #I wanted a shorter method for actually rendering them since this has to be called hundreds of times per second to refresh it on the screen since the screen has to be refreshed
    #I assumed a longer method might take longer to run through and there could be other issues with running through certain lines so many times, especially if no new time is being input
    def print(self,dimen):
        self.item = 0
        y_height = 475
        ranges = [5,12]
        count = 0
        for number in ranges:
            for i in range(len(ranges)):
                titles = ["Average of {0}".format(number),"Fastest of {0}".format(number)]
                text = self.font.render(titles[i], True, "Black")
                dimen.blit(text, [20, y_height+(50*count)])
                count += 1
        text = self.font.render("Fastest Overall Time", True, "Black")
        dimen.blit(text, [20, y_height - 50])
        if len(self.sorted_time) > 0:
            text = self.font.render(self.fastestoverall, True, "Black")
            dimen.blit(text, [20, y_height - 25])
            if self.avgof12 >= 5:
                text = self.font.render(self.formatted_avgof5, True, "Black")
                dimen.blit(text, [20, y_height + 25])
                text = self.font.render(self.fastestof5, True, "Black")
                dimen.blit(text, [20, y_height + 75])
            else:
                text = self.font.render("DNF", True, "Black")
                dimen.blit(text, [20, y_height + 25])

            if self.avgof12 == 12:
                text = self.font.render(self.formatted_avgof12, True, "Black")
                dimen.blit(text, [20, y_height + 125])
                text = self.font.render(self.fastestof12, True, "Black")
                dimen.blit(text, [20, y_height + 175])
            else:
                text = self.font.render("DNF", True, "Black")
                dimen.blit(text, [20, y_height + 125])
            for items in range(self.counter,0,-1):
                self.item+=1
                text = self.font.render(self.sorted_time[self.index - self.item], True, "Black")
                dimen.blit(text, [960, (self.item*25)])
                if self.item > 10:
                    self.item = 10 

    def average(self, solve_time, movecount):
        avg1 = 12
        avg2 = 5
        self.rawtimes.append(solve_time)
        self.moveslist.append(movecount)
        self.fastestoverall = self.uniform_avg(self.rawtimes,self.moveslist,len(self.rawtimes))[0]
        if self.avgof12 == avg1:
            avgof12 = self.uniform_avg(self.rawtimes[-avg1:],self.moveslist[-avg1:],avg1)
            self.formatted_avgof12 = avgof12[1]
            self.fastestof12list.append(avgof12[2])
            self.movesof12list.append(avgof12[3])
            resultsfor12 = self.pairs(self.fastestof12list,self.movesof12list,len(self.fastestof12list))
            fastest12time = resultsfor12[3]
            self.fastestof12 = "Time: {2:02}:{1:02}.{0:03} | {3} Avg Moves".format(self.time_formatter(fastest12time)[0],self.time_formatter(fastest12time)[1],self.time_formatter(fastest12time)[2],resultsfor12[0])
        if self.avgof12 >= avg2:
            avgof5 = self.uniform_avg(self.rawtimes[-avg2:],self.moveslist[-avg2:],avg2)
            self.formatted_avgof5 = avgof5[1]
            self.fastestof5list.append(avgof5[2])
            self.movesof5list.append(avgof5[3])
            resultsfor5 = self.pairs(self.fastestof5list,self.movesof5list,len(self.fastestof5list))
            fastest5time = resultsfor5[3]
            self.fastestof5 = "Time: {2:02}:{1:02}.{0:03} | {3} Avg Moves".format(self.time_formatter(fastest5time)[0],self.time_formatter(fastest5time)[1],self.time_formatter(fastest5time)[2],resultsfor5[0])


    def uniform_avg(self,times,moves,ranges):
        avgtotal = 0
        avgmoves = 0
        averaged_times = []
        movesinrange = []
        for solves in range(ranges):
            avgtotal = avgtotal + times[-solves]
            avgmoves = avgmoves + moves[-solves]
            averaged_times.append(times[-solves])
            movesinrange.append(moves[-solves])
        results = self.pairs(averaged_times,movesinrange,ranges)
        slowesttimemoves = results[1]
        fastesttimemoves = results[0]
        if ranges > 2:
            avgmoves = avgmoves - slowesttimemoves - fastesttimemoves
            avgmoves = avgmoves/(ranges-2)
            avgmoves = math.ceil(avgmoves)
            avgtotal = avgtotal - results[2]
            avgtotal = avgtotal/(ranges-2)
            avgtotal = math.ceil(avgtotal)
        fastestinrange ="Time: {2:02}:{1:02}.{0:03} | {3} Moves".format(self.time_formatter(results[3])[0],self.time_formatter(results[3])[1],self.time_formatter(results[3])[2],fastesttimemoves)
        formatted_avg = "Time: {2:02}:{1:02}.{0:03} | {3} Avg Moves".format(self.time_formatter(avgtotal)[0],self.time_formatter(avgtotal)[1],self.time_formatter(avgtotal)[2],avgmoves)
        averaged_times.clear()
        movesinrange.clear()
        return[fastestinrange,formatted_avg,avgtotal,avgmoves]
        
    def time_formatter(self,time):
        ms = time % 1000
        seconds = (time // 1000) % 60
        minutes = (time//60000)
        return[ms,seconds,minutes]
    
    def pairs(self,timelist,moveslist,ranges):
        pairslist = []
        pairslist.append(timelist)
        pairslist.append(moveslist)
        timelist = sorted(timelist)
        fastesttime = 0
        for i in range(ranges):
            if pairslist[0][i-1] == timelist[0]:
                fastesttimemoves = pairslist[1][i-1]
                break
        for i in range(ranges):
            if pairslist[0][i-1] == timelist[-1]:
                slowesttimemoves = pairslist[1][i-1]
                break
        fastesttime = timelist[0]
        maxmin = timelist[0] + timelist[-1]
        pairslist.clear()
        timelist.clear()
        return[fastesttimemoves, slowesttimemoves, maxmin, fastesttime]
