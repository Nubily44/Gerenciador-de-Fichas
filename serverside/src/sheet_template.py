import random

class Sheet_Template:
    def __init__(self, nome, AttB, AttC, AttV):
        self.nome = nome
        self.B = AttB
        self.C = AttC
        self.V = AttV
        self.Alive = 1
        self.WeaponsBackpack = []
        self.UsablesBackpack = []
        self.PermanentsBackpack = []

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

    def Display(self):
        print("Nome: ", self.nome)
        print("B: ", self.B)
        print("C: ", self.C)
        print("V: ", self.V)
        print("Alive: ", self.Alive)
        for _ in self.getWeapons():
            print("Weapons: ", _)  
        for _ in self.getUsables():
            print("Usable: ", _)
        for _ in self.getPermanents():
            print("Permanents: ", _)    

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    # Getters and Setters
    def AttB_SetValue(self, AttB):
        self.B = AttB

    def AttB_GetValue(self):
        return self.B
    

    # Additional methods
    def AttB_ModifyAtr(self, x): # Damage, Heal, etc
        self.B = self.B + x
        if self.B < 0:
            self.B = 0
            self.Alive = 0

    def AttB_isZero(self): 
        return self.B == 0

    def AttB_isLessThan(self, x):
        return self.B < x


    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    
    #Getters and Setters
    def AttC_SetValue(self, AttC):
        self.C = AttC

    def AttC_GetValue(self):
        return self.C


    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    
    #Getters and Setters
    def AttV_SetValue(self, AttV):
        self.V = AttV

    def AttV_GetValue(self):
        return self.V


    # Additional methods
    def AttV_RollAtr(self, dice, target, count): # Roll dices
        return self.Roll_DiceWithCount(dice, count) + self.V >= target

    def AttV_RollAtrWithCountMod(self, dice, target, count, mod):
        return self.Roll_DiceWithCountMod(dice, count, mod) + self.V >= target
        
    def AttV_UpgradeAtr(self, x): # Upgrade the attribute
        self.V = self.V + x

    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    
    def isAlive(self):
        return self.Alive
    
    def IsDead(self):
        return self.Alive
    
    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
   
    def addWeapon(self, weapon, quantity):
        if quantity > 0:
            self.WeaponsBackpack.append([weapon.Get_name(), quantity])

        if quantity < 0:
            for i in range(len(self.WeaponsBackpack)):
                if self.WeaponsBackpack[i][0] == weapon:
                    self.WeaponsBackpack[i][1] = self.WeaponsBackpack[i][1] + quantity
                    if self.WeaponsBackpack[i][1] <= 0:
                        self.WeaponsBackpack.pop(i)
                        break
    
    def getWeapons(self):
        return self.WeaponsBackpack
    
    def addUsable(self, usable, quantity):
        if quantity > 0:
            self.UsablesBackpack.append([usable.Get_name(), quantity])

        if quantity < 0:
            for i in range(len(self.UsablesBackpack)):
                if self.UsablesBackpack[i][0] == usable:
                    self.UsablesBackpack[i][1] = self.UsablesBackpack[i][1] + quantity
                    if self.UsablesBackpack[i][1] <= 0:
                        self.UsablesBackpack.pop(i)
                        break
    
    def getUsables(self):
        return self.UsablesBackpack
    
    def addPermanent(self, permanent, quantity):
        if quantity > 0:
            self.PermanentsBackpack.append([permanent.Get_name(), quantity])

        if quantity < 0:
            for i in range(len(self.PermanentsBackpack)):
                if self.PermanentsBackpack[i][0] == permanent:
                    self.PermanentsBackpack[i][1] = self.PermanentsBackpack[i][1] + quantity
                    if self.PermanentsBackpack[i][1] <= 0:
                        self.PermanentsBackpack.pop(i)
                        break

    def getPermanents(self):
        return self.PermanentsBackpack

          
                    
            
