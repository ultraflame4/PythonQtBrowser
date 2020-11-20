def typecheck(type_,val):
    if type(val) != type_:
        print(f"Value Error: Needed {type_} got {type(val)}!")
        raise ValueError(f"Needed {type_} got {type(val)}")