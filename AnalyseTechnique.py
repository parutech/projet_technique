import os
import pandas


def CalculerEMA(closingData, period) :
    listEMA = [0] * (period - 1)
    
    pass


def CalculerPositions(listEMAi, listEMAj) :
    pass


def TrierPositions(listPositions) :
    pass


def CalculerScore(closingData, listPositions) :
    pass


def AnalyserValeursHistoriques(symbol, dateStart) :
    filePath = os.getcwd() + '\\data\\' + symbol + '\\' + dateStart.replace('/', '-') + '_3Y.txt'
    dataFrame = pandas.read_csv(filePath, sep=';', names=['Date', 'Ouverture', 'Cloture'])[::-1]

    closingData = dataFrame['Cloture'].tolist()
    bestParameters = [0, 0, 0] # Période i, Période j, Score PTF

    for i in range(10, 250, 10) :           # j >= i, donc si EMA(i) > EMA(j) : croissance
        for j in range(i, 250, 10) :        #              si EMA(i) < EMA(j) : décroissance
            listEMAi = CalculerEMA(closingData, i)
            listEMAj = CalculerEMA(closingData, j)
            listPositions = CalculerPositions(listEMAi, listEMAj)
            score = CalculerScore(closingData[250:], listPositions[250:])
            if (score > bestParameters[2]) :
                bestParameters = [i, j, score]

    print(dataFrame)
    print(dataFrame['Ouverture'].tolist())

#AnalyserValeursHistoriques('1rPAB', '01/01/2016')

liste = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
print(liste[2:])