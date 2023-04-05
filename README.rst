========
PySettle
========

Settling solver - the BEANSp edition
-----------------------------------------------------------------

* Forked from settle project by Andrew Cumming
  https://github.com/andrewcumming/settle
* BEANSp Repo: https://github.com/adellej/beans

Features
--------

This code computes ignition conditions for Type I X-ray bursts using a multi-zone model of the accreting layer (including hot CNO hydrogen burning, but not helium burning), but a one-zone ignition criterion. For more details, see Cumming & Bildsten (2000).

Credits
-------

Rotational Evolution During Type I X-Ray Bursts, Andrew Cumming, Lars Bildsten (2000) - https://arxiv.org/abs/astro-ph/0004347

Package installation and usage
------------------------------

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
   
      from pySettle import settler as se

   (See `test_settle_sft.py <https://github.com/ADACS-Australia/beans/blob/adacs_mc/settle/tests/test_settle_sft.py>`_.)

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

**Test PyPI** : testing all works, but not really publishing to a place where all the world is searching for python packages.

.. code-block::

   python3 -m twine upload --repository testpypi dist/*

.. ::

**Real PyPI**

.. code-block::

   python3 -m twine upload dist/*

.. ::

