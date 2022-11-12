from app import db

class Ingredient(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String)
  breakfast_items = db.relationship('Breakfast', secondary='breakfast_ingredient', back_populates='ingredients')

  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name,
      "breakfast_items": self.get_all_breakfast_items()
    }

  def get_all_breakfast_items(self):
    breakfast_items_list = []
    for item in self.breakfast_items:
      breakfast_items_list.append(item.name)
    return breakfast_items_list

  @classmethod
  def from_dict(cls, ingredient_dict):
    return cls(name=ingredient_dict["name"])