import random

class Equipment_Template:
    def __init__(self, name, type, rarity, state):
        self.name = name
        self.type = type
        self.rarity = rarity
        self.state = state

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
        print("adicionou arma:", name, "\n tipo:", type, "\n raridade:", rarity, "\n estado:", state)
    
    def getRange(self):
        return self.range
    
    def setRange(self, range):
        self.range = range

    def roll_Damage_TwoDicesMod(self, n, x, m, y, modifier):
        temp = (n * self.roll_Dice(x) + m * self.roll_Dice(y) + modifier)
        print("Usando arma:", self.name, "\nDano: causado", temp)
        return temp
    
    def roll_Damage_TwoDices(self, n, x, m, y, ):
        temp = (n * self.roll_Dice(x) + m * self.roll_Dice(y))
        print("Usando arma:", self.name, "\nDano: causado", temp)
        return temp
    
    def roll_Damage_OneDiceMod(self, n, x, modifier):
        temp = (n * self.r_Dice(x) + modifier)
        print("Usando arma:", self.name, "\nDano: causado", temp)
        return temp
    
    def roll_Damage_OneDice(self, n, x):
        temp = (n * self.roll_Dice(x))
        print("Usando arma:", self.name, "\nDano: causado", temp)
        return temp
    
    def roll_Damage_Fixed(self, modifier):
        print("Usou arma:", self.name, "\nDano causado:", modifier)
        return modifier
    
    def roll_DamageWithCountMod(self, n, x, modifier):
        temp = self.roll_DiceWithCountMod(x, n, modifier)
        print("Usando arma:", self.name, "\nDano: causado", temp)
        return temp
    
class Usable_Template(Equipment_Template):
    def __init__(self, name, type, rarity, state, durability):
        super().__init__(name, type, rarity, state)
        self.durability = durability
        print("Adicionou o equipamento:", self.name)
    
    def useInSomeone(target, effect, self):
        target.AttV_setValue(target.AttV_getValue() + effect)
        self.durability -= 1
        print("Usou", self.name, "em", self.target, "causando", self.effect, "\n Restam:", self.durability ,"usos")
    
    def use(self):
        self.durability -= 1
        print("Usou", self.name, "\n Restam:", self.durability ,"usos")
    
    def getDurability(self):
        return self.durability
    
class Permanent_Template(Equipment_Template):
    def __init__(self, name, type, rarity, state):
        super().__init__(name, type, rarity, state)
        print("Criou o equipamento:", self.name)


class Permanent_Buff_Template(Equipment_Template):
    def __init__(self, name, type, rarity, state, effect):
        super().__init__(name, type, rarity, state)
        self.effect = effect
        print("Adicionou o equipamento", self.name)
    
    def Apply(target, self):
        target.AttV_setValue(target.AttV_getValue() + self.effect)
    
    def getEffect(self):
        return self.effect

    

    
    
