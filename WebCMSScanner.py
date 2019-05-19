# -*- coding: utf-8 -*-
from gevent import monkey;monkey.patch_all()
import sys
import gevent
from gevent.pool import Pool
import md5
import json

import ssl
import requests
ssl._create_default_https_context = ssl._create_unverified_context


class WebCMSScanner():
    def __init__(self):
        self.domain = ''
        self.m_lRezw = []
        self.m_lMd5zw = []
        self.m_lOut = []
        self.m_bOut = False

    def Reques(self, m_sUrl):
        
        m_mRequeshead = requests.head('http://'+self.domain+m_sUrl, timeout=5)
        if m_mRequeshead.status_code != 200:
            return 'NULL'
        m_mReques = requests.get('http://'+self.domain+m_sUrl, timeout=5)
        return m_mReques.text

    def Rezw(self, m_dRezw):
        try:
            m_sText = self.Reques(m_dRezw['url'])
            if m_sText == 'NULL':
                return
            elif m_dRezw['re'] in m_sText:
                self.m_lOut.append(m_dRezw['name'])
                self.m_bOut = True
        except:
            pass

    def Mdzw(self, m_dMd5zw):
        try:
            m_sText = self.Reques(m_dMd5zw['url'])
            if m_sText == 'NULL':
                return
            m_mMd5 = md5.md5(m_sText).hexdigest()
            if m_mMd5 == m_dMd5zw['md5']:
                self.m_lOut.append(m_dMd5zw['name'])
                self.m_bOut = True
        except:
            pass

    def WebCMS(self, url):
        r = open("data.json")
        j = json.load(r, encoding='utf-8')
        r.close()
        for x in j:
            if x['re'] != "":
                self.m_lRezw.append(x)
            else:
                self.m_lMd5zw.append(x)
        m_mPool = Pool(200)
        m_lPool = []
        for m_dRezw in self.m_lRezw:
            m_mThear = m_mPool.spawn(self.Rezw, m_dRezw)
            m_lPool.append(m_mThear)
            if self.m_bOut == True:
                break
        for m_dMd5zw in self.m_lMd5zw:
            m_mThear2 = m_mPool.spawn(self.Mdzw, m_dMd5zw)
            m_lPool.append(m_mThear2)
            if self.m_bOut == True:
                break
        gevent.joinall(m_lPool)

    def Run(self):
        self.WebCMS(self.domain)
        #self.m_lOut = list(set(self.m_lOut))
        if self.m_lOut != []:
            print self.m_lOut[0]
        else:
            print "没找到"

if __name__ == '__main__':
    cmsobj = WebCMSScanner()
    cmsobj.domain = sys.argv[1]
    cmsobj.Run()
