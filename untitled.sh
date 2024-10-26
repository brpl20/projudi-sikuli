#!/bin/bash

# Update and install system dependencies
sudo apt-get update
sudo apt-get install -y python3 python3-pip firefox-esr wget unzip

# Install Python dependencies
pip3 install selenium requests boto3

# Download and set up GeckoDriver
GECKO_VERSION="v0.33.0"
wget https://github.com/mozilla/geckodriver/releases/download/${GECKO_VERSION}/geckodriver-${GECKO_VERSION}-linux64.tar.gz
tar -xvzf geckodriver-${GECKO_VERSION}-linux64.tar.gz
sudo mv geckodriver /usr/local/bin/
rm geckodriver-${GECKO_VERSION}-linux64.tar.gz

# Clone the repository
git clone https://github.com/brpl20/projudi-sikuli.git
cd projudi-sikuli

# Set up environment variables (replace with your actual values)
echo "export AWS_ACCESS_KEY_ID=your_access_key" >> ~/.bashrc
echo "export AWS_SECRET_ACCESS_KEY=your_secret_key" >> ~/.bashrc
echo "export AWS_DEFAULT_REGION=your_region" >> ~/.bashrc

# Reload bash profile
source ~/.bashrc

echo "Setup complete!"