#!/bin/sh -e

# one file for all repositories, because
# sudo apt-get update really slow, and it take long time
# to do it after repo add in each file

sudo apt-get update

sudo apt-get -y install python-software-properties

PG_REPO_APT_SOURCE=/etc/apt/sources.list.d/pgdg.list
if [ ! -f "$PG_REPO_APT_SOURCE" ]
then
  # Add PG apt repo:
  echo "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main" > "$PG_REPO_APT_SOURCE"

  # Add PGDG repo key:
  wget --quiet -O - https://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | apt-key add -
fi

# it will add node and will update apt cache
curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -

apt-get -y upgrade