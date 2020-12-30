#!/usr/bin/env python3
import os
from pathlib import Path
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '/')

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
