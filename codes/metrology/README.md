

install uldaq drivers

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


```
conda create -n irfts numpy scipy jupyterlab matplotlib
conda activate irfts
pip install uldaq
```
