from components.tome import Tome, StrengthUpgrade, AgilityUpgrade, HPUpgrade

class Shop:
    def __init__(self, floor):
        self.floor = floor

    def get_message(self):
        return "Shop at Floor %i" % self.floor

    @property
    def options(self):
        return [
            Tome("Tome of Strength", 10, StrengthUpgrade(1)),
            Tome("Tome of Agility", 10, AgilityUpgrade(1)),
            Tome("Tome of Vitality", 10, HPUpgrade(20))
        ]
        
