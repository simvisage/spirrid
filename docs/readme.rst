
Source directory for documentation generation
=============================================

The generated documentation is available online at

http://simvisage.com/docs/spirrid
 
In order to generate the
documentation you need to install sphinx utility
(http://sphinx.pocoo.org). On it can be installed by issuing

    $ apt-get install python-sphinx 

Then, run the 

	$ cd docs
	$ export PYTHONPATH="../"
	$ python gendocs.py
	
The generated documentation is located in the directory 

    $HOME/.spirrid/index.html 

