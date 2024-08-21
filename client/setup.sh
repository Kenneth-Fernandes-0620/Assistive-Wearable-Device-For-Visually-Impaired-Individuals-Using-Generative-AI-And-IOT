#!/bin/bash

# Update the package list
echo "Updating package list..."
sudo apt-get update && sudo apt-get upgrade -y

# Install espeak
echo "Installing espeak..."
sudo apt-get install -y espeak

# Install portaudio19-dev
echo "Installing portaudio19-dev..."
sudo apt-get install -y portaudio19-dev

echo "Packages Installation completed!"
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-aarch64.sh -O /tmp/miniforge.sh
bash /tmp/miniforge.sh -b

Echo "modify the alsa config to use the correct card"