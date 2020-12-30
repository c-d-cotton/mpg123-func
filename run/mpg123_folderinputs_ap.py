#!/usr/bin/env python3
import os
from pathlib import Path
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '/../')

sys.path.append(str(__projectdir__))
from mpg123_func import mpg123_folderinputs_ap
mpg123_folderinputs_ap()
