#!/usr/bin/env python
# -*- coding:gbk -*-
"""
  Author:   --<>
  Purpose: 
  Created: 2015/1/15
"""

import unittest
import SelectContract as SC
import sqlite3
from dateutil.parser import parser
import datetime
import os


def run(vol, delta, riskfreeRate, month2Expiry, rolloverDayAdj, startDate, endDate):
    ########################################################################
    # Step1 set up volatility, risk free rate, spot price
    ########################################################################
    volatility = float(vol/100.0)
    spotPrices = {}
    a = file("ETF_Price.csv","r")
    a.readline()
    for line in a:
        lst = line.split(',')
        _date = datetime.datetime.strptime(lst[0], '%Y-%m-%d').strftime('%Y%m%d')
        spotPrices[_date] = float(lst[3])

    ########################################################################
    # Step2 determine trading days for backtest
    ########################################################################
    cx = sqlite3.connect("OptionData.db")
    cu = cx.cursor()
    cmd = "select distinct F2_3517 from OptionData order by F2_3517"
    cu.execute(cmd)
    _tradingDays = cu.fetchall()
    tradingDays = []
    for dt in _tradingDays:
        tradingDays.append(repr(dt[0]))
    cmd = "select distinct G3_3015 from OPtionData order by G3_3015"
    cu.execute(cmd)
    _expiryDays = cu.fetchall()
    expiryDays = []
    for dt in _expiryDays:
        if str(dt[0])<= tradingDays[-1]:
            expiryDays.append(str(dt[0]))
    print expiryDays
    expiryDaysPosi = []
    for dt in expiryDays:
        expiryDaysPosi.append(tradingDays.index(dt))
    rolloverDays = []
    for n in expiryDaysPosi:
        rolloverDays.append(tradingDays[n+rolloverDayAdj])
    

    ########################################################################
    # Step3 run strategy
    ########################################################################
    rollingDate = ""
    targetDelta = delta
    targetContract = []
    #print rollingDate
    if os.path.exists('BacktestRecord_IV'+repr(vol)):
        pass
    else:
        os.makedirs('BacktestRecord_IV'+repr(vol))
    output = file('BacktestRecord_IV'+repr(vol)+'\\delta'+repr(targetDelta)+'.csv','w')
    output.write('交易日,是否交易,开仓合约,平仓合约,开仓合约delta,开仓价,平仓价,持仓合约,持仓合约收盘价,现货收盘价,平仓合约Strike\n')

    for date in tradingDays:
        if date<startDate or date>endDate or date=="20140402" or date == "20140408":
            pass
        else:
            output.write(date+',')
            if date!=startDate and date not in rolloverDays:
                contractId = targetContract[-2]
                contractName = targetContract[-3]
                cmd = "select F6_3517 from OptionData where F2_3517={0} and F1_3517={1}".format(date,contractId)
                cu.execute(cmd)
                closePrice = cu.fetchall()[0][0]
                print date,closePrice
                output.write('No,,,,,,{0},{1},{2}\n'.format(contractName.encode('gbk'), closePrice, spotPrices[date]))
                pass
            else:
                spotPrice = spotPrices[date] 
                sc = SC.SelectContract(date, volatility, spotPrice, riskfreeRate, targetDelta, month2Expiry)
                sc.connect_to_database("OptionData.db")
                sc.search_database()
                closeContract = targetContract
                targetContract = sc.targetContract
                #print date
                #print sc.targetContract
                rollingDate = sc.expiry
      
                targetContractId = targetContract[-2]
                targetContractName = targetContract[-3]
                cmd = "select F6_3517 from OptionData where F2_3517={0} and F1_3517={1}".format(date,targetContractId)
                cu.execute(cmd)
                targetContractPrice = cu.fetchall()[0][0]
                if len(closeContract)!=0:
                    closeContractId = closeContract[-2]
                    closeContractName = closeContract[-3]
                    cmd = "select F6_3517 from OptionData where F2_3517={0} and F1_3517={1}".format(date,closeContractId)
                    cu.execute(cmd)
                    closeContractPrice = cu.fetchall()[0][0]               
                    output.write('Yes,{0},{1},{2},{3},{4},{5},{6},{7},{8}\n'
                                 .format(targetContractName.encode('gbk'),
                                         closeContractName.encode('gbk'),
                                         targetContract[-1],
                                         targetContractPrice,
                                         closeContractPrice,
                                         targetContractName.encode('gbk'),
                                         targetContractPrice,
                                         spotPrices[date],
                                         closeContract[4]))
                else:
                    output.write('Yes,{0},{1},{2},{3},{4},{5},{6},{7}\n'
                                 .format(targetContractName.encode('gbk'),
                                         "",
                                         targetContract[-1],
                                         targetContractPrice,
                                         "",
                                         targetContractName.encode('gbk'),
                                         targetContractPrice,
                                         spotPrices[date]))
    output.close()
                









if __name__ == '__main__':
    unittest.main()
