
==========
Billometer
==========

Sample pillar
-------------

.. code-block:: yaml

    billometer:
      server:
        enabled: true
        workers: 3
        secret_key: secret_token
        sync_time: 600
        collect_time: 1800
        metric:
          in:
            engine: graphite
            host: 10.10.10.180
            port: 80
          out:
            engine: statsd
            host: 10.10.10.180
            prefix: foo
            port: 81
        bind:
          address: 0.0.0.0
          port: 9753
          protocol: tcp
        source:
          type: 'git'
          address: 'git@repo1.robotice.cz:python-apps/billometer.git'
          rev: 'master'
        cache:
          engine: 'memcached'
          host: '127.0.0.1'
          prefix: 'CACHE_DJANGO_ENC'
        database:
          engine: 'postgresql'
          host: '127.0.0.1'
          name: 'django_billometer'
          password: 'db-pwd'
          user: 'django_billometer'
        identity:
          engine: 'keystone'
          region: 'regionOne'
          token: 'token'
          host: '127.0.0.1'
          port: 5000
          api_version: 2
        mail:
          host: 'mail.domain.com'
          password: 'mail-pwd'
          user: 'mail-user'
        logging:
          engine: sentry
          dsn: pub@sec:dsn.cz/12

Extra Resources
---------------

.. code-block:: yaml

    billometer:
      server:
        enabled: true
        workers: 3
        secret_key: secret_token
        sync_time: 600
        collect_time: 1800
        extra_resource:
          network.rx:
            label: Network RX
            resource: network.rx
            price_rate: 0.0002
            threshold: 150000
          7k2_SAS
            price_rate: 0.008205
            resource: cinder.volume
            name: 7k2_SAS
            label: 7k2 SA
          10k_SAS
            price_rate: 0.027383
            resource: cinder.volume
            label: 10k2 SAS
            name: 10k_SAS
          15k_SAS
            price_rate: 0.034232
            resource: cinder.volume
            label: 15k2 SAS
            name: 15k_SAS
          EasyTier
            price_rate: 0.041082
            resource: cinder.volume
            label: Easy Tier
            name:'EasyTier


Read more
---------

* http://docs.gunicorn.org/en/latest/configure.html

Documentation and Bugs
======================

To learn how to install and update salt-formulas, consult the documentation
available online at:

    http://salt-formulas.readthedocs.io/

In the unfortunate event that bugs are discovered, they should be reported to
the appropriate issue tracker. Use Github issue tracker for specific salt
formula:

    https://github.com/salt-formulas/salt-formula-billometer/issues

For feature requests, bug reports or blueprints affecting entire ecosystem,
use Launchpad salt-formulas project:

    https://launchpad.net/salt-formulas

You can also join salt-formulas-users team and subscribe to mailing list:

    https://launchpad.net/~salt-formulas-users

Developers wishing to work on the salt-formulas projects should always base
their work on master branch and submit pull request against specific formula.

    https://github.com/salt-formulas/salt-formula-billometer

Any questions or feedback is always welcome so feel free to join our IRC
channel:

    #salt-formulas @ irc.freenode.net
