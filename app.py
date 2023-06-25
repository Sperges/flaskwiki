import os
import markdown
from pathlib import Path
from flask import Flask, abort, render_template


def get_sitemap_id():
	id = -1
	def increment():
		nonlocal id
		id += 1
		return id
	return increment


app = Flask(__name__)
base_md_path = 'md'
sitemap_id = get_sitemap_id()


def generate_tree_dict(folder_path):
    return generate_inner_tree_dict(folder_path)['children']


def generate_inner_tree_dict(folder_path):
    if not os.path.isdir(folder_path):
        return None
    
    folder_name = os.path.basename(folder_path)
    tree = {
        'title': folder_name,
        'href': None,
        'children': [],
        'id': sitemap_id(),
	}

    files = sorted(os.listdir(folder_path))
    for file_name in files:
        file_name = Path(file_name).resolve().stem
        file_path = f'{folder_path}/{file_name}'
        if os.path.isdir(file_path):
            subtree = generate_inner_tree_dict(file_path)
            if subtree:
                tree['children'].append(subtree)
        else:
            tree['children'].append({
                'title': file_name,
                'href': file_path.lstrip(base_md_path),
                'children': None,
                'id': sitemap_id(),
			})

    return tree

@app.route('/api/<path:location>')
def page_api(location=None):
	file_path = f'{base_md_path}/{location}.md'
        
	if not os.path.exists(file_path):
		abort(404)

	file = open(file_path, 'r')
	return markdown.markdown(file.read())

@app.route('/<path:location>')
def page(location=None):
	return render_template(
		'page.html',
        sitemap=generate_tree_dict(base_md_path),
		#sidebar=render_template('sidebar.html', sitemap=generate_tree_dict(base_md_path)),
		path=location,
		)


@app.errorhandler(404)
def page_not_found(error):
	return render_template('page_not_found.html'), 404