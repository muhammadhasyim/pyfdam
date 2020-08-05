# PyFDAM

PyFDAM is a Python implementation of the Frequency Domain Admittance Method (FDAM), whose purpose is to fit electrochemical models to impedance data and compute its charge/discharge behavior with inverse Laplace transform. FDAM and this code was used to perform the work in modeling electric double layer capacitors [in this paper](https://iopscience.iop.org/article/10.1149/2.0051713jes) and pseudocapacitors [in this paper](https://iopscience.iop.org/article/10.1149/1945-7111/ab6722)

This is a very lightweight Python module. In fact, it is essentially a small wrapper to the [LMFIT package](https://lmfit.github.io/lmfit-py/) to do non-linear fitting of impedance data and our own numerical implementation for inverse Laplace transform to perform time-domain "simulations". The theory behind these methods can be found on the previous papers!

# Installation

If you're on Linux, you can clone this project on the terminal and run the pip install command directly on the source folder 

```console
$ git clone https://github.com/muhammadhasyim/pyfdam.git
$ cd pyfdam
$ pip install .
```

All Python dependency should be automatically installed once you run the pip install command.
