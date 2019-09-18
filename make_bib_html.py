"""
Generates HTML version of bibliography.
"""

import shutil
import subprocess

bibfile = 'References'
htmldir = 'build_html/'

# get rid of unwanted keys
args = ['bib2bib', 
		'-s', '$key',
		'-ob', bibfile + '.bib',
		'--remove', '__markedentry',
		'--no-comment',
		bibfile + '.bib']
subprocess.check_call(args)

args = ['bibtex2html', bibfile + '.bib']
subprocess.check_call(args)
shutil.copy(bibfile + '.html', htmldir + bibfile + '.html')
shutil.copy(bibfile + '_bib.html', htmldir + bibfile + '_bib.html')
