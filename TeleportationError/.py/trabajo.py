from qiskit import QuantumCircuit
from qiskit.extensions import Initialize
from qiskit_textbook.tools import random_state
import measure
import numpy as np
import std
import teleportation as tel
import matplotlib.pyplot as plt
import depcounts as dp
import fidelity as fid

def Preparado():
    qcx = QuantumCircuit(1,1)
    qcy = QuantumCircuit(1,1)
    qcz = QuantumCircuit(1,1)
    qt_axis=[qcx,qcy,qcz]
    psi = random_state(1) #crea un estado aleatorio
    init_gate = Initialize(psi) #la compuerta de inicializacion lleva el estado a psi
    init_gate.label = "Estado aleatorio" #nombra la compuerta
    qpsi=0
    c=0
    #Inicialización del qubit en los tres circuitos
    qcx.append(init_gate, [qpsi])
    qcx.barrier()
    qcy.append(init_gate, [qpsi])
    qcy.barrier()
    qcz.append(init_gate, [qpsi])
    qcz.barrier()
    #mediciones en las tres direcciones
    measure.X(qcx,qpsi,c)
    measure.Y(qcy,qpsi,c)
    measure.Z(qcz,qpsi,c)
    return qt_axis,psi
"""
n=20 #numero de puntos de la grafica
m=100 #cuantas veces se corre para aplicación del teorema del límite central
l=500 #el paso que se da en la cantidad de experimentos corridos, n*l será el número máximo
#n=50 m=200 l=200 
"""

def FidGraph(n,m,l,circ,psi):
    grfid=[]
    for i in range(1,n+1):
        arfid=[]
        for k in range(m):
            counts=dp.Simulate_QASM(l*i, circ)
            rho=fid.Build_Density(counts, l*i)
            fidel=fid.Fidelity(rho, psi)
            arfid.append(fidel)
        avgfid=np.average(arfid)
        print("Fidelity point calculated: ",i)
        grfid.append(avgfid)
    return grfid
def NoisyFidGraph(n,m,l,circ,psi):
    grfid=[]
    for i in range(1,n+1):
        arfid=[]
        for k in range(m):
            counts=dp.Simulate_Noisy_QASM(l*i, circ)
            rho=fid.Build_Density(counts, l*i)
            fidel=fid.Fidelity(rho, psi)
            arfid.append(fidel)
        avgfid=np.average(arfid)
        print("Noisy fidelity point calculated: ",i)
        grfid.append(avgfid)
    return grfid

    

n=20 #numero de puntos de la grafica
m=60 #cuantas veces se corre para sacar promedio de fidelidad dados l*n shots
l=500 #el paso que se da en la cantidad de experimentos corridos, n*l será el número máximo

qt_axis,psi=tel.Teleport()
#qt_axis,psi=Preparado()
Fide=FidGraph(n,m,l,qt_axis,psi)
NoFide=NoisyFidGraph(n,m,l,qt_axis,psi)
#NoisyStdGr=std.Noisy_Dist(n,m,l,qt_axis,'y')
#StdGr=std.Dist(n,m,l,qt_axis,'y')
lx=np.arange(l,l*(n+1),l)
#plt.plot(lx,1/np.sqrt(lx),'k',label=r'$1/\sqrt{n}$')
plt.plot(lx,Fide,'k--',label='Modelo sin ruido')
plt.plot(lx,NoFide,'k-.',label='Modelo ibmq_santiago')
plt.xlabel('n')
plt.ylabel(r'$F(n)$')
plt.legend()
plt.show()