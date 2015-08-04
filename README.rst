modoboa-domain-limits
=====================

Installation
------------

    $ git clone git@github.com:bearstech/modoboa-domain-limits.git
    $ cd modoboa-domain-limits
    $ pip install -e .

Append ``modoboa_domain_limits`` in ``MODOBOA_APPS`` list in your
``settings.py``.

Next, resync db :

    $ python manage.py syncdb
