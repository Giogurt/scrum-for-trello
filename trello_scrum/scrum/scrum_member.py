from trello import member

class ScrumMember(member.Member):
    """
    Class representing  trello member with scrum implementation
    """
    
    def __init__(self, client, member_id, full_name=''):
        super().__init__(client, member_id, full_name)
        self.points = {}

    def set_points(self, list_name, points):
        self.points[list_name] = points

    def add_points(self, list_name, points):
        self.points[list_name] += points