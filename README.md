# braindump

![Brian](https://raw.githubusercontent.com/opthomas-prime/braindump/master/braindump.png)

## Org mode FTW
I discovered Org mode for me. I won't maintain this anymore...

## Introduction
I'm getting older - and i keep forgetting stuff.
I'm not talking about contact data, user credentials, technical documentations and such things.
There are well-known tools to store such information in a sorted/organized manner.
I talk about undefined/unstructured information.
My workmate always keeps one plain text file in his favorite editor opened to store such arbitrary information and uses it's search mechanism to lookup things.
I wanted that too, but in a slightly more 'structured' fashion.
So i built this little tool to accomplish this...

tl;dr: Helps to remember stuff that wont fit in any scheme.

## Disclaimer
- Read `LICENSE`. If anything in this repository bricks your PC - not my fault!

## Dependencies
- Python 3 (build and tested with 3.6.0)
- Whoosh - https://pypi.python.org/pypi/Whoosh (build and tested with 2.7.4):
    - `sudo pip3 install whoosh`
- Build and tested on Arch Linux. Mac OS and BSD shouldn't be a problem.
Theoretically it should work on Windows too...

## Installation
- It's one single script. Place it where you want.
- If you don't know what to do:
    - Copy `braindump.py` to a place where your `$PATH` points to (e.g. `sudo cp braindump.py /usr/local/bin/brian`).
    - Ensure the script is executable (`sudo chmod +x /usr/local/bin/brian`).
- If you trust me and still don't know what to do (also installs Whoosh):

```
curl https://raw.githubusercontent.com/opthomas-prime/braindump/master/setup.sh | sh
```

## Brian?
Initially i wanted to name the command/executable `brain` - but i kept typing `brian` accidentally... As well i found it cocky to introduce a command named `brain`. Besides that, i think Brian is a nice name.

## Usage
- Normally you don't need to do anything before you can start using this.
The configuration should be created with default values.
Just write down the first thing you want to remember with:

```
➜  ~ brian dump

```
- Braindump tries to detect an installed editor (in my favorite order). If you want to change the editor open `~/.braindump.conf` after the first start and reconfigure it.
- There are basically two operations: `dump` and `remember` (you can use `rem` for that too):
    - `dump`: opens an editor for a new entry (memory) and indexes the contents after the editor is closed.
    - `remember [terms [terms ...]]`: lookup things via one or more search terms. If there is exactly one hit - the entry is opened automatically. If there are several hits - you get a list of results to choose from.
