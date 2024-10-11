import random

class Equipment_Template:
    def __init__(self, name, type, rarity, state):
        self.name = name
        self.type = type
        self.rarity = rarity
        self.state = state

    # Dices
    
    def Roll_Dice(self, x):
        return random.randint(1, x)
    
    def Roll_DiceWithCount(self, x, count):
        rolls = [self.Roll_Dice(x) for _ in range(count)]
        return max(rolls)
    
    def Roll_DiceWithCountMod(self, x, count, mod):
        rolls = [self.Roll_Dice(x) for _ in range(count + abs(mod))]
        if mod > 0:
            return max(rolls)
        else:
            return min(rolls)


    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    #Getters and Setters
    def Get_name(self):
        return self.name
    def Set_name(self, name):
        self.name = name

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    #Getters and Setters
    def Get_type(self):
        return self.type
    def Set_type(self, type):
        self.type = type

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    #Getters and Setters
    def Get_rarity(self):
        return self.rarity
    def Set_rarity(self, rarity):
        self.rarity = rarity

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    #Getters and Setters
    def Get_state(self):
        return self.state
    def Set_state(self, state):
        self.state = state
    
#Weapon_Template class extends Equipment_Template
    
class Weapon_Template(Equipment_Template):
    def __init__(self, name, type, rarity, state, range):
        super().__init__(name, type, rarity, state)
        self.range = range
    
    def Get_range(self):
        return self.range
    
    def Set_range(self, range):
        self.range = range

    def Roll_Damage(self, n, x, m, y, modifier):
        return (n * self.roll_Dice(x) + m * self.roll_Dice(y) + modifier)
    
    def Roll_Damage(self, n, x, modifier):
        return (n * self.roll_Dice(x) + modifier)
    
    def Roll_Damage(self, n, x):
        return (n * self.roll_Dice(x))
    
    def Roll_Damage(self, modifier):
        return modifier
    
class Usable_Template(Equipment_Template):
    def __init__(self, name, type, rarity, state, durability):
        super().__init__(name, type, rarity, state)
        self.durability = durability
    
    def Use(target, effect, self):
        target.AttV_SetValue(target.AttV_GetValue() + effect)
        self.durability -= 1
    
    def Get_durability(self):
        return self.durability
    
class Permanent_Template(Equipment_Template):
    def __init__(self, name, type, rarity, state):
        super().__init__(name, type, rarity, state)


class Permanent_Buff_Template(Equipment_Template):
    def __init__(self, name, type, rarity, state, effect):
        super().__init__(name, type, rarity, state)
        self.effect = effect
    
    def Apply(target, self):
        target.AttV_SetValue(target.AttV_GetValue() + self.effect)
    
    def Get_effect(self):
        return self.effect

    

    
    
