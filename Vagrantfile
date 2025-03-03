# set up the default terminal
ENV["TERM"]="linux"

# set minimum version for Vagrant
Vagrant.require_version ">= 2.2.10"
Vagrant.configure("2") do |config|
  # Share the local project directory with the VM
  config.vm.synced_folder ".", "/vagrant_data"
    # Provisioning scripts
  config.vm.provision "shell", inline: <<-SHELL
    sudo zypper update -y
    sudo zypper install -y apparmor-parser curl
    curl -sfL https://get.k3s.io | sudo sh -
  SHELL
  
  # Set the image for the vagrant box
  config.vm.box = "opensuse/Leap-15.2.x86_64"
  # Set the image version
  config.vm.box_version = "15.2.31.632"
  

  # Forward the ports from the guest VM to the local host machine
  # Forward more ports, as needed
  config.vm.network "forwarded_port", guest: 8080, host: 8080
  config.vm.network "forwarded_port", guest: 6111, host: 6111
  config.vm.network "forwarded_port", guest: 6112, host: 6112
  config.vm.network "forwarded_port", guest: 7111, host: 7111
  config.vm.network "forwarded_port", guest: 3111, host: 3111
  config.vm.network "forwarded_port", guest: 4111, host: 4111
  config.vm.network "forwarded_port", guest: 30007, host: 30007
  config.vm.network "forwarded_port", guest: 30008, host: 30008


  # Set the static IP for the vagrant box
  config.vm.network "private_network", ip: "192.168.50.4"
  
  # Configure the parameters for VirtualBox provider
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "4096"
    vb.cpus = 4
    vb.customize ["modifyvm", :id, "--ioapic", "on"]
  end
end
