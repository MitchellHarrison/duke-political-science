#
 # Copyright (c) 2021, David A Siegel
 # All rights reserved.
 #
 # Redistribution and use in source and binary forms, with 
 # or without modification, are permitted provided that the following 
 # conditions are met:
 #
 #	 Redistributions of source code must retain the above copyright notice,
 #	 this list of conditions and the following disclaimer.
 #
 #	 Redistributions in binary form must reproduce the above copyright notice,
 #	 this list of conditions and the following disclaimer in the documentation
 #	 and/or other materials provided with the distribution.
 #
 #	 Proper citation to the corresponding AJPS paper should be made if code
 #   is used to enact method of sequential parameter sweeping (SPS). 
 #
 # The name of David A Siegel may not be otherwise used to endorse or promote
 # products derived from this software without specific prior written permission.
 #
 # THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER
 # ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 # LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
 # PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
 # BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 # EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 # PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 # PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 # LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 # NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
 # EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 #

import math
import numpy as np
from os.path import exists

#Utility functions
def revperCalc(agentList,revList,rabbleList):	#Calculates the percentage of people with rev=1 and # rabble-rousers (b>=1)
    if len(agentList)>0: 
        rv=len(revList)/len(agentList)
        rb=len(rabbleList)/len(agentList)
    else:
        rv=0.0
        rb=0.0
    return [rv,rb]

def stdevCalc(vec, mn, rns):  #Standard Deviation of vectors across runs calculator
	vari = 0
	rs = rns
	for i in range(rns):	#only include actual numbers, not NaN
		if vec[i]>-1000000 and vec[i]<1000000: vari = vari + (vec[i] - mn)**2
		else: rs-=1
	if rs>1: vari = math.sqrt(vari /(rs-1))
	else: vari=0
	return vari

#Reads input file into parameter matrix. Looks for file BurInput.txt in same folder
#The first five lines of this file contain single values
#The next three contain three numbers for loop settings (initial final step_size) or random number generation (lower_bound upper_bound number_runs)
#All numbers of runs are multiplied together to yield total number of runs in latter case
def ReadParams(): #Reads input file into parameter list and sets output file names
    #Parameter arrays from input
    params1 = np.zeros(6)
    params = np.zeros((9,3))
    param = list()             #Stores all parameters from input file
    #opens output file; will quit if file is not found
    try: fin = open("BurInput.txt")
    except: 
        print('Input File Not Found')
        quit()
    for line in fin:
        words=line.split()
        ps=list()
        for word in words:
            try: ps.append(float(word))
            except: break
        param.append(ps)
    fin.close()

    #transfers parameters into arrays and checks to ensure parameters chosen won't loop infinitely
    # CHANGED: ensure additional parameter was accounted for in this loop
    if len(param)!=13: 
        print("Incorrect Number of Parameters in Input File")
        quit()
    i = 0
    for ps in param:
        if i<5 and len(ps)==1: params1[i+1]=int(ps[0])
        elif i<5:
            print("Incorrect Number of Parameters in Input File")
            quit()
        elif len(ps)==3:
            #check to see if the step size will result in an infinite loop
            if ps[2]<=0: 
                print("Improper Step Size")
                quit()
            params[i-4][0]=ps[0]
            params[i-4][1]=ps[1]
            params[i-4][2]=ps[2]
        else:
            print("Incorrect Number of Parameters in Input File")
            quit()
        i+=1

    #create and open for appendix main output file
    outFile = "bur-out.csv"
    if exists(outFile):
        i=1
        outFile="bur-out-"+str(i)+".csv"
        while exists(outFile):
            i+=1
            outFile="bur-out-"+str(i)+".csv"

    #If data per period is saved and printed, then create second output file
    if params1[3]==1:
        outpFile = "bur-period-out.csv"
        if exists(outpFile):
            i=1
            outpFile="bur-period-out-"+str(i)+".csv"
            while exists(outpFile):
                i+=1
                outpFile="bur-period-out-"+str(i)+".csv"
    else:
        outpFile=None
    return [outFile,outpFile, params1, params]

def initSettings():	#set model parameters that are not looped and prints them to output file
    #Parameters set at start that don't vary
    periodsEnd=int(params1[1]) #Ends the periods at number periodsEnd
    runs=int(params1[2])	#number of times each set of parameters is tested					
    printPeriodData=int(params1[3]) #Whether or not to output (and save in program--memory intensive) all periods to file
    printEveryNPeriods=int(params1[4]) #How Often to print by period data 
    dataTakingForm=int(params1[5]) #Whether to loop over parameters (0), pick random points (1), or take partial derivatives at random points (2)
    fout.write("periodsEnd,"+"runs,"+"printPeriodData,"+"printEveryNPeriods,"+"dataTakingForm\n")
    fout.write(str(periodsEnd)+",")
    fout.write(str(runs)+",")
    fout.write(str(printPeriodData)+",")
    fout.write(str(printEveryNPeriods)+",")
    fout.write(str(dataTakingForm)+"\n")
    if printPeriodData==1:
        foutp.write("periodsEnd,"+"runs,"+"printPeriodData,"+"printEveryNPeriods,"+"dataTakingForm\n")
        foutp.write(str(periodsEnd)+",")
        foutp.write(str(runs)+",")
        foutp.write(str(printPeriodData)+",")
        foutp.write(str(printEveryNPeriods)+",")
        foutp.write(str(dataTakingForm)+"\n")
    return [periodsEnd, runs, printPeriodData,printEveryNPeriods, dataTakingForm]

#Initializes agent population and lists
def addInitialNodes(): 		#Initialize Population

	#lists of agents
    agentList = list()		#List of all people
    revList = list()		#List of people w/ rev=1
    rabbleList = list()		#List of people w/ b>1

    #initialize internal variables for each run
    revper=0    			#percent of population with rev=1 each period
    timetoEq=0  			#time until equilibrium
    totalb=0    			#sum of b for all nodes, used for bureaucratic application of economic interventions
    # CHANGED: add total_d
    total_d = 0
    maxb=-1000     			#largest b in the population
    # CHANGED: implement maximum external influence d
    max_d = -1000
    eqRev=0     			#equilibrium participation level
    rabbleRousers=0     	#percent of population who are rabble-rousers in each period

    #Create list of individuals
    personcounter=0 		#counter for setting personNum
    #Create lists
    while personcounter<N:
        #Set node properties
        #A node is a list of properties: personcounter, b, c, rev, lastrev
        #Could also do this with objects but that slows down code somewhat
        b=np.random.normal(loc=bmean, scale=bstdev, size=None) #set internal motivation
        # CHANGED: add distribution for external influence
        d = np.random.normal(loc = ext_mean, scale = ext_std_dev, size = None)
        c = -1 	#everyone starts off with minimum external motivation
        if b+c>0: rev=1 #decision is if b+c>0, then participate
        # CHANGED: if external pressures are effective, act.
        elif d + c > 0: rev = 1
        else: rev=0
        lastrev=rev
        #create node with those properties
        node = [personcounter, b, c, rev, lastrev, d]
        #add to lists
        agentList.append(node)
        if rev==1: revList.append(node)
        if b>1: rabbleList.append(node)
        #keep track of totalb and max b
        totalb+=b
        # CHANGED: keep track of total d and max d
        total_d += d
        if b>maxb: maxb=b
        # CHANGED: set max_d if over max
        if d > max_d: max_d = d
        personcounter+=1
    return [[agentList,revList,rabbleList],[revper, timetoEq, totalb, maxb, eqRev, rabbleRousers]]

#Routine changes b according to economic intervention
#Incorporates both intervention and the bureaucracy that acts on it
def bInt(totalb, maxb, agentList, rabbleList):
    bav = totalb/len(agentList)	    #average b value in population
    eqbC = econInt/len(agentList) 	#size of equal economic interventions for all
    if burFear==0:	#if bureaucracies always operate according to:
        #rule for adjusting with bureaucracy is that the higher one's b is above average, the relatively more adjustment one gets
                    #stronger bureaucracies can apply this more, while weaker ones do this relatively less, as opposed to just applying adjustment equally
        for node in agentList: #Figure out how much intervention to apply to each person and apply it
            node[1] -= eqbC*((1-burStr)*1+burStr*(node[1]/bav)) #adjust b downward
            if node[1]<1 and node in rabbleList: rabbleList.remove(node) 
    elif burFear==1: #if bureaucracies operate according to above rule only if not afraid:
        burOpChance = 1.0/(math.exp(2*(maxb-bmean)))	#chance bureaucracy operates depends on how far maximum observed dissatisfaction (maxb) is from mean b (bmean)
        if np.random.uniform(low=0.0, high=1.0, size=None)<burOpChance:
            for node in agentList:	#Figure out how much intervention to apply to each person and apply it
                node[1] -= eqbC*((1-burStr)*1+burStr*(node[1]/bav)) #adjust b downward
                if node[1]<1 and node in rabbleList: rabbleList.remove(node) 
                else:	#Apply equal intervention
                    for node in agentList:
                        node[1] -= eqbC #adjust b downward
                if node[1]<1 and node in rabbleList: rabbleList.remove(node) 

#Routine collects all data and stores it in arrays 
def dataGather(pd, rn, done, revper, rabbleRousers, timetoEq, eqRev, dataList):
    [revperpp, revperm, eqrevpp, eqrevm, timetoEqpp, timetoEqm, rabbleRouserspp, rabbleRousersm]=dataList
    #Compute measures that only need to be computed at beginning, end, or if all periods are printed
    if pd==0 or done or printPeriodData==1:
        pds=pd
        if done and printPeriodData==0: pds=1
        revperpp[pds][rn]=revper			#percent of population with rev=1 each period
        revperm[pds]+=revper/runs			#Mean percent of population with rev=1
        eqrevpp[pds][rn]=eqRev			    #Equilibrium percent of population with rev=1 each period
        eqrevm[pds]+=eqRev/runs				#Mean Equilibrium percent of population with rev=1
        timetoEqpp[pds][rn]=timetoEq		#Time to Equilibrium by period
        timetoEqm[pds]+=timetoEq/runs		#Time to Equilibrium, meaned
        rabbleRouserspp[pds][rn]=rabbleRousers	#percent of population who are rabble-rousers in each period, per period
        rabbleRousersm[pds]+=rabbleRousers/runs	#Mean percent of population who are rabble-rousers in each period, per period
    if done and printPeriodData==1:	        #if done and printing all data, fill in rest
        j=pd+1
        while j<=periodsEnd:
            revperpp[j][rn]=revper			#percent of population with rev=1 each period
            revperm[j]+=revper/runs			#Mean percent of population with rev=1
            eqrevpp[j][rn]=eqRev			#Equilibrium percent of population with rev=1 each period
            eqrevm[j]+=eqRev/runs			#Mean Equilibrium percent of population with rev=1
            timetoEqpp[j][rn]=timetoEq		#Time to Equilibrium by period
            timetoEqm[j]+=timetoEq/runs		#Time to Equilibrium, meaned
            rabbleRouserspp[j][rn]=rabbleRousers    #percent of population who are rabble-rousers in each period, per period
            rabbleRousersm[j]+=rabbleRousers/runs	#Mean percent of population who are rabble-rousers in each period, per period
            j+=1

#Prints all the data
def printData(marker, dataList):
    [revperpp, revperm, eqrevpp, eqrevm, timetoEqpp, timetoEqm, rabbleRouserspp, rabbleRousersm]=dataList
    pds=1
    if (printPeriodData==1): pds=periodsEnd
    fout.write(str(marker)+",")
    fout.write(str(N)+","+str(bmean)+","+str(bstdev)+","+str(econInt)+","+str(burStr)+","+str(burFear)+",")
    fout.write(str(revperm[pds])+","+str(stdevCalc(revperpp[pds],revperm[pds],runs))+",")
    fout.write(str(eqrevm[pds])+","+str(stdevCalc(eqrevpp[pds],eqrevm[pds],runs))+",")
    fout.write(str(timetoEqm[pds])+","+str(stdevCalc(timetoEqpp[pds],timetoEqm[pds],runs))+",")
    fout.write(str(rabbleRousersm[pds])+","+str(stdevCalc(rabbleRouserspp[pds],rabbleRousersm[pds],runs))+"\n")
    if (printPeriodData==1):
        foutp.write("Marker,N,bmean,bstdev,")
        foutp.write("econInt,"+"burStr,"+"burFear,")
        foutp.write("Period,"+"Mean_Percent_Acting,"+"StDev_Percent_Acting,"+
                    "Mean_Eq_Percent_Acting,"+"StDev_Eq_Percent_Acting,"+
                    "Mean_Time_to_Equilibrium,"+"StDev_Time_to_Equilibrium,"+
                    "Mean_Time_from_Start_to_End_of_Action,"+"StDev_Time_from_Start_to_End_of_Action,"+
                    "Mean_%_Population_Who_Are_Rabble-Rousers,"+"StDev_%_Population_Who_Are_Rabble-Rousers\n")
        pd = 0
        while pd<=periodsEnd:
            if pd%printEveryNPeriods==0:
                foutp.write(str(marker)+",")
                foutp.write(str(N)+","+str(bmean)+","+str(bstdev)+",")
                foutp.write(str(econInt)+","+str(burStr)+","+str(burFear)+",")
                foutp.write(str(pd)+",")
                foutp.write(str(revperm[pd])+","+
                            str(stdevCalc(revperpp[pd],revperm[pd],runs))+",")
                foutp.write(str(eqrevm[pd])+","+
                            str(stdevCalc(eqrevpp[pd],eqrevm[pd],runs))+",")
                foutp.write(str(timetoEqm[pd])+","+
                            str(stdevCalc(timetoEqpp[pd],timetoEqm[pd],runs))+",")
                foutp.write(str(rabbleRousersm[pd])+","+str(stdevCalc(rabbleRouserspp[pd],rabbleRousersm[pd],runs))+"\n")

#Main routine for simulation runs for each given set of parameter values
# Order of Events:
# 0) (Not repeated) Apply economic intervention once
# Repeat following:
# 1) Simultaneously update c based on last period's actions 
# 2) Simultaneously update rev based on new c
# 3) Aggregate data taken (revper calc)

def ModelRun(marker): #Operations that occur in every period
    #Initialize data gathering matrices
    dataSize=2          	#if printing only end period, only save initial and end period to cut down on memory use
    if printPeriodData==1: dataSize=periodsEnd+1
    revperpp = np.zeros((dataSize,runs))	#percent of population with rev=1 each period
    revperm = np.zeros(dataSize)		#Mean percent of population with rev=1
    eqrevpp	= np.zeros((dataSize,runs))		#Equilibrium percent of population with rev=1 each period
    eqrevm = np.zeros(dataSize)			#Mean Equilibrium percent of population with rev=1
    timetoEqpp = np.zeros((dataSize,runs))	#Time to Equilibrium by period
    timetoEqm = np.zeros(dataSize)		#Time to Equilibrium, meaned
    rabbleRouserspp = np.zeros((dataSize,runs))	#percent of population who are rabble-rousers in each period, per period
    rabbleRousersm = np.zeros(dataSize)	#Mean percent of population who are rabble-rousers in each period, per period
    dataList = [revperpp, revperm, eqrevpp, eqrevm, timetoEqpp, 
                timetoEqm, rabbleRouserspp, rabbleRousersm]

    for rn in range(runs):
        done=False
        #Initialize agent lists and internal variables
        [pl,intern] = addInitialNodes()
        [agentList, revList,rabbleList]=pl
        [revper, timetoEq, totalb, maxb, eqRev, rabbleRousers]=intern
        #revper; needed for cUpdate and data collection
        [revper, rabbleRousers]=revperCalc(agentList,revList,rabbleList) 
        #Apply economic intervention
        bInt(totalb, maxb, agentList, rabbleList) 					    
        #Gather initial period's data
        dataGather(0, rn, done, revper, rabbleRousers, 
                   timetoEq, eqRev, dataList)	    
        for i in range(periodsEnd):
            pd=i+1

            #Code block for updating c and making decisions
            #Everyone decides what action to take at same time
            #then updates lastrev for each node
            #gets number of agents to avoid calling len function repeatedly
            agentnum = len(agentList) 
            for node in agentList:
                #Calc individuals' c, correcting for own behavior
                node[2] = (revper*agentnum-node[3])/(agentnum-1)-1
                #make action decision
                # CHANGED: add "or" statement to accound for ext pressures
                if node[1]+node[2]>0 or node[2] + node[5] > 0: #if over threshold, act
                    node[3] = 1
                    if node[4]==0: revList.append(node)	#if not already in revList, then add if part 2 periods in row
                else:
                    node[3] = 0 #otherwise do not
                    if node[4]==1: revList.remove(node)	#remove from revList
                #update last-period placeholder
                node[4]=node[3]

            #if no change in outcome for 50 periods or no one left is 
            #participating or end of runs is set,
            #fill in rest of data with values from this period
            if timetoEq>50 or len(agentList)==0 or pd==periodsEnd: done=True
            #revper; needed for cUpdate and data collection
            [revper, rabbleRousers]=revperCalc(agentList,revList,rabbleList) 
            if timetoEq <50: 	    #Dual-purpose: checks to see if revper hasn't
                if revper != eqRev: #changed for 50 consecutive periods
                    eqRev = revper	#then, once it hasn't, set time to equilibrium
                    timetoEq=1
                else: timetoEq+=1
            elif timetoEq==50: timetoEq = pd
            dataGather(pd, rn, done, revper, rabbleRousers, 
                       timetoEq, eqRev, dataList)	#Gather data
            if (done): break
    printData(marker, dataList)

#**************Main code begins*****************
#Read input parameters and set output files
[outf1, outf2, params1, params]=ReadParams() 
#open output files for writing
fout = open(outf1,"a")
if outf2!=None: foutp = open(outf2,"a")
[periodsEnd, runs, printPeriodData,printEveryNPeriods,
 dataTakingForm]=initSettings()  #Set non-looping parameters

#Print headers for main output file
fout.write("Marker,N,bmean,bstdev,")
fout.write("econInt,"+"burStr,"+"burFear,")
fout.write("Mean_Percent_Acting,"+"StDev_Percent_Acting,")
fout.write("Mean_Eq_Percent_Acting,"+"StDev_Eq_Percent_Acting,")
fout.write("Mean_Time_to_Equilibrium,"+"StDev_Time_to_Equilibrium,")
fout.write("Mean_%_Population_Who_Are_Rabble-Rousers,"+
           "StDev_%_Population_Who_Are_Rabble-Rousers\n")
marker=1	#marker delineates different parameter settings for convenience

#loop or randomize over all xx parameters depending on inputs
if dataTakingForm==0:			#if looping over parameters
    #initial parameter values, with one while loop for each
    i1=params[1][0]
    while i1<=params[1][1]:
        i2=params[2][0]
        while i2<=params[2][1]:
            i3=params[3][0]
            while i3<=params[3][1]:
                i4=params[4][0]
                while i4<=params[4][1]:
                    i5=params[5][0]
                    while i5<=params[5][1]:
                        i6=params[6][0]
                        while i6<=params[6][1]:
                            # CHANGED: added inner loops for new parameters
                            i7 = params[7][0]
                            while i7 <= params[7][1]:
                                i8 = params[8][0]
                                while i8 <= params[8][1]:
                                    #Set parameter values for each run
                                    N=i1			#number of people
                                    bmean=i2		#mean of internal motivation dist
                                    bstdev=i3		#stdev of internal motivation dist
                                    econInt=i4		#total economic intervention to be split up among individuals according to strength of bureaucracy
                                    burStr=i5		#strength of the bureaucracy determines how economic intervention is distributed throughout population
                                    burFear=i6		#0 if bureaucrats always do their jobs 1 if there is a chance they don't

                                    # CHANGED: mean and std. deviation of external motivation distribution
                                    ext_mean = i7
                                    ext_std_dev = i8
                                    
                                    #Do runs
                                    ModelRun(marker)
                                    marker+=1
                                    i8 += params[8][2]
                                i7 += params[7][2]
                            i6+=params[6][2]
                        i5+=params[5][2]
                    i4+=params[4][2]
                i3+=params[3][2]
            i2+=params[2][2]
        i1+=params[1][2]
    #end looping loop
else:							#Does one big loop, choosing random params
    totalruns = 1				#Calculates total parameter sets to test
    for i in range(6): totalruns*=params[i+1][2] #Each set is repeated "runs" times
    for tr in range(totalruns):
        i1=np.random.uniform(low=params[1][0], high=params[1][1], size=None)
        i2=np.random.uniform(low=params[2][0], high=params[2][1], size=None)
        i3=np.random.uniform(low=params[3][0], high=params[3][1], size=None)
        i4=np.random.uniform(low=params[4][0], high=params[4][1], size=None)
        i5=np.random.uniform(low=params[5][0], high=params[5][1], size=None)
        i6=np.random.uniform(low=params[6][0], high=params[6][1], size=None)
        i7=np.random.uniform(low=params[7][0], high=params[7][1], size=None)
        i8=np.random.uniform(low=params[8][0], high=params[8][1], size=None)

        # set parameter values for run
        N=i1				#number of people
        bmean=i2			#mean of internal motivation dist
        bstdev=i3			#stdev of internal motivation dist
        econInt=i4			#total economic intervention to be split up among 
                            #individuals according to strength of bureaucracy

        burStr=i5			#strength of the bureaucracy determines how economic 
                            #intervention is distributed throughout population

        burFear=i6			#0 if bureaucrats always do their jobs 1 if there is
                            #a chance they don't

        # CHANGED: additional variables for new parameters
        ext_mean = i7
        ext_std_dev = i8

        #Do runs
        ModelRun(marker)
        marker+=1
#close output files
fout.close()
if outf2!=None: foutp.close()
