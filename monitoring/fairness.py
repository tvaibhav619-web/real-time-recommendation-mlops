def gini(values):
    values = sorted(values)
    n = len(values)
    return sum((2*i-n-1)*v for i,v in enumerate(values)) / (n*sum(values))
