from bson.objectid import ObjectId

class User:
    def __init__(self, nombre, email, password):
        self.nombre = nombre
        self.email = email
        self.password = password

    def toDBCollection(self):
        return {
            "nombre": self.nombre,
            "email": self.email,
            "password": self.password
        }

class Hobby:
    def __init__(self, user_id, description, level, percentage):
        # Aseguramos que user_id sea ObjectId
        self.user_id = ObjectId(user_id) if not isinstance(user_id, ObjectId) else user_id
        self.description = description
        self.level = level
        self.percentage = percentage
    
    def toDBCollection(self):
        return {
            "user_id": self.user_id,
            "description": self.description,
            "level": self.level,
            "percentage": self.percentage
        }
