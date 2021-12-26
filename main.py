from flask import Flask, render_template, request, redirect
from DbMS import DbMS
from api import API

app = Flask(__name__)
db = DbMS()
api = API()

# Временная тема
name = "Sergey"
db.add_user(name)


@app.route('/')
def main():
    currencies = api.get_currencies()

    return render_template("Main.html", currencies=currencies)


@app.route('/graph/<string:id>', methods=["GET", "POST"])
def graph(id):
    curr = api.get_currency_by_id(id)

    if request.method == "POST":
        amount = 0
        try:
            amount = float(request.form["amount"])
        except Exception:
            amount = -1
        if amount <= 0:
            return redirect(f'/graph/{id}')
        if request.form.get("Buy") is None:
            db.add_operation(name, "Sell", id, amount, float(curr["data"]["priceUsd"]))
        else:
            db.add_operation(name, "Buy", id, amount, float(curr["data"]["priceUsd"]))
        return redirect(f'/graph/{id}')

    return render_template("Trends.html", curr=curr)


@app.route('/balance')
def balance():
    data = db.get_portfolio(name)
    return render_template("balance.html", data=data)


@app.route('/history')
def history():
    operations = db.get_history(name)
    return render_template("History.html", operations=operations)


if __name__ == '__main__':
    app.run(debug=True)
