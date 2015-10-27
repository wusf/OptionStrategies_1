#!/usr/bin/env python
#coding:utf-8
# Author:  Wusf --<>
# Purpose: 
# Created: 2014/6/9

import sys
import unittest
import numpy as np

########################################################################
class PerformanceAssessment(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, retArr, trdDayNum, riskFreeRate):
        """Constructor"""
        self.retArr = retArr
        self.trdDayNum = trdDayNum
        self.riskFreeRate = riskFreeRate
        
    #----------------------------------------------------------------------
    def CumRet(self):
        """"""
        self.cumRet = []
        __cumRet = 0
        for r in self.retArr:
            __cumRet = __cumRet + r
            self.cumRet.append(__cumRet)
        return self.cumRet
    
    #----------------------------------------------------------------------
    def AnnRet(self):
        """"""
        self.annRet = round(np.mean(self.retArr)*self.trdDayNum,3)
        return self.annRet
    
    #----------------------------------------------------------------------
    def AnnVol(self):
        """"""
        self.annVol = round(np.std(self.retArr)*np.sqrt(self.trdDayNum),3)
        return self.annVol
    
    #----------------------------------------------------------------------
    def AnnSemiVol(self):
        """"""
        self.annSemiVol = self.__GetMdd(self.retArr)*np.sqrt(self.trdDayNum)
        return self.annSemiVol
    
    #----------------------------------------------------------------------
    def SR(self):
        """"""
        self.sharpeRatio = round((self.annRet - self.riskFreeRate)/self.annVol,3)
        return self.sharpeRatio
    
    #----------------------------------------------------------------------
    def Mdd(self):
        """"""
        self.mdd = round(self.__GetMdd(self.retArr),3)
        return self.mdd
    
    #----------------------------------------------------------------------
    def SortinoR(self):
        """"""
        self.sortinoRatio = (self.annRet - self.riskFreeRate)/self.annSemiVol
        return self.sortinoRatio
        
    #----------------------------------------------------------------------
    def __GetMdd(self, arr):
        cumArr = []
        maxCumArr = []
        dd = []
        __cumArr = 0
        for r in arr:
            __cumArr = __cumArr + r
            cumArr.append(__cumArr)
        __maxCumArr = 0
        for cr in cumArr:
            if cr >= __maxCumArr:
                __maxCumArr = cr
            else:
                pass
            maxCumArr.append(__maxCumArr)
            dd.append(__maxCumArr - cr)
        return max(dd)
    
    #----------------------------------------------------------------------
    def __GetSemiVol(self, arr):
        """"""
        newArr = []
        m = np.mean(newArr)
        for a in arr:
            if a<=m:
                newArr.append(a*a)
        n = len(newArr)
        v = sum(newArr)/n
        s = np.sqrt(v)
        return s
        
        
        
    
    

if __name__=='__main__':
    unittest.main()