from pyparsing import Word, alphas, alphanums, nums, QuotedString, Suppress, Group, Dict, LineEnd, OneOrMore, ZeroOrMore
from typing import Any
from . import Device

Type_To_Table:dict[str,str] = {
    'ether':'interface/ethernet',
    'vlan':'interface/vlan',
    'wg':'interface/wireguard',
    }

class Mikrotik(Device):
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
