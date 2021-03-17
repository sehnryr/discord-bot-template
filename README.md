# Discord Bot Template

<p align="center">
  <a href="//github.com/Sehnryr/discord-bot-template/releases"><img src="https://img.shields.io/github/v/release/Sehnryr/discord-bot-template"></a>
  <a href="//github.com/Sehnryr/discord-bot-template/commits/main"><img src="https://img.shields.io/github/last-commit/Sehnryr/discord-bot-template"></a>
  <a href="//github.com/Sehnryr/discord-bot-template/releases"><img src="https://img.shields.io/github/downloads/Sehnryr/discord-bot-template/total"></a>
  <a href="//github.com/Sehnryr/discord-bot-template/blob/main/LICENSE.md"><img src="https://img.shields.io/github/license/Sehnryr/discord-bot-template"></a>
  <a href="//github.com/Sehnryr/discord-bot-template"><img src="https://img.shields.io/github/languages/code-size/Sehnryr/discord-bot-template"></a>
  <a href="//github.com/Sehnryr/discord-bot-template/issues"><img src="https://img.shields.io/github/issues-raw/Sehnryr/discord-bot-template"></a>
</p>

A discord bot template written in Python with `discord.py` working with cogs.

This repository is a discord bot template for everyone to use for their own projects freely.

## Installation
Since this repo is a template, you can simply click on the **Use this template** button *(which is beside the download one)* to create a GitHub repository based on this template.

- Alternatively you can Clone/Download the repository using `git clone`

And then you'll have to install the depencies :
- Windows : `pip install -r requirements.txt`
- Linux/Debian : `pip3 install -r requirements.txt` (you may not have `pip3` installed, as such, you can get it with : `apt install python3-pip`)

## Getting Started
> *As this template is written in Python, you may need basis in this language.*

The config file being pretty much obvious to use, I don't think there's much to explain here.

- For an extended explanation you can find the wiki [here](//github.com/Sehnryr/discord-bot-template/wiki)

> *You will also need some knowledge of cogs in `discord.py`.*

Cogs will need to be stored in `./cogs` by default.

You can find some basic Cogs [here](//github.com/Sehnryr/cogs)

Once everything setup you'll just need to execute `bot.py`
- Windows : `python bot.py`
- Linux/Debian : `python3 bot.py` (you can also run `bot.py` as is thanks to the shebang, make sure to have the right permission to do so, you can always use `chmod +x bot.py` to set them)

## Disclaimers
Before starting using this template blindly, please note that this template is not supposed to be the best template, but is objectivly a good template to start creating a new discord bot in a simple way.

Considering every system, you may need the according interpreter. *I suggest using Python 3.7 since I didn't test my program in anterior versions of Python*

## Versioning
We're using [SemVer](https://semver.org/) for versioning.