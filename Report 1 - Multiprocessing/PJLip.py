# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 15:32:42 2019

@author: Admin
"""

import os
import numpy as np
import subprocess

def ip_list():
    '''
    IP 136.159.54.X
    '''
    lst = [('noatun','31'),
            ('nagifar','30'),
            ('asgard','20'),
            ('bifrost','22'),
            ('branstock','23'),
            ('fenris','24'),
            ('garm','25'),
            ('heimdall','26'),
            ('hoth','27'),
            ('munin','29'),
            ('tyr','32'),
            ('sigyn','33'),
            ('ymir','34'),
            ('embla','35'),
            ('odin','36'),
            ('frigga','37'),
            ('frey','38'),
            ('weiland','43'),
            ('mimir','41'),
            ('thor','39'),
            ('embla','35'),
            ('dyne','151'),
            ('knot','71'),
            ('nerthus','55'),
            ('mjolnir','64'),
            ('niflheim','58'),]

    return lst


if __name__ == '__main__':
    
    ip = ip_list()
    sp = []
    for j in range(len(ip)):
        n = ip[j] 
        sp.append(subprocess.Popen('plink -ssh alexander.hickey@136.159.54.'+n[1]+' -pw Pug.life6 -m C:/Users/Admin/Desktop/commands.txt'))
        print(n)

    
    