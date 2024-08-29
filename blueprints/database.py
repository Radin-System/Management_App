from flask import Blueprint, render_template, request, abort

from classes.component import ComponentContainer, SQLManager

def DataBase(CC: ComponentContainer) -> Blueprint:
    SQL: SQLManager = CC.Get('MainSQLManager')

    bp = Blueprint('database', __name__, url_prefix='/database')

    @bp.route('/')
    def index():
        return render_template('database/index.html')

    @bp.route('/<Table_Name>', methods=['GET', 'POST', 'PUT', 'DELETE'])
    def main(Table_Name):
        Table = SQL.Models.get(Table_Name)
        Action = request.args.get('action', None)

        if not Action:
            return abort(400)

        if Table:
            if request.method == 'GET':
                if Action == 'list_view':
                    Data = SQL.Query(Table, Detached=True, Eager=True, Sort=[('id','desc')])
                    return render_template('database/index.html', Table=Table, Data=Data, Action='list_view')
            # Other CRUD operations will get implemented soon
        else:
            return abort(404)

    return bp
