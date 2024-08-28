from flask import Blueprint, Response, abort, render_template, request
from xml.etree.ElementTree import Element, SubElement, tostring

from classes.component import ComponentContainer, SQLManager
from functions.callcenter import Add_Soft_Key, Show_Contacts

def CallCenter(CC:ComponentContainer) -> Blueprint:
    SQL:SQLManager = CC.Get('MainSQLManager')

    bp = Blueprint('callcenter', __name__, url_prefix='/callcenter')

    @bp.route('/')
    def index():
        return render_template('faq/index.html')

    @bp.route('/callcenter/menu.xml')
    def menu():
        # Create the root element
        Root_Element = Element('CiscoIPPhoneMenu')

        # Add children elements
        SubElement(Root_Element, 'Title').text = 'PartFidar Books'
        SubElement(Root_Element, 'Prompt').text = 'Select address book'

        # Construct the URL for the contacts XML
        Contacts_url = 'http://localhost:5000/callcenter/contacts.xml'

        Menu_Item = SubElement(Root_Element, 'MenuItem')
        SubElement(Menu_Item, 'Name').text = 'Book 1'
        SubElement(Menu_Item, 'URL').text = Contacts_url

        # Convert the ElementTree to a string
        XML_Str = tostring(Root_Element, encoding='unicode')

        return Response(XML_Str, mimetype='text/xml')

    @bp.route('/contacts.xml')
    def contacts():
        xml = Element('CiscoIPPhoneInput')
        SubElement(xml, 'Title').text = 'Search for Person'
        SubElement(xml, 'Prompt').text = 'Enter search criteria'
        SubElement(xml, 'URL').text = 'http://5.160.100.129:5000/search.xml'

        item1 = SubElement(xml, 'InputItem')
        SubElement(item1, 'DisplayName').text = 'Name'
        SubElement(item1, 'QueryStringParam').text = 'name'
        SubElement(item1, 'DefaultValue').text = ''
        SubElement(item1, 'InputFlags').text = 'A'

        item2 = SubElement(xml, 'InputItem')
        SubElement(item2, 'DisplayName').text = 'Number'
        SubElement(item2, 'QueryStringParam').text = 'number'
        SubElement(item2, 'DefaultValue').text = ''
        SubElement(item2, 'InputFlags').text = 'T'

        Add_Soft_Key(xml, 'Search', 'SoftKey:Submit', 1)
        Add_Soft_Key(xml, 'Exit', 'SoftKey:Exit', 2)
        Add_Soft_Key(xml, 'Del', 'SoftKey:<<', 3)

        return Response(tostring(xml, encoding='utf-8'), mimetype='text/xml')

    @bp.route('/search.xml')
    def search():
        Contacts:list = []

        if 'name' in request.args:
            Contacts = SQL.Query(SQL.Contact, Detached=True, Sort=[('firstname_en','des')], name__like = request.args.get('name'))

        elif 'number' in request.args:
            Contacts = SQL.Query(SQL.Contact, Detached=True, Sort=[('firstname_en','des')], number__like = request.args.get('number'))

        else:
            return abort(400)

        [Contact.calc_fullname() for Contact in Contacts]

        return Response(Show_Contacts(Contacts), mimetype='text/xml')

    return bp