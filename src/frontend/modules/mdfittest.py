# Test fitting a mdmodel from testdata
# Functions to do calculations and fits with mdmodel class

from mdmodel import MdModel, MdTableModel
from unit_system import UnitSystem
from numpy import exp,sinh,log10,zeros_like,diff
from time import perf_counter
from scipy.optimize import curve_fit
from scipy.stats import linregress
import matplotlib.pyplot as pl

# Redefine TestData class to include all of the values to calc strain and strainrate predicted by mdmodel
class TestData:
    def __init__(
        self,
        time_list: list,
        strain_list: list,
        stress_list: list,
        temperature_list: list,
        ):
        self.time = time_list
        self.strain = strain_list
        self.stress = stress_list
        self.temperature = temperature_list
        self.strainrate=self.get_strainrate()
    
    # Get Strain Rate from testdata
    def get_strainrate(self):
        return diff(self.strain)/diff(self.time)

    # Heavyside Function
    def H(self,v):
        if v<=0:
            return 0.0
        else:
            return 1.0

    # Get predicted strain rate from MD Model Parameters
    # def MDstrain(self,time,mdmodel):
    def MDstrain(self,time,a1,n1,q1divr,a2,n2,q2divr,b1,b2,q,sig0,k0,m,c,alpha,beta,delta,mu):
        # Create array for strain
        eps=zeros_like(time)
        zeta=0
        # Loop through input times to calculate strain
        for i in range(1,len(time),1):
            # Calcualte steady-state strain limit 
            epss = a1*exp(-q1divr/self.temperature[i])*(self.stress[i]/mu)**n1 + a2 * exp(-q2divr/self.temperature[i])*(self.stress[i]/mu)**n2 + H(self.stress[i]-sig0)*(b1 * exp(-q1divr/self.temperature[i])  + b2 * exp(-q2divr/self.temperature[i])) * sinh(q * ((self.stress[i]- sig0)/mu))
            # Calculate transient strian limit epsilon star
            epsstar=k0*exp(c*self.temperature[i])*(self.stress[i]/mu)**m
            # Calculate delta
            delta = alpha + beta * log10(self.stress[i]/ mu)
            dt=self.time[i]-self.time[i-1]
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

# Define function to take in MDTableModel and testdata and return best fit model and errors
def mdfit(testdata:TestData,mdtable:MdTableModel):

    fixtol=1+1e-6

    fm=mdtable.flag_model
    flags=[fm.a1_flag,fm.n1_flag,fm.q1divr_flag,fm.a2_flag,fm.n2_flag,fm.q2divr_flag,fm.b1_flag,fm.b2_flag,fm.q_flag,fm.sig0_flag,fm.k0_flag,fm.m_flag,fm.c_flag,fm.alpha_flag,fm.beta_flag,fm.delta_flag,fm.mu_flag]
    valm=mdtable.val_model
    valmv=[valm.a1,valm.n1,valm.q1divr,valm.a2,valm.n2,valm.q2divr,valm.b1,valm.b2,valm.q,valm.sig0,valm.k0,valm.m,valm.c,valm.alpha,valm.beta,valm.delta,valm.mu]
    minm=mdtable.min_model
    minmv=[minm.a1,minm.n1,minm.q1divr,minm.a2,minm.n2,minm.q2divr,minm.b1,minm.b2,minm.q,minm.sig0,minm.k0,minm.m,minm.c,minm.alpha,minm.beta,minm.delta,minm.mu]
    maxm=mdtable.max_model
    maxmv=[maxm.a1,maxm.n1,maxm.q1divr,maxm.a2,maxm.n2,maxm.q2divr,maxm.b1,maxm.b2,maxm.q,maxm.sig0,maxm.k0,maxm.m,maxm.c,maxm.alpha,maxm.beta,maxm.delta,maxm.mu]
    
    mdbounds=[minmv,maxmv]

    for i,(v,flag) in enumerate(zip(valmv,flags)):
        if flag==False:
            mdbounds[0,i]=v
            mdbounds[1,i]=v*fixtol

    popt, pcov = curve_fit(testdata.MDstrain,testdata.time,testdata.strain,p0=valmv,bounds=mdbounds)

    r_value  = linregress(testdata.strain, testdata.MDstrain(testdata.time, *popt))[2]
    
    fitmodel=MdModel()
    fitmodel.set_custom_vals_units(popt[0],popt[1],popt[2],popt[3],popt[4],popt[5],popt[6],popt[7],popt[8],popt[9],popt[10],popt[11],popt[12],popt[13],popt[14],popt[15],popt[16],valm.unit_system)

    return fitmodel,r_value





# Read in a test and declare a testdata class



# Create a Test class


# Create a mdmodel class and set it with soft salt values to test




# Give 
