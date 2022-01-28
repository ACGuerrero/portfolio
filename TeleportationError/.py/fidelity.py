"""
Funciones para la tomografía
"""
import numpy as np
import pauli


def ProbVect(counts,n):
    p=[] #aqui van las probabilidades de cada resultado (0 en x, 1 en x, 0 en y...)
    l=["0","1"] 
    for i in range(len(counts)):
        for j in range(len(l)):
            if l[j] in counts[i]: #Si "0" está en el diccionario
                p.append(counts[i][l[j]]/n) #mete la probabilidad
            else:
                p.append(0) #si no, mete 0
    p=np.array(p)
    r=np.array([p[0]-p[1], p[2]-p[3], p[4]-p[5]]) #vector de diferencias
    return r
    
def KetBra(phi):
    ket=np.array([phi]).T
    bra=np.array([phi]).conj()
    return ket,bra

def Density(psi):
    ket,bra=KetBra(psi)
    dens=np.matmul(ket,bra)
    return dens

def Build_Density(counts,n): 
    r=ProbVect(counts,n)
    rho=(pauli.I+r[0]*pauli.X+r[1]*pauli.Y+r[2]*pauli.Z)/2 #matriz de densidad
    return rho

def Purity(rho): #calcula la pureza de rho
    rho2=np.matmul(rho,rho)
    purity=np.trace(rho2)
    return purity

def Fidelity(rho,phi): #calcula la fidelidad de rho respecto a phi
    ket,bra=KetBra(phi)
    F=np.matmul(bra,np.matmul(rho,ket))
    return np.real(F[0][0])

def DeployFIPU(counts,n,phi):
    #plot_histogram(counts)
    rho=Build_Density(counts,n)
    Fid=Fidelity(rho,phi)
    Pur=Purity(rho)
    print ('la matriz de densidad del estado original:')
    print(KetBra(phi))
    print('La matriz de densidad del estado final:')
    print(rho)
    print('La fidelidad es:',Fid)
    print('La pureza es:', Pur)
    return rho,Density(phi)
