import importlib
from typing import Any
from pyparsing import Word, alphas, alphanums, nums, QuotedString, Suppress, Group, Dict, LineEnd, OneOrMore, ZeroOrMore
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from . import InfoMixin, OwnerMixin
from classes.connection.base import Connection as Con
from classes.validator import English, EnglishSpecial, Hostname, FQDN, Ipv4OrFQDN, Port

class Device(InfoMixin, OwnerMixin):
    ## SQL Table
    __tablename__      = 'devices'
    id                 = Column(Integer, primary_key=True, autoincrement=True)
    hostname           = Column(String, nullable=False, info={'Validator':(EnglishSpecial,Hostname)})
    fqdn               = Column(String, nullable=False, unique=True, info={'Validator':(EnglishSpecial,FQDN)})
    type               = Column(String, nullable=False, info={'Validator':EnglishSpecial})
    management_address = Column(String, nullable=True, info={'Validator':(EnglishSpecial,Ipv4OrFQDN)})
    connection_method  = Column(String, nullable=False, info={'Validator':English})
    connection_port    = Column(Integer, nullable=False, info={'Validator':Port})

    company            = relationship("Company", back_populates="devices")
    company_id         = Column(Integer, ForeignKey('companies.id'), nullable=False)

    location           = relationship("Location", back_populates="devices")
    location_id        = Column(Integer, ForeignKey('locations.id'), nullable=False)

    authentication     = relationship("Authentication", back_populates="devices")
    authentication_id  = Column(Integer, ForeignKey('authentications.id'), nullable=False)

    ## Logic And Functions

    Logger = print
    Connection:Con = None

    def Connect(self) -> None :
        via = importlib.import_module(self.connection_method,'Class.connection')
        self.Connection = via(
            Host=self.fqdn,
            Port=self.connection_port,
            Username=self.authentication.username,
            Password=self.authentication.password
            )

        self.Prepare_Connection()

    def Prepare_Connection(self) -> None:
        raise NotImplementedError('Please provide connection prepare actions')

    def __str__(self) -> str :
        return f'<Device :{self.__name__}>'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(*Args,**Kwargs)'

Type_To_Table:dict[str,str] = {
    'ether':'interface/ethernet',
    'vlan':'interface/vlan',
    'wg':'interface/wireguard',
    }

class Mikrotik():
    def Prepare_Connection(self) -> None:
        pass

    def Get_Hostname(self) -> str:
        return self.Connection.Send('system identity print').replace('name:','').strip()

    def Get_Config(self) -> str:
        return self.Connection.Send('export show-sensitive verbose',10)

    def Ping(self,Address:str,*,
            Count:int = 4,
            Size:int = 56,
            ttl:int = 255,
            SRC_Address:str = None
            ) -> list[bool]:

        Resault = []
        Table = self.Connection.Send(f'ping address={Address} count={Count} size={Size} ttl={ttl} {f'src-address={SRC_Address}' if SRC_Address else ''}')
        if Table :
            Records = Table.strip().splitlines()[1:Count+1]
            for Record in Records :
                if 'timeout' in Record.lower() or 'host unreached' in Record.lower(): Resault.append(False)
                else: Resault.append(True)
        
        return Resault

    def Get_Parsed_Table(self,Table:str,*,
            Where:tuple[str:str]=None,
            ) -> list[dict[str,str]]:

        Query:str = f'{Table} print detail without-paging{' where '+f'{Where[0]+'='+Where[1]}' if Where else ''}'
        Table = self.Connection.Send(Query)
        Parsed_Table = self.Parse_Detail(Table)

        return Parsed_Table

    def Parse_Detail(self, Input:str) -> list[dict[str, Any]]:
        Lines = [Line.strip() for Line in Input.split('\n') if Line.strip()]

        # Define pyparsing grammar
        Integer = Word(nums)
        Flags = Word(alphas)
        Key = Word(alphas + "-")
        Value = QuotedString('"') | Word(alphanums + ":.-")
        Key_Value_Pair = Group(Key + Suppress('=') + Value)
        Index_And_Flags = Group(Integer("index") + Flags("flags"))
        Line_Parser = Index_And_Flags + Dict(OneOrMore(Key_Value_Pair))
        Continuation_Line = Dict(OneOrMore(Key_Value_Pair))
        Line_With_Values = Line_Parser + ZeroOrMore(LineEnd() + Continuation_Line)

        # Parse the input data
        Parsed_Data = []
        Records = []
        Record = ''

        for Line in Lines:
            if Line[0].isdigit():
                if Record: 
                    Records.append(Record)
                Record = Line
            else:
                if Record: 
                    Record += ' ' + Line

        if Record:
            Records.append(Record)

        for Record in Records:
            Result = Line_With_Values.parseString(Record)
            Parsed_Data.append(Result.asDict())

        return Parsed_Data

class Cisco():
    def Prepare_Connection(self) -> None:
        self.Set_State('privileged')
        self.Connection.Send('terminal width 0')
        self.Connection.Send('terminal length 0')
        self.Connection.Send('terminal no monitor')

    def Get_Command_Prompt(self) -> str :
        return self.Connection.Send(' ')

    def Get_Hostname(self) -> str:
        self.Set_State('privileged')
        Command_Prompt = self.Get_Command_Prompt()
        return Command_Prompt.replace('#','').strip()

    def Get_Config(self, Mode:str='full') -> str:
        self.Set_State('privileged')
        return self.Connection.Send(f'show running-config {Mode}',5.5)

    def State(self) -> str:
        Command_Prompt = self.Get_Command_Prompt()
        if '(config)#' in Command_Prompt : return 'configure'
        if '(config-'  in Command_Prompt : return 'interface'
        if '#'         in Command_Prompt : return 'privileged'
        if '>'         in Command_Prompt : return 'userEXEC'
        raise ValueError(f'Unable to parse current state from command prompt : {Command_Prompt}')

    def Set_State(self, New_State:str) -> None:
        Current_State = self.State()
        if Current_State == 'userEXEC'   and New_State == 'privileged' : self.Connection.Send('enable') ; self.Connection.Send(self.Enable) ; return
        if Current_State == 'privileged' and New_State == 'userEXEC'   : self.Connection.Send('disable') ; return
        if Current_State == 'privileged' and New_State == 'configure'  : self.Connection.Send('configure terminal') ; return
        if Current_State == 'configure'  and New_State == 'privileged' : self.Connection.Send('exit') ; return

        if Current_State == 'interface'  and New_State != 'interface'  : self.Connection.Send('exit') ; self.Set_State(New_State) ; return

        if Current_State == 'userEXEC'   and New_State == 'configure'  : self.Set_State('privileged') ; self.Set_State('configure') ; return
        if Current_State == 'configure'  and New_State == 'userEXEC'   : self.Set_State('privileged') ; self.Set_State('userEXEC') ; return
        if Current_State == New_State                                  : pass # Do Nothing
        else : raise Exception(f'Invalid States : Current_State={Current_State} , New_State={New_State}')