#!/usr/bin/python3

###################################################################
#    File name     : silpandas.py
#    Author        : sha-ou
#    Date          : 2019年05月21日 星期二 08时38分19秒
#    Description   :
###################################################################

import os
import sys
import numpy as np
import pandas as pd


class SilPandas():
    def __init__(self, on,
                 avaf='ava.csv', oxif='oxi.csv',
                 slpf='slp.csv', vthf='vth.csv'):

        self.__avaf = None
        self.__oxif = None
        self.__slpf = None
        self.__vthf = None

        self.__avadf = None
        self.__oxidf = None
        self.__slpdf = None
        self.__vthdf = None
        self.__alldf = None

        if os.path.isfile(avaf):
            self.__avaf = avaf
            self.__avadf = pd.read_csv(self.__avaf)
        if os.path.isfile(oxif):
            self.__oxif = oxif
            self.__oxidf = pd.read_csv(self.__oxif)
        if os.path.isfile(slpf):
            self.__slpf = slpf
            self.__slpdf = pd.read_csv(self.__slpf)
        if os.path.isfile(vthf):
            self.__vthf = vthf
            self.__vthdf = pd.read_csv(self.__vthf)

        if self.__avadf is not None and self.__oxidf is not None:
            self.__alldf = self.__avadf.merge(self.__oxidf, how='outer', on=on)
            self.__alldf['bv'] = self.__alldf. \
                loc[:, ['ava', 'oxi']].apply(np.min, axis=1)
        elif self.__avadf is not None:
            self.__alldf = self.__avadf
            self.__alldf['bv'] = self.__avadf['ava']
        if self.__slpdf is not None:
            self.__alldf = self.__alldf.merge(self.__slpdf, how='outer', on=on)
        if self.__vthdf is not None:
            self.__alldf = self.__alldf.merge(self.__vthdf, how='outer', on=on)

    def calcalldf(self, calcfunc=None):
        if calcfunc is None:
            self.__alldf['devw'] = 6 + self.__alldf.jfetw/2
            self.__alldf['ronsp'] = self.__alldf.devw/self.__alldf.slp*1e-5
            self.__alldf['fom'] = self.__alldf.bv**2 / \
                self.__alldf.ronsp*1e-3
        else:
            self.__alldf = calcfunc(self.__alldf)
        return self.__alldf

        @property
        def avaf(self):
            return self.__avaf

        @avaf.setter
        def avaf(self, avaf):
            if os.path.isfile(str(avaf)):
                self.__avaf = avaf
                self.__avadf = pd.read_csv(self.__avaf)
            else:
                raise FileNotFoundError("%s not found" % avaf)

        @property
        def oxif(self):
            return self.__oxif

        @oxif.setter
        def oxif(self, oxif):
            if os.path.isfile(str(oxif)):
                self.__oxif = oxif
                self.__oxidf = pd.read_csv(self.__oxif)
            else:
                raise FileNotFoundError("%s not found" % oxif)

        @property
        def slpf(self):
            return self.__slpf

        @slpf.setter
        def slpf(self, slpf):
            if os.path.isfile(str(slpf)):
                self.__slpf = slpf
                self.__slpdf = pd.read_csv(self.__slpf)
            else:
                raise FileNotFoundError("%s not found" % slpf)

        @property
        def vthf(self):
            return self.__vthf

        @vthf.setter
        def vthf(self, vthf):
            if os.path.isfile(str(vthf)):
                self.__vthf = vthf
                self.__vthdf = pd.read_csv(self.__vthf)
            else:
                raise FileNotFoundError("%s not found" % vthf)

        @property
        def avadf(self):
            return self.__avadf

        @property
        def oxidf(self):
            return self.__oxidf

        @property
        def slpdf(self):
            return self.__slpdf

        @property
        def vthdf(self):
            return self.__vthdf

        @property
        def alldf(self):
            return self.__alldf


if __name__ == '__main__':
    silpandas = SilPandas(
        on=['jfetw', 'pdriftt', 'pdriftc', 'pdriftw', 'cslthick', 'cslconc'])
    alldf = silpandas.calcalldf()
    print(alldf)
