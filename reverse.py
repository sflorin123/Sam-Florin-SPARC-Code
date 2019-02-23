import timeit
import matplotlib.pyplot as plt

start = timeit.default_timer()
''' prices lower based on streaks there, otherwise they go down 1
if they drop below the price of gas, the next week they are doubled
variables: gas stations (seem not to matter much bc only searching like 20-30), range of prices, gas price (don't really matter but if range bigger, program should search more), boundary for searching (should test many)
'''
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


  for i in range(len(prices)):
    if i==streak[0]:
        prices[streak[0]]+=streak[1]
    else:
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
  '''if knownPrices == {}:
    knownPrices = {choice:prices[choice]}
  elif choice not in list(knownPrices.keys()):
    knownPrices[choice]=prices[choice]'''
  prices = nextWeek(streak,prices,gasPrice)
  #knownPrices = setKnownPrices(prices,knownPrices)

  return streak,prices,knownPrices,choice

def insertSort(insert,old,d):
  items = list(old.items())
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
    expensive = max(list(prices.values()))
    avg=sum(list(prices.values()))/len(list(prices.values()))
    notPicked = list(prices.keys())

    for _ in range(1000):
      streak,prices,newKnownPrices,choice = week(streak, knownPrices,prices,bound,gasPrice,notPicked)

      knownPrices = setKnownPrices(prices,knownPrices)
      if choice not in list(knownPrices.keys()):

        notPicked.remove(choice)
        knownPrices[choice]=prices[choice]
      knownPrices = dict(sorted(knownPrices.items(), key=lambda kv: kv[1]))

      cheapest+=min(list(prices.values()))
      expensive+=max(list(prices.values()))
      avg+=sum(list(prices.values()))/len(list(prices.values()))

      money+=prices[choice]
    m+=money
    c+=cheapest
    e+=expensive
    a+=avg

  return c,m,e,a
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

  for i in list(priceIfPicked.keys()):
    if i==streak[0]:
        priceIfPicked[i]+=(streak[1]+1)
    else:
        priceIfPicked[i]+=1
    if priceIfPicked[i]<gasPrice:
      priceIfPicked[i]*=2
    else:
      notDouble.append(i)


  #print(priceIfPicked)


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




def graph(gasStations,gasPrice,rep,precision,rev,doIt=True):
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
        if not rev:
            plt.savefig('minRatio'+str(gasStations)+'-'+str(gasPrice)+'.png')
        else:
            plt.savefig('reverse'+str(gasStations)+'-'+str(gasPrice)+'.png')
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
f = open('200scoresRev2txt','a+')
stations = [200]
prices = [50,75,100,125,150,175,180,190,195,200,205,210,225,250,275,300,325,350,400,500]
ratios = []
locs = []
mins = []
ranges = []
for j in prices:
    i=200
    g=graph(i,j,25,25,True)
    a =[]
    for x in g:
        a.append(x[1])

    ratios.append(j/200)
    mini = min(a)
    mins.append(mini)
    locs.append(g[a.index(mini)][0])
    ranges.append(max(a)-min(a))
    f.write(str(i)+' '+str(j)+', min: '+str(mini)+' at: '+str(g[a.index(mini)][0])+' range: '+str(max(a)-min(a))+'\n')
f.close()
plt.figure(2)
plt.plot(ratios,locs)
plt.savefig('200bestLocsRev2.png')
plt.figure(3)
plt.plot(ratios,mins)
plt.savefig('200bestScoresRev2.png')
plt.figure(4)
plt.plot(ratios,ranges)
plt.savefig('200rangesRev2.png')

end  = timeit.default_timer()
print(end-start)
