#install
sudo apt-get update
sudo apt-get upgrade -y

sudo apt-get install -y zip python3-pip i2c-tools python3-dev


sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel



sudo apt install -y libhdf5-103

sudo apt-get install -y libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install -y libxvidcore-dev libx264-dev
sudo apt-get install -y libgtk2.0-dev libgtk-3-dev

sudo apt-get install -y libilmbase-dev
sudo apt-get install -y libopenexr-dev
sudo apt-get install -y libgstreamer1.0-dev

sudo apt-get install -y libqtgui4
sudo apt install -y libqt4-test

sudo apt-get install -y libatlas-base-dev



sudo pip3 install opencv-contrib-python==3.4.3.18


sudo apt-get install -y cmake
sudo apt-get install -y qt4-default
git clone https://github.com/RPi-Distro/RTIMULib/ RTIMU
cd RTIMU/Linux/python
python3 setup.py build
python3 setup.py install
cd ~

mkdir data

echo "python3 /home/pi/handcam/v4collectionRig/main.py" >> /etc/rc.local