import os

from dotenv import load_dotenv
from flask import Flask


app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY=os.environ["SECRET_KEY"],
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )


@app.route("/")
def hello():
    return "Hello World"


if __name__ == "__main__":
    app.run(load_dotenv=True)
