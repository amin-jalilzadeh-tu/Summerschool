import numpy as np
import pandas as pd
from scripts.HouseConfig import HouseConfig

def read_data(file_path) -> list[HouseConfig]:
    df = pd.read_csv(file_path)
    res: list[HouseConfig] = []
    for _, row in df.iterrows():
        house_config = HouseConfig(
            id=row['id'],
            pv=row['pv'],
            daylight=row['daylight'],
            compactness=row['compactness'],
            fsi=row['fsi']
        )
        res.append(house_config)
    return res

def read_data_with_threshold(file_path, pv: float, daylight: float, compactness: float, fsi: float) -> list[HouseConfig]:
    dataset = read_data(file_path)
    res: list[HouseConfig] = []

    for house in dataset:
        if (house.pv >= pv and house.daylight >= daylight and 
            house.compactness >= compactness and house.fsi >= fsi):
            res.append(house)
    return res

def convert_to_numpy_array(dataset: list[HouseConfig]) -> np.ndarray:
    return np.array([[house.pv, house.daylight, house.compactness, house.fsi] for house in dataset])