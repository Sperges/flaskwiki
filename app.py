import os
import markdown
from markupsafe import Markup
from flask import Flask, abort, jsonify, render_template

def generate_tree_data():
	tree_data = []
	for root, dirs, files in os.walk(base_md_path):
		node = {
			'id': root,
			'text': os.path.basename(root),
			'children': [],
		}
		for file in files:
			node['children'].append({
				'id': os.path.join(root, file),
				'text': file,
			})
		tree_data.append(node)
	return tree_data


app = Flask(__name__)
base_md_path = 'md/'
tree_data = generate_tree_data()


@app.route('/tree')
def tree():
	return jsonify(tree_data)


@app.route('/')
def hello_world():
    return '<p>Hello, World!</p>'


@app.route('/<page>')
def page(page=None):
	file_path = f'{base_md_path}{page}.md'

	if not os.path.exists(file_path):
		abort(404)

	file = open(file_path, 'r')
	md_content = Markup(markdown.markdown(file.read()))

	return render_template('wiki_page.html', content=md_content)


@app.errorhandler(404)
def page_not_found(error):
	return render_template('page_not_found.html'), 404