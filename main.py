from flask import Flask, render_template, request
from DbMS import DbMS


app = Flask(__name__)
# db = DbMS("bolt://localhost:7687", "neo4j", "password")


@app.route('/balance')
def balance():
    # res = db.greeting("hello, world")
    # return res
    return render_template("balance.html")


@app.route('/history')
def history():
    # res = db.greeting("hello, world")
    # return res
    return render_template("History.html")


if __name__ == '__main__':
    app.run(debug=True)
