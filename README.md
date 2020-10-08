# The Modulus Book
The purpose of this book is to provide the reader with a brief introduction to the concept of discrete modulus along with the Python modulus code.

## Reading the book
The easiest way to read the book is in HTML form.  A current copy of the book can be found [here](https://nathan-albin.github.io/modulus_book/).

## Running the code
In order to run the code for yourself, you'll need a Python environment.  The current version of the book is developed using the [pipenv](https://github.com/pypa/pipenv) tool to manage the environment.  If you use pipenv, then everything you need is contained in `Pipfile` and `Pipfile.lock`.  If you have some other way of managing your Python environment, then you'll want to look at `Pipfile` for a list of important packages.  These include
- python3
- jupyter
- networkx
- numpy
- matplotlib
- cvxpy
- pycddlib

Once your Python environment is set up, you should start jupyter notebook in the project root directory.  There you will find the notebook files used to generate the book.    You can also find the essential modulus library code in the `modulus_tools` directory.

## Building the book
In order to build the book from source, you'll need to have your system configured to run the code.  You'll also need the jupyter-book package (included in the python environment).  To build the book, enter the following command in the project root directory.

```jupyter-book build .```