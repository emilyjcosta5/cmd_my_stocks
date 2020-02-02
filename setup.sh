#!/usr/bin/env bash

# Make Linux command from python script.
mkdir ~/bin
chmod +x trading_bot.py
cp trading_bot.py ~/bin/trading_bot
echo 'export PATH-$PATH":HOME/bin"' >> ~/.bashrc
source ~/.bashrc

# Make sure pip is installed/updated
sudo apt update
sudo apt-get install python3
sudo apt install python3-pip

# Make sure all depencies are installed.
if python -c "import alpaca_trade_api" &> /dev/null; then
	echo 'alpaca_trade_api already installed'
else
        pip3 install alpaca-trade-api
fi
if python -c "import requests" &> /dev/null; then
	echo 'requests already installed'
else
        pip3 install requests
fi
if python -c "import ta" &> /dev/null; then
	echo 'ta-lib already installed'
else
        # curl -O https://downloads.sourceforge.net/project/ta-lib/ta-lib/0.4.0/ta-lib-0.4.0.jar?r=https%3A%2F%2Fsourceforge.net%2Fprojects%2Fta-lib%2Ffiles%2Flatest%2Fdownload&ts=1580637169
	# tar -xvf ta-lib-0.4.0-src.tar.gz
	pip3 install ta-lib
fi
if python -c "import numpy" &> /dev/null; then
	echo 'numpy already installed'
else
        pip3 install numpy
fi
if python -c "import pytz" &> /dev/null; then
	echo 'pytz already installed'
else
        pip3 install pytz
fi
if python -c "import pandas" &> /dev/null; then
	echo 'pandas already installed'
else
        pip3 install pandas
fi

