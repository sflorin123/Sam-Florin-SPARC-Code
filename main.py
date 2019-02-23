import timeit
import matplotlib.pyplot as plt

start = timeit.default_timer()

import numpy as np
import random
import operator

prices = {}
def create(gasStations,gasPrice):
  prices = {}
  for i in range(gasStations):
    prices[i]=random.uniform(gasPrice,2*gasPrice)
  return prices
knownPrices = {}
streak = []
def nextWeek(streak,prices,gasPrice):

  prices[streak[0]]-=streak[1]

  for i in range(len(prices)):
    prices[i]-=1
    if prices[i]<gasPrice:
      prices[i]*=2
  return prices

def setKnownPrices(prices,known):
  new = {}
  for i in list(known.keys()):
    new[i]=prices[i]
  return new
def week(streak,knownPrices,prices,bound,gasPrice,notPicked):

  choice = pick(streak,knownPrices,len(list(prices.keys())),bound,gasPrice,notPicked)

  #print(choice[1])
  choice = choice[0]
  if streak==[]:
    streak = [choice,1]
  else:
    if streak[0]==choice:
      streak[1]+=1
    else:
      streak = [choice,1]

  prices = nextWeek(streak,prices,gasPrice)


  return streak,prices,knownPrices,choice

def insertSort(insert,old,d):
  items = list(old.items())
  for i in items:
      if i[0]==old:
          items.remove(i)
  for i in range(len(items)):
    if d[insert]<items[i][1]:
      items.insert(i,(insert,d[insert]))
      return dict(items)
  items.append((insert,d[insert]))
  return dict(items)


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
def pick(streak,knownPrices,gasstations,bound,gasPrice,notPicked):

  notDouble = []
  if streak==[]:
    return random.randrange(gasstations),'random'
  priceIfPicked = knownPrices.copy()
  priceIfPicked[streak[0]]-=streak[1]
  for i in list(priceIfPicked.keys()):
    priceIfPicked[i]-=2
    if priceIfPicked[i]<gasPrice:
      priceIfPicked[i]*=2
    else:
      notDouble.append(i)




  if len(list(knownPrices.keys()))==gasstations:

    if notDouble==[]:
      return index(knownPrices,min(list(knownPrices.values()))),'out of options'
    return notDouble[0],'cheapest with nothing left'
  if notDouble==[]:
    return random.choice(notPicked),'nothing great,everything doubles'
  if knownPrices[notDouble[0]]>=bound*gasPrice:
    return random.choice(notPicked),'nothing great'
  return notDouble[0],'cheapest not doubling'



def findBest(gasStations,gasPrice):
  #This doesn't actually work
  bound = 1
  bestRatio = 0
  for i in range(1,21):
    print(bound)
    Tpaid = 0
    Tavg = 0
    prices = create(gasStations,gasPrice)
    streak = []
    knownPrices = {}
    j = doItAll(prices,bound,gasPrice,10)
    Tpaid+=j[1]
    Tavg+=j[3]
    print(Tavg/Tpaid)
    if Tavg/Tpaid>bestRatio:
      bound+=2**(-1*i)
      bestRatio = Tavg/Tpaid
      print('going up',2**(-1*i))
    else:
      bound-=2**(-1*i)
      bestRatio = Tavg/Tpaid
      print('going down',2**(-1*i))
  return bound,bestRatio

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


def score(g,p,b):
    r=repeat(g,p,b,25)
    return r[1]/r[0]
def cheap(g,p):
    scores = []
    for i in range(25,51):
        b = i/25
        scores.append(score(g,p,b))
    return min(scores)
def bestPrice(g):
    cheaps = []
    prices = []
    for i in range(10,40):
        p = g*i/25
        prices.append(p)
        cheaps.append(cheap(g,p))
    return prices[cheaps.index(min(cheaps))]




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
        #Tavg+=j[3]
        #Texp+=j[2]
        y1.append(Tpaid/Tmin)
        #y2.append(Tpaid/Tavg)
        #y3.append(Tpaid/Texp)
    if doIt:
        plt.figure(1)
        plt.plot(x,y1)
        plt.savefig('minRatio'+str(gasStations)+'-'+str(gasPrice)+'.png')
        plt.clf()
    return list(zip(x,y1))

def createStreak(streak,choice):
    if streak==[]:
        return [choice,1]
    if choice == streak[0]:
        streak[1]+=1
        return streak
    return [choice,1]

'''
stations = [50,100,150,200,250,300,350,400,450,500,600,700,800,900,1000]
ratios = []
location = []
minimum = []
cheapest = []
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
f = open('200score.txt','w+')
stations = [50]
prices = [5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,120,130,140,150,160,170,180,190,200]
ratios = []
locs = []
mins = []
ranges = []
for j in prices:
    i=100
    g=graph(i,2*j,25,25,True)
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
plt.savefig('200bestLocs.png')
plt.clf()
plt.plot(ratios,mins)
plt.savefig('200bestScores.png')
plt.clf()
plt.plot(ratios,ranges)
plt.savefig('200ranges.png')
plt.clf()
end  = timeit.default_timer()
print(end-start)
