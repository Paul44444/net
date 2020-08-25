import pyopencl as cl
import numpy as np

import os
os.environ['PYOPENCL_COMPILER_OUTPUT'] = '0'
os.environ['PYOPENCL_CTX'] = '0'

#(n, m, p) = (3, 4, 5)
#(n, m, p) = (3000, 4000, 5000)

# a = np.random.randn(n, m).astype(np.float32)
# b = np.random.randn(m, p).astype(np.float32)
#a = np.random.randint(2, size=(n*m))
#b = np.random.randint(2, size=(m*p))

def multiply_cl(a, b): 
    """
    info: calculate the matrix product of two matrices a and b on the GPU by using OpenCL
    input: a: matrix
        b: matrix
    output: product of a and b
    """    

    # do we have to cite the source?
    
    sz_a = a.shape
    sz_b = b.shape
    (n, m, p) = (sz_a[0], sz_a[1], sz_b[1])
    
    #c = np.zeros((n*p), dtype=np.float32)
    c = np.zeros((n*p), dtype=np.float32)
    
    a = a.astype(np.float32)
    b = b.astype(np.float32)
    
    #ctx = cl.create_some_context()
    platform = cl.get_platforms()
    my_gpu_devices = platform[0].get_devices(device_type=cl.device_type.GPU)
    ctx = cl.Context(devices=my_gpu_devices)

    queue = cl.CommandQueue(ctx)
    
    mf = cl.mem_flags
    a_buf = cl.Buffer\
       (ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a)
    b_buf = cl.Buffer\
       (ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b)
    c_buf = cl.Buffer(ctx, mf.WRITE_ONLY, c.nbytes)
    
    prg = cl.Program(ctx, """
        __kernel void multiply(ushort n,
        ushort m, ushort p, __global float *a,
        __global float *b, __global float *c)
        {
          int gid = get_global_id(0);
          c[gid] = 0.0f;
          int rowC = gid/p;
          int colC = gid%p;
          __global float *pA = &a[rowC*m];
          __global float *pB = &b[colC];
          for(int k=0; k<m; k++)
          {
             pB = &b[colC+k*p];
             c[gid] += (*(pA++))*(*pB);
          }
        }
        """).build()
    
    prg.multiply(queue, c.shape, None,
                 np.uint16(n), np.uint16(m), np.uint16(p),
                 a_buf, b_buf, c_buf)
    
    a_mul_b = np.empty_like(c)
    cl.enqueue_copy(queue, a_mul_b, c_buf)
    
    return a_mul_b.reshape(n, p)

def divide_cl(a, b):
    """
    info: perform elementwise division of two matrices a and b on the GPU by using OpenCL
    input: a: matrix
        b: matrix
    output: resultmatrix
    """
    # do we have to cite the source?

    sz_a = a.shape
    sz_b = b.shape
    (n, m, p) = (sz_a[0], sz_a[1], sz_b[1])

    #c = np.zeros((n*p), dtype=np.float32)
    c = np.zeros((n*p), dtype=np.float32)

    a = a.astype(np.float32)
    b = b.astype(np.float32)

    #ctx = cl.create_some_context()
    platform = cl.get_platforms()
    my_gpu_devices = platform[0].get_devices(device_type=cl.device_type.GPU)
    ctx = cl.Context(devices=my_gpu_devices)

    queue = cl.CommandQueue(ctx)

    mf = cl.mem_flags
    a_buf = cl.Buffer\
       (ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a)
    b_buf = cl.Buffer\
       (ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b)
    c_buf = cl.Buffer(ctx, mf.WRITE_ONLY, c.nbytes)

    prg = cl.Program(ctx, """
        __kernel void multiply(ushort n,
        ushort m, ushort p, __global float *a,
        __global float *b, __global float *c)
        {
          int gid = get_global_id(0);
          c[gid] = 0.0f;
          c[gid] = a[gid]/b[gid];
        }
        """).build()

    prg.multiply(queue, c.shape, None,
                 np.uint16(n), np.uint16(m), np.uint16(p),
                 a_buf, b_buf, c_buf)

    a_mul_b = np.empty_like(c)
    cl.enqueue_copy(queue, a_mul_b, c_buf)
    
    return a_mul_b.reshape(n, p)

def subtract_cl(a, b):
    """
    info: perform subtraction of two matrices a and b on the GPU by using OpenCL
    input: a: matrix
        b: matrix
    output: resultmatrix
    """
    # do we have to cite the source?

    sz_a = a.shape
    sz_b = b.shape
    (n, m, p) = (sz_a[0], sz_a[1], sz_b[1])

    #c = np.zeros((n*p), dtype=np.float32)
    c = np.zeros((n*p), dtype=np.float32)

    a = a.astype(np.float32)
    b = b.astype(np.float32)

    #ctx = cl.create_some_context()
    platform = cl.get_platforms()
    my_gpu_devices = platform[0].get_devices(device_type=cl.device_type.GPU)
    ctx = cl.Context(devices=my_gpu_devices)
    print("\n my_gpu_devices: ", my_gpu_devices)
    print("\n ctx: ", ctx)

    queue = cl.CommandQueue(ctx)

    mf = cl.mem_flags
    a_buf = cl.Buffer\
       (ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a)
    b_buf = cl.Buffer\
       (ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b)
    c_buf = cl.Buffer(ctx, mf.WRITE_ONLY, c.nbytes)

    prg = cl.Program(ctx, """
        __kernel void multiply(ushort n,
        ushort m, ushort p, __global float *a,
        __global float *b, __global float *c)
        {
          int gid = get_global_id(0);
          c[gid] = 0.0f;
          c[gid] = a[gid] - b[gid];
        }
        """).build()

    prg.multiply(queue, c.shape, None,
                 np.uint16(n), np.uint16(m), np.uint16(p),
                 a_buf, b_buf, c_buf)

    a_mul_b = np.empty_like(c)
    cl.enqueue_copy(queue, a_mul_b, c_buf)
    
    return a_mul_b.reshape(n, p)

def levenshtein_cl(strings=['ABC', 'DEF']):
    """
    info: calculate the distance matrix of the list of strings "strings" using the levenshtein distance on the GPU by using OpenCL
    input: strings: list of strings
    output: distance matrix 
    """
    
    # do we have to cite the source?


    c = np.zeros((len(strings)*len(strings)), dtype=np.float32)
    
    ascii_total = list()
    #strings = strings.astype(np.float32)
    
    max_len = 40
    for i in range(len(strings)):
        s = strings[i]
        for j in range(len(s), max_len):
            s.append('0')
        ascii_code = [ord(c) for c in s]
        ascii_total.append(ascii_code)
    ascii_total = np.array(ascii_total)
    ascii_total = ascii_total.astype(np.uint16)
    
    #ctx = cl.create_some_context()
    platform = cl.get_platforms()
    my_gpu_devices = platform[0].get_devices(device_type=cl.device_type.GPU)
    ctx = cl.Context(devices=my_gpu_devices)
    print("\n my_gpu_devices: ", my_gpu_devices)
    print("\n ctx: ", ctx)

    queue = cl.CommandQueue(ctx)

    mf = cl.mem_flags
    strings_buf = cl.Buffer\
        (ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=ascii_total)

    #a_buf = cl.Buffer\
    #   (ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a)
    #b_buf = cl.Buffer\
    #   (ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b)
    c_buf = cl.Buffer(ctx, mf.WRITE_ONLY, c.nbytes)
    print("\n I am in the GPU levenshtein")
    
    prg = cl.Program(ctx, """
        __kernel void multiply(__global ushort *strings, __global float *c, ushort strings_length)
        {
            // info: remember, that "strings" is just numbers here

            //int strings_length = strlen((char*)strings);
            //int strings_length = sizeof((char*)strings)/sizeof(char);
            //int strings_length = 3; // change that back afterwards
            int gid1 = get_global_id(0)/strings_length - get_global_id(0)%strings_length;
            int gid2 = get_global_id(0)%strings_length;
            uint *s = strings[gid1];
            uint *t = strings[gid2];
            
            int ls = 0;
            int lt = 0;

            for (int i = 0; i<sizeof(s)/sizeof(s[0]); i++)
            {
                if (ls == 0)
                {
                    if (s[i] == '0')
                    {
                        ls = i
                    }
                }
                if (lt == 0)
                {
                    if (t[i] == '0')
                    {
                        lt = i
                    }
                }
                // remove 0, that are coded in ASCII code
            }
            // still have to remove element from array
  
            ushort m = sizeof((uint*)s)/sizeof(uint);
            ushort n = sizeof((uint*)t)/sizeof(uint);
            
            int v0[n+1];
            int v1[n+1];
            
            for (int i = 0; i<n; i++)
            {
                v0[i] = i;
            }
            
            for (int i = 0; i < m - 1; i++)
            {
                v1[0] = i + 1;
                
                for (int j = 0; j < n-1; j++)
                {
                    int deletionCost = v0[j+1] + 1;
                    int insertionCost = v1[j] + 1;
                    int substitutionCost = 1000; // info: this is just a dummy value, which will be set to the real value below
                    if (s[i] == t[j])
                    {
                        substitutionCost = v0[j];
                    }
                    else
                    {
                        substitutionCost = v0[j] + 1;
                    }
                    
                    // info: calculate the minimum:
                    if (deletionCost < insertionCost)
                    {
                        v1[j+1] = deletionCost;
                    }
                    else
                    {
                        v1[j+1] = insertionCost;
                    }
                    if (substitutionCost < v1[j+1])
                    {
                         v1[j+1] = substitutionCost;
                    }
                }
                //v0 = v1; // should we do some kind of "swap"?
                for (int j = 0; j < n-1; j++)
                {
                    v0[j] = v1[j];
                }
            }
            //strcpy(c[get_global_id(0)], v0[n])
            //c[get_global_id(0)] = v0[n];
            
        }
        """).build()
    prg.multiply(queue, ascii_total.shape, None, strings_buf, c_buf, np.uint16(len(strings)))

    a_mul_b = np.empty_like(c)
    cl.enqueue_copy(queue, a_mul_b, c_buf)
     
    return a_mul_b
    #return a_mul_b.reshape(n, p)



