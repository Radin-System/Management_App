class Convert :

    @staticmethod
    def CSVToList(CSV:str) -> list :
        return [Item.strip() for Item in CSV.split(',')]