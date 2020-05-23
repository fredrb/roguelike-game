from components.tome import Tome, StrengthUpgrade, AgilityUpgrade, HPUpgrade, MagicUpgrade
import math

class Shop:
    def __init__(self, floor):
        self.floor = floor

    def get_message(self):
        return "Shop at Floor %i" % self.floor

    @property
    def options(self):
        factor = math.ceil(self.floor/3)
        return [
            Tome("Tome of Strength", (15*factor)+self.floor, StrengthUpgrade(factor*1)),
            Tome("Tome of Agility", (15*factor)+self.floor, AgilityUpgrade(factor*1)),
            Tome("Tome of Vitality", (15*factor)+self.floor, HPUpgrade(factor*20)),
            Tome("Tome of Magic", (15*factor)+self.floor, MagicUpgrade(factor*1))
        ]
        
