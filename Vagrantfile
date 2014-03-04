# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # config.vm.network :forwarded_port, guest: 80, host: 8080

  # Bridge
  config.vm.network :public_network

  # Host only
  config.vm.network :private_network, ip: "192.168.33.10"
  config.vm.network :private_network, ip: "192.168.34.10"

  # Bootstrap env
$script = <<SCRIPT
  echo Bootstraping NAZS environment...
  apt-get install -y make python-pip python-virtualenv git-core
  cd /vagrant
  make env

  echo DONE!
  echo Now you should:
  echo vagrant ssh
  echo cd /vagrant
  echo sudo make run
SCRIPT

  config.vm.provision "shell", inline: $script
end
