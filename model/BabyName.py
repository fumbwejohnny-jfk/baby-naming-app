
class BabyName:
    def __init__(self):
        # self.access_token = None
        self.role = None# Store JWT token after login for authenticated requests
        # self.refresh_token = None
        self.username = None
        self.babies = []  # Store baby names data after fetching from server
        self.babies_stats = {}  # Store baby name stats for charts

    def getUserInfo(self, resp):
        # self.access_token = resp.get("access")
        # self.refresh_token = resp.get("refresh")
        user = resp.get("user")
        self.username = user.get("username") if user else None  
        self.role = 'Admin' if user.get("is_admin") else 'User'
        
     