#!/usr/bin/env python
# -*- coding:gbk -*-
"""
  Author:   --<>
  Purpose: 
  Created: 2015/1/17
"""

import unittest

def calc_return(filename):
    rawContext = open(filename, 'r')
    rawContext.readline()


    cashIn = 0
    gain = 0
    cum_rets = []
    rets = []
    dates = []
    last_ret = 0
    initalETPPrice = 0

    for line in rawContext:
        _list = line.rstrip().split(',')
        #print _list
        date = _list[0]
        dates.append(date)
        value = -float(_list[8])
        if initalETPPrice == 0:
            initalETPPrice = float(_list[-2])
        if _list[1] != "No":
            cashIn = 0
        if _list[1] == "Yes":
            if len(_list[3]) == 0:
                cashIn = float(_list[5])
            if len(_list[3]) != 0:
                strikePrice = float(_list[-1])
                spotPrice = float(_list[-2])
                if spotPrice<strikePrice:
                    cashIn = float(_list[5])
                else:
                    cashIn = float(_list[5])-float(_list[6])
            gain = cashIn + gain
        _ret = gain + value + float(_list[-2]) - initalETPPrice
        ret = _ret-last_ret
        last_ret = _ret
        rets.append(ret)
        cum_rets.append(_ret)
    return dates,cum_rets,rets



        
                
                
            
        
    




if __name__ == '__main__':
    unittest.main()