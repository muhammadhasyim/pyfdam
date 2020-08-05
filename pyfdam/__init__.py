import lmfit as lm
import numpy as np
import scipy as sp
from contextlib import redirect_stdout

# A helper flattening function
def realimag(array):
        return np.array([(x.real, x.imag) for x in array]).flatten() 

# A class for parameters, which just passes lmfit's Parameters class
class Params(lm.Parameters):
    pass

# A class for impedace modeling and fitting
class ImpedanceFitter(object):
    def __init__(self,model,parameters,namedata):
        self.model = model
        self.parameters = parameters
        data = np.loadtxt(namedata) 
        self.zdata = data[:,1]+1j*data[:,2]
        self.f = data[:,0]
        
        #Define function to minimize
        def fcn2min(params):
            om = 2*1j*np.pi*self.f
            return realimag(self.model(om,params)-self.zdata)
        
        #Store it inside the minimizer object 
        self.minimizer = lm.Minimizer(fcn2min,parameters)
    
    def run(self,method,ncycles):
        
        #Start minimizing
        out1 = self.minimizer.minimize(method=method)
        for i in range(ncycles):
            out1 = self.minimizer.minimize(method='leastsq',params=out1.params)
        
        #Write error report
        lm.report_fit(out1.params) 
        
        #Copy the values in
        self.parameters = out1.params
   
    #Return the parameters value
    def get_params(self):
        return self.parameters
    
    #Saving the parameters values and uncertainties
    def save_params(self,filename):
        with open(filename, 'w') as f:
            with redirect_stdout(f):
                #Write error report
                lm.report_fit(out1.params) 
    
    #Return the impedance values from fitted model
    def get_impedancemodel(self,freq):
        om = 2*1j*np.pi*freq
        return self.model(om,self.parameters)
    
    #Return the impedance values from fitted model
    def get_impedanceexp(self):
        return (self.f,self.zdata)

    #Save impedance data given frequency values
    def save_impedance(self,freq,filename):
        om = 2*1j*np.pi*freq
        zdata = self.model(om,self.parameters)
        with open(filename,"w+") as file:
            file.write("Freq Z' Z'' \n")
            for i in range(len(om)):
                file.write("{} {} {} \n".format(freq[i], zdata.real[i], zdata.imag[i]))

##The Gaver-Stehfest Method for numerical inverse laplace transform
def csteh(n,i):
    fact = sp.special.factorial
    acc = 0.0
    for k in range(int(np.floor((i+1)/2.0)), int(min(i, n/2.0))+1):
        num = k**(n/2.0) * fact(2 * k)
        den = fact(i - k) * fact(k -1) * fact(k) * fact(2*k - i) * fact(n/2.0 - k)
        acc += (num /den)
    expo = i+n/2.0
    term = np.power(-1+0.0j,expo)
    res = term * acc
    return res.real

def numinvlap(F, t,n):
    acc = 0.0
    lton2 = np.log(2)/t
    for i in range(1, n+1):
        a = csteh(n,i)
        b = F(i*lton2)
        acc += (a * b)
    return lton2 * acc


#Class to do galvanostatic experiments with the stehfest method
class Galvanostatic(object):
    
    def __init__(self,model,parameters):
        self.model = model
        self.parameters = parameters
        self.output = None
        self.time = None
    
    def run(self,time,Iapp,V0,A=1.0,Nterms=10):
        self.time = time

        #Define the function to invert
        def f(s):
            return V0/s+Iapp*self.model(s,self.parameters)/(s*A)
        
        self.output = numinvlap(f,time,Nterms)

    #Obtaining the output
    def get_output(self):
        return (self.time, self.output)
    
    #Saving the output
    def save_output(self,filename):
        np.savetxt(filename,(self.time,self.output))
        with open(filename,"w+") as file:
            file.write("Time Voltage \n")
            for i in range(len(self.time)):
                file.write("{} {} \n".format(self.time[i], self.output[i]))
