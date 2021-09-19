import flask

app = flask.Flask(__name__)

@app.route("/")  # Python decorator
def main():
    return flask.render_template("index.html")

app.run(
    debug=True
)

