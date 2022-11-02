import os, re, secrets, sys


def get_random_secret_key():
    """
    Return a 50 character random string usable as a SECRET_KEY setting value.
    (Retrieved from django.core.management.utils.get_random_secret_key.
    Take a look at original implements: https://github.com/django/django/blob/bfe9665502c77baf14ce6cf52af974033bd43164/django/utils/crypto.py#L51 )
    """
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
    length = 50
    return "".join(secrets.choice(chars) for i in range(length))


def initialize_secret_key():
    SECRET_KEY = get_random_secret_key()

    with open('djangopj/settings.py', encoding='utf-8', mode='r') as f:
        original = f.read()

    result = re.sub(r"SECRET_KEY = '[^']*'", f"SECRET_KEY = r'{SECRET_KEY}'", original)

    with open('djangopj/settings.py', encoding='utf-8', mode='w') as f:
        f.write(result)


def set_heroku_secret_key():
    from djangopj.settings import SECRET_KEY

    SECRET_KEY_FOR_HEROKU = SECRET_KEY.replace('(', '"("').replace(')', '")"').replace('&', '"&"')

    os.system(f'heroku config:set SECRET_KEY={SECRET_KEY_FOR_HEROKU}')
    os.system(f'heroku config:set DISABLE_COLLECTSTATIC=1')

if __name__ == '__main__':
    if sys.argv[1] == 'init':
        initialize_secret_key()
        
    elif sys.argv[1] == 'heroku':
        set_heroku_secret_key()
        
    else:
        raise Exception('Invalid argument')

