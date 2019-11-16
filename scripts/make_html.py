"""
Generates HTML files from notebooks.
"""

import os
import subprocess
from shutil import rmtree, copy
import re

build_dir     = '../html/'
notebook_dir  = '../notebooks/'
code_dir      = 'modulus_tools/'
template_file = '../templates/html.tpl'
bib_file      = 'References'
github_base   = 'https://github.com/nathan-albin/modulus_book/blob/master/notebooks/'

chapters = ['Contents', 
			'Introduction',
			'The_Basic_Algorithm']

# regular expression for bib entries in html file
bib_entry = re.compile(r'\[<a name="(.*)">(.*)</a>\]')

# regular expression for code links
code_link = re.compile('<a href=".*">(' + code_dir + '.*)</a>')

# process the bibfile data
bibdata = {}
print('Processing bib file...')
with open(build_dir + bib_file + '.html') as f:
    for line in f:
        match = bib_entry.search(line)
        if match:
            bibdata[match.group(1)] = match.group(2)

# process chapters
for i, chapter in enumerate(chapters):
    source_file = notebook_dir + chapter + '.ipynb'
    target_file = build_dir  + chapter + '.html'
    print()
    print('-------------------------------------')
    print('Processing {}...'.format(source_file))

    # check if the html file already exists
    if os.path.isfile(target_file) and os.path.getmtime(source_file) <= os.path.getmtime(target_file):

        print('  {} is up to date'.format(target_file))

    else:

        # run nbconvert
        args = ['jupyter', 'nbconvert', '--to', 'html', '--execute',
                '--ExecutePreprocessor.kernel_name=python',
                '--template', template_file,
                '--output', target_file, source_file]
        subprocess.check_call(args)

    # post-process files
    with open(target_file, 'r') as f:
    	content = f.read()

    # process ipynb links to html links in the generated file
    print('Replacing links to other notebooks...')
    for c in chapters:
    	content = content.replace('{}.ipynb'.format(c), '{}.html'.format(c))

    # replace any links to the code
    print('Replacing links to code...')
    content = code_link.sub('<a href="{}\\1">\\1</a>'.format(github_base), content)

    # replace citations
    print('Replacing citations...')
    for cite in bibdata:
        key = bibdata[cite]
        src = '<a href="">' + cite + '</a>'
        tgt = '[<a href="' + bib_file + '.html#' + cite + '">' + key + '</a>]'
        content = content.replace(src, tgt)

    # check for empty links
    if content.find('href=""') >= 0:
        print('*** WARNING *** Empty hyperlinks found.')

    # rewrite the post-processed file
    with open(target_file, 'w') as f:
        f.write(content)
