# The Modulus Book
An introduction to discrete modulus concepts and algorithms through Jupyter notebooks.

## Reading the book
The easiest way to read the book is in HTML form.  A current copy of the book can be found [here]().

## Running the code
In order to run the code for yourself, you'll need a Python environment.  The current version of the book is developed using the [pipenv](https://github.com/pypa/pipenv) tool to manage the environment.  If you use pipenv, then everything you need is contained in `Pipfile` and `Pipfile.lock`.  If you have some other way of managing your Python environment, then you'll want to look at `Pipfile` for a list of important packages.  These include
- python3.7
- jupyter
- networkx
- numpy
- matplotlib
- cvxpy
Once your Python environment is set up, you should start jupyter notebook and navigate into the `notebooks` directory.  There you will find the notebook files used to generate the book.  (Note: many links may not work in the notebook text.  These notebooks were designed to generate the book, and links are processed specially by the build code.)  You can also find the essential modulus library code in `notebooks/modulus_tools`.

## Building the book
In order to build the book from source, you'll need to have your system configured to run the code.  You'll also need [bibtex2html](https://github.com/backtracking/bibtex2html) in order to build the bibliography files.  In the `scripts` directory, you'll find two Python scripts.  `make_bib_html.py` processes the BibTeX file into HTML form and `make_html.py` runs `nbconvert` on the Modulus Book's notebooks, converting them to HTML and post-processing them to make the pages link together.
