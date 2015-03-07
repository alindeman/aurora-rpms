# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "puppetlabs/centos-7.0-64-puppet"

  config.vm.provision "shell", inline: <<-EOF
    sudo yum install -y rpmdevtools rpmlint yum-utils
    sudo yum groupinstall -y "Development Tools"
    sudo yum-builddep -y /vagrant/aurora.spec
  EOF
  config.vm.provision "shell", path: "build.sh", args: ["/vagrant"]
end
