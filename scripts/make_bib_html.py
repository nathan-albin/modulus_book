"""
Generates HTML version of bibliography.
"""

import shutil
import subprocess

bibdir  = '../references/'
bibfile = 'References'
htmldir = '../html/'

# get rid of unwanted keys
args = ['bib2bib', 
		'-s', '$key',
		'-ob', bibdir + bibfile + '.bib',
		'--remove', '__markedentry',
		'--no-comment',
		bibdir + bibfile + '.bib']
subprocess.check_call(args)

# process with bibtex2html
args = ['bibtex2html', bibdir + bibfile + '.bib']
subprocess.check_call(args)

# move html files ot html directory
shutil.move(bibfile + '.html', htmldir + bibfile + '.html')
shutil.move(bibfile + '_bib.html', htmldir + bibfile + '_bib.html')
