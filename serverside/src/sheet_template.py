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

    def Display(self):
        print("Nome: ", self.nome)
        print("B: ", self.B)
        print("C: ", self.C)
        print("V: ", self.V)
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

    # getters and setters
    def AttB_setValue(self, AttB):
        self.B = AttB

    def AttB_getValue(self):
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
    
    #getters and setters
    def AttC_setValue(self, AttC):
        self.C = AttC

    def AttC_getValue(self):
        return self.C


    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    
    #getters and setters
    def AttV_setValue(self, AttV):
        self.V = AttV

    def AttV_getValue(self):
        return self.V


    # Additional methods
    def AttV_rollAtr(self, dice, target, count): # roll dices
        return self.roll_DiceWithCount(dice, count) + self.V >= target

    def AttV_rollAtrWithCountMod(self, dice, target, count, mod):
        return self.roll_DiceWithCountMod(dice, count, mod) + self.V >= target
        
    def AttV_UpgradeAtr(self, x): # Upgrade the attribute
        self.V = self.V + x

    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    
    def isAlive(self):
        return self.Alive
    
    def isDead(self):
        return self.Alive
    
    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
   
    def addWeapon(self, weapon, quantity):
        if quantity > 0:
            self.WeaponsBackpack.append([weapon, quantity])

        if quantity < 0:
            for i in range(len(self.WeaponsBackpack)):
                if self.WeaponsBackpack[i][0] == weapon:
                    self.WeaponsBackpack[i][1] = self.WeaponsBackpack[i][1] + quantity
                    if self.WeaponsBackpack[i][1] <= 0:
                        self.WeaponsBackpack.pop(i)
                        break
    
    def getWeapons(self):
        WeaponListNames = []
        for i in range(len(self.WeaponsBackpack)):
            quant = self.WeaponsBackpack[i][1]
            for j in range(quant):
                WeaponListNames.append(self.WeaponsBackpack[i][0].getName())
        return WeaponListNames

    def getWeaponsBackpack(self):
        return self.WeaponsBackpack

    
    def addUsable(self, usable, quantity):
        if quantity > 0:
            self.UsablesBackpack.append([usable, quantity])

        if quantity < 0:
            for i in range(len(self.UsablesBackpack)):
                if self.UsablesBackpack[i][0] == usable:
                    self.UsablesBackpack[i][1] = self.UsablesBackpack[i][1] + quantity
                    if self.UsablesBackpack[i][1] <= 0:
                        self.UsablesBackpack.pop(i)
                        break
    
    def getUsables(self):
        UsableListNames = []
        for i in range(len(self.UsablesBackpack)):
            quant = self.UsablesBackpack[i][1]
            for j in range(quant):
                UsableListNames.append(self.UsablesBackpack[i][0].getName())
        return UsableListNames

    def getUsablesBackpack(self):
        return self.UsablesBackpack

    
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
              
    def getPermanents(self):
        PermanentListNames = []
        for i in range(len(self.PermanentsBackpack)):
            quant = self.PermanentsBackpack[i][1]
            for j in range(quant):
                PermanentListNames.append(self.PermanentsBackpack[i][0].getName())
        return PermanentListNames
    
    def getPermanentsBackpack(self):
        return self.PermanentsBackpack
             

          
                    
            
