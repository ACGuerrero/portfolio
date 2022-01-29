# -*- coding: utf-8 -*-
"""
Este codigo resuelve la ecuación de Burgers
"""
import numpy as np
import matplotlib.pyplot as plt
from inicon import GaussInit, CoshInit
from scipy import integrate

def Phi(x):
    return (x**2)/2

print('This program solves de Burgers equation using two finite difference schemes')

dx=0.1
cl=30
nu=0.0
n=int(cl/dx)
totaltime=1
c=8 #soliton speed
dt=0.00001
p=int(totaltime/dt)
#U=U(x,t)
u=np.zeros((n,p))
u=np.zeros((n,p))

print('Do you want to use \n 1. a gaussian c.i. \n 2 an cosh c.i.')
ci=int(input())
if (ci==1):
    a = GaussInit(u,n,dx,dt,c,0)
elif (ci==2):
    a = CoshInit(u,n,dx,dt,c,0)
else:
     print('Invalid choice')
nmax=int(c*n-2*a*c/dx)
solint=int(a/dx)
k=0
cuenta=0
print('Do you want to use \n 1. Zabusky scheme \n 2. my own ')


scheme=int(input())
if (scheme==1):
    if (ci==1):
        a = GaussInit(u,n,dx,dt,c,1)
    elif (ci==2):
        a = CoshInit(u,n,dx,dt,c,1)
    for m in range (1,p-1) :
        cuenta+=0.001
        posicion=int(cuenta)
        if (True in (u[:,m]>1.05*c/2)):
            break
        for j in range(posicion,2*solint+posicion):
               u[j,m+1]=u[j,m-1]-2*(dt/dx)*(u[j+1,m]+u[j,m]+u[j-1,m])*(u[j+1,m]-u[j-1,m])+nu*(dt/dx**2)*(u[j+1,m]-2*u[j,m]+u[j-1,m])
        k+=1
       
elif (scheme==2):
    for m in range (p-1) :
        cuenta+=0.001
        posicion=int(cuenta)
        if (True in (u[:,m]>1.05*c/2)):
            break
        for j in range(posicion,2*solint+posicion):
            u[j,m+1]=u[j,m]-(dt/dx)*( Phi(u[j,m])-Phi(u[j-1,m]) )+nu*(dt/dx**2)*(u[j+1,m]-2*u[j,m]+u[j-1,m])
        k+=1
print('Numero de pasos antes de que se rompiera:',k)
canal=np.arange(0,cl,cl/n)
intervalo=np.arange(0,k*dt,dt)

def grafica():
    ki=0
    km=int(k/2)
    kf=int(k-1)
    dti=dt*ki
    dtm=dt*km
    dtf= dt*kf
    plt.plot(canal,u[:,ki],'k-',label=('t=%s' % dti))
    plt.plot(canal,u[:,km],'k--',label=('t=%s' % dtm))
    plt.plot(canal,u[:,kf],'k-.',label=('t=%s' % dtf))
    plt.xlim(5,10)
    plt.title('c=%f'%c)
    plt.legend()
    plt.show()    
    
def graficauno(t):
    dti=t*dt
    plt.plot(canal,u[:,t],'k-',label=('t=%s' % dti))
    plt.xlim(5,10)
    plt.title('c=%f'%c)
    plt.legend()
    plt.show()

def SurGraph():
    intervalo=np.arange(0,k*dt,dt)
    ny = len(intervalo)
    y = np.arange(0,cl/2,dx)
    nx=len(y)
    x = intervalo
    Z = u[0:nx,0:ny]
    hf = plt.figure()
    ha = hf.add_subplot(111, projection='3d')
    X, Y = np.meshgrid(x, y)
    ha.plot_surface(X, Y, Z, cmap='viridis')
    plt.show()
    
grafica()
#SurGraph()


u2i=np.square(u[:,0])
u2m=np.square(u[:,int(k/2)])
u2f=np.square(u[:,k-1])

poweri=integrate.simps(u2i,canal)
powerm=integrate.simps(u2m,canal)
powerf=integrate.simps(u2f,canal)


u3i=np.power(u[:,0],3)
u3m=np.power(u[:,int(k/2)],3)
u3f=np.power(u[:,k-1],3)

integrandi=u3i
integrandm=u3m
integrandf=u3f
hami=integrate.simps(integrandi,canal)
hamm=integrate.simps(integrandm,canal)
hamf=integrate.simps(integrandf,canal)
print(poweri,powerm,powerf)
print(hami,hamm,hamf)