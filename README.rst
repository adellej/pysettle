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

This code computes ignition conditions for Type I X-ray bursts using a multi-zone model of the accreting layer (including hot CNO hydrogen burning, but not helium burning), but a one-zone ignition criterion. For more details, see Cumming & Bildsten (2000).

Credits
-------

Rotational Evolution During Type I X-Ray Bursts, Andrew Cumming, Lars Bildsten (2000) - https://arxiv.org/abs/astro-ph/0004347

Package installation and usage
------------------------------
pySettle is on pyPI (https://pypi.org/project/pySettle/) so installation is easy - either straight or in virtual environment:

   .. code-block::
   
      pip install pySettle
  
   .. ::
   
   .. code-block::
   
      from pySettle import settler

(See `test_settle_sft.py <tests/test_settle_sft.py>`_.)

Build and installation from this github repository
--------------------------------------------------

See `build instructions <BUILD.rst>`_.
