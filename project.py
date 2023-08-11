import networkx as nx
import numpy
import math
import random
import sys
import time
import contextlib

def init (G, N):
    for player in G.nodes:
        p = random.random()                           #atributes of the players 
        q = random.random()
        G.nodes[player]["p"] = p                                 
        G.nodes[player]["q"] = q
        G.nodes[player]["play"] = 1
        
def play(G, generations, start_time, p_qAverageList, timeList, fairList, payoffAverageList, networkType, N, mutationError, lowOffersPenaltyFlag):
    if(networkType != "none"):   #network environment where each player only plays with its neighbours
        for i in range(generations):
            G.graph["payoff"] = numpy.zeros(N)                  #atributes of the graph
            G.graph["offerPayoffMatrix"] = numpy.zeros((N, N))
            G.graph["rewardPayoffMatrix"] = numpy.zeros((N, N))            
            print(i)
            fairCount = 0
            playCount = 0
            pSum = 0
            qSum = 0
            p_qList = []
            for player in G.nodes:                 #Ultimatum game plays
                p_qList.append([G.nodes[player]["p"], G.nodes[player]["q"]])
                pSum += G.nodes[player]["p"]
                qSum += G.nodes[player]["q"]
                for neighbor in G.neighbors(player):
                    playCount += 1
                    if(G.nodes[player]["p"] >= G.nodes[neighbor]["q"] and G.nodes[neighbor]["play"] == 1):
                        if(G.nodes[player]["p"] >= 0.4 and G.nodes[player]["p"] <= 0.5):
                            fairCount += 1
                        G.graph["offerPayoffMatrix"][player][neighbor] += 1 - G.nodes[player]["p"]
                        G.graph["rewardPayoffMatrix"][neighbor][player] += G.nodes[player]["p"]
                        
                        if(lowOffersPenaltyFlag == 1):
                            if(G.nodes[player]["p"] >= 0.1 and G.nodes[player]["p"] <= 0.2):
                                G.nodes[player]["play"] = 0
                                
            p_qAverageList.append([pSum/N, qSum/N])
                        
            totalPayoff = 0
            for player in G.nodes:         #update payoffs
                offerPayoff = 0
                rewardPayoff = 0
                for neighbor in G.neighbors(player):
                    offerPayoff += G.graph["offerPayoffMatrix"][player][neighbor]
                    rewardPayoff += G.graph["rewardPayoffMatrix"][player][neighbor]
                G.graph["payoff"][player] = offerPayoff + rewardPayoff
                totalPayoff += G.graph["payoff"][player]
            
            parentsPayoffPropotion = []
            indexList = []
            for player in G.nodes:                 #find most fittest players according to their payoffs 
                propotion = G.graph["payoff"][player]/totalPayoff
                parentsPayoffPropotion.append(propotion)
                indexList.append(player)
            
            payoffAverageList.append(totalPayoff/N)

            parentsIndexList = numpy.random.choice(indexList, N, p = parentsPayoffPropotion)
            node = 0
            for parent in parentsIndexList:                  #Natural selection
                pChild = random.uniform(p_qList[parent][0] - mutationError, p_qList[parent][0] + mutationError)
                if pChild < 0:
                    pChild = 0
                elif pChild > 1:
                    pChild = 1
                
                qChild = random.uniform(p_qList[parent][1] - mutationError, p_qList[parent][1] + mutationError)
                if qChild < 0:
                    qChild = 0
                if qChild > 1:
                    pChild = 1
                    
                G.nodes[node]["p"] = pChild                                 
                G.nodes[node]["q"] = qChild            
                node += 1
            
            t = math.log(float((time.time() - start_time)), 10)
            timeList.append(t)
            fairList.append(float(fairCount/playCount))    
    else:  #baseline environment where all players play with everyone else
        for i in range(generations):
            G.graph["payoff"] = numpy.zeros(N)                  #atributes of the graph
            G.graph["offerPayoffMatrix"] = numpy.zeros((N, N))
            G.graph["rewardPayoffMatrix"] = numpy.zeros((N, N))            
            print(i)
            fairCount = 0
            playCount = 0
            pSum = 0
            qSum = 0
            p_qList = []
            for player in G.nodes:              #Ultimatum game plays
                p_qList.append([G.nodes[player]["p"], G.nodes[player]["q"]])
                pSum += G.nodes[player]["p"]
                qSum += G.nodes[player]["q"]                
                for player2 in G.nodes:
                    if(player != player2):
                        playCount += 1
                        if(G.nodes[player]["p"] >= G.nodes[player2]["q"] and G.nodes[player2]["play"] == 1):
                            if(G.nodes[player]["p"] >= 0.4 and G.nodes[player]["p"] <= 0.5):
                                fairCount += 1
                            G.graph["offerPayoffMatrix"][player][player2] += 1 - G.nodes[player]["p"]
                            G.graph["rewardPayoffMatrix"][player2][player] += G.nodes[player]["p"]
                            
                            if(lowOffersPenaltyFlag == 1):
                                if(G.nodes[player]["p"] >= 0.1 and G.nodes[player]["p"] <= 0.2):
                                    G.nodes[player]["play"] = 0
            
            p_qAverageList.append([pSum/N, qSum/N])
            
            totalPayoff = 0             
            for player in G.nodes:                               #update payoffs
                offerPayoff = 0
                rewardPayoff = 0
                for player2 in G.nodes:
                    if(player != player2):
                        offerPayoff += G.graph["offerPayoffMatrix"][player][player2]
                        rewardPayoff += G.graph["rewardPayoffMatrix"][player][player2]
                G.graph["payoff"][player] = offerPayoff + rewardPayoff
                totalPayoff += G.graph["payoff"][player]
            
            payoffAverageList.append(totalPayoff/N)
            
            parentsPayoffPropotion = []
            indexList = []
            for player in G.nodes:                  #find most fittest players according to their payoffs  
                if(totalPayoff != 0):
                    propotion = G.graph["payoff"][player]/totalPayoff
                else:
                    propotion = 0
                parentsPayoffPropotion.append(propotion)
                indexList.append(player)
            
            if(lowOffersPenaltyFlag == 1):
                soma = 0
                for prob in parentsPayoffPropotion:
                    soma += prob                
                
                if(soma != 0):
                    parentsIndexList = numpy.random.choice(indexList, N, p = parentsPayoffPropotion)
                else:
                    parentsIndexList = []
            
            else:
                parentsIndexList = numpy.random.choice(indexList, N, p = parentsPayoffPropotion)
            
            node = 0
            for parent in parentsIndexList:           #Natural selection
                pChild = random.uniform(p_qList[parent][0] - mutationError, p_qList[parent][0] + mutationError)
                if pChild < 0:
                    pChild = 0
                elif pChild > 1:
                    pChild = 1
                
                qChild = random.uniform(p_qList[parent][1] - mutationError, p_qList[parent][1] + mutationError)
                if qChild < 0:
                    qChild = 0
                elif qChild > 1:
                    pChild = 1
                    
                G.nodes[node]["p"] = pChild                                 
                G.nodes[node]["q"] = qChild            
                node += 1
            
            t = math.log(float((time.time() - start_time)), 10)
            timeList.append(t)
            fairList.append(float(fairCount/playCount))            
            
def main(argv):      
    N = int(argv[0])
    m = int(argv[1])
    generations = int(argv[2])
    prob = float(argv[3])
    networkType = argv[4]
    mutationError = float(argv[5])
    lowOffersPenaltyFlag = int(argv[6])
    
    if(networkType == "none" or networkType == "ba"):
        G = nx.barabasi_albert_graph(N, m) # generating Albert Barabasi graph or baseline
    elif(networkType == "rand"):
        G = nx.fast_gnp_random_graph(N,prob) #generating Random graph
    elif(networkType == "wt"):
        G = nx.watts_strogatz_graph(N, m, prob) #generating Watts Strogatz graph
    
    init(G, N)
    start_time = time.time()
    timeList = []
    fairList = []
    p_qAverageList = []
    payoffAverageList = []
    play(G, generations, start_time, p_qAverageList, timeList, fairList, payoffAverageList, networkType, N, mutationError, lowOffersPenaltyFlag)
    
    
    print("Simulation Complete")
    
    file_path = 'p_qFile.txt'
    with open(file_path, "w") as o:
        with contextlib.redirect_stdout(o):
            for i in range(generations):
                print(str(i) + " " + str("{:.2f}".format(float(p_qAverageList[i][0]))) + " " + str("{:.2f}".format(float(p_qAverageList[i][1]))))    
    
    file_path2 = 'timeFile.txt'
    with open(file_path2, "w") as o:
        with contextlib.redirect_stdout(o):          
            for i in range(generations):
                print(str(i) +  " " + str("{:.3f}".format(float(timeList[i]))))
    
    file_path3 = 'fairFile.txt'
    with open(file_path3, "w") as o:
        with contextlib.redirect_stdout(o):          
            for i in range(generations):    
                print(str(i) +  " " + str("{:.2f}".format(float(fairList[i]))))
    
    file_path4 = 'payoffFile.txt'
    with open(file_path4, "w") as o:
        with contextlib.redirect_stdout(o):          
            for i in range(generations):    
                print(str(i) +  " " + str("{:.2f}".format(float(payoffAverageList[i]))))    
            
if __name__ == "__main__":
    main(sys.argv[1:])