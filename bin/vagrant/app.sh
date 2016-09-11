#!/bin/sh -e

sudo apt-get -y install python-pip
sudo apt-get -y install python-virtualenv

mkdir /home/vagrant/build/
sudo chmod -R 777 /home/vagrant/build/

# install python from sources
sudo apt-get -y install build-essential checkinstall
sudo apt-get -y install libsqlite3-dev

sudo apt-get -y install python-pip python-virtualenv python-dev
sudo apt-get -y install python3.5 python3.5-dev

# install python libraries
virtualenv --python=/usr/bin/python3.5 /home/vagrant/env/
sudo chmod -R 777 /home/vagrant/env/
/home/vagrant/env/bin/pip install --upgrade pip
/home/vagrant/env/bin/pip install -r /vagrant/project/requirements.txt
sudo chmod -R 777 /home/vagrant/env/

SECRET_KEY=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 64 | head -n 1)
cat > /vagrant/project/mahjong_stat/local_settings.py <<- EOM
DEBUG = True

SECRET_KEY = '${SECRET_KEY}'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/vagrant/project/mahjong.db',
        'HOST': 'localhost',
        'USER': '',
        'PASSWORD': '',
    }
}
EOM

/home/vagrant/env/bin/python /vagrant/project/manage.py migrate

# activate virtualenv on login and go to working dir
sh -c "echo 'source /home/vagrant/env/bin/activate' >> /home/vagrant/.profile"
sh -c "echo 'cd /vagrant/project' >> /home/vagrant/.profile"