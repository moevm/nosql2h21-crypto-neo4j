from neo4j import GraphDatabase, Result
import time


class DbMS:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="10122000"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def __del__(self):
        self.driver.close()

    def add_user(self, name):
        query = "MATCH (n:Client {name:\'" + name + "\'}) RETURN n"
        res = self._make_query(query)
        if not res:
            query = "CREATE (n:Client {name:\'" + name + "\'})"
            self._make_query(query)

    def add_operation(self, name, operation, id, amount, priceUsd):
        price = amount * priceUsd
        date = round(time.time() * 1000)

        query = "MATCH (n:Client {name:\'" + name + "\'}),(m:Сryptocurrency {name:\'" + id + "\'}) RETURN n, m"
        res = self._make_query(query)
        if res:
            query = "MATCH (n:Client {name:\'" \
                    + name \
                    + "\'}), (m:Сryptocurrency {name:\'" \
                    + id \
                    + "\'}) CREATE (n)-[r:Operation {count:" \
                    + str(amount) \
                    + ", date:" \
                    + str(date) \
                    + ",price:" \
                    + str(price) \
                    + ",type:\'" \
                    + operation \
                    + "\'}]->(m)"
        else:
            query = "MATCH (n:Client {name:\'" \
                    + name \
                    + "\'}) CREATE (n)-[r:Operation {count:" \
                    + str(amount) \
                    + ", date:" \
                    + str(date) \
                    + ",price:" \
                    + str(price) \
                    + ",type:\'" \
                    + operation \
                    + "\'}]->(m:Сryptocurrency {name:\'" + id + "\'})"
        self._make_query(query)

    def export_data(self):
        query = "MATCH (n) RETURN n"
        return self._make_query(query)

    def get_history(self, name):
        query = "MATCH (n:Client {name: \'" \
                + name \
                + "\'})-[r:Operation]->(m:Сryptocurrency) RETURN r.type, m.name, r.count, r.date, r.price"
        return self._make_query(query)

    def get_portfolio(self, name):
        query = "MATCH (n:Client {name: \'" \
                + name \
                + "\'})-[r:Operation]->(m:Сryptocurrency) RETURN r.type, m.name, r.count, r.date, r.price"
        data = self._make_query(query)

        # Конвертируем из операций в имеющиеся валюты
        names = set(map(lambda el: el["m.name"], data))
        result = []
        for name in names:
            count = 0
            price = 0
            for operation in data:
                if operation["m.name"] == name:
                    if operation["r.type"] == "Buy":
                        count += operation["r.count"]
                        price += operation["r.price"]
                    else:
                        count -= operation["r.count"]
                        price -= operation["r.price"]
            result.append({"name": name, "count": count, "price": price})

        return result

    def _make_query(self, query):
        with self.driver.session() as session:
            result = session.run(query)
            return result.data()
