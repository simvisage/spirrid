Source directory for documentation generation
=============================================

The generated documentation is available online at

http://simvisage.com/docs/spirrid
 
In order to generate the
documentation you need to install sphinx utility
(http://sphinx.pocoo.org). On ubuntu 
it can be installed by issuing
::

    $ apt-get install python-sphinx 

Then, the **gen_docs.py** script can be run to 
generate the documentation. The root directory
of the **spirrid** package must be contained in the 
PYTHONPATH environment variable. 
::

    $ cd docs
    $ export PYTHONPATH="../"
    $ python gen_docs.py
	
The generated documentation is located in the directory
::

    $HOME/.spirrid/index.html 

