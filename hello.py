import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    with open("items.jl", "r") as json_file:
        data = json_file.readlines()

    return data[0]

if __name__ == "__main__":
    app.run(debug=True)
