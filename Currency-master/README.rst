Py Currency
===========

Version: 1.0.2

A simple currency module to:

* Retrieve various info about currency
* Format currency price
* Convert between currencies

Requirements
------------

* python3
* Internet connection (optional)

Installation
------------

.. code:: bash

    $ pip install nh-currency

Usage
-----

.. code:: python

    import currency

Get currency name
^^^^^^^^^^^^^^^^^

.. code:: python

    currency.name('USD')
    currency.name('USD', plural=True)

.. code:: python

    'US Dollar'
    'US dollars'

Symbol
^^^^^^

.. code:: python

    currency.symbol('CAD')
    currency.symbol('CAD', native=False)
    currency.symbol('NOK')
    currency.symbol('NOK', native=False)

.. code:: python

    '$'
    'CA$'
    'kr'
    'Nkr'

Number of decimal digits
^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    currency.decimals('USD')
    currency.decimals('JPY')

.. code:: python

    2
    0

Round to the maximum decimal digits
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    currency.rounding(100.115735, 'USD')
    currency.rounding(2253.12309, 'ISK')

.. code:: python

    100.12
    2253

Currency increment used for rounding
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    currency.roundto('USD')
    currency.roundto('CHF')

.. code:: python

    0
    0.05

Format currency
^^^^^^^^^^^^^^^

.. code:: python

    currency.pretty(10050000.2394, 'USD')
    currency.pretty(10050000.2394, 'USD', trim=True)
    currency.pretty(10050000.2394, 'USD', abbrev=False)

.. code:: python

    '$10,050,000.2394'
    '$10,050,000.24'
    '10,050,000.2394 USD'

Convert to other currency
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    currency.convert('USD', 'EUR')
    currency.convert('USD', 'EUR', 2)
    currency.convert('JPY', 'AUD', 100)

.. code:: python

    0.815797
    1.631594
    1.1759

Currency info
^^^^^^^^^^^^^

.. code:: python

    currency.info('USD')

.. code:: python

    # Output has been formatted for representation purpose
    {
        'symbol': '$', 
        'name': 'US Dollar',
        'symbol_native': '$',
        'decimal_digits': 2,
        'rounding': 0,
        'code': 'USD',
        'name_plural': 'US dollars'
    }

Testing
-------

.. code:: bash

    $ cd .../py-currency
    $ python -m unittest

Related Work
------------

`coinify <https://github.com/StorePilot/coinify>`__

Resources
---------

https://gist.github.com/Fluidbyte/2973986

https://www.wikipedia.org/
