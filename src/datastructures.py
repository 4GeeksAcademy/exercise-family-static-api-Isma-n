"""
Update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- get_member: Should return a member from the self._members list
"""

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._next_id = 1
        self._members = []
        
        # Así empiezo con los 3 miembros especificados en el ejercicio de API estática
        self.add_member({
            "first_name": "John",
            "age": 33,
            "lucky_numbers": [7, 13, 22]
        })
        
        self.add_member({
            "first_name": "Jane", 
            "age": 35,
            "lucky_numbers": [10, 14, 3]
        })
        
        self.add_member({
            "first_name": "Jimmy",
            "age": 5,
            "lucky_numbers": [1]
        })

    # This method generates a unique incremental ID (copiado de la página inicial de datastructures.py)
    def _generate_id(self):
        generated_id = self._next_id
        self._next_id += 1
        return generated_id

    def add_member(self, member):
        """
        Agrega un nuevo miembro a la lista de _members
        Si el miembro no tiene ID, se genera uno automáticamente
        """
        # Si no viene con ID, se genera uno
        if "id" not in member:
            member["id"] = self._generate_id()
        else:
            # Si viene con ID, actualizamos el _next_id para evitar duplicados
            if member["id"] >= self._next_id:
                self._next_id = member["id"] + 1
        
        # Aseguramos que tenga last_name  Michael Jackson jajajajaj
        member["last_name"] = self.last_name
        
        # Con esto agrego a la lista
        self._members.append(member)
        
        return member

    def delete_member(self, id):
        """
        Elimina el miembro con el ID proporcionado
        Retorna True si se eliminó, False si no se encontró
        """
        for i, member in enumerate(self._members):
            if member["id"] == id:
                del self._members[i]
                return True
        return False

    def get_member(self, id):
        """
        Busca y retorna el miembro con el ID proporcionado
        Retorna None si no se encuentra
        """
        for member in self._members:
            if member["id"] == id:
                return member
        return None

    # This method is done, it returns a list with all the family members (copiado de la página inicial de datastructures.py)
    def get_all_members(self):
        return self._members