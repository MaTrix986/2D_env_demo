from shapely.ops import unary_union

class Obstacle:
    def __init__(self, id, geometry):
        self.id = id
        self.geometry = geometry
        
    def union(self, geometry):
        self.geometry = unary_union([
            self.geometry, geometry
        ])

    def get_geometry(self):
        return self.geometry


