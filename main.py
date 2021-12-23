from flask import Flask
from neo4j import GraphDatabase


class HelloWorldExample:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def greeting(self, message):
        with self.driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message)
            return greeting

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]


app = Flask(__name__)


@app.route('/')
def hello_world():
    greeter = HelloWorldExample("bolt://localhost:7687", "neo4j", "password")
    res = greeter.greeting("hello, world")
    greeter.close()
    return res


if __name__ == '__main__':
    app.run()
