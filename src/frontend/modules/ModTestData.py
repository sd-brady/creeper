# Test Data class that includes calculation of strain for md model

from numpy import exp,sinh,log10,zeros_like,diff

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

