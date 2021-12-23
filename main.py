from flask import Flask, render_template, request
from DbMS import DbMS
from api import API

app = Flask(__name__)
# db = DbMS()
api = API()


@app.route('/')
def main():
    currencies = api.get_currencies()

    return render_template("Main.html", currencies=currencies)


@app.route('/graph/<string:id>')
def graph(id):

    return render_template("Trends.html", id=id)


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
