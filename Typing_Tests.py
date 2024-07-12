from Typing import Username,Password,Domain,Email,IPv4,Port,Mac

if __name__ == '__main__' :
    test_usernames = [
        'm.heydari',
        '_admin',
        'Alireza4251',
        'Mamad Heydari',
        'Mohamm@d',
        'Am!r"',
        'a',
        'user_123',
        'test_user',
        'john.doe',
        'admin_user',
        'user@domain',
        'root',
        'guest',
        '123456',
        'test123',
        'sample_user',
        'username!',
        'user.name',
        'test.user'
    ]

    test_passwords = [
        'HDie@3419',
        'asdasda',
        'Admin',
        'asd@123',
        'password',
        '12345',
        'qwerty',
        'P@ssw0rd!',
        'letmein',
        'admin123',
        'rootpass',
        'userpass',
        'testpass',
        'simplepass',
        'complexP@ss',
        'easy123',
        'hard2guess',
        'securePass1!',
        'passW0rd',
        'P@ssword123'
    ]

    test_domains = [
        'rsto.ir',
        'reza',
        'zabbix.sdiqoifqasdasdasdqwerqwrqdasdasdqwerasdqwfgqegqrgqdfwofid.qofnoqudfdqwfqgerqrg.qfenfoqjenfdqfnqefqegqsafas.qpdfoqdf',
        '-ali.asd',
        'mamad..ali',
        '7ho.st',
        'Google.com',
        'example.com',
        'test-domain.org',
        'my-site.net',
        'sub.domain.co',
        'invalid_domain',
        'domain..com',
        '1invalid-domain',
        'another-test.org',
        'sub..domain.com',
        'valid-domain.ir',
        'another.invalid.domain',
        'newdomain.info',
        'mysite.example'
    ]

    test_emails = [
        'Admin@rsto.ir',
        'Admin@rsto',
        'Adm$in@rsto.ir',
        'Admin@@rsto.ir',
        'Admin',
        'user@example.com',
        'test@domain.org',
        'email@sub.domain.com',
        'invalid-email',
        'user@domain',
        'admin@site',
        'root@localhost',
        'test@localhost.local',
        'guest@guest',
        'username@domain.com',
        'user@domain..com',
        'email@invalid',
        'user@domain.com.',
        'user@.domain.com',
        'user@domain.com..'
    ]

    test_ipv4s = [
        '192.168.10.10 255.255.255.0',
        '192.168.1.1',
        '256.143.1.4',
        'Admin',
        '172.24.10.1/32',
        '172.42.17/255.255.252.0',
        '172.20.30.2/0.255.255.255',
        '10.0.0.1',
        '192.168.0.256',
        '192.168.1',
        '172.16.0.1',
        '10.10.10.10/24',
        '300.300.300.300',
        '127.0.0.1',
        'localhost',
        '192.168.0.1/33',
        '192.168.1.1/255.255.255.0',
        'invalid.ip',
        '192.168.10.10',
        '172.16.254.1/16'
    ]

    test_ports = [
        1324,
        123,
        12657489,
        1,
        0,
        467,
        80,
        8080,
        65536,
        22,
        21,
        443,
        3306,
        5432,
        27017,
        99999,
        25,
        110,
        53,
        2049
    ]

    test_macs = [
        '00:14:22:01:23:45',
        '01:23:45:67:89:ab',
        'AA:BB:CC:DD:EE:FF',
        '00-14-22-01-23-45',
        '01-23-45-67-89-ab',
        'aa-bb-cc-dd-ee-ff',
        '0014.2201.2345',
        '0123.4567.89ab',
        'aabb.ccdd.eeff',
        '00:14:22:01:23:45:67',
        '01:23:45:67:89:ab:cd',
        'AA:BB:CC:DD:EE:FF:11',
        '00-14-22-01-23-45-67',
        '01-23-45-67-89-ab-cd',
        'aa-bb-cc-dd-ee-ff-11',
        '0014.2201.2345.6789',
        '0123.4567.89ab.cdef',
        'aabb.ccdd.eeff.gghh',
        '00:14:22:01:23',
        '01:23:45:67:89'
    ]


    Tests = [
        (test_usernames,Username),
        (test_passwords,Password),
        (test_domains,Domain),
        (test_emails,Email),
        (test_ipv4s,IPv4),
        (test_ports,Port),
        (test_macs,Mac),
    ]

    ats = 40*'_'

    for Test in Tests :
        print(ats)
        print(f'{10*'_'}Testing {Test[1].__name__}')
        for Item in Test[0] :
            try : print(f'Valid {Test[1].__name__} : {Test[1](Item)}')
            except Exception as e: print(f'Invalid {Test[1].__name__} : {e}')
