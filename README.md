This project was created for learning purpose only. **Please do not use in production environment.**

---

# gitgauto
A simple to use git CLI automation using python

```
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
```

To use it as a CLI tool give permission and copy to `PATH`
```
//change the name as per your choice doesn't effect the functioning

$ chmod a+x git_automate.py   
$ sudo cp git_automate.py ~/.local/bin/
```
