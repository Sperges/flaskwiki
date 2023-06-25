import json
import app


print(json.dumps(app.generate_inner_tree_dict(app.base_md_path), indent=4))