#!/bin/bash

# Define colors
GREEN='\033[38;2;0;150;0m'  
LIGHTGREEN='\033[38;2;0;220;0m'  
CYAN='\033[0;36m'
NC='\033[0m'            

# Run a command and capture output
run_command() {
  "$@"
  printf "${GREEN}Done.${NC}\n\n"
}

# Update Environment
printf "${GREEN}Updating environment...${NC}\n"
run_command sudo apt-get -y update

# Upgrading system
printf "${GREEN}Upgrading system...${NC}\n"
run_command sudo apt-get -y upgrade

# Perform dist-upgrade
printf "${GREEN}Performing dist-upgrade...${NC}\n"
run_command sudo apt-get -y dist-upgrade

# Removing unnecessary packages
printf "${GREEN}Removing unnecessary packages...${NC}\n"
run_command sudo apt-get -y autoremove

# Install Python and Pip
printf "${GREEN}Installing Python & Pip...${NC}\n"
run_command sudo apt-get install -y python3-pip

# Install other apt packages
printf "${GREEN}Installing necessary apt packages...${NC}\n"
run_command sudo apt-get -y install zip unzip git graphviz

# Install Python packages
printf "${GREEN}Installing general Python packages...${NC}\n"
run_command pip3 install jupyter==1.1.1 pandas==2.2.3 numpy==2.2.3 matplotlib==3.10.0 requests==2.32.3 statistics==1.0.3.5 graphviz==0.20.3 ipython==8.32.0

# MP4
printf "${GREEN}Installing packages for MP4...${NC}\n"
run_command pip3 install selenium==4.28.1 Flask==3.1.0 lxml==5.3.1 html5lib==1.1

# MP5
printf "${GREEN}Installing packages for MP5...${NC}\n"
run_command pip3 install beautifulsoup4==4.13.3

# MP6 
printf "${GREEN}Installing packages for MP6...${NC}\n"
run_command pip3 install geopandas==1.0.1 shapely==2.0.7 descartes==1.1.0 geopy==2.4.1 netaddr==0.10.0

# MP7
printf "${GREEN}Installing packages for MP7...${NC}\n"
run_command pip3 install rasterio==1.4.3 pillow==11.1.0 scikit-learn==1.6.1

# Install Chromium
printf "${GREEN}Installing Chromium...${NC}\n"
run_command sudo apt-get install -y chromium-browser xdg-utils

# Install Chrome & WebDriver Manager dependencies
printf "${GREEN}Installing Chrome dependencies...${NC}\n"
run_command sudo apt-get install -y wget libasound2 libgbm1 libnspr4 libnss3 libu2f-udev libvulkan1 && sudo rm -rf /var/lib/apt/lists/*

# Ensure dpkg is configured properly
printf "${GREEN}Configuring dpkg if needed...${NC}\n"
run_command sudo dpkg --configure -a

# Download Google Chrome 
printf "${GREEN}Downloading Google Chrome...${NC}\n"
sudo wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
printf "${LIGHTGREEN}Installing...${NC}\n"
run_command sudo apt install ./google-chrome-stable_current_amd64.deb

# Extra Selenium requirements
printf "${GREEN}Installing extra Selenium requirements...${NC}\n"
run_command pip install webdriver-manager==4.0.2

# Clean up
printf "${GREEN}Cleaning up directory...${NC}\n"
run_command rm -f google-chrome-stable_current_amd64.deb

printf "${GREEN}All installations and configurations are complete.${NC}\n"
