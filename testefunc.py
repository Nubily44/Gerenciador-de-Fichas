class MyClass:
    def hello(self):
        print("Hello from MyClass!")
    def bye(self):
        print("babaiiii")

class MyClass2:
    def hello(self):
        print("Hello from MyClass!2")
    def bye(self):
        print("babaiiii2")

# Create an instance of the class
obj = MyClass2()

# Store the method name as a string
method_name = "bye"

# Use `getattr` to retrieve the method and call it
method_to_call = getattr(obj, method_name, None)
if method_to_call:
    method_to_call()
else:
    print("Method not found.")


teste = "Bolo"
validade = 0
match teste.lower():
    case "bolo":
        match validade:
            case 1:
                print("Bolo Podre")
            case 0:
                print("Bolo Bom")
    case "torta":
        match validade:
            case 1:
                print("Torta podre")
            case 0:
                print("Torta boa")
    case _:
        print("Geladeira vazia")
        
        

