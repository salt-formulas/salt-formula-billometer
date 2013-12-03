
# Billometer

## Sample pillar

    billometer:
      server:
        enabled: true
        secret_key: secret_token
        source:
          type: 'git'
          address: 'git@repo1.robotice.cz:django/django-billometer.git'
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

## Read more

* TODO