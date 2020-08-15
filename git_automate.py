#!/usr/bin/env python3

# For main file
import click                        # For default values in input
from sys import argv                # To get command arguments
import subprocess as cmd            # To execute bash commands
from colorama import Fore, Style    # For colored and formatted output

# For functions
import os                           # To get the downloads path
import platform                     # Check platform (linux, macos, windows)
from pathlib import Path            # Get the user home directory

# Copy this file to root directory of local git repo
# Add this file to .gitignore
args = argv[1:]


def difference():
    print(f"\n{Fore.GREEN}{Style.BRIGHT}+++++ Difference between last committed and current code +++++\n{Style.RESET_ALL}")
    cmd.run('git --no-pager diff origin/master...master', check=True, shell=True)


def checkout():
    if (args.count('-y') == 1 or args.count('--yes') == 1):
        print(
            f"\n\n{Fore.GREEN}{Style.BRIGHT}+++++ CHECKOUT BRANCH +++++\n{Style.RESET_ALL}")

    elif branch != 'master' or get_current_branch() != branch:
        ch = input(
            f"\nCheckout branch FROM {Fore.RED}{get_current_branch()} TO {Fore.GREEN}{branch}{Style.RESET_ALL}? [Y]/n :  ")

        print('\n')
        if ch.lower().startswith('n'):
            return
        else:
            cmd.run(f'git checkout -b {branch}', check=True, shell=True)


def commit():
    print(f"\n{Fore.GREEN}{Style.BRIGHT}+++++ Git Status +++++\n{Style.RESET_ALL}")
    cmd.run('git status', check=True, shell=True)

    if (args.count('-y') == 1 or args.count('--yes') == 1):
        print(
            f"\n{Fore.GREEN}{Style.BRIGHT}+++++ Staging all the changes +++++\n{Style.RESET_ALL}")

    else:
        ch = input(
            f"\n\n{Fore.GREEN}+++ Stage all the changes? [Y]/n :{Style.RESET_ALL}  ")

        if ch == 'n':
            print(f"\n{Fore.RED}Can't continue, why?")
            print(
                f"How you gonna push changes without commiting them.. huh?{Style.RESET_ALL}")
            exit()

    cmd.run('git add . -v', check=True, shell=True)
    msg = input(f'\n{Fore.GREEN}+++ Commit message: {Style.RESET_ALL}')
    cmd.run(f'git commit -v -m "{msg}"', check=True, shell=True)


def reset():
    if (args.count('-y') == 1 or args.count('--yes') == 1):
        print("\n+++ This one is serious. So, skip confirmation prompt won't work :)")
    ch = input(
        f"\n{Fore.RED}{Style.BRIGHT}+++ Reset the staged changes? [N]/y :  {Style.RESET_ALL}")

    print('\n')
    if ch.lower().startswith('n'):
        return
    else:
        cmd.run('git reset *', check=True, shell=True)


def push():
    if (args.count('-y') == 1 or args.count('--yes') == 1):
        print(
            f"\n{Fore.GREEN}{Style.BRIGHT}+++++ PUSH REPO +++++\n{Style.RESET_ALL}")

    else:
        ch = input(
            f"\n{Fore.GREEN}{Style.BRIGHT}+++ Push commits to origin?{Style.RESET_ALL}   ")
        if ch.lower().startswith('n'):
            return

    cmd.run(f'git remote set-url origin https://{user}:{password}@github.com/{user}/{repo}.git',
            check=True, shell=True)
    cmd.run('git push -u origin master', check=True, shell=True)


def pull():
    if (args.count('-y') == 1 or args.count('--yes') == 1):
        print(
            f"\n{Fore.GREEN}{Style.BRIGHT}+++++ PULL REPO +++++\n{Style.RESET_ALL}")
    else:
        ch = input(
            f"\n{Fore.GREEN}{Style.BRIGHT}+++ Pull commits from origin?{Style.RESET_ALL}   ")
        if ch.lower().startswith('n'):
            return

    cmd.run('git pull -v --rebase origin', check=True, shell=True)


def download_zip():
    print(f"\n{Fore.GREEN}+++++ Downloading source code zip from github +++++\n{Style.RESET_ALL}")
    print('\nChange directory as per your needs [default = Downloads]')

    download_dir = get_downloads_folder()
    cmd.run(f'wget https://github.com/{user}/{repo}/archive/{branch}.zip -P {download_dir}',
            check=True, shell=True)


#
#
#
# program start
commands = [
    '--version',
    '--help',
    '-h',
    'reset',
    '-r',
    'pull',
    '-p',
    'download',
    '-d',
    '--yes',
    '-y'
]

if len(args) > 0:
    for i in args:
        if commands.count(i) == 0:
            print(f'{Fore.RED}{Style.BRIGHT}Program terminated.')
            print(f'Invalid command given{Style.RESET_ALL}')
            exit()


if (args.count('--version') == 1):
    print("\ngitgauto (jit-g auto): v1.0 Initial Release -- just kidding it's a time pass")
    exit()

elif (args.count('--help') == 1 or args.count('-h') == 1):
    print_help()
    exit()


user = click.prompt('Username ',
                    type=str,
                    default=''
                    )
password = click.prompt('Password ',
                        type=str,
                        default='',
                        hide_input=True,
                        show_default=True
                        )
repo = click.prompt('Repo name ',
                    type=str,
                    default=''
                    )
branch = click.prompt('Enter working branch  ',
                      type=str,
                      default='master'
                      )


check_git_path()
checkout()
difference()
# Reset or pull after showing defference
if args.count('reset') == 1 or args.count('-r') == 1:
    reset()
    exit()
if args.count('pull') == 1 or args.count('-p') == 1:
    pull()
    exit()
#
commit()
push()

# Download source code zip file after pushing latest commits
if args.count('download') == 1 or args.count('-d') == 1:
    download_zip()
    exit()


# Functions
def print_help():
    print(
        '''
    Git Automation Script by Gagan Yadav @ github.com/gaganyadav80

    usage: gitgauto.py [options] <commands>

    Where <commands> is one of:

                reset (-r) - Unstage (reset) the changes in the local repo
                 pull (-p) - Perform the <git pull> command on your current local repo
             download (-d) - After commit and push changes download the source code zip file

    Program will exit after performing the <command> passed to script.

    Options:
     --version          : show program's version number and exit
     -h [--help]        : show this help message and exit
     -y [--yes]         : skip confirmation prompt for all automation actions
    '''
    )
    return

# Get the location for user's download folder


def get_downloads_folder():
    path = str(os.path.join(Path.home(), "Downloads"))
    return path


# return the current branch user is working on
def get_current_branch():
    current_branch = cmd.run('git --no-pager branch',
                             check=True, shell=True, stdout=cmd.PIPE)

    current_branch = str(current_branch.stdout).replace("\\n'", '')
    return current_branch[4:]


# Return the present directory of the script
def get_current_dir():
    directory = str(os.getcwd())
    length = len(directory)-1   # 20

    if (platform == 'linux' or platform == 'darwin'):
        slash = '/'
    else:
        slash = '\\'

    index = directory.rfind(slash)    # 11
    stringDir = directory[-(length - index):]
    return stringDir


# Check if the current directory is a git repo
def check_git_path():
    if (cmd.call(["git", "branch"], stderr=cmd.STDOUT, stdout=open(os.devnull, 'w')) != 0):
        print("\n+++++ This directory is not a git working tree. +++++")

        # ch = input("\nWant to initialize a git repository? [y]/n")
        print('\nChange directory to correct one OR')
        ch = click.prompt('Do you want to initialize a NEW git repo here? y/[N] ',
                          type=str,
                          default='n',
                          show_default=False
                          )

        if ch.lower().startswith('n'):
            exit(0)
        else:
            if (get_current_dir() != repo):
                print("\nThis directory doesn't match your defined repository name.")

                ch = input("You sure it's the right folder? [Y/n]:  ")
                if ch.lower().startswith('n'):
                    repo_path = input(
                        'Enter the root path of local repository:  ')
                    cmd.run(f'cd {repo_path} && git init',
                            check=True, shell=True)
            else:
                cmd.run('git init', check=True, shell=True)

            cmd.run(f'git remote add origin https://{user}:{password}@github.com/{user}/{repo}.git',
                    check=True, shell=True)
