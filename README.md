For TTB2020.

## Inspiration
We love trading stocks, Linux, and algorithms. 

## What it does
It always a user to run a trading bot using simple Linux commands. The user simply needs to hook it up to his Alpaca account, then run the bot with optional custom settings!

## How we built it
We set up an Alpaca account, built a simple trading bot (inspired by some on the internet), built the Linux command, and connected it to Google Cloud for endless trading and financial growth.

## Challenges we ran into
The biggest challenge would be making it easy for a user to connect it to Google Cloud. Now, the user can simply create a VM instance and input a few details, then the bot automatically will run on the remote machine.

## Accomplishments that we're proud of
Emily- this was my first time building my own Linux command. Seeing several topics that excite me (cloud computing, Linux, python, finance, and math) combine for such a practical application feels like such an accomplishment.
Andrea- making a command line tool that programmers will love using to create custom algorithms. 

## What we learned
We learned about the extensions amount of tools (API, learning resources, data) available for online stock trading. We definitely see so much opportunity in the fields of finance and investment for our fellow computer nerds! 
Andrea- I also learned a ton about cloud computing and secure shell for your trading needs (hooking up our algorithm to the cloud).

## What's next for cmd_my_stocks
We want to develop it so it is easy for mathematicians/programmers to implement their own algorithms. So, we would probably separate a lot of the functions so a person can simply run a python script containing the algorithms straight on the cloud or his pc.

NAME
trading_bot - a simple command to connect with your Alpaca trading platform and automate running trading bots from your command line.

SYNOPSIS
trading_bot [--info]

DESCRIPTION
trading_bot is seemlessly designed to appeal to the tech-savvy and fiscally responsible individual.

STARTUP OPTIONS
	--info
		Prints the current set base-url, api-key, and secret-key.
	-s <key> <value>
		Sets the key (base-url, api-key, or secret-key) to designated value.

LOGGING AND INPUT FILE OPTIONS
	-v 
		Turn on verbose output, with all the available data. The default is not verbose.
	-r <float>
		Customize the risk of your portfolio when executing a command to run a trading bot.
	-d <float>
		Customize the stop limit of your trading bot when executing a command to run a trading bot.
	-l <float>
		Customize the minimum previous-day dollar volume for a stock we may consider.
	-x <float>
		Customize the maximum of the range of the price of stocks to purchase.
	-n <float>
		Customize the minimum of the range of the price of stocks to purchase.
		
SYNTAX
	trading_bot-run
		Runs 
AUTHORS
	trading_bot was written by and is maintained by Emily Costa and Andrea Vieira.
