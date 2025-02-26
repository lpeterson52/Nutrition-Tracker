class Food:
    def __init__(self, name: str, calories, total_fat, total_carbs, protein):
        self._name = name
        self.calories = calories
        self.total_fat = total_fat
        self.total_carbs = total_carbs
        self.protein = protein
    
    def __repr__(self):
        return (self.name + ": Calories: " + str(self.calories) + 
                ", Total Fat: " + str(self.total_fat) + 
                ", Total Carbs: " + str(self.total_carbs) + 
                ", Protein: " + str(self.protein))
    def _get_name(self):
        return self._name
    
    def _set_name(self, name):
        self._name = name
        
    name = property(
        fget=_get_name,
        fset=_set_name
    )
    def calories(self):
        return self.calories

    def total_fat(self):
        return self.total_fat
    
    def total_carbs(self):
        return self.total_carbs
    
    def protein(self):
        return self.protein
    @property
    def dict_form(self):
        return {"name": self.name,
                "calories": self.calories,
                "total_fat": self.total_fat,
                "total_carbs": self.total_carbs,
                "protein": self.protein}
        