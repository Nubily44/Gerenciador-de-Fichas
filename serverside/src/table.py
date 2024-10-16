class Table:
    def __init__(self, idn, name):
        self.id = idn
        self.name = name
        self.sheets = []

    def getId(self):
        return self.id
    
    def setId(self, idn):
        self.id = idn
    
    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name
    
    def addSheet(self, sheet):
        self.sheets.append(sheet)
    
    def removeSheet(self, sheet):
        self.sheet.remove(sheet)
    
    def getSheet(self, sheet):
        return self.sheets[sheet]
    
    def displayTable(self):
        print("Table: ", self.name)
        for sheet in self.sheets:
            sheet.Display()

    