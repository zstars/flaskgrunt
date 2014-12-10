import os
from flask import Flask, current_app, render_template_string, send_file
from werkzeug.exceptions import NotFound

app = Flask(__name__)

app.config["DEBUG"] = True
app.config["FLASK_YEOMAN_DEBUG"] = True

@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve_index(path):
    flask_yeoman_debug = app.config.get("FLASK_YEOMAN_DEBUG", False) or int(os.environ.get('FLASK_YEOMAN_DEBUG', False))
    fpath = 'dist'

    # While developing, we serve the app directory
    if flask_yeoman_debug:
        fpath = 'app'

    root_path = os.path.join(current_app.root_path, "ngapps/myapp")
    default_path = os.path.join(root_path, fpath)

    default_path_abs = os.path.join(default_path, path)

    if os.path.isfile(default_path_abs):
        if path == 'index.html':
            # If index.html is requested, we inject the Flask current_app config
            return render_template_string(open(default_path_abs).read().decode('utf-8'),
                                          config=current_app.config)
        return send_file(default_path_abs)

    # While development, we must check the .tmp dir as fallback, and watch out for bower_components.
    if flask_yeoman_debug:
        if path.startswith('bower_components'):
            alt_path = os.path.join(root_path)
            alt_path_abs = os.path.join(alt_path, path)
            if os.path.isfile(alt_path_abs):
                return send_file(alt_path_abs)

        # The .tmp dir is used by compass and for the template file
        alt_path = os.path.join(root_path, '.tmp')
        alt_path_abs = os.path.join(alt_path, path)
        if os.path.isfile(alt_path_abs):
            return send_file(alt_path_abs)

    raise NotFound()


if __name__ == '__main__':
    app.run()
