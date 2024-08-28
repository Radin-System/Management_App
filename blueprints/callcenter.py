from flask import Blueprint, Response, render_template, request
from classes.component.sqlmanager import SQLManager
from xml.etree.ElementTree import Element, SubElement, tostring

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    extension = db.Column(db.String(50), nullable=False)

class RingGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    grpnum = db.Column(db.String(50), nullable=False)

def create_cisco_phone_error(title, prompt, text):
    xml = Element('CiscoIPPhoneText')
    SubElement(xml, 'Title').text = title
    SubElement(xml, 'Prompt').text = prompt
    SubElement(xml, 'Text').text = text
    add_soft_key(xml, 'Exit', 'SoftKey:Exit', 1)
    return tostring(xml, encoding='utf-8')

def add_soft_key(xml, name, url, position):
    soft_key = SubElement(xml, 'SoftKeyItem')
    SubElement(soft_key, 'Name').text = name
    SubElement(soft_key, 'URL').text = url
    SubElement(soft_key, 'Position').text = str(position)

def show_addresses(mode, query):
    if mode == 'number':
        users = User.query.filter(User.extension.like(query)).all()
        ringgroups = RingGroup.query.filter(RingGroup.grpnum.like(query)).all()
    else:  # 'name'
        users = User.query.filter(User.name.like(query)).all()
        ringgroups = RingGroup.query.filter(RingGroup.description.like(query)).all()

    if not users and not ringgroups:
        return create_cisco_phone_error('No results', 'Try again', f'No results found for {query}')

    xml = Element('CiscoIPPhoneDirectory')
    SubElement(xml, 'Title').text = 'Grace Academy'
    SubElement(xml, 'Prompt').text = 'Dial selected'

    for user in users:
        entry = SubElement(xml, 'DirectoryEntry')
        SubElement(entry, 'Name').text = user.name
        SubElement(entry, 'Telephone').text = user.extension

    for group in ringgroups:
        entry = SubElement(xml, 'DirectoryEntry')
        SubElement(entry, 'Name').text = group.description
        SubElement(entry, 'Telephone').text = group.grpnum

    add_soft_key(xml, 'Dial', 'SoftKey:Dial', 1)
    add_soft_key(xml, 'Exit', 'SoftKey:Exit', 2)
    
    return tostring(xml, encoding='utf-8')

def CallCenter(SQL:SQLManager) -> Blueprint:
        
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

        add_soft_key(xml, 'Search', 'SoftKey:Submit', 1)
        add_soft_key(xml, 'Exit', 'SoftKey:Exit', 2)
        add_soft_key(xml, 'Del', 'SoftKey:<<', 3)

        return Response(tostring(xml, encoding='utf-8'), mimetype='text/xml')

    @bp.route('/search.xml')
    def search():
        mode = None
        query = None

        if 'name' in request.args:
            mode = 'name'
            query = f"%{request.args.get('name')}%"
        elif 'number' in request.args:
            mode = 'number'
            query = f"%{request.args.get('number')}%"

        return Response(show_addresses(mode, query), mimetype='text/xml')

    return bp