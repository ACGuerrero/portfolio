from qiskit import Aer, IBMQ, execute,BasicAer,transpile,assemble
from qiskit.providers.aer.noise import NoiseModel
import numpy as np
import fidelity as fid

provider=IBMQ.load_account()

def StdD(n,circ):
    backend = BasicAer.get_backend('qasm_simulator')
    tomography=execute(circ,backend,shots=n)
    counts = tomography.result().get_counts()
    r=fid.ProbVect(counts,n)
    return r

def Noisy_StdD(n,circ):  
    simulator=Aer.get_backend('qasm_simulator')
    backend = provider.get_backend('ibmq_santiago')
    noise_model=NoiseModel.from_backend(backend)
    coupling_map = backend.configuration().coupling_map
    basis_gates = noise_model.basis_gates
    transpiled=transpile(circ,backend,optimization_level=3)
    assembled=assemble(transpiled,shots=n)
    sim_job=simulator.run(assembled,coupling_map=coupling_map,basis_gates=basis_gates,noise_model=noise_model)
    sim_result=sim_job.result()
    counts=sim_result.get_counts()
    r=fid.ProbVect(counts,n)
    return r

def Dist(n,m,l,circ,var):
    stdr=[]
    if var=='x':
        a=0
    elif var=='y':
        a=1
    elif var=='z':
        a=2
    else:
        print('wrong variable, must be x, y or z')
        return
    for i in range(1,n+1):
        tra=[]
        for j in range(m):    
            r=StdD(i*l,circ)
            tra.append(r[a])
        stdr.append(np.std(tra))
        print('Std point: ',i)
    return stdr

def Noisy_Dist(n,m,l,circ,var):
    stdr=[]
    if var=='x':
        a=0
    elif var=='y':
        a=1
    elif var=='z':
        a=2
    else:
        print('wrong variable, must be x, y or z')
        return
    for i in range(1,n+1):
        tra=[]
        for j in range(m):    
            r=Noisy_StdD(i*l,circ)
            tra.append(r[a])
        stdr.append(np.std(tra))
        print('Noisy std point: ', i)
    return stdr



