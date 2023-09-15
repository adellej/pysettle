========
pySettle
========

Settling solver - the BEANSp edition
-----------------------------------------------------------------

* Forked from settle project by Andrew Cumming
  https://github.com/andrewcumming/settle
* pySettle Repo: https://github.com/adellej/pysettle
* BEANSp Repo: https://github.com/adellej/beans (related, using and depends on pySettle)

Features
--------

This code computes ignition conditions for Type I X-ray bursts using a
multi-zone model of the accreting layer (including hot CNO hydrogen
burning, but not helium burning), via a one-zone ignition criterion. For
more details, see
`Cumming & Bildsten (2000) <https://iopscience.iop.org/article/10.1086/317191>`_.

The code contains updates and improvements as described in `Goodwin et al.
(2019) <https://academic.oup.com/mnras/article/490/2/2228/5572467>`_
and subsequent work since.

Credits
-------

The original code was written by Andrew Cumming, with subsequent
modifications and updates by Adelle J. Goodwin, Martin Cupak, & Duncan K.
Galloway

Package installation and usage
------------------------------
pySettle is on pyPI (https://pypi.org/project/pySettle/) so installation is easy - either straight or in virtual environment:

   .. code-block::
   
      pip install pySettle
  
   .. ::
   
   .. code-block::
   
      from pySettle import settler

(See the code of test script `test_settle_sft.py <https://github.com/adellej/pysettle/blob/master/tests/test_settle_sft.py>`_ as an example.)

Build and installation from this github repository
--------------------------------------------------

Please refer to `build instructions <https://github.com/adellej/pysettle/blob/master/BUILD.rst>`_.

