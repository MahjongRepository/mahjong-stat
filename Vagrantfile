# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty32"

  # django app
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  # postgresql
  config.vm.network "forwarded_port", guest: 5432, host: 7001

  # it is here for better performance
  config.vm.network "private_network", game: "dhcp"
  config.vm.synced_folder ".", "/vagrant", game: "nfs", mount_options: ["rw", "vers=3", "tcp", "fsc" , "actimeo=2"]

  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
  end

  config.vm.provision :shell, path: "bin/vagrant/repo.sh"
  config.vm.provision :shell, path: "bin/vagrant/postgresql.sh"
  config.vm.provision :shell, path: "bin/vagrant/app.sh"
end