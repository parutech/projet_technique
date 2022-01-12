import os
import pandas


def CalculerEMA(closingData, period) :
    listEMA = [0] * (period - 1)
    valueSMA = sum(closingData[:period]) / period
    listEMA.append(valueSMA)
    k = 2 / (period + 1)
    for i in range(period, len(closingData)) :
        valueEMA = (closingData[i] * k) + (listEMA[i-1] * (1 - k))
        listEMA.append(valueEMA)
    return listEMA


def CalculerPositions(listEMAi, listEMAj, hysteresis) :
    listPositions = []
    for i in range(len(listEMAi)) :
        if (listEMAi[i] > listEMAj[i] * (1 + hysteresis)) :
            listPositions.append('BUY')
        elif (listEMAi[i] < listEMAj[i] * (1 - hysteresis)) :
            listPositions.append('SELL')
        else :
            listPositions.append(listPositions[i])
    listPositions = TrierPositions(listPositions)
    return listPositions


def TrierPositions(listPositions) :
    for i in range(len(listPositions)-1, 0, -1) :
        if (listPositions[i] == listPositions[i-1]) :
            listPositions[i] = 'NONE'
    return listPositions


def CalculerScore(closingData, listPositions) :
    score = 1
    buyPrice = 0
    sellPrice = 0
    for i in range(len(listPositions)) :
        if (listPositions[i] == 'BUY') :
            buyPrice = closingData[i]
        elif (listPositions[i] == 'SELL') & (buyPrice != 0) :
            sellPrice = closingData[i]
            score = (sellPrice / buyPrice) * score
            buyPrice = 0
            sellPrice = 0
    return score


def AnalyserValeursHistoriques(symbol, dateStart) :
    filePath = os.getcwd() + '\\data\\' + symbol + '\\' + dateStart.replace('/', '-') + '_3Y.txt'
    dataFrame = pandas.read_csv(filePath, sep=';', names=['Date', 'Ouverture', 'Cloture'])[::-1]
    pandas.to_numeric(dataFrame['Ouverture'])
    pandas.to_numeric(dataFrame['Cloture'])

    closingData = dataFrame['Cloture'].tolist()
    bestParameters = [0, 0, 0] # Période i, Période j, Score PTF

    for i in range(10, 300, 10) :           # j >= i, donc si EMA(i) > EMA(j) : croissance
        for j in range(i+10, 300, 10) :        #              si EMA(i) < EMA(j) : décroissance
            #for k in range(0.0001, 0.005, 0.0001) :
            listEMAi = CalculerEMA(closingData, i)
            listEMAj = CalculerEMA(closingData, j)
            listPositions = CalculerPositions(listEMAi[300:], listEMAj[300:], 0)
            score = CalculerScore(closingData[300:], listPositions)
            if (score > bestParameters[2]) :
                bestParameters = [i, j, score]
    print(bestParameters)

with open('ListeSymboles.txt', 'r') as file :
        lines = file.readlines()
        for line in lines :
            symbole = line.strip().split(';')[1]
            print(symbole, end='')
            AnalyserValeursHistoriques(symbole, '01/01/2016')
