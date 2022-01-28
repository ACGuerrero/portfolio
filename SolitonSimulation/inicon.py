import numpy as np

def GaussInit(u,n,dx,dt,c,tau):
    a=np.sqrt((-2/np.sqrt(2))*np.log(2*dt/c))
    for j in range(n):
        u[j,tau]=c*np.exp(np.sqrt(c)*(-(dx*j-a-c*tau*dt)**2)/2)/2
    return a

def CoshInit(u,n,dx,dt,c,tau):
    a=2/np.sqrt(c)*np.arccosh(np.sqrt(c/(2*(0.5*dt))))
    for j in range(n):
        u[j,tau]=(c/2)/(np.cosh( (np.sqrt(c)/2)*(dx*j-a-c*tau*dt) ))**2
    return a

def CosInit(u,n,dx,dt,c,tau):
    for j in range(n):
        u[j,tau]=c*np.cos(np.pi*dx*j)/2
    return