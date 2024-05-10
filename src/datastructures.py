from random import randint
class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        # example list of members
        self._members = [
            {
                "id": self._generateId(),
                "first_name": "John",
                "last_name": self.last_name,
                "age": 33,
                "lucky_numbers": [7, 13, 22]
            },
            {
                "id": self._generateId(),
                "first_name": "Jane",
                "last_name": self.last_name,
                "age": 35,
                "lucky_numbers": [10, 14, 3]
            },
            {
                "id": self._generateId(),
                "first_name": "Jimmy",
                "last_name": self.last_name,
                "age": 5,
                "lucky_numbers": [1]
            }
        ]
    def _generateId(self):
        """ Generate a random member ID. """
        return randint(0, 99999999)
    def add_member(self, member):
        """ Adds a member to the family if they don't already exist based on the ID. """
        if any(m['id'] == member['id'] for m in self._members):
            return {"error": "Member already exists"}, 400
        self._members.append(member)
        return member, 201
    def delete_member(self, id):
        """ Deletes a member from the family based on their ID. """
        for i, member in enumerate(self._members):
            if member['id'] == id:
                del self._members[i]
                return {"message": "Member deleted"}, 200
        return {"error": "Member not found"}, 404
    def get_member(self, id):
        """ Returns a member from the family based on their ID. """
        for member in self._members:
            if member['id'] == id:
                return member, 200
        return {"error": "Member not found"}, 404
    def get_all_members(self):
        """ Returns a list of all family members. """
        return self._members
    def update_member(self, id, updates):
        """ Updates a member's information based on their ID. """
        for member in self._members:
            if member['id'] == id:
                member.update(updates)
                return member, 200
        return {"error": "Member not found"}, 404  