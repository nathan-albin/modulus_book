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

chapters = ['Contents', 
			'Introduction',
			'The_Basic_Algorithm']

# regular expression for bib entries in html file
bib_entry = re.compile(r'\[<a name="(.*)">(.*)</a>\]')

# regular expression for code links
code_link = re.compile('<a href=".*">(' + code_dir + '.*)\\.py</a>')

# delete the modulus code files from the build directory
if os.path.exists(build_dir + code_dir):
    rmtree(build_dir + code_dir)

# process the bibfile data
bibdata = {}
print('Processing bib file...')
with open(build_dir + bib_file + '.html') as f:
    for line in f:
        match = bib_entry.search(line)
        if match:
            bibdata[match.group(1)] = match.group(2)

# walk through the code directory
for root, _, files in os.walk(notebook_dir + code_dir):

    loc_dir = root[len(notebook_dir):]

    # skip ipynb hidden files
    if root.find('.ipynb_checkpoints') == -1:

        # create the root directory in build
        os.mkdir(build_dir + loc_dir)

        # pygmentize .py files
        for f in files:
            if f[-3:] == '.py':
                
                args = ['pygmentize', '-f', 'html', '-O', 'full,linenos=1',
                        '-o', build_dir + loc_dir + '/' + f[:-3] + '_py.html',
                        root + '/' + f ]
                print('Pygmentizing {}...'.format(root + f))
                subprocess.check_call(args)
    
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
    content = code_link.sub('<a href="\\1_py.html">\\1.py</a>', content)

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
