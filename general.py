import timeit
import matplotlib.pyplot as plt
#Issue: With reverse, always running out of options. Issue with notdouble
start = timeit.default_timer()
''' prices lower based on streaks there, otherwise they go down 1
if they drop below the price of gas, the next week they are doubled
variables: gas stations (seem not to matter much bc only searching like 20-30), range of prices, gas price (don't really matter but if range bigger, program should search more), boundary for searching (should test many)
'''
import numpy as np
import random
import operator
import math
prices = {}
def create(gasStations,gasPrice):
  prices = {}
  for i in range(gasStations):
    prices[i]=random.uniform(gasPrice,2*gasPrice)
  return prices
knownPrices = {}
streak = []

def fPicked(price,streak):
    return price+streak**2
def fNotPicked(price,streak):
    return price-streak
def fNotInBound(price,gasPrice):
    if price<gasPrice:
        #return gasPrice+gasPrice*1/(gasPrice-price+1)
        return gasPrice*2
    if price>2*gasPrice:
        #return 2*gasPrice-gasPrice*1/(price-2*gasPrice+1)
        return gasPrice/2
def nextWeek(streak,prices,gasPrice):


  for i in range(len(prices)):
    if i==streak[0]:
        prices[streak[0]]=fPicked(prices[streak[0]],streak[1])
    else:
        prices[i]=fNotPicked(prices[i],streak[1])
    if prices[i]<gasPrice or prices[i]>2*gasPrice:
      prices[i]=fNotInBound(prices[i],gasPrice)
  return prices

def createStreak(streak,i):
    if streak==[]:
        return [i,1]
    if i == streak[0]:
        newStreak = [streak[0],streak[1]+1]
    else:
        newStreak = [i,1]
    return newStreak

def setKnownPrices(prices,known):
  new = {}
  for i in list(known.keys()):
    new[i]=prices[i]
  return new
def week(streak,knownPrices,prices,bound,gasPrice,notPicked):
  choice = pick(streak,knownPrices,len(list(prices.keys())),bound,gasPrice,notPicked)


  choice = choice[0]
  streak = createStreak(streak,choice)
  prices = nextWeek(streak,prices,gasPrice)


  return streak,prices,knownPrices,choice



def doItAll(prices,bound,gasPrice,repeat=1):
  m = 0
  c = 0
  e = 0
  a = 0
  for i in range(repeat):
    streak = []
    knownPrices = {}
    money = 0
    cheapest = min(list(prices.values()))

    notPicked = list(prices.keys())

    for _ in range(1000):
      streak,prices,newKnownPrices,choice = week(streak, knownPrices,prices,bound,gasPrice,notPicked)

      knownPrices = setKnownPrices(prices,knownPrices)
      if choice not in list(knownPrices.keys()):
        if choice in notPicked:
            notPicked.remove(choice)
        knownPrices[choice]=prices[choice]
      knownPrices = dict(sorted(knownPrices.items(), key=lambda kv: kv[1]))


      cheapest+=min(list(prices.values()))
       money+=prices[choice]
    m+=money
    c+=cheapest

  return c,m
def index(dictionary,value):
  for k, v in dictionary.items():
    if v == value:
      return k

'''

Pick cheapest unless picking it makes it not the cheapest
Then, pick streak or 2nd cheapest or cheapest so it doesn't double unless this unless price > 25. Then pick random new
'''
def pickedResult(streak,price,gasPrice):
    new = fPicked(price,streak[1])
    if new<gasPrice or new>2*gasPrice:
        return fNotInBound(new,gasPrice)
    return new

def pick(streak,knownPrices,gasstations,bound,gasPrice,notPicked):

  notDouble = []
  if streak==[]:
    return random.randrange(gasstations),'random'
  priceIfPicked = knownPrices.copy()

  for i in list(priceIfPicked.keys()):
    newStreak = createStreak(streak,i)
    priceIfPicked[i]=pickedResult(newStreak,priceIfPicked[i],gasPrice)
    if priceIfPicked[i]<=fPicked(priceIfPicked[i],newStreak[1]):
      notDouble.append(i)
  if notDouble==[]:
      print('ruh roh',len(list(knownPrices.keys())))



  if len(list(knownPrices.keys()))==gasstations:

    if notDouble==[]:
      return index(knownPrices,min(list(knownPrices.values()))),'out of options'
    return notDouble[0],'cheapest with nothing left'
  if notDouble==[]:
    return random.choice(notPicked),'nothing great,everything doubles'
  if knownPrices[notDouble[0]]>=bound*gasPrice:
    return random.choice(notPicked),'nothing great'
  return notDouble[0],'cheapest not doubling'



def repeat(gasStations,gasPrice,bound,rep):
  c = 0
  m = 0
  e = 0
  a = 0
  for i in range(rep):
    print(i)
    prices = create(gasStations,gasPrice)
    results = doItAll(prices,bound,gasStations,1)
    c+=results[0]
    m+=results[1]

  return c,m




def graph(gasStations,gasPrice,rep,precision,doIt=True):
    x = []
    y1  = []
    y2 = []
    y3 = []
    for i in range(precision,precision*2):
        b = i/precision
        print(b,'-',gasStations,gasPrice)
        x.append(b)
        Tpaid = 0
        Tmin = 0
        Tavg = 0
        Texp = 0
        streak = []
        knownPrices = {}
        j = repeat(gasStations,gasPrice,b,rep)
        Tpaid+=j[1]
        Tmin+=j[0]

        y1.append(Tpaid/Tmin)

    if doIt:
        plt.figure(1)
        plt.plot(x,y1)
        plt.savefig('general4-'+str(gasStations)+'-'+str(gasPrice)+'.png')
        plt.clf()
    return list(zip(x,y1))

'''
stations = [6000,7000,8000,9000,10000,12500,15000,17500,20000]
ratios = []
location = []
minimum = []
for i in stations:
    g=graph(i,i,25,25)
    a =[]
    for x in g:
        a.append(x[1])

    ratios.append(i)
        #f.write(str(i)+' stations '+str(j)+' dollars gives '+str(r[0])+' at '+str(r[1])+'\n')
    location.append(g[a.index(min(a))][0])
    minimum.append(g[a.index(min(a))][1])
    f=open('pricesEqualStations.txt','a+')
    f.write(str(i)+': min: '+str(min(a))+' at: '+str(g[a.index(min(a))][0])+'\n')
    f.close()
plt.figure(2)
plt.plot(ratios,location)
plt.savefig('pricesEqualStationsLocation3.png')
plt.figure(3)
plt.plot(ratios,minimum)
plt.savefig('pricesEqualStationsMinimum3.png')
'''
f = open('50scoreGeneral4.txt','a+')
stations = [50]
prices = [5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,120,130,140,150,160,170,180,190,200]
ratios = []
locs = []
mins = []
ranges = []
for j in prices:
    i=50
    g=graph(i,j,25,25,True)
    a =[]
    for x in g:
        a.append(x[1])

    ratios.append(j/50)
    mini = min(a)
    mins.append(mini)
    locs.append(g[a.index(mini)][0])
    ranges.append(max(a)-min(a))
    f.write(str(i)+' '+str(j)+', min: '+str(mini)+' at: '+str(g[a.index(mini)][0])+' range: '+str(max(a)-min(a))+'\n')
f.close()
plt.plot(ratios,locs)
plt.savefig('50bestLocsGeneral4.png')
plt.clf()
plt.plot(ratios,mins)
plt.savefig('50bestScoresGeneral4.png')
plt.clf()
plt.plot(ratios,ranges)
plt.savefig('50rangesGeneral4.png')
plt.clf()


end  = timeit.default_timer()
print(end-start)
