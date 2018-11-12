# The notebook-agnostic notebook
or: A simple workflow to collaborate in an IPython notebook with people not knowing about IPython notebooks, and publish to journals that don't, either.

## The two major obstacles...
to using IPython notebooks all the way from data analysis to publishing in many fields of science are

1. Traditional journals do not accept notebooks for submission, and
2. Most collaborators are unwilling to learn new software to integrate themselves into a collaborative workflow.

## The solution...
is easy, just make everyone learn about notebooks!

Jk, but we have to hide the intricacies of the notebook behind some nice Markdown, which can be edited by our collaborators without straining their willingness to read obscure code in obscure software, and eventually converted to latex (or other) before submission to a journal.

## `markbook`...
addresses those problems by a simple workflow that lets you convert between .ipynb and .md files, while **preserving all metadata**!

Problem 1. is solved by putting a textstring (default: '@export') anywhere into any markdown cell you'd like to see exported, e.g.

```
I'd like this sentence to end up in my final publication. @export
Also, $$E=mc^2$$.
```

Problem 2. is addressed by bluntly putting all notebook cell metadata as JSON strings into Markdown comments. This can't be the ultimate solution because one has to stay clear of a big chunk of the .md file while editing, but it works. Maybe someone at some point finds a more genuine way of doing this, let me know, if ever...

## Usage

```python
from markbook import to_markdown
to_markdown('demo.ipynb', 'demo.md')
```

`demo.md` can then be edited in the cloud, e.g. using a Google Drive & Stack Edit, and versioned locally. When changes are merged, they can be pulled back into a .ipynb file using

```python
from markdown import from_markdown
from_markdown('demo.md', 'demo-reimported.ipynb')
```

## Other software
There are two other packages (I'm aware of) that address the conversion Markdown <-> IPython notebooks:
[Notedown](https://github.com/aaren/notedown), and [ipymd](https://github.com/rossant/ipymd). Both seem to lose metadata to some extent (as far as I understand), making pulling back incremental changes into the .ipynb difficult. Also, in the standard notebook, exporting only a subset of the cells requires defining cell metadata, somewhat cumbersome in Jupyter Lab as it has to be formatted as JSON.

## Improvements, hints, tips, ...

are always welcome!
