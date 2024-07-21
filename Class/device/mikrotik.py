import io,re,pandas
from . import Device

class Mikrotik(Device):
    def Ping(self,Address:str,Count:int=4,Size:int=56,ttl:int=255,SRC_Address:str=None) -> list:
        Table = self.Connection.Send(f'ping address={Address} count={Count} size={Size} ttl={ttl} {f'src-address={SRC_Address}' if SRC_Address else ''}')
        #return self.Parse_Table(Table) # Not Implemented Yet
        return Table.strip().splitlines()[1:Count+1]


    def Get_Hostname(self) -> str:
        return self.Connection.Send('system identity print').replace('name:','').strip()

    def Get_Export(self) -> str:
        return self.Connection.Send('export',15)

    """
    def Parse_Table(self,Table:str) -> dict:
        # Split the data into lines
        lines = Table.strip().split('\n')
        
        # Extract the header
        header = lines[0].strip()
        
        # Create a string buffer for the actual data excluding the header
        data_buffer = io.StringIO("\n".join(lines[1:]))
        
        # Read the fixed-width file data using pandas
        df = pandas.read_fwf(data_buffer, header=None)
        
        # Process the header to split into column names correctly
        header_cols = re.split(r'\s{2,}', header)
        df.columns = header_cols
        
        # Drop any rows that are completely empty or contain summary statistics
        df = df.dropna(how='all')
        df = df[~df[header_cols[0]].astype(str).str.contains('sent=', na=False)]
        
        # Convert the dataframe to a list of dictionaries
        results = df.to_dict(orient='records')
        
        return results
    """