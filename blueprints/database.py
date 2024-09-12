from flask import Blueprint, redirect, render_template, request, abort, url_for

from classes.component import ComponentContainer, SQLManager
from classes.convert import StringTool
from functions.decorator import login_required

@login_required
def DataBase(CC: ComponentContainer) -> Blueprint:
    SQL: SQLManager = CC.Get('MainSQLManager')

    bp = Blueprint('database', __name__, url_prefix='/database')

    @bp.route('/')
    def index():
        return render_template('database/index.html')

    @bp.route('/<Model_Name>', methods=['GET', 'POST', 'PUT', 'DELETE'])
    def main(Model_Name):
        Model = SQL.Models.get(Model_Name)
        Action = request.args.get('action', None)

        if not Action:
            return abort(400)

        if Model:
            if request.method == 'GET':
                if Action == 'list_view':
                    Data = SQL.Query(Model, Detached=True, Eager=True, Sort=[('id','desc')])
                    return render_template('database/index.html', Table=Model, Data=Data, Action='list_view')

            if request.method == 'POST':
                if Action == 'create':
                    raise NotImplementedError('')

            if request.method == 'PUT':
                if Action == 'edit':
                    raise NotImplementedError('')

            if request.method == 'DELETE':
                if Action == 'delete':
                    Id = request.args.get('id', None)
                    Item = SQL.Query(Model, Detached=True, Eager=True, id=Id)
                    SQL.Delete(Item)

                if Action == 'mass_delete':
                    Ids = request.args.get('ids', None)
                    for Id in StringTool.CsvToList(Ids):
                        try:
                            Item = SQL.Query(Model, Detached=True, Eager=True, id=Id)
                            SQL.Delete(Item)
                        except:
                            print('Delete Error')
            
            return redirect(url_for('database.main', Model_Name=Model, action='list_view'))

        else:
            return abort(404)

    return bp