
# Billometer

## Sample pillar

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
          address: 'git@repo1.robotice.cz:django/billometer.git'
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

## Read more

* http://docs.gunicorn.org/en/latest/configure.html