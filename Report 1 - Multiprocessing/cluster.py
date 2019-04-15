# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#Import useful libraries
import pp, paramiko
import numpy as np
import math
import matplotlib.pyplot as plt
import time
import getpass


#import warnings
#with warnings.catch_warnings():
#    warnings.simplefilter("ignore")
#    import paramiko



#Retrieve username and prompt user for password
user = getpass.getuser()
#passw = getpass.getpass('Password for '+user+': ')
passw = 'Pug.life6'


hostlist = list(np.loadtxt('test.out', dtype = 'S13'))




def run_ppserver(hostlist):

        
    #Terminal command to activate the parallel python server.
    #Python27 corresponds to a conda environment on my account
    #that is used to run Python 2.7.16.
    command = 'conda activate Python27 && ppserver.py -a'
    
    #Counter
    cnt = 0
    
    #Start client on each valid host
    for host in hostlist:
        try:
            with paramiko.SSHClient() as ssh:
                
                #Set host key policy
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                
                #Connect to host
                ssh.connect(host, username=user, password=passw,timeout=2)
                
                #Execute command on host
                ssh.exec_command(command)
                
                #Update counter
                cnt += 1
    
        except:
            None
            
    print 'ppserver.py executed on %s hosts'%cnt
    
    
    
def kill_server(hostlist):
    
    command = 'pkill -u alexander.hickey'
    cnt = 0
    for host in hostlist:
        
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, username=user, password=passw,timeout=2)
            ssh.exec_command(command)
            ssh.close()
            cnt += 1
            
        except:
            None
            
    print 'disconnected from %s hosts'%cnt
    



def isprime(n):
    """Returns True if n is prime and False otherwise"""
    if not isinstance(n, int):
        raise TypeError("argument passed to is_prime is not of 'int' type")
    if n < 2:
        return False
    if n == 2:
        return True
    max = int(math.ceil(math.sqrt(n)))
    i = 2
    while i <= max:
        if n % i == 0:
            return False
        i += 1
    return True

def sum_primes(n):
    """Calculates sum of all primes below given integer n"""
    return sum([x for x in xrange(2,n) if isprime(x)])




def main(N):
    
    run_ppserver(hostlist)
    ppservers = tuple(hostlist)
    
    # Creates jobserver with ncpus workers
    #job_server = pp.Server(ncpus, ppservers=ppservers)
    
    #print "Starting pp with", job_server.get_ncpus(), "workers"
    
    #sev = []
    time_list = []
    
    for n in range(N,N+1):
        job_server = pp.Server(ppservers=ppservers)
        res =[]
        inputs = tuple(np.tile([200000],n))
        start_time = time.time()
    
        jobs = [job_server.submit(sum_primes,(i,), (isprime,), ('math',)) for i in inputs]
        
        for job in jobs:
            res.append(job())
    
        time_list.append(time.time() - start_time)
        print res
        job_server.destroy()
    
    kill_server(hostlist)
    
    return time_list[0]
    
if __name__ == '__main__':
    plt.plot(main(1))
    
    
    
    
    
    