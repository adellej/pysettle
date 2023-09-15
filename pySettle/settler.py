from __future__ import division
from __future__ import print_function

import ctypes as ct
import numpy
import pathlib

# print out settle library that will be used
settler_basepath = pathlib.Path(__file__).parent.parent.absolute()
print("settle library = ")
libsettle_path = sorted(pathlib.Path(settler_basepath).glob('*settle*.so'))
print(libsettle_path)
print("selecting ")
print(libsettle_path[0])

# MCU: This creates new instance of library each time called
# Makes sense to put it in the Settle class __init__() constructor, not here
# libsettle = ct.cdll.LoadLibrary("libsettle.so")

# MCU: This creates global instance of library
# That should save resources (loading and creating new instance each time)
#
# This works on Linux, but not on Mac (in case of setuptools wheel build)
# But works perfectly on both Linux and Mac for
# manually built and installed /usr/lcoal/lib/libsettle.so
#   libsettle = ct.CDLL("libsettle.so")
#
# This works both on Linux, and on Mac - but not for
# manually built and installed /usr/local/lib/libsettle.so
libsettle = ct.CDLL(libsettle_path[0])


class Settle(object):
    """
    Super basic interface to settle code
    """

    def __init__(self, F=0.1, C=0):
        """
        Will just return a convenient object to call settle

        Has methods:

        full: calls settle with all arguments, in case you want to change paramenters,
              it overrides the default F and C, but does not overwrite them
              Takes f, m, x, z, c
        run : more compact call, which assumes f and c from initialization.
              Takes m, x, and z

        :param F: the flux from the bottom
        :param C: include compressional heating (1) or not (0)

        :return: alpha, trec [hr], fluence [1e39 erg], all values in
          the observer frame
        """
        #        path_to_data_file = (
        #            pathlib.Path(__file__).resolve().parent.parent / "settle" / "libsettle.so"
        #        )

        # MCU note:
        # Option A:
        # This creates new instance of library each time called
        # Makes sense to put it in the Settle class __init__() constructor
        #
        # This works on Linux, but not on Mac (setuptools wheel build)
        # But works perfectly on both Linux and Mac for
        # manually built and installed /usr/lcoal/lib/libsettle.so
        #   self.libsettle = ct.cdll.LoadLibrary("libsettle.so")
        #
        # This works both on Linux, and on Mac - but not for
        # manually built and installed /usr/local/lib/libsettle.so
        #   self.libsettle = ct.cdll.LoadLibrary(libsettle_path[0])

        # MCU note:
        # Only one global instance of library exists:
        # Here we assign the mainer function to this instance of Settle class
        # That should save resources (loading library and creating
        # new library instance each time Settle class is declared)
        self.mainer = libsettle.mainer

        # mainer(double* flu, double* Z, double* X, double* mdo, int* docomp,
        #        double* trec, double* alpha, double* fluen,
        #        double* radius, double* mass)

        self.mainer.argtypes = [
            ct.POINTER(ct.c_double),
            ct.POINTER(ct.c_double),
            ct.POINTER(ct.c_double),
            ct.POINTER(ct.c_double),
            ct.POINTER(ct.c_int),
            ct.POINTER(ct.c_double),
            ct.POINTER(ct.c_double),
            ct.POINTER(ct.c_double),
            ct.POINTER(ct.c_double),
            ct.POINTER(ct.c_double),
        ]
        self.mainer.returntype = ct.c_int

        self.init_vars(F, C)

    def init_vars(self, F=0.1, C=0):
        """
        Takes:

        F: [default: 0.1] the flux from the bottom
        C: [default: 0  ] 0 or 1: to do compressional heating or not

        Has attributes:

        F, C     : the default parameters
                   (so that you do not specify these all the times, just for lazyness)
        libsettle: link to the settle code library
        mainer   : the real callable of the library (should not be used directly by user)
        """
        self.F = ct.c_double(F)
        self.C = ct.c_int(C)

    def run(self, M, X, Z, R, Ma):
        """
        Runs settle, you CANNOT specify F and C,
        because it uses the defaults you specified at creation.

        Can pass either scalars, or equally long arrays.
        """
        T = ct.c_double()
        A = ct.c_double()
        E = ct.c_double()

        if hasattr(M, "__iter__"):

            resA = []
            resR = []
            resE = []

            for i in range(len(M)):

                ret = self.mainer(
                    ct.byref(self.F),
                    ct.byref(ct.c_double(Z[i])),
                    ct.byref(ct.c_double(X[i])),
                    ct.byref(ct.c_double(M[i])),
                    ct.byref(self.C),
                    ct.byref(T),
                    ct.byref(A),
                    ct.byref(E),
                    ct.byref(ct.c_double(R[i])),
                    ct.byref(ct.c_double(Ma[i])),
                )

                resA.append(A.value)
                resR.append(T.value)
                resE.append(E.value)

            return numpy.array(resA), numpy.array(resR), numpy.array(resE)

        else:
            ret = self.mainer(
                ct.byref(self.F),
                ct.byref(ct.c_double(Z)),
                ct.byref(ct.c_double(X)),
                ct.byref(ct.c_double(M)),
                ct.byref(self.C),
                ct.byref(T),
                ct.byref(A),
                ct.byref(E),
                ct.byref(ct.c_double(R)),
                ct.byref(ct.c_double(Ma)),
            )

            return A.value, T.value, E.value

    def full(self, F, M, X, Z, C, R, Ma):
        """
        Runs settle, needs the full set of parameters.

        Can pass either scalars, or equally long arrays.
        """

        T = ct.c_double()
        A = ct.c_double()
        E = ct.c_double()

        if hasattr(M, "__iter__"):

            resA = []
            resR = []
            resE = []

            for i in range(len(M)):

                ret = self.mainer(
                    ct.byref(ct.c_double(F[i])),
                    ct.byref(ct.c_double(Z[i])),
                    ct.byref(ct.c_double(X[i])),
                    ct.byref(ct.c_double(M[i])),
                    ct.byref(ct.c_double(C[i])),
                    ct.byref(T),
                    ct.byref(A),
                    ct.byref(E),
                    ct.byref(ct.c_double(R[i])),
                    ct.byref(ct.c_double(Ma[i])),
                )

                resA.append(A.value)
                resR.append(T.value)
                resE.append(E.value)

            return numpy.array(resA), numpy.array(resR), numpy.array(resE)

        else:
            #print(self.mainer(ct.c_double(F),ct.c_double(Z),ct.c_double(X),ct.c_double(M),ct.c_double(C),ct.c_double(T),ct.c_double(A),ct.c_double(E),ct.c_double(R),ct.c_double(Ma)))
            ret = self.mainer(
                ct.byref(ct.c_double(F)),
                ct.byref(ct.c_double(Z)),
                ct.byref(ct.c_double(X)),
                ct.byref(ct.c_double(M)),
                ct.byref(ct.c_int(C)),
                ct.byref(T),
                ct.byref(A),
                ct.byref(E),
                ct.byref(ct.c_double(R)),
                ct.byref(ct.c_double(Ma)),
            )

            return A.value, T.value, E.value


    def summary(self, mdot=None, X=[0.7, 0.5, 0.3, 0.1, 0.01], Q_b=0.3, 
        Z=0.016, show=True, **kwargs):
        """
        Generate a summary plot showing burst rate as a function of mdot
	for a few different compositions, to replicate figure 1 from
        Galloway et al. 2006

        :param mdot: range of mdot values (relative to Eddington)
        :param X: list of X values to plot
        :param Q_b: base flux for input to settle (common for all plots)
        :param Z: CNO metallicity (common for all plots)
        :param show: default is to show the plot, set to False if you want
          to add some elements (e.g. for a model comparison)

        :returns: plot
        """

        import matplotlib.pyplot as plt

        if mdot is None:
            mdot = numpy.arange(0.01, 0.17, 0.002)

        fig = plt.figure(**kwargs)

        for _X in X:
            rate = []
            for _mdot in mdot:
                res = self.full(Q_b, _mdot, _X, Z, 0, 10., 1.4)
                rate.append(1./res[1])
    
            plt.plot(mdot,rate,label='$X_0= {}$'.format(_X))
        plt.yscale('log')
        plt.legend()
        plt.ylim(1e-3,0.6)
        plt.xlabel('Accretion rate [$\dot{m}_\mathrm{Edd}$]')
        plt.ylabel('Burst rate [hr$^{-1}$]')

        if show:
            plt.show()

        return fig
