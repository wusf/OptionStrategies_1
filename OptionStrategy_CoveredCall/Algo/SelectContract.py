#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Wusf
  Purpose: Simple option strategy
  Created: 2015/1/12
"""

import sqlite3
import numpy as np
import scipy.stats as stats
import time,datetime
from dateutil import rrule
from dateutil.parser import parse
import copy


########################################################################
class SelectContract:
    """Select the contract will expire within 1 month and with delta 20"""

    #----------------------------------------------------------------------
    def __init__(self, date, volatility, spotPrice, r, delta, month2Expriry):
        """Constructor"""
        self.date = date
        self.volatility = volatility
        self.spotPrice = spotPrice
        self.r = r
        self.delta = delta
        self.month2Expiry = month2Expriry
        
    #----------------------------------------------------------------------
    def connect_to_database(self, databaseName):
        """"""
        self.cx = sqlite3.connect(databaseName)
            
    #----------------------------------------------------------------------
    def search_database(self):
        """"""
        cu = self.cx.cursor()
        contractCandidate = []
        cmd = "select F6_3517, G1_3015, G3_3015, G10_3015, G11_3015, G13_3015, F1_3517 from OptionData where F2_3517 = {0}".format(self.date)
        cu.execute(cmd)
        temp = cu.fetchall()
        #print temp
        putContract = []
        thisMoncontract = []
        nextMonContract = []
        #print contractCandidate,contractCandidate[-1][-1]
        for item in temp:
            if int(item[3]) == 708001000 and len(item[2])!=4:# and self.date!=item[2]:
                putContract.append(item)
        diffDays = []
        for item in putContract:
            expiry = item[2]
            days = self.workdays(self.date, expiry)
            diffDays.append(days)
        
        _diffDays = copy.deepcopy(diffDays)
        _diffDays.sort()
        _diffDaysDistinct = [_diffDays[0]]
        for i in range(1,len(_diffDays)):
            if _diffDays[i] != _diffDays[i-1]:
                _diffDaysDistinct.append(_diffDays[i])
        
        for item1,item2 in zip(diffDays, putContract):
            if 40 < item1 < 90:
                nextMonContract.append(item2)
            if 3 < item1 < 30:
                thisMoncontract.append(item2)
        #print nextMonContract
                
        deltaDiff = 10000
        if self.month2Expiry == 0:
            targetMonthContract = thisMoncontract
        else:
            targetMonthContract = nextMonContract
        for item in targetMonthContract:
            vol =self.volatility
            expiry = item[2]
            s = self.spotPrice
            k = float(item[-3])
            _delta = self.calc_greeks(vol, expiry, s, k, self.r)
            _deltaDiff = np.abs(np.abs(_delta*100)-self.delta)
            newItem = list(item)
            newItem.append(_delta*100)
            #print  newItem
            if _deltaDiff<deltaDiff:
                deltaDiff = _deltaDiff
                targetContract = newItem
            self.targetContract = targetContract
            self.expiry = expiry
    
    #----------------------------------------------------------------------
    def workdays(self, start, end, holidays=0, days_off=None):
        if days_off is None:
            days_off = 5, 6
        workdays = [x for x in range(7) if x not in days_off]
        days = rrule.rrule(rrule.DAILY, dtstart=parse(start), until=parse(end), byweekday=workdays)
        return days.count() - holidays
                 
    #----------------------------------------------------------------------
    def calc_greeks(self, vol, expiry, s, k, r):
        """"""
        days = self.workdays(self.date, expiry)
        t = float(days/250.0)
        d1 = (np.log(s/k)+(r+vol*vol/2)*t)/(vol*np.sqrt(t))
        delta = stats.norm.cdf(d1)
        return delta
    


if __name__ == '__main__':
    a = stats.norm.cdf(-4)
    print a
    sc = SelectContract("20140228", 0.2, 1.4, 0.03,20)
    sc.connect_to_database("OptionData.db")
    sc.search_database()

