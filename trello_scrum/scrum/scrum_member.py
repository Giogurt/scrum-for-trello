from trello import member

class ScrumMember(member.Member):
    """
    Class representing  trello member with scrum implementation
    """
    
    def __init__(self, client, member_id, full_name=''):
        super().__init__(client, member_id, full_name)
        self.points = 0

    def set_points(self, points):
        self.points = points

    def add_points(self, points):
        self.points += points