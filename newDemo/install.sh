
conda update -n base -c defaults conda

conda create --name ho27 python=2.7
conda activate ho27

conda install -c anaconda tensorflow=1.15
conda install -c conda-forge keras
conda install -c conda-forge tf_object_detection


conda install -c anaconda flask
conda install -c anaconda requests
#conda install -c conda-forge google-cloud-sdk
#conda install -c conda-forge google-cloud-storage

#conda install -c auto python-firebase

sudo apt install libjasper1 libjasper-dev
conda install -c conda-forge opencv

conda install -c conda-forge matplotlib

conda install -c anaconda pillow
