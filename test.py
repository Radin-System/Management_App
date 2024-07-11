from Typing import Username,Password,Domain,IPv4,Email

if __name__ == '__main__' :
    test_usernames = [
        'm.heydari','_admin','Alireza4251',
    ]

    test_passwords = [
        'HDie@3419','asd','Admin','asd@123',
    ]
    test_domains = [
        'rsto.ir','reza','zabbix.sdiqoifqwofid.qofnoqudf.qfenfoqjenfdqfn.qpdfoqdf','-.asd..',
    ]

    test_ipv4s = [
        '192.168.10.10 255.255.255.0',
        '192.168.1.1',
        '256.143.1.4',
        'Admin',
    ]

    test_emails = [
        'Admin@rsto.ir',
        'Admin@rsto',
        'Adm$in@rsto.ir',
        'Admin@@rsto.ir',
        'Admin',
    ]

    for User in test_usernames :
        try : print(f'Valid Username : {Username(User)}')
        except ValueError as e : print(f'Invalid Username : {User} : {e}')
    
    for Pass in test_passwords :
        try : print(f'Valid Password : {Password(Pass)}')
        except ValueError as e : print(f'Invalid Password : {Pass} : {e}')
    
    for Dom in test_domains :
        try : print(f'Valid Domain : {Domain(Dom)}')
        except ValueError as e : print(f'Invalid Domain : {Dom} : {e}')
    
    for ip in test_ipv4s :
        try : print(f'Valid IPv4 : {IPv4(ip)}')
        except ValueError as e : print(f'Invalid IPv4 : {ip} : {e}')
    
    for email in test_emails :
        try : print(f'Valid Email : {Email(email)}')
        except ValueError as e : print(f'Invalid Email : {email} : {e}')
    