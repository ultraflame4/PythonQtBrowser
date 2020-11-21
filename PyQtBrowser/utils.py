def typecheck(type_,val):
    if type(val) != type_:
        print(f"Value Error: Needed {type_} got {type(val)}!")
        raise ValueError(f"Needed {type_} got {type(val)}")



class dumb_Tab:
    def __init__(self, i, o):
        self.index = i
        self.o = o

    def setTabIcon(self, icon):
        self.o.setTabIcon(self.index, icon)

    def setTabText(self, text):
        self.o.setTabText(self.index, text)