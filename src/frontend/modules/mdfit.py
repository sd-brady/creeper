# Function to Fit MD model given Test Data Class and MdTableModel Class

from mdmodel import MdModel, MdTableModel
from ModTestData import TestData
from scipy.optimize import curve_fit
from scipy.stats import linregress

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



