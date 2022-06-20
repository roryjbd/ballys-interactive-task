from pymysql.cursors import DictCursor
from flask import Response, jsonify, request
from flaskext.mysql import MySQL


def add_to_where_clause(
    execution_statement: list,
    execution_arguments: dict,
    new_argument_name: str,
    value: str,
):

    execution_statement.append(f"AND {new_argument_name} = %({new_argument_name})s")
    execution_arguments[new_argument_name] = value


def create_route(db: MySQL, inital_sql_statement: list) -> Response:

    try:
        args = request.args
        member_id = args.get("member_id")
        game_id = args.get("game_id")
        month = args.get("month")

        execution_statement = [inital_sql_statement]
        execution_arguments = {"member_id": member_id}

        if game_id:
            add_to_where_clause(
                execution_statement, execution_arguments, "GAME_ID", game_id
            )

        if month:
            add_to_where_clause(
                execution_statement, execution_arguments, "ACTIVITY_YEAR_MONTH", month
            )

        conn = db.connect()
        cur = conn.cursor(DictCursor)

        statement = " ".join(execution_statement)
        cur.execute(statement, execution_arguments)

        rows = cur.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp

    finally:
        cur.close()
        conn.close()
