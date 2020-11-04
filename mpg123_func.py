#!/usr/bin/env python3
# PYTHON_PREAMBLE_START_STANDARD:{{{

# Christopher David Cotton (c)
# http://www.cdcotton.com

# modules needed for preamble
import importlib
import os
from pathlib import Path
import sys

# Get full real filename
__fullrealfile__ = os.path.abspath(__file__)

# Function to get git directory containing this file
def getprojectdir(filename):
    curlevel = filename
    while curlevel is not '/':
        curlevel = os.path.dirname(curlevel)
        if os.path.exists(curlevel + '/.git/'):
            return(curlevel + '/')
    return(None)

# Directory of project
__projectdir__ = Path(getprojectdir(__fullrealfile__))

# Function to call functions from files by their absolute path.
# Imports modules if they've not already been imported
# First argument is filename, second is function name, third is dictionary containing loaded modules.
modulesdict = {}
def importattr(modulefilename, func, modulesdict = modulesdict):
    # get modulefilename as string to prevent problems in <= python3.5 with pathlib -> os
    modulefilename = str(modulefilename)
    # if function in this file
    if modulefilename == __fullrealfile__:
        return(eval(func))
    else:
        # add file to moduledict if not there already
        if modulefilename not in modulesdict:
            # check filename exists
            if not os.path.isfile(modulefilename):
                raise Exception('Module not exists: ' + modulefilename + '. Function: ' + func + '. Filename called from: ' + __fullrealfile__ + '.')
            # add directory to path
            sys.path.append(os.path.dirname(modulefilename))
            # actually add module to moduledict
            modulesdict[modulefilename] = importlib.import_module(''.join(os.path.basename(modulefilename).split('.')[: -1]))

        # get the actual function from the file and return it
        return(getattr(modulesdict[modulefilename], func))

# PYTHON_PREAMBLE_END:}}}

import argparse
import os
import subprocess

# Get List of Music:{{{1
def getmusicinputs(filenameslist):
    cwd = os.getcwd() + '/'
    # add cwd to start if filename is not a full path
    filenameslist = [cwd + filename if filename[0] != '/' else filename for filename in filenameslist]

    retlist = []
    for filename in filenameslist:
        if os.path.isdir(filename):
            # get all music files inside folder
            folderfilenames = sorted([os.path.join(dp, f) for dp, dn, files in os.walk(filename) for f in files])
            print(folderfilenames[0: 100])
            folderfilenames = [folderfilename for folderfilename in folderfilenames if folderfilename.endswith('.mp3')]

            retlist = retlist + folderfilenames
        else:
            retlist.append(filename)

    return(retlist)


# mpg123 Basic Run:{{{1
def mpg123(mp3list, shuffle = False):
    arginputs = ['mpg123']
    if shuffle is True:
        arginputs.append('-Z')
    arginputs = arginputs + mp3list
    subprocess.call(arginputs)


# mpg123 Run Folder Inputs:{{{1
def mpg123_folderinputs_ap():
    """
    Play music in a set of folders/MP3files as specified on command line.
    """
    #Argparse:{{{
    import argparse
    
    parser=argparse.ArgumentParser()
    parser.add_argument("-Z", "--shuffle", action = 'store_true')
    parser.add_argument("filenameslist", nargs = '+')
    
    args=parser.parse_args()
    #End argparse:}}}

    mp3list = getmusicinputs(args.filenameslist)

    mpg123(mp3list, shuffle = args.shuffle)
# mpg123 Run from File:{{{1
def mpg123_fileinput(filename, shuffle = False):
    """
    Play music from file.
    """
    with open(filename) as f:
        filenameslist = f.read().splitlines()

    folder = os.path.abspath(os.path.dirname(filename)) + '/'
    # add filename's folder to start if filename is not a full path
    filenameslist = [folder + filename if filename[0] != '/' else filename for filename in filenameslist]

    mp3list = getmusicinputs(filenameslist)

    mpg123(mp3list, shuffle = shuffle)



def mpg123_fileinput_ap():
    #Argparse:{{{
    import argparse
    
    parser=argparse.ArgumentParser()
    parser.add_argument("-Z", "--shuffle", action = 'store_true')
    parser.add_argument("filename")
    
    args=parser.parse_args()
    #End argparse:}}}
    mpg123_fileinput(args.filename, shuffle = args.shuffle)
