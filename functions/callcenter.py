from typing import Any
from xml.etree.ElementTree import Element, SubElement, tostring

def Add_Soft_Key(Xml, Name, Url, Position) -> None:
    Soft_Key = SubElement(Xml, 'SoftKeyItem')
    SubElement(Soft_Key, 'Name').text = Name
    SubElement(Soft_Key, 'URL').text = Url
    SubElement(Soft_Key, 'Position').text = str(Position)

def Create_Contacts(Contacts:list) -> Any:
    Xml = Element('CiscoIPPhoneDirectory')
    SubElement(Xml, 'Title').text = 'Grace Academy'
    SubElement(Xml, 'Prompt').text = 'Dial selected'

    for Contact in Contacts:
        Entry = SubElement(Xml, 'DirectoryEntry')
        SubElement(Entry, 'Name').text = Contact.fullname_en
        SubElement(Entry, 'Telephone').text = Contact.number

    Add_Soft_Key(Xml, 'Dial', 'SoftKey:Dial', 1)
    Add_Soft_Key(Xml, 'Exit', 'SoftKey:Exit', 2)
    
    return tostring(Xml, encoding='utf-8')

def Create_Cisco_Error(Error_Detail:dict) -> Any:
    Xml = Element('CiscoIPPhoneText')
    SubElement(Xml, 'Title').text = str(Error_Detail.get('name','UnkhownError'))
    SubElement(Xml, 'Prompt').text = str(Error_Detail.get('code','NoCode'))
    SubElement(Xml, 'Text').text = str(Error_Detail.get('description','no more detail'))
    
    Add_Soft_Key(Xml, 'Exit', 'SoftKey:Exit', 1)
    
    return tostring(Xml, encoding='utf-8')