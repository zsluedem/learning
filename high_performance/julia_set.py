import time
from functools import wraps

x1 = -1.8
x2 = 1.8
y1 = -1.8
y2 = 1.8
c_real = -0.62772
c_imag = -.42193


def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        print ("@timefn" + fn.func_name + "took" + str(t2-t1) + "seconds")
        return result
    return measure_time


@timefn
def calc_pure_python(desired_width, max_iterations):
    x_step = (float(x2 - x1)/float(desired_width))
    y_step = (float(y1 - y2)/float(desired_width))
    x = []
    y = []
    ycoord = y2
    while ycoord > y1:
        y.append(ycoord)
        ycoord +=y_step

    xcoord = x1
    while xcoord < x2:
        x.append(xcoord)
        xcoord += x_step

    zs = []
    cs = []

    for ycoord in y:
        for xcoord in x:
            zs.append(complex(xcoord, ycoord))
            cs.append(complex(c_real, c_imag))

    print "Length of x :", len(x)
    print "Total elements:", len(zs)

    start_time = time.time()
    output = calculate_z_serial_purepython(max_iterations, zs, cs)
    end_time = time.time()
    secs = end_time - start_time
    print calculate_z_serial_purepython.func_name + "took" , secs , 'seconds'

    assert sum(output) == 33219980


# @profile
# def calculate_z_serial_purepython(maxiter, zs, cs):
#     output = [0] * len(zs)
#     for i in range(len(zs)):
#         n = 0
#         z = zs[i]
#         c = cs[i]
#         while abs(z) < 2 and n < maxiter:
#             z = z * z +c
#             n += 1
#         output[i] = n
#     return output


@profile
def calculate_z_serial_purepython(maxiter, zs, cs):
    output = [0] * len(zs)
    for i in range(len(zs)):
        n = 0
        z = zs[i]
        c = cs[i]
        while True:
            not_yet_escaped = abs(z) <2
            iterations_left = n <maxiter
            if not_yet_escaped and iterations_left:
                z = z*z +c
                n+=1
            else:
                break
        output[i] = n
    return output




if __name__ == "__main__":
    calc_pure_python(desired_width=1000, max_iterations=300)