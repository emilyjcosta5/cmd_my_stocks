(For TTB2020.)

## Inspiration
We love stocks, Linux, and algorithms. We believe financial literacy can be fun, and it belongs on the terminal.

## What it does
*cmd_my_stocks* uses a trading bot to allow users to customize automated day trading decisions with Linux commands. Using transformative Alpaca API, users simply need to hook our bot to their Alpaca account and run our script to be on the road making great trade choices. Later, instead of leaving your computer running all day, you can watch how your algorithm has bought and sold stocks through the week by using Google Cloud VM- just another thing our script facilitates.

## How we built it
We set up an Alpaca account, built a simple trading bot (inspired by some on the Internet and more than a few Medium articles), developed a Linux command line interface, and connected our portfolios to Google Cloud for endless trading and financial growth.

## Challenges we ran into
Integrating all of our ideas and findings was the greatest challenge, and facilitating a connection with Google Cloud while retaining all our other functions. We were happy to overcome our challenge with the remote machine after reading a rabbit-hole of Google Cloud docs and piecing some wins together. Now, our user can start by creating a VM instance, inputting a few details, and our bot will automatically run on the remote machine soon after.

## Accomplishments that we're proud of
Emily - This was my first time building my own Linux command. Seeing several topics that excite me (cloud computing, Linux, python, finance, and math) combine for such a practical application feels like such an accomplishment.  

Andrea - Simplifying the many choices people have to make on a daily basis and increasing productivity is always something I'm very excited about. Trading individual stock can be extremely time consuming, as it requires time to study market behavior and being in the know with trends. We're passionate about doing the most that we can with our time, and the command line certainly has helped us do that. If we could encourage people to do tiny bits of research to greatly benefit the long run (i.e., learning about stock momentum and some simple math), 

## What we learned
Emily - We learned about the extensions amount of tools (API, learning resources, data) available for online stock trading. We definitely see so much opportunity in the fields of finance and investment for our fellow computer nerds!  

Andrea - I also learned a great deal about cloud computing and secure shell for secure trading, I had previously had much more experience with mobile development (Android) and less experience with Linux programming, but coding with one of my best friends changed that for me!

## What's next for cmd_my_stocks
We want to develop it so it is easy for mathematicians/programmers to implement their own algorithms. So, we would probably separate a lot of the functions so a person can simply run a python script containing the algorithms straight on the cloud or their PC.

**NAME**\
`trading_bot` is a simple command to connect with your Alpaca trading platform and automate running trading bots from your command line.

**SYNOPSIS**\
`trading_bot [--info]`

**DESCRIPTION**\
trading_bot is seemlessly designed to appeal to the tech-savvy and fiscally responsible individual.

**OVERVIEW**
1. Create account portfolio on Alpaca for buying and selling stock.  
2. Create VM of choice of cloud (our algorithm works with Google Cloud) and set up SSH keys:   
...Google Cloud Console -> Compute Engine -> VM Instances -> Create instance\
...Generate key: `ssh-keygen -t rsa`, copy and paste key into SSH keys section within VM instance editing.  
...Securely connect with instance: `ssh -I ~/.ssh/id_rsa <user>@<external_ip>`
3. Clone repo onto local machine.  
4. Run source code (`source file.sh`), which loads info into VM.
5. Enjoy bot trading!  

**STARTUP OPTIONS**\
`--info`\
Prints the current set base-url, api-key, and secret-key.\
`-s`\
Sets the key (base-url, api-key, or secret-key) to designated value.\

**LOGGING AND INPUT FILE OPTIONS**\
`-v`\
Turn on verbose output, with all the available data. The default is not verbose.\
`-r`\
Customize the risk of your portfolio when executing a command to run a trading bot.\
`-d`  
Customize the stop limit of your trading bot when executing a command to run a trading bot.\
`-l`\
Customize the minimum previous-day dollar volume for a stock we may consider.\
`-x`\
Customize the maximum of the range of the price of stocks to purchase.\
`-n`\
Customize the minimum of the range of the price of stocks to purchase.

**SYNTAX**\
`trading_bot-run`\ Runs the simple trading bot.

**AUTHORS**\
trading_bot was written by and is maintained by Emily Costa and Andrea Vieira.
