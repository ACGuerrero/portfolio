from qiskit import IBMQ,execute,BasicAer,Aer,transpile,assemble
from qiskit.providers.aer.noise import NoiseModel
from qiskit.tools.monitor import job_monitor
from qiskit.providers.ibmq import least_busy
provider=IBMQ.load_account()

def Simulate_QASM(n,circ):    
    backend = BasicAer.get_backend('qasm_simulator')
    tomography=execute(circ,backend,shots=n)
    counts = tomography.result().get_counts()
    return counts

def Simulate_Noisy_QASM(n,circ):  
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
    return counts

def Send_IBMQ(n,circ):
    provider = IBMQ.get_provider(hub='ibm-q')
    backend = least_busy(provider.backends(filters=lambda b: b.configuration().n_qubits >= 3 and
                                   not b.configuration().simulator and b.status().operational==True))
    tomography = execute(circ, backend=backend, shots=n)
    job_monitor(tomography)
    counts = tomography.result().get_counts()
    return counts
