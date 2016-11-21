GESSA is a software for dense landmarking of 3D polyhedral surfaces. For more details on the methodology, please see https://arxiv.org/abs/1608.08199.

Requirements
------------
The GESSA software is written in python and compiled using Nuitka (http://nuitka.net/). At the moment, the software is available for systems running GNU/Linux (Tested on Linux Mint LMDE 2, with Python 2.7). 

Required python packages are: numpy, scipy, sklearn, mayavi.

For debian-based systems, the following commands should install all required packages:
sudo apt-get install python python-numpy python-scipy python-sklearn
sudo pip install mayavi

3D polyhedral surfaces should be in .ply ascii format.

Installation
------------

To install GESSA, download the uncompress the package folder. 

Usage
-----

A python script that showcases how to import and use the GESSA is included in the gessa package folder (gessa/ensemble_sampling.py).

We strongly encourage users to follow as their guideline the bash script 'example/run_example.sh'.

In order to run the example, cd to the example folder and execute the run_example.sh script:
# bash ./run_example 

See inside the example bash script for comments on the parameters.

The gessa directory can be added to the python's library path (please see known issue 2).


Known Issues
------------
1. Example error: "ImportError: gessa/FaceViewer.so: undefined symbol: _PyUnicodeUCS4_AsDefaultEncodedString"

The package has been compiled for use with a Python 2.7 interpreter built with Unicode UCS2. If, when importing a a gessa module, a similar error as above is encountered, it means that the Python interpreter in that system uses Unicode UCS4. Please let us know in such an event, and we will attempt to provide a suitable package version.

2. Example error: "PicklingError: Can't pickle FaceViewer.FaceViewer: it's not the same object as FaceViewer.FaceViewer"

At the moment, there is an issue when trying to use gessa from a script on a different folder from the gessa package, and use multiple cores. The software fails with an error similar to the above.

Until the bug is fixed, please run gessa with multiprocessing enabled through the script (ensemble_sampling.py) provided in the gessa folder.

Contact and Bug Report
----------------------

For further questions or problems, please send an e-mail at d.tsagkrasoulis12@imperial.ac.uk.
