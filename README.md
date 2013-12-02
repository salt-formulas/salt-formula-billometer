
# Billometer

## Sample pillar

    billometer:
      server:
        enabled: true
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
          name: 'django_enc'
          password: 'db-pwd'
          user: 'django_enc'
        mail:
          host: 'mail.domain.com'
          password: 'mail-pwd'
          user: 'mail-user'

## Read more

* TODO