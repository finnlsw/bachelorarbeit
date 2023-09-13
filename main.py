#am besten hier alles zusammenführen
import numpy as np
l=550e-9 #lambda
dx1=1.9 #delta x for 10cm
dx2=1.2 #delta x for 20cm
sc1=3.71 #imagescale for 10cm
sc2=2.11
d1=l/(dx1*sc1)*180/np.pi*60*1000 #*1000 for mm
d2=l/(dx2*sc2)*180/np.pi*60*1000
#print("d1 =",d1,"mm")
#print("d2 =",d2,"mm")

from matplotlib import pyplot as plt

x=np.linspace(0,10,100)
plt.plot(x,np.sin(x))
plt.show()
