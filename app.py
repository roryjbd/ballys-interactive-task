import os
from flask import Flask
from flaskext.mysql import MySQL

from utils.flask_utils import create_route

app = Flask(__name__)
app.config["MYSQL_DATABASE_USER"] = os.environ.get("MYSQL_USER", None)
app.config["MYSQL_DATABASE_PASSWORD"] = os.environ.get("MYSQL_PASS", None)
app.config["MYSQL_DATABASE_DB"] = os.environ.get("MYSQL_DB", None)
app.config["MYSQL_DATABASE_HOST"] = os.environ.get("MYSQL_HOST", None)

mysql = MySQL(app)
mysql.init_app(app)


@app.route("/")
def home():
    return "hello"


@app.route("/wins")
def wins():
    return create_route(
        mysql,
        "SELECT ROUND(SUM(WIN_AMOUNT),2) as WIN_AMOUNT FROM REVENUE_ANALYSIS WHERE MEMBER_ID = %(member_id)s",
    )


@app.route("/wagers")
def wagers():
    return create_route(
        mysql,
        "SELECT ROUND(SUM(WAGER_AMOUNT),2) as WAGER_AMOUNT FROM REVENUE_ANALYSIS WHERE MEMBER_ID = %(member_id)s",
    )


@app.route("/count-placed")
def count():
    return create_route(
        mysql,
        "SELECT SUM(NUMBER_OF_WAGERS) as TOTAL_WAGERS_PLACED FROM REVENUE_ANALYSIS WHERE MEMBER_ID = %(member_id)s",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0")
