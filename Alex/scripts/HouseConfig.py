class HouseConfig:
    def __init__(self, id:str, pv:float, daylight:float, compactness:float, fsi:float):
        self.id = id
        self.pv = pv
        self.daylight = daylight
        self.compactness = compactness
        self.fsi = fsi
        
    def __str__(self):
        return f"HouseConfig(id={self.id}, pv={self.pv}, daylight={self.daylight}, compactness={self.compactness}, fsi={self.fsi})"