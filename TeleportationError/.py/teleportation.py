"""
Este código realiza teleportación cuántica
"""

from qiskit import QuantumCircuit
from qiskit.extensions import Initialize
from qiskit_textbook.tools import random_state
import measure

def Bell_Pair(qc,q1,q2):
    qc.h(q1)
    qc.cx(q1,q2)

def Alice(qc,psi,q1):
    qc.cx(psi,q1)
    qc.h(psi)

def Bob(qc,psi,q1,q2):
    qc.cx(q1, q2) 
    qc.cz(psi, q2)
    
def Teleport():      
    qcx = QuantumCircuit(3,1)
    qcy = QuantumCircuit(3,1)
    qcz = QuantumCircuit(3,1)
    qt_axis=[qcx,qcy,qcz]


    psi = random_state(1) #crea un estado aleatorio
    init_gate = Initialize(psi) #la compuerta de inicializacion lleva el estado a psi
    init_gate.label = "Estado aleatorio" #nombra la compuerta

#Nombre de los qubits: 
    qpsi=0
    qA=1
    qB=2
    c=0

#Inicialización del qubit de Alice, en los tres circuitos, usando el mismo psi
    qcx.append(init_gate, [qpsi])
    qcx.barrier()
    qcy.append(init_gate, [qpsi])
    qcy.barrier()
    qcz.append(init_gate, [qpsi])
    qcz.barrier()


#Proceso de Teleportación: creación del par de Bell
    Bell_Pair(qcx, qA, qB)
    qcx.barrier()
    Bell_Pair(qcy, qA, qB)
    qcy.barrier()
    Bell_Pair(qcz, qA, qB)
    qcz.barrier()


#Aplicación de compuertas al qubit de Alice
    Alice(qcx, qpsi, qA)
    qcx.barrier()
    Alice(qcy, qpsi, qA)
    qcy.barrier()
    Alice(qcz, qpsi, qA)
    qcz.barrier()


#Aplicación controlada de compuertas al qubit de Bob
    Bob(qcx, qpsi, qA, qB)
    qcx.barrier()
    Bob(qcy, qpsi, qA, qB)
    qcy.barrier()
    Bob(qcz, qpsi, qA, qB)
    qcz.barrier()

#Proceso de medición en cada eje
    measure.X(qcx,qB,c)
    measure.Y(qcy,qB,c)
    measure.Z(qcz,qB,c)
    return qt_axis,psi
#display(qcx.draw(output='mpl'),qcy.draw(output='mpl'),qcz.draw(output='mpl'))