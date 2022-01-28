def X(qc,q2,c):
    qc.h(q2)
    qc.measure(q2,c)

def Y(qc,q2,c):
    qc.sdg(q2)
    qc.h(q2)
    qc.measure(q2,c)

def Z(qc,q2,c):
    qc.measure(q2,c)