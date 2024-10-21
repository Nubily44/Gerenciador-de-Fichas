import random

class Sheet_Template:
    def __init__(self, name, AttB, AttC, AttV):
        self.name = name
        self.AttB = AttB
        self.AttC = AttC
        self.AttV = AttV
        self.Alive = 1
        self.WeaponsBackpack = []
        self.UsablesBackpack = []
        self.PermanentsBackpack = []

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    # Dices

    def roll_Dice(self, x):
        return random.randint(1, x)
    
    def roll_DiceWithCount(self, x, count):
        rolls = [self.roll_Dice(x) for _ in range(count)]
        return max(rolls)
    
    def roll_DiceWithCountMod(self, x, count, mod):
        rolls = [self.roll_Dice(x) for _ in range(count + abs(mod))]
        if mod > 0:
            return max(rolls)
        else:
            return min(rolls)
        
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    def Display(self):
        print("Nome: ", self.name)
        print("B: ", self.AttB)
        print("C: ", self.AttC)
        print("V: ", self.AttV)
        print("Alive: ", self.Alive)
        print("\n-=-=-=-=-=-=-Backpack-=-=-=-=-=-=-")
        # Print Weapons
        print("-Weapons: ")
        print(", ".join(self.getWeapons()))

        # Print Usables
        print("-Usables: ")
        print(", ".join(self.getUsables()))

        # Print Permanents
        print("-Permanents: ")
        print(", ".join(self.getPermanents()))

        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")
    
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    # Funções para retornar informações ao cliente e criar os json files

    def DisplayString(self):
        display_string = (
            f"Nome: {self.name}\n"
            f"B: {self.AttB}\n"
            f"C: {self.AttC}\n"
            f"V: {self.AttV}\n"
            f"Alive: {self.Alive}\n"
            "\n-=-=-=-=-=-=-Backpack-=-=-=-=-=-=-\n"
            "-Weapons: \n"
            f"{', '.join(self.getWeapons())}\n"
            "-Usables: \n"
            f"{', '.join(self.getUsables())}\n"
            "-Permanents: \n"
            f"{', '.join(self.getPermanents())}\n"
            "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n"
        )

        return display_string

    def logging(self, f):
        with open(f, "w") as f:
            f.write(f"Nome: {self.name}\n")
            f.write(f"B: {self.AttB}\n")
            f.write(f"C: {self.AttC}\n")
            f.write(f"V: {self.AttV}\n")
            f.write(f"Alive: {self.Alive}\n")
            f.write("\n-=-=-=-=-=-=-Backpack-=-=-=-=-=-=-\n")

            # Write Weapons
            f.write(f"-Weapons: {', '.join(self.getWeapons())}\n")

            # Write Usables
            f.write(f"-Usables: {', '.join(self.getUsables())}\n")

            # Write Permanents
            f.write(f"-Permanents: {', '.join(self.getPermanents())}\n")

            f.write("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")

    def to_dict(self):
        return {
            "name": self.name,
            "AttB": self.AttB,
            "AttC": self.AttC,
            "AttV": self.AttV,
            "Alive": self.Alive,
            "WeaponsBackpack": [
                {"weapon": weapon[0].getName(), "quantity": weapon[1]} for weapon in self.WeaponsBackpack
            ],
            "UsablesBackpack": [
                {"usable": usable[0].getName(), "quantity": usable[1]} for usable in self.UsablesBackpack
            ],
            "PermanentsBackpack": [
                {"permanent": permanent[0].getName(), "quantity": permanent[1]} for permanent in self.PermanentsBackpack
            ]
        }

    @classmethod
    def from_dict(cls, data):
        # Create a new instance of the class using the data dictionary
        sheet = cls(data['name'], data['AttB'], data['AttC'], data['AttV'])
        sheet.Alive = data['Alive']

        # Store the values in backpacks as attributes
        for item in data['WeaponsBackpack']:
            sheet.WeaponsBackpack[item['weapon']] = item['quantity']
        
        for item in data['UsablesBackpack']:
            sheet.UsablesBackpack[item['usable']] = item['quantity']
        
        for item in data['PermanentsBackpack']:
            sheet.PermanentsBackpack[item['permanent']] = item['quantity']

        return sheet

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    # getters and setters
    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    # getters and setters
    def AttB_setValue(self, AttB):
        self.AttB = AttB


    def AttB_getValue(self):
        return self.AttB
    

    # Additional methods
    def AttB_ModifyAtr(self, x): # Damage, Heal, etc
        self.AttB = self.AttB + x
        print(self.name + "recebeu" + x +"para AttB")
        if self.AttB < 0:
            self.AttB = 0
            self.Alive = 0
            print(self.name + "está morto")

    def AttB_isZero(self): 
        return self.AttB == 0

    def AttAttB_isLessThan(self, x):
        return self.AttB < x


    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    
    #getters and setters
    def AttC_setValue(self, AttC):
        self.AttC = AttC

    def AttC_getValue(self):
        return self.AttC


    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    
    #getters and setters
    def AttV_setValue(self, AttV):
        self.AttV = AttV

    def AttV_getValue(self):
        return self.AttV


    # Additional methods
    def AttV_rollAtr(self, dice, target, count): # roll dices
        return self.roll_DiceWithCount(dice, count) + self.AttV >= target

    def AttV_rollAtrWithCountMod(self, dice, target, count, mod):
        return self.roll_DiceWithCountMod(dice, count, mod) + self.AttV >= target
        
    def AttV_UpgradeAtr(self, x): # Upgrade the attribute
        self.AttV = self.AttV + x

    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    
    def isAlive(self):
        return self.Alive
    
    def isDead(self):
        return self.Alive
    
    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
   
    def addWeapon(self, weapon, quantity):
        if quantity > 0:
            self.WeaponsBackpack.append([weapon, quantity])
            print("Você pegou ", weapon.getName())

        if quantity < 0:
            for i in range(len(self.WeaponsBackpack)):
                if self.WeaponsBackpack[i][0] == weapon:
                    self.WeaponsBackpack[i][1] = self.WeaponsBackpack[i][1] + quantity
                    if self.WeaponsBackpack[i][1] <= 0:
                        self.WeaponsBackpack.pop(i)
                        break
    
    def removeWeapon(self, weapon, quantity):
        for i in range(len(self.WeaponsBackpack)):
            if self.WeaponsBackpack[i][0] == weapon:
                self.WeaponsBackpack[i][1] = self.WeaponsBackpack[i][1] - quantity
                if self.WeaponsBackpack[i][1] <= 0:
                    self.WeaponsBackpack.pop(i)
                    print("Você perdeu", weapon.getName())

    def getWeapons(self):
        WeaponListNames = []
        for i in range(len(self.WeaponsBackpack)):
            quant = self.WeaponsBackpack[i][1]
            for j in range(quant):
                WeaponListNames.append(self.WeaponsBackpack[i][0].getName())
        return WeaponListNames

    def getWeaponsBackpack(self):
        return self.WeaponsBackpack

    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    #Funções para lidar com mochilas e itens
    
    def addUsable(self, usable, quantity):
        if quantity > 0:
            self.UsablesBackpack.append([usable, quantity])
            print("Você ganhou", usable.getName())

        if quantity < 0:
            for i in range(len(self.UsablesBackpack)):
                if self.UsablesBackpack[i][0] == usable:
                    self.UsablesBackpack[i][1] = self.UsablesBackpack[i][1] + quantity
                    if self.UsablesBackpack[i][1] <= 0:
                        self.UsablesBackpack.pop(i)
                        break
    
    def removeUsable(self, usable, quantity):
        for i in range(len(self.UsablesBackpack)):
            if self.UsablesBackpack[i][0] == usable:
                self.UsablesBackpack[i][1] = self.UsablesBackpack[i][1] - quantity
                if self.UsablesBackpack[i][1] <= 0:
                    self.UsablesBackpack.pop(i)
                    print("Você perdeu",usable.getName())

    def getUsables(self):
        UsableListNames = []
        for i in range(len(self.UsablesBackpack)):
            quant = self.UsablesBackpack[i][1]
            for j in range(quant):
                UsableListNames.append(self.UsablesBackpack[i][0].getName())
        return UsableListNames

    def getUsablesBackpack(self):
        return self.UsablesBackpack

    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    def addPermanent(self, permanent, quantity):
        if quantity > 0:
            self.PermanentsBackpack.append([permanent, quantity])

        if quantity < 0:
            for i in range(len(self.PermanentsBackpack)):
                if self.PermanentsBackpack[i][0] == permanent:
                    self.PermanentsBackpack[i][1] = self.PermanentsBackpack[i][1] + quantity
                    if self.PermanentsBackpack[i][1] <= 0:
                        self.PermanentsBackpack.pop(i)
                        break

    def removePermanent(self, permanent):
        for i in range(len(self.PermanentsBackpack)):
            if self.PermanentsBackpack[i][0] == permanent:
                    self.PermanentsBackpack.pop(i)
                    print("Você perdeu",permanent.getName() )
              
    def getPermanents(self):
        PermanentListNames = []
        for i in range(len(self.PermanentsBackpack)):
            quant = self.PermanentsBackpack[i][1]
            for j in range(quant):
                PermanentListNames.append(self.PermanentsBackpack[i][0].getName())
        return PermanentListNames
    
    def getPermanentsBackpack(self):
        return self.PermanentsBackpack
             
    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    #Ações de Personagem 

    def dance(self, target): #(também conhecida como "dançar pros cria")
        print(self.name, "dançou com", target.name)
        if self.AttV_rollAtr(20, 50, 1):
            print("Dançou muito bem. Daaaaaale!")
        else:
            print("Dançou mal. Não foi poggers amigo")

    def punch(self, target, damage):
        print(self.name, "bateu em", target.name)
        if target is not None:
            if self.AttV_rollAtr(20, 50, 1):
                print("Acertou em cheio!")
                self.attV -= damage
            else:
                print("Bateu mal. Errou o alvo")
    
    def wink(self, target):
        print(self.name, "piscou para", target.name)

    def send(self, target, item, quantity):
        print(self.name, "entregou", item.getName(), "para", target.name)
        print(target.name, "recebeu", item.getName())
        if hasattr(item, 'range'):
            target.addWeapon(item, quantity)
            self.removeWeapon(item, quantity)
        elif hasattr(item, 'durability'):
            target.addUsable(item, quantity)
            self.removeUsable(item, quantity)
        else:
            target.addPermanent(item, quantity)
            self.removePermanent(item)


