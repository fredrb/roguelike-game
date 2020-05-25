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
            Tome("Fighter's Tome", (10*factor), StrengthUpgrade(factor*1)),
            Tome("Templar's Tome", (10*factor), AgilityUpgrade(factor*1)),
            Tome("Cleric's Tome", (12*factor), HPUpgrade(factor*20)),
            Tome("Wizard's Tome", (15*factor), MagicUpgrade(factor*1))
        ]
        
