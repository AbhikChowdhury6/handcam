

#install
sudo apt install libatlas3-base libsz2 libharfbuzz0b libtiff5 libjasper1 libilmbase12 libopenexr22 libilmbase12 libgstreamer1.0-0 libavcodec57 libavformat57 libavutil55 libswscale4 libqtgui4 libqt4-test libqtcore4
sudo pip3 install opencv-contrib-python libwebp6

git clone https://github.com/RPi-Distro/RTIMULib/ RTIMU
cd RTIMU/Linux/python
sudo apt install python3-dev
python setup.py build
python setup.py install
sudo apt install libopenjp2-7

sudo apt-get install zip