# implement the calculation of the jaccard distance

import numpy as np
import numba as nb
import opencl_matrix as om
"""
def jaccard(a, b):
    
    info: calculate the jaccard distance between two strings
    input: strings a, b
    output: float: jaccard distance value # or double?
    
    aSet = list()
    bSet = list()
     
    d = -1
    if not (len(a) == len(b)):
        d = 1
    else:
        for i in range(len(a)-1):
            aSet.append(a[i:i+2])
        for i in range(len(b)-1):
            bSet.append(b[i:i+2])

        print("\n aSet: ", aSet)
        print("\n bSet: ", bSet)
        
        U = np.union1d(aSet, bSet)
        I = np.intersect1d(aSet, bSet)
        
        print("\n len(U): ", len(U))
        print("\n len(I): ", len(I))
        d = 1 - len(I)/len(U)
    return d
"""
def make_el_matrix(strings):
    """
    info: make the elemente matrix
    input: strings: list of strings
    output: el_matrix
    """
    # How exactly should we deal with strings, which contain e.g. "GS" two times? Is it okay to just count that as one element?
    el_matrix = {}
    """
        try:
            if len(nets[seqElIndex]) < lMax:
                nets[seqElIndex].append(seqEl)

        except:
            nets[seqElIndex] = []
            nets[seqElIndex].append(seqEl)
    """
    for i in range(len(strings)):
        s = strings[i]
        for j in range(len(s)-1):
            el = s[j:j+2]
            try:
                if len(el_matrix[el]) < i+1:
                    el_matrix[el].append(1)
            except:
                el_matrix[el] = [0]*i  # i or i-1?
                el_matrix[el].append(1)
        for j in range(len(el_matrix)):
            el = list(el_matrix.values())[j]
            if len(el) == i+1:
                pass
            elif len(el) == i:
                el.append(0)
                list(el_matrix.values())[j] = el
            else: 
                print("\n That is really strange: el in el_matrix has a wrong length while building")
    
    matrix_pre = list(el_matrix.values())
    matrix = np.matrix(matrix_pre)
    return matrix

def jaccard(strings):
    """
    info: calculate the jaccard distances among many strings and return the results as a matrix
    input: strings: list of strings
    output: matrix, containing the jaccard distance between the i-th string and j-th string at the position (i,j)
    """
    print("\n len(strings): ", len(strings))
    el_matrix = make_el_matrix(strings)
   
    # info: square el_matrix to get the intersections (el_matrix*el_matrix^T I think):
    #intersection = np.matmul(el_matrix, el_matrix.transpose())
    intersection = om.multiply_cl(el_matrix, el_matrix.transpose())
     
    # info: 1 - (square (1 - el_matrix)) to get the intersections (el_matrix*el_matrix^T I think):
    el_matrix_minus = om.subtract_cl(np.ones(el_matrix.shape), el_matrix)
    #unity = np.matmul(el_matrix_minus, el_matrix_minus.transpose())
    unity = om.multiply_cl(el_matrix_minus, el_matrix_minus.transpose())
    sz = unity.shape
    max_matrix = np.ones(sz)
    #unity = np.matmul(max_matrix, max_matrix.transpose()) - unity
    max_matrix_square = om.multiply_cl(max_matrix, max_matrix.transpose())
    unity = om.subtract_cl(max_matrix_square, unity)
    #print("\n unity: ", unity)    

    # info: 1 - quotient (this time, divide elementwise)
    quotient = om.divide_cl(intersection, unity.transpose()) # replace that by GPU operations
    quotient = om.subtract_cl(np.ones(quotient.shape), quotient)
    #print("\n quotient: ", quotient)
    return quotient
"""    
string_val = list()
string_val.append("ABC")
string_val.append("BCD")
string_val.append("CDE")
string_val.append("DEF")
string_val.append("EFG")
string_val.append("FGH")
quotient = jaccard(string_val) 
print("\n quotient: ", quotient)
"""
