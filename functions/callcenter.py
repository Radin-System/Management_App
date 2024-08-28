from xml.etree.ElementTree import Element, SubElement, tostring

def Add_Soft_Key(xml, name, url, position):
    Soft_Key = SubElement(xml, 'SoftKeyItem')
    SubElement(Soft_Key, 'Name').text = name
    SubElement(Soft_Key, 'URL').text = url
    SubElement(Soft_Key, 'Position').text = str(position)

def Show_Contacts(Contacts:list):
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
