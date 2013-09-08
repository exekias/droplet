# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  # Redirect admin interface
  #config.vm.network :forwarded_port, guest: 80, host: 8000

  # Host-only and bridged networks
  config.vm.network :private_network, ip: "192.168.33.10"
  config.vm.network :public_network

  config.vm.synced_folder ".", "/nazs", owner: "nobody"

  # Example for VirtualBox:
  #
  # config.vm.provider :virtualbox do |vb|
  #   vb.gui = true
  #   vb.customize ["modifyvm", :id, "--memory", "1024"]
  # end
  #
end
