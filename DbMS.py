from neo4j import GraphDatabase, Result


class DbMS:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="10122000"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def __del__(self):
        self.driver.close()

    # Пример использования
    def add_operation(self):
        query = ""
        return self._make_query(query)

    def get_history(self, name):
        query = "MATCH (n:Client {name: \'" \
                + name \
                + "\'})-[r:Operation]->(m:Сryptocurrency) RETURN r.type, m.name, r.count, r.date, r.price"
        return self._make_query(query)

    def get_portfolio(self):
        query = "MATCH (n:Client)-[r:Operation]->(m:Сryptocurrency) RETURN r.type, m.name, r.count, r.date, r.price"
        values = self._make_query(query)
        # TODO
        return

    def _make_query(self, query):
        with self.driver.session() as session:
            result = session.run(query)
            return result.data()

