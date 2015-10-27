#!/usr/bin/env python
# -*- coding:gbk -*-
"""
  Author:   --<>
  Purpose: 
  Created: 2015/1/19
"""

import Algo.GenerateTrades as gt
import Algo.CalcReturn as cr

#-------------------------------------------------------#
#----------------------Parameters-----------------------#
#-------------------------------------------------------#
assetPrice = 2.5
leverage = 4.0
IV = 25
targetDeltas = [20, 25, 30] 
riskFreeRate = 0.04

begDate = "20140221"
endDate = "20141231"

cla
#-------------------------------------------------------#
#--------------------Generate Report--------------------#
#-------------------------------------------------------#
import os
initialMoney = assetPrice/leverage
month2ExpiryOfTargetContract = 0
rollOverDay = 0
for delta in targetDeltas:
    gt.run(IV, delta, riskFreeRate, 
           month2ExpiryOfTargetContract,
           rollOverDay,
           begDate, endDate)
initial = initialMoney
returns = []
fileList = os.listdir('BacktestRecord_IV'+repr(IV))
for filename in fileList:
    print filename
    out = cr.calc_return('BacktestRecord_IV'+repr(IV)+'\\'+filename)
    returns.append(out[1])
    print len(out)
output = file('IV'+repr(IV)+'Cum_Returns.csv', 'w')

output.write("Initial Money:"+repr(initialMoney)+"\n")
output.write("Risk Free Rate:"+repr(riskFreeRate)+"\n")
output.write("Month to Expiry:"+repr(month2ExpiryOfTargetContract)+"\n")
output.write("Roll Over Day:"+repr(rollOverDay)+"\n")

output.write("")
for item in targetDeltas:
    output.write(","+"Delta"+repr(item))
output.write("\n")
for i in xrange(len(out[0])):
    output.write(out[0][i])
    for j in xrange(len(returns)):
        output.write(','+repr(returns[j][i]/initial))
    output.write('\n')
output.close()

#-------------------------------------------------------#
#--------------------Graw Charts------------------------#
#-------------------------------------------------------#
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedFormatter, MultipleLocator, FuncFormatter, NullFormatter
from matplotlib.finance import candlestick
from matplotlib.dates import date2num
from matplotlib.ticker import MultipleLocator
import numpy
import matplotlib.cm as cm
import Algo.PerformanceAssessment as PA

fig = plt.figure(num=None, figsize=None, dpi=125, facecolor=None, 
                edgecolor=None, frameon=True)
ax = fig.add_subplot(111)
ax.set_axis_bgcolor('lightyellow')
xlocator = MultipleLocator(1)
ylocator = MultipleLocator(0.05)
y2locator = MultipleLocator(0.01)
ax.xaxis.set_minor_locator(xlocator)
ax.yaxis.set_major_locator(ylocator)
ax.yaxis.set_minor_locator(y2locator)
lenOfDays = len(returns[0])
plt.xlim(0,lenOfDays+1)
plt.ylim(min(min(returns))/initial-0.01, max(max(returns))/initial+0.01)
interval = lenOfDays/30
dates = out[0]
x = range(0,lenOfDays)
plt.xticks(x[::interval],dates[::interval],rotation=45, size=6,color='black')
plt.yticks(size = 8, color='black')
plt.grid()
for i in  xrange(len(returns)):
    rets = [returns[i][0]]
    for k in range(1,len(returns[i])):
        rets.append(returns[i][k]/initial-returns[i][k-1]/initial)
    pa = PA.PerformanceAssessment(rets, 250, 0.04)
    pa.AnnRet()
    pa.AnnVol()
    pa.SR()
    pa.Mdd()
    
    plt.plot(returns[i], label = 'Delta:'+repr(targetDeltas[i])+
             ' R:'+repr(pa.annRet)+' V:'+repr(pa.annVol)
             +' SR:'+repr(pa.sharpeRatio)+' MDD:'+repr(pa.mdd))
    
plt.legend(loc='upper left',fontsize = 8, frameon=True)
plt.title('SellPutStrategy|IV='+repr(IV)+'|LeverageRatio='+repr(int(leverage)), color = 'black',fontweight="bold")
date = out[0]
plt.savefig('Sell_put_strategy.jpeg', dpi=125, format="jpeg")
