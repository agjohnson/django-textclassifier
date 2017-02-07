# -*- coding: utf-8 -*-

project = u'django-textclassifier'
copyright = u'2017, Anthony Johnson'
author = u'Anthony Johnson'

version = u'1.0'
release = u'1.0'

extensions = []

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

language = None

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
todo_include_todos = False

html_static_path = ['_static']
htmlhelp_basename = 'django-textclassifierdoc'

latex_elements = {}
latex_documents = [
    (master_doc, '{0}.tex'.format(project), project, author, 'manual'),
]

man_pages = [
    (master_doc, project, project, [author], 1)
]

texinfo_documents = [
    (master_doc, project, project, author, project, project, 'Miscellaneous'),
]
