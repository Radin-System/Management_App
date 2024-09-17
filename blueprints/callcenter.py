from flask import Blueprint, Response, abort, redirect, request, url_for
from xml.etree.ElementTree import Element, SubElement, tostring

from classes.component import ComponentContainer, SQLManager, Config
from functions.callcenter import Add_Soft_Key, Create_Contacts

def CallCenter(CC:ComponentContainer) -> Blueprint:
    SQL:SQLManager = CC.Get('MainSQLManager')
    Con:Config = CC.Get('MainConfig')

    bp = Blueprint('callcenter', __name__, url_prefix='/callcenter')

    @bp.route('/')
    def index():
        return redirect(url_for('callcenter.menu'))

    @bp.route('/menu.xml')
    def menu():
        # Create the root element
        Root_Element = Element('CiscoIPPhoneMenu')

        # Add children elements
        SubElement(Root_Element, 'Title').text = f'{Con.Get('GLOBALS','name')} Books'
        SubElement(Root_Element, 'Prompt').text = 'Select address book'

        Books = SQL.Query(SQL.Contact_Book, Detached=True, name__sort='desc')

        for Book in Books:
            Menu_Item = SubElement(Root_Element, 'MenuItem')
            SubElement(Menu_Item, 'Name').text = str(Book.name)
            SubElement(Menu_Item, 'URL').text = url_for('callcenter.contacts', Book_Name=Book.name, _external=True)

        # Convert the ElementTree to a string
        XML_Str = tostring(Root_Element, encoding='unicode')

        return Response(XML_Str, mimetype='text/xml')

    @bp.route('/contacts/<Book_Name>.xml')
    def contacts(Book_Name):
        Xml = Element('CiscoIPPhoneInput')
        SubElement(Xml, 'Title').text = 'Search for Contact'
        SubElement(Xml, 'Prompt').text = 'Enter search criteria'
        SubElement(Xml, 'URL').text = url_for('callcenter.search', Book_Name=Book_Name, _external=True)

        item1 = SubElement(Xml, 'InputItem')
        SubElement(item1, 'DisplayName').text = 'Name'
        SubElement(item1, 'QueryStringParam').text = 'name'
        SubElement(item1, 'DefaultValue').text = ''
        SubElement(item1, 'InputFlags').text = 'A'

        item2 = SubElement(Xml, 'InputItem')
        SubElement(item2, 'DisplayName').text = 'Number'
        SubElement(item2, 'QueryStringParam').text = 'number'
        SubElement(item2, 'DefaultValue').text = ''
        SubElement(item2, 'InputFlags').text = 'T'

        Add_Soft_Key(Xml, 'Search', 'SoftKey:Submit', 1)
        Add_Soft_Key(Xml, 'Exit', 'SoftKey:Exit', 2)
        Add_Soft_Key(Xml, 'Del', 'SoftKey:<<', 3)

        return Response(tostring(Xml, encoding='utf-8'), mimetype='text/xml')

    @bp.route('/search/<Book_Name>.xml')
    def search(Book_Name):
        Book = SQL.Query(SQL.Contact_Book, Detached=True, First=True, name=Book_Name)
        Contacts:list = []
        if Book is not None:
            if 'name' in request.args:
                Contacts = SQL.Query(SQL.Contact,
                    Detached = True, 
                    firstname_en__sort = 'desc',
                    name__like = request.args.get('name'),
                    contact_book_id = Book.id,
                    )

            elif 'number' in request.args:
                Contacts = SQL.Query(SQL.Contact,
                    Detached = True,
                    firstname_en__sort = 'desc',
                    number__like = request.args.get('number'),
                    contact_book_id = Book.id,
                    )

            else:
                return abort(400)

        else :
            return abort(404)
    
        [Contact.calc_fullname() for Contact in Contacts]

        return Response(Create_Contacts(Contacts), mimetype='text/xml')

    return bp