## installation on fresh Raspberry Pi 5

### install uldaq drivers (as admin)

https://github.com/mccdaq/uldaq

```bash
sudo apt-get install gcc g++ make
sudo apt-get install libusb-1.0-0-dev
wget -N https://github.com/mccdaq/uldaq/releases/download/v1.2.2/libuldaq-1.2.2.tar.bz2
tar -xvjf libuldaq-1.2.2.tar.bz2
cd libuldaq-1.2.2
./configure && make
sudo make install
```

### install miniforge (as user - non admin)

```bash
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-aarch64.sh
bash Miniforge3-Linux-aarch64.sh
source ~/.bashrc
```

### create environment (as user - non admin)

```bash
conda create -n irfts numpy scipy jupyterlab matplotlib
conda activate irfts
pip install uldaq
```
