
#============================================================================================================================
#   Libraries
#============================================================================================================================
from numpy import exp,sinh,log10,zeros_like
from time import perf_counter
import pandas as pd
from scipy.optimize import curve_fit
from scipy.stats import linregress
import matplotlib.pyplot as plt

#============================================================================================================================
#  Read in single Test to Fit
#============================================================================================================================

class cmstest:
    def __init__(self) :
        data=pd.read_csv('cmsexample.csv')
        # print(data)
        self.time=data['time'].astype(float)
        self.eps=data['eps'].astype(float)
        self.sige=data['sige'].astype(float)
        self.tabs=data['Tabs'].astype(float)
        self.q1r=12589 #K
        self.q2r=5035.5 #K
        self.q=5335
        self.sig0=20.57 #MPa
        self.c=0.009198 #1/K
        self.delta=0.58
        self.mu=12400 #MPa

    def H(self,v):
        if v<=0:
            return 0.0
        else:
            return 1.0
    
    def MDeps(self,time,a1,n1,a2,n2,b1,b2,k0,m,alpha,beta):
        # Create array for strain
        eps=zeros_like(time)
        zeta=0
        # Loop through input times to calculate strain
        for i in range(1,len(time),1):
            # Calcualte steady-state strain limit 
            epss = a1*exp(-self.q1r/self.tabs[i])*(self.sige[i]/self.mu)**n1 + a2 * exp(-self.q2r/self.tabs[i])*(self.sige[i]/ self.mu)**n2 + \
                self.H(self.sige[i]-self.sig0)*(b1 * exp(-self.q1r/self.tabs[i])  + b2 * exp(-self.q2r/self.tabs[i])) * sinh(self.q * ((self.sige[i]- self.sig0)/self.mu))
            # Calculate transient strian limit epsilon star
            epsstar=k0*exp(self.c*self.tabs[i])*(self.sige[i]/self.mu)**m
            # Calculate delta
            delta = alpha + beta * log10(self.sige[i]/ self.mu)
            dt=time[i]-time[i-1]
            # Piece-wise factor formula
            if zeta<epsstar:
                F=exp(delta*(1.0-zeta/epsstar)**2)
            elif zeta==epsstar:
                F=1.0
            elif zeta<epsstar:
                F=exp(-delta*(1.0-zeta/epsstar)**2)
            epseqv=F*epss
            eps[i]=dt*epseqv+eps[i-1]
            # Calculate state variable zeta
            zetadt=(F-1.0)*epss
            zeta=zeta+dt*zetadt
        return eps

cms=cmstest()




#============================================================================================================================
#   Sciopt Curve Fit Trial and Time
#============================================================================================================================
t1_start = perf_counter()
initialguess=(8.480000e+27,5.50,9.780000e+17,5.00,6.150000e+11,3.070000e+03,627500.000,3.000,-17.370,-7.738)
mdbounds=((1e26,2,1e16,2,1e10,1e3,1e5,2,-20,-10),(1e28,7,1e19,7,1e12,1e4,1e7,6,20,10))

popt, pcov = curve_fit(cms.MDeps,cms.time,cms.eps,p0=initialguess,bounds=mdbounds)

t1_end = perf_counter()
print(f"Elapsed time during the whole program in seconds:{t1_end-t1_start}")

#============================================================================================================================
#   Calculate r^2 
#============================================================================================================================
r_value  = linregress(cms.eps, cms.MDeps(cms.time, *popt))[2]
print(f"true: {r_value**2}")

#============================================================================================================================
#  Print Values 
#============================================================================================================================
print("Munson Dawson Params:\na1=%1.5e\nn1=%5.3f\na2=%1.5e\nn2=%5.3f\nb1=%1.5e\nb2=%1.5e\nk0=%1.5e\nm=%5.3f\nalpha=%5.3f\nbeta=%5.3f" % tuple(popt))


#============================================================================================================================
# Plot them 
#============================================================================================================================

plt.plot(cms.time,cms.eps, 'b', label="data")
plt.plot(cms.time, cms.MDeps(cms.time, *popt), 'r-',label='fit')
plt.xlabel('Time (days)')
plt.ylabel('Axial Strain (-)')
plt.grid(True)
plt.legend()
plt.show()


#============================================================================================================================
#   Define Constant Mean Stress Test
#============================================================================================================================
# class cmstest:
#     def __init__(self,file):
#         self.read(file)
#         self.effstressx={'MPa': np.linspace(1,100,100),
#             'psi': np.linspace(100,10000,100),
#             'psf': np.linspace(10000,1000000,100)}
#         self.d['Test']="bla"
#         return
#             
#     def read(self,file):
#         self.d = json.load(open(file,'r'))
#         return
#
#     def write(self,file):
#         json.dump(self.d, open(file,'w'), indent=4)
#         return
#
#     def unifyunits(self,su,teu,tiu):
#         return
#
#     # def SS():
#     #     error=sum(self.)
#     #     return error
#     
#     # def fit(self):
#     #     # Values to fit to A1,A2,B1,B2 is gamma multiplied by equivalent hard salt parameters
#     #     # Change values of alpha (<=-0.001) k and gamma (>=0) using grg nonlinear solver to minimize sum of squares of differences between fit and data
#     #     scipy.optimize.minimize(self.SS, x0, args=(), method=None, jac=None, hess=None, hessp=None, bounds=None, constraints=(), tol=None, callback=None, options=None)
#     #     return
#     
# def H(self,v):
#     if v<=0:
#         return 0.0
#     else:
#         return 1.0
#
# def calcEpsilon(self,time,sigE,Tabs):
#     # Create array for strain
#     eps=np.zeros_like(time)
#     zeta=0
#     # Loop through input times to calculate strain
#     for i in range(1,len(time),1):
#         # Calcualte steady-state strain limit 
#         epss = self.a1*np.exp(-self.q1r/Tabs)*(sige[i]/self.mu)**self.n1 + self.a2 * np.exp(-self.q2r/Tabs)*(sige[i]/ self.mu)**self.n2 + \
#             self.H(sige[i]-self.sig)*(self.b1 * np.exp(-self.q1r/Tabs)  + self.b2 * np.exp(-self.q2r/Tabs)) * np.sinh(self.q * ((sige[i]- self.sig)/self.mu))
#         # Calculate transient strian limit epsilon star
#         epsstar=self.k*np.exp(self.c*Tabs)*(sige[i]/self.mu)**self.m
#         # Calculate delta
#         delta = self.alpha + self.beta * np.log10(sige[i]/ self.mu)
#         dt=time[i]-time[i-1]
#         # Piece-wise factor formula
#         if zeta<epsstar:
#             F=np.exp(delta*(1.0-zeta/epsstar)**2)
#         elif zeta==epsstar:
#             F=1.0
#         elif zeta<epsstar:
#             F=np.exp(-delta*(1.0-zeta/epsstar)**2)
#         epseqv=F*epss
#         eps[i]=dt*epseqv+eps[i-1]
#         # Calculate state variable zeta
#         zetadt=(F-1.0)*epss
#         zeta=zeta+dt*zetadt
#     return eps
#
# def calcEpsilonSS(self):
#     sigmas=self.effstressx[stressunit]
#     #   Steady State Strain Rate vs Effective Stress
#     T=cu.temp(temp,tempunit,self.tempunit)
#     ess=[]
#     for se in sigmas:
#         ess.append(self.a1*np.exp(-self.q1r/T)*(se/self.mu)**self.n1+self.a2*np.exp(-self.q2r/T)*(se/self.mu)**self.n2+(self.b1*np.exp(-self.q1r/T)+self.b2*np.exp(-self.q2r/T))*np.sinh(self.q*(se-self.sig)/self.mu)*self.H(se-self.sig))
#     return ess
#
# def calcEpsilonStar(self):
#     sigmas=self.effstressx[stressunit]
#     #   Transient Strain Limit vs Effective Stress
#     epsstar=[]
#     T=cu.temp(temp,tempunit,self.tempunit)
#     for se in sigmas:
#         epsstar.append(self.k*np.exp(self.c*T)*(se/self.mu)**self.m)
#     return epsstar
#
# def calcDelta(self):
#     sigmas=self.effstressx[stressunit]
#     #   Delta vs Effective Stress
#     delta=[]
#     for se in sigmas:
#         delta.append(self.alpha+self.beta*np.log10(se/self.mu))
#     return delta
#
# test=cmstest("WEST7_4342.18.cms")
# test.write("WEST7_4342.182.cms")
# test.read("WEST7_4342.18.cms")

# print(test.d.keys())
# # print(cu.temp(0,"C","K"))
#
#

#         self.depth=tempf2[0][9][-7:]
#         self.effstress=float(tempf2[0][21][15:23])
#         self.temp=float(tempf2[0][20][15:23])+273.15
#         self.name=str(round(self.effstress*145.0377377))+'psi - '+str(round(((self.temp-273.15)*1.8)+32,1))+'F - '+self.depth[-9:-2]+'ft'
#         self.time=np.array(data['time'])/(3600*24)
#         self.sige=np.array(data['sig1'])-np.array(data['sig3'])
#         self.eps1=np.array(data['eps1'])
#         self.modulus=float(tempf2[0][61])
#         self.stressunit='MPa'
#         self.timeunit='day'
#         self.tempunit='K'
#         # Subtract Elastic Strain From Creep Strain
#         for e in range(len(self.time)-1):
#             if np.abs(self.effstress-self.sige[e])<0.01:
#                 self.eps1load=self.eps1[e]
#                 self.tstart=self.time[e]
#                 break
#         self.KronDelta=(self.eps1load-(self.effstress/self.modulus))
#         self.eps1C=self.eps1[e:]-self.KronDelta
#         self.timeC=self.time[e:]-self.tstart
#         # Calculate Steady State Strain Rate
#         mp=0
#         for i in range(len(self.time)):
#             m,b = np.polyfit(self.timeC[i:],self.eps1C[i:],1)
#             if np.abs((m-mp)/m)<0.00001:
#                 break
#             mp=m
#         print(self.timeC[i])
#         self.ess=m
#         # Calculate Estar
#         self.estar=-self.ess*self.timeC[-1]+self.eps1C[-1]
#         # Calculate Delta
#         self.delta=5

# #============================================================================================================================
# #   Define MD Fit Class
# #============================================================================================================================
# class mdfit:
#     def __init__(self,name,params,stressunit,timeunit,tempunit):
#         self.name=name
#         self.a1=float(params[0])
#         self.n1=float(params[1])
#         self.q1r=float(params[2])
#         self.a2=float(params[3])
#         self.n2=float(params[4])
#         self.q2r=float(params[5])
#         self.b1=float(params[6])
#         self.b2=float(params[7])
#         self.q=float(params[8])
#         self.sig=float(params[9])
#         self.k=float(params[10])
#         self.m=float(params[11])
#         self.c=float(params[12])
#         self.alpha=float(params[13])
#         self.beta=float(params[14])
#         self.delta=float(params[15])
#         self.mu=float(params[16])
#         self.stressunit=stressunit
#         self.timeunit=timeunit
#         self.tempunit=tempunit
#         self.effstressx={'MPa': np.linspace(1,100,100),
#             'psi': np.linspace(100,10000,100),
#             'psf': np.linspace(10000,1000000,100)}
    
#     def H(self,v):
#         if v<=0:
#             return 0.0
#         else:
#             return 1.0
    
#     def getplt1data(self,time,sige,Tabs):
#         # Create array for strain
#         eps=np.zeros_like(time)
#         zeta=0
#         # Loop through input times to calculate strain
#         for i in range(1,len(time),1):
#             # Calcualte steady-state strain limit 
#             epss = self.a1*np.exp(-self.q1r/Tabs)*(sige[i]/self.mu)**self.n1 + self.a2 * np.exp(-self.q2r/Tabs)*(sige[i]/ self.mu)**self.n2 +  self.H(sige[i]-self.sig)*(self.b1 * np.exp(-self.q1r/Tabs)  + self.b2 * np.exp(-self.q2r/Tabs)) * np.sinh(self.q * ((sige[i]- self.sig)/self.mu))
#             # Calculate transient strian limit epsilon star
#             epsstar=self.k*np.exp(self.c*Tabs)*(sige[i]/self.mu)**self.m
#             # Calculate delta
#             delta = self.alpha + self.beta * np.log10(sige[i]/ self.mu)
#             dt=time[i]-time[i-1]
#             # Piece-wise factor formula
#             if zeta<epsstar:
#                 F=np.exp(delta*(1.0-zeta/epsstar)**2)
#             elif zeta==epsstar:
#                 F=1.0
#             elif zeta<epsstar:
#                 F=np.exp(-delta*(1.0-zeta/epsstar)**2)
#             epseqv=F*epss
#             eps[i]=dt*epseqv+eps[i-1]
#             # Calculate state variable zeta
#             zetadt=(F-1.0)*epss
#             zeta=zeta+dt*zetadt
#         return eps

#     def getplt2data(self,stressunit,temp,tempunit):
#         sigmas=self.effstressx[stressunit]
#         #   Steady State Strain Rate vs Effective Stress
#         T=convertTemp(temp,tempunit,self.tempunit)
#         ess=[]
#         for se in sigmas:
#             ess.append(self.a1*np.exp(-self.q1r/T)*(se/self.mu)**self.n1+self.a2*np.exp(-self.q2r/T)*(se/self.mu)**self.n2+(self.b1*np.exp(-self.q1r/T)+self.b2*np.exp(-self.q2r/T))*np.sinh(self.q*(se-self.sig)/self.mu)*self.H(se-self.sig))
#         return ess
    
#     def getplt3data(self,stressunit,temp,tempunit):
#         sigmas=self.effstressx[stressunit]
#         #   Transient Strain Limit vs Effective Stress
#         epsstar=[]
#         T=convertTemp(temp,tempunit,self.tempunit)
#         for se in sigmas:
#             epsstar.append(self.k*np.exp(self.c*T)*(se/self.mu)**self.m)
#         return epsstar

#     def getplt4data(self,stressunit):
#         sigmas=self.effstressx[stressunit]
#         #   Delta vs Effective Stress
#         delta=[]
#         for se in sigmas:
#             delta.append(self.alpha+self.beta*np.log10(se/self.mu))
#         return delta
