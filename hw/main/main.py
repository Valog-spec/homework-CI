from flask import Flask

from .flaskr.app import create_app

app: Flask = create_app()


if __name__ == "__main__":
    app.run(debug=True)
