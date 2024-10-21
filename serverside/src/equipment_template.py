import random

class Equipment_Template:
    def __init__(self, name, type, rarity, state):
        self.name = name
        self.type = type
        self.rarity = rarity
        self.state = state

    # Dices
    
    def to_dict(self):
        return {
            'name': self.name,
            'type': self.type,
            'rarity': self.rarity,
            'state': self.state
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            type=data['type'],
            rarity=data['rarity'],
            state=data['state']
        )

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

    #Getters and setters
    def getName(self):
        return self.name
    def setName(self, name):
        self.name = name

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    #Getters and setters
    def getType(self):
        return self.type
    def setType(self, type):
        self.type = type

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    #Getters and setters
    def getRarity(self):
        return self.rarity
    def setRarity(self, rarity):
        self.rarity = rarity

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    #Getters and setters
    def getState(self):
        return self.state
    def setState(self, state):
        self.state = state
    
#Weapon_Template class extends Equipment_Template
    
class Weapon_Template(Equipment_Template):
    def __init__(self, name, type, rarity, state, range):
        super().__init__(name, type, rarity, state)
        self.range = range
        print("Criou arma:", name, "\n tipo:", type, "\n raridade:", rarity, "\n estado:", state)
    
    def DisplayString(self):
        display_string = (
            f"Weapon: {self.name}\n"
            f"Type: {self.type}\n"
            f"Rarity: {self.rarity}\n"
            f"State: {self.state}\n"
            f"Range: {self.range}\n"
            "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n"
        )
        return display_string

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'range': self.range
        })
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            type=data['type'],
            rarity=data['rarity'],
            state=data['state'],
            range=data['range']
        )
    
    def getRange(self):
        return self.range
    
    def setRange(self, range):
        self.range = range
            
    def roll_Damage_TwoDicesMod(self, n, x, m, y, modifier, target:None):
        temp = (n * self.roll_Dice(x) + m * self.roll_Dice(y) + modifier)
        print("Usando arma:", self.name, "\nDano: causado", temp)
        temp = temp*(-1)
        if target is not None:
            target.AttB_modifyAtr(temp)
        return temp
    
    def roll_Damage_TwoDices(self, n, x, m, y, target):
        temp = (n * self.roll_Dice(x) + m * self.roll_Dice(y))
        print("Usando arma:", self.name, "\nDano: causado", temp)
        temp = temp*(-1)
        if target is not None:
            target.AttB_modifyAtr(temp)
        return temp
    
    def roll_Damage_OneDiceMod(self, n, x, modifier, target):
        temp = (n * self.r_Dice(x) + modifier)
        print("Usando arma:", self.name, "\nDano: causado", temp)
        temp = temp*(-1)
        if target is not None:
            target.AttB_modifyAtr(temp)
        return temp
    
    def roll_Damage_OneDice(self, n, x, target):
        temp = (n * self.roll_Dice(x))
        print("Usando arma:", self.name, "\nDano: causado", temp)
        temp = temp*(-1)
        if target is not None:
            target.AttB_modifyAtr(temp)
        return temp
    
    def roll_Damage_Fixed(self, modifier, target):
        print("Usou arma:", self.name, "\nDano causado:", modifier)
        modifier = modifier*(-1)
        if target is not None:
            target.AttB_modifyAtr(modifier)
        return modifier
    
    def roll_DamageWithCountMod(self, n, x, modifier, target):
        temp = self.roll_DiceWithCountMod(x, n, modifier)
        print("Usando arma:", self.name, "\nDano: causado", temp)
        temp = temp*(-1)
        if target is not None:
            target.AttB_modifyAtr(temp)
        return temp
    
class Usable_Template(Equipment_Template):
    def __init__(self, name, type, rarity, state, durability):
        super().__init__(name, type, rarity, state)
        self.durability = durability
        print("Criou o equipamento:", self.name)
    
    def DisplayString(self):
        display_string = (
            f"Usable: {self.name}\n"
            f"Type: {self.type}\n"
            f"Rarity: {self.rarity}\n"
            f"State: {self.state}\n"
            f"Durability: {self.durability}\n"
            "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n"
        )
        return display_string

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'durability': self.durability
        })
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            type=data['type'],
            rarity=data['rarity'],
            state=data['state'],
            durability=data['durability']
        )

    def rollUse(self, x, hit):
        temp = self.roll_Dice(x)
        if temp < hit:
            print("acerto com valor de dado de:" + temp)
            if self.durability == 1:
                print("Usou", self.name, "\nO item acabou")
                self.setName(self.name + "usado")
                self.state = "usado"
                self.durability -= 1
            elif self.durability < 1:
                print("O item já está usado")
            else:
                self.durability -= 1
                print("Usou", self.name, "\n Restam:", self.durability ,"usos")
        else:
            print("falha no uso de:" + self.name + " o dado foi menor que " + self.hit)
    
    def useInSomeone(self, effect, target):
        if self.durability == 1:
            target.AttV_setValue(target.AttV_getValue() + effect)
            self.durability -= 1
            print("Usou", self.name, "em", target.name, "causando", self.effect, "\nO item acabou")
            self.setName(self.name + " usado")
            self.state = "usado"
        elif self.durability < 1:
            print("O item já está usado")
        else:
            self.durability -= 1
            target.AttV_setValue(target.AttV_getValue() + effect)
            print("Usou", self.name, "em", self.target, "causando", self.effect, "\n Restam:", self.durability ,"usos")

    def Use(self):
        if self.durability == 1:
            print("Usou", self.name, "\nO item acabou")
            self.setName(self.name + " usado")
            self.state = "usado"
            self.durability -= 1
        elif self.durability < 1:
            print("O item já está usado")
        else:
            self.durability -= 1
            print("Usou", self.name, "\n Restam:", self.durability ,"usos")
    
    def getDurability(self):
        return self.durability
    
    def addDurability(self, durability):
        self.durability += durability
    
class Permanent_Template(Equipment_Template):
    def __init__(self, name, type, rarity, state):
        super().__init__(name, type, rarity, state)
        print("Criou o equipamento:", self.name)

    def DisplayString(self):
        display_string = (
            f"Permanent: {self.name}\n"
            f"Type: {self.type}\n"
            f"Rarity: {self.rarity}\n"
            f"State: {self.state}\n"
            "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n"
        )
        return display_string

    def to_dict(self):
        data = super().to_dict()
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            type=data['type'],
            rarity=data['rarity'],
            state=data['state']
        )

class Permanent_Buff_Template(Permanent_Template):
    def __init__(self, name, type, rarity, state, effect):
        super().__init__(name, type, rarity, state)
        self.effect = effect
    
    def DisplayString(self):
        display_string = (
            f"Permanent Buff: {self.name}\n"
            f"Type: {self.type}\n"
            f"Rarity: {self.rarity}\n"
            f"State: {self.state}\n"
            f"Effect: {self.effect}\n"
            "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n"
        )
        return display_string

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'effect': self.effect
        })
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            type=data['type'],
            rarity=data['rarity'],
            state=data['state'],
            effect=data['effect']
        )

    def applyInAttV(self, target):
        target.AttV_setValue(target.AttV_getValue() + self.effect)
        print("Aplicou", self.effect, "em", target.name)
        
    def removeFromAttV(self, target):
        target.AttV_setValue(target.AttV_getValue() - self.effect)
        print("Removeu", self.effect, "de", target.name)    
    
    def getEffect(self):
        return self.effect
    
    

    

    
    
