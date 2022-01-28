import os
import pandas
import time


def CalculerEMA(closingData, period) :
    listEMA = [0] * (period - 1)
    valueSMA = sum(closingData[:period]) / period
    listEMA.append(valueSMA)
    k = 2 / (period + 1)
    for i in range(period, len(closingData)) :
        valueEMA = (closingData[i] * k) + (listEMA[i-1] * (1 - k))
        listEMA.append(valueEMA)
    return listEMA


def CalculerPositions(listEMAi, listEMAj, hysteresis, tri = 1) :
    listPositions = []
    for i in range(len(listEMAi)) :
        if (listEMAi[i] > listEMAj[i] * (1 + hysteresis)) :
            listPositions.append('ACHETER')
        elif (listEMAi[i] < listEMAj[i] * (1 - hysteresis)) :
            listPositions.append('VENDRE')
        else :
            if (len(listPositions) == 0) :
                listPositions.append('ATTENDRE')
            else :
                listPositions.append(listPositions[i-1])
    if tri :
        listPositions = TrierPositions(listPositions)
    return listPositions


def TrierPositions(listPositions) :
    for i in range(len(listPositions)-1, 0, -1) :
        if (listPositions[i] == listPositions[i-1]) :
            listPositions[i] = 'NONE'
    return listPositions


def CalculerScore(closingData, listPositions) :
    score = 1
    buyPrice = closingData[0]
    sellPrice = 0
    for i in range(len(listPositions)) :
        if (listPositions[i] == 'BUY') :
            buyPrice = closingData[i]
        elif (listPositions[i] == 'SELL') & (buyPrice != 0) :
            sellPrice = closingData[i]
            score = (sellPrice / buyPrice) * score
            buyPrice = 0
            sellPrice = 0
    if (buyPrice != 0) & (sellPrice == 0) :
        sellPrice = closingData[-1]
        score = (sellPrice / buyPrice) * score
    return score


def AnalyserValeursHistoriques(symbol, dateStart) :
    filePath = os.getcwd() + '\\data\\' + symbol + '\\' + dateStart.replace('/', '-') + '_3Y.txt'
    dataFrame = pandas.read_csv(filePath, sep=';', names=['Date', 'Ouverture', 'Cloture'])[::-1]
    pandas.to_numeric(dataFrame['Ouverture'])
    pandas.to_numeric(dataFrame['Cloture'])

    closingData = dataFrame['Ouverture'].tolist()
    bestParameters = [0, 0, 0, 0] # Période i, Période j, Score PTF

    startTime = time.time()

    for i in range(10, 150, 10) :           # j >= i, donc si EMA(i) > EMA(j) : croissance
        for j in range(i+10, 150, 10) :     #              si EMA(i) < EMA(j) : décroissance
            for k in range(1, 51) :
                hysteresis = 0.0001 * k
                listEMAi = CalculerEMA(closingData, i)
                listEMAj = CalculerEMA(closingData, j)
                listPositions = CalculerPositions(listEMAi[150:], listEMAj[150:], hysteresis)
                score = CalculerScore(closingData[150:], listPositions)
                if (score > bestParameters[3]) :
                    bestParameters = [i, j, k, score]
    # print(bestParameters, (time.time() - startTime))
    # print(len(listEMAi), len(listEMAj), len(listPositions))
    return bestParameters[0], bestParameters[1], bestParameters[2]

""" with open('ListeSymboles.txt', 'r') as file :
    lines = file.readlines()
    for line in lines :
        symbole = line.strip().split(';')[1]
        print(symbole, end='')
        AnalyserValeursHistoriques(symbole, '01/01/2016') """
