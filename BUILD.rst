========
pySettle
========

Build and installation from this github repository
--------------------------------------------------

This includes compilation of the underlaying C/C++ library (libsettle.so) and including it in the python package. On Linux, GCC development tools must be installed, on Mac, it works with clang compiler.

#. Clone the pysettle repository

   .. code-block::
    
      git clone https://github.com/adellej/pysettle
      cd pysettle
   

#. Create and activate a clean conda environment

   The example is for python 3.8, but should work for any version 3.6 to 3.11 as well.

   .. code-block::
    
      # remove existing environment if needed - to start from scratch
      conda remove -n settle-3.8 --all
      # create blank conda environment
      conda create --name settle-3.8 python==3.8.*
      conda activate settle-3.8

      
#. Install/upgarde pip, build and local install

   .. code-block::
  
      python3 -m pip install --upgrade pip
      python3 -m pip install --upgrade build

   .. code-block::
  
      # test build & local install
      # The "-e" install does not seem to be reliable for re-install 
      #       - keeps pulling some old build from somewhere middlewhere.
      # *Do not use:        python -m pip install -e .*
      # This is more reliable:
      python3 -m build
      python3 -m pip install .

   .. ::
   
   *Note: when workinng on the code, in case of doubts that recent changes got propagated, uninstall & purge the installed module _before_* ``pip install`` *to ensure the installed version has all the recent modifications.*

   .. code-block::
     
      python3 -m pip -v uninstall pySettle
      python3 -m pip -v cache purge

   After this, in that enviroment, pySettle just works from every directorty, providing the conda environment is activated.
   Imports like:

   .. code-block::
   
      from pySettle import settler

   (See `test_settle_sft.py <tests/test_settle_sft.py>`_.)


Run short functional test (SFT) manually
----------------------------------------

.. code-block::

   cd tests
   python ./test_settle_sft.py
 

Publish package on PyPI
----------------------------------------

.. code-block::

   python3 -m pip install twine

.. ::

**Test PyPI** : for testing that all works, but not yet really publishing to a place where all the world is searching for python packages.

.. code-block::

   python3 -m twine upload --repository testpypi dist/*

.. ::

**The Real PyPI**

.. code-block::

   python3 -m twine upload dist/*

.. ::

`pySettle on PyPI:  https://pypi.org/project/pySettle/ <https://pypi.org/project/pySettle/>`_


Building and publishing linux wheels
----------------------------------------
PyPI will not accept just whatever linux compiled packages (wheels). One of manylinux targets must be used (see https://github.com/pypa/manylinux). Fore pySettle, there is included a dockerfile that helps to automates the linux wheels build. Please follw the instructions below.

#. In `docekrfile <docker/settle_manylinux2014_x86_64.dockerfile>`_ select python version and make sure GIT_REPO and SETTLE _DIR are set up correctly. This may take several minutes.

   .. code-block::

      ...
      # select python version - works with 3.6 - 3.11
      ARG PY_VER_MAJOR=3
      ARG PY_VER_MINOR=8
      ...
      ARG SETTLE_DIR=${BASE_DIR}"/pysettle"
      ARG GIT_REPO="https://github.com/adellej/pysettle"
      ...

   .. ::

#. Repeat the rest of the steps for each python version.

   .. code-block::

      docker build -t settle_manylinux2014_x86_64:latest - < ./settle_manylinux2014_x86_64.dockerfile   

   .. ::

   .. code-block::
  
      # run and enter the container with bash
      docker run -it settle_manylinux2014_x86_64:latest bash
   
      # cd ${SETTLE_DIR}
      cd /usr/src/pysettle
      # publish manylinux wheels on PyPI
      python3 -m twine upload wheelhouse/*
      # exit and stop the container when done
      exit

   .. ::

