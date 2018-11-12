import re
from os import system
import json
import warnings

import nbformat

def _comment(cell, commentstart='<!--', commentend='-->'):
    """
    Change the source of the cell to include the entire cell JSON as formatted string.

    Parameters
    ----------
    cell : JSON cell dict
    commentstart : Start of comment string in markdown
    commentend : End of comment string in markdown
    """
    newcell = {}
    newcell['source'] = commentstart + json.dumps(cell) + commentend
    return newcell

def _export_or_comment(cell, exportflag):
    """
    Parameters
    ----------
    cell : JSON cell dict
    exportflag : str
    """
    if exportflag in cell['source'] and cell['cell_type']=='markdown':
        flaglocation = cell['source'].find(exportflag)
        cell['source'] = (
            cell['source'][:flaglocation]
            + cell['source'][flaglocation+len(exportflag):]
            + '\n\n'
            + _comment(cell)['source']
        )
    else:
        cell['source'] = _comment(cell)['source']
    cell['cell_type'] = 'markdown'
    return cell


def to_markdown(from_ipynb_file, to_markdown_file, exportflag='@export',
                commentstart='<!--', commentend='-->'):
    """
    Parameters
    ----------
    from_ipynb_file, to_markdown_file : str
    exportflag : str
    """
    nb = nbformat.read(from_ipynb_file, as_version=4)
    nb['cells'] = [_export_or_comment(c, exportflag) for c in nb['cells']]

    tmpfile = 'tmp_' + from_ipynb_file
    nbformat.write(nb, tmpfile, version=4)
    _ = system('jupyter nbconvert --to markdown {} --output {}'
               .format(tmpfile, to_markdown_file))
    _ = system('rm {}'.format(tmpfile))

    # Prepend metadata
    nb_meta = nb.copy()
    _ = nb_meta.pop('cells')

    meta = commentstart + json.dumps(nb_meta) + commentend

    with open(to_markdown_file, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(meta.rstrip('\r\n') + '\n' + content)

    # with open(to_markdown_file, 'a') as mdfile:
    #    mdfile.write(meta)

def from_markdown(from_markdown_file, to_ipynb_file, exportflag='@export',
                  commentstart='<!--', commentend='-->'):
    """
    Parameters
    ----------
    from_markdown_file, to_ipynb_file : str
    exportflag : str
    """
    # initialize imported notebook
    nbimport = {}
    nbimport['cells'] = []

    with open(from_markdown_file) as mdfile:
        rawimport = mdfile.read()
    cellstart = [m.end() for m in re.finditer(commentstart, rawimport)]
    cellend = [m.start() for m in re.finditer(commentend, rawimport)]

    cells = []
    # first cell is always notebook metadata, skip that.
    for s, e in zip(cellstart[1:], cellend[1:]):
        try:
            cells.append(json.loads(rawimport[s:e]))
        except json.JSONDecodeError:
            # omit anything that doesn't fit
            warnings.warn('Could not parse {}'.format(rawimport[s:e]))

    for k, cell in enumerate(cells):
        if exportflag in cell['source'] and cell['cell_type']=='markdown':
            if k==0:
                contentstart = 0
            else:
                contentstart = cellend[k-1]+len(commentend)
            contentend = cellstart[k]-len(commentstart)
            cell['source'] = re.sub(r'(\n)\1+', r'\1\1',
                                    rawimport[contentstart:contentend]
                                   ) + exportflag
    nbimport['cells'] = cells

    nbimport.update(json.loads(rawimport[cellstart[0]:cellend[0]]))
    nbformat.write(nbformat.from_dict(nbimport), to_ipynb_file)
