from app import db

class Breakfast(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    rating = db.Column(db.Float)
    prep_time = db.Column(db.Integer)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    menu = db.relationship('Menu', back_populates='breakfast_items')
    ingredients = db.relationship('Ingredient', secondary='breakfast_ingredient', back_populates='breakfast_items')

    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "rating":self.rating,
            "prep_time":self.prep_time,
            "menu_id":self.menu_id,
            "ingredients": self.get_all_ingredients()
        }
    
    def get_all_ingredients(self):
        ingredient_list = []
        for ingredient in self.ingredients:
            ingredient_list.append(ingredient.to_dict())
        return ingredient_list

    @classmethod
    def from_dict(cls, breakfast_dict):
        return cls(
            name=breakfast_dict["name"],
            rating=breakfast_dict["rating"],
            prep_time=breakfast_dict["prep_time"],
            menu_id=breakfast_dict["menu_id"]
        )
