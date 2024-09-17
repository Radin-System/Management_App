from flask import Blueprint, redirect, render_template, request, abort, url_for
from flask_login import current_user

from classes.component import ComponentContainer, SQLManager
from classes.convert import StringTool
from classes.tool import ToolContainer

def DataBase(CC:ComponentContainer, TC:ToolContainer) -> Blueprint:
    SQL:SQLManager = CC.Get('Main_SQLManager')

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
                    Data = SQL.Query(Model, Detached=True, Eager=True, id__sort='desc')
                    return render_template('database/index.html', Table=Model, Data=Data, Action=Action)

            if request.method == 'POST':
                if Action == 'create':
                    New_Instance = Model(**request.form)
                    SQL.Create(New_Instance)

            if request.method == 'PUT':
                if Action == 'edit':
                    Edit_Instance = SQL.Query(Model, Detached=True, Eager=True, First=True, id=Id)
                    [setattr(Edit_Instance, Key, Value) for Key, Value in request.form.items()]
                    SQL.Update(Edit_Instance)

            if request.method == 'DELETE':
                if Action == 'delete':
                    Id = request.args.get('id', None)
                    Item = SQL.Query(Model, Detached=True, Eager=True, First=True, id=Id)
                    SQL.Delete(Item)

                if Action == 'mass_delete':
                    Ids = request.args.get('ids', None)
                    for Id in StringTool.CsvToList(Ids):
                        try:
                            Item = SQL.Query(Model, Detached=True, Eager=True, First=True, id=Id)
                            SQL.Delete(Item)
                        except:
                            print('Delete Error')

            return redirect(url_for('database.main', Model_Name=Model, action='list_view'))

        else:
            return abort(404)

    return bp