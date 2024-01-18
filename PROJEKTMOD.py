import numpy as np
import matplotlib.pyplot as plt
import cloudpickle
from PIL import Image


class HeatingModel():

    def __init__(self, apart_dict):
        self.params = apart_dict
        self.partial_matrix = {}
        self.result_matrix = np.zeros((100,100))
        self.mask_matrix = np.zeros((100,100))
        self.build_partial_matrix(apart_dict.get('rooms'))

    def build_partial_matrix(self, rooms_dict):
        matrix = np.zeros((100, 100), dtype=int)
        for room, details in rooms_dict.items():
            row_range = range(details['rowmin'], details['rowmax'])
            col_range = range(details['colmin'], details['colmax'])
            matrix[np.ix_(row_range, col_range)] = 1
        return matrix





if __name__ == '__main__':
    apartment = {
        'rooms': {
            'A1': {
                "rowmin": 2, "rowmax": 48, "colmin": 2, "colmax": 38
            },
            'A2': {
                "rowmin": 2, "rowmax": 48, "colmin": 52, "colmax": 98
            },
            'A3': {
                "rowmin": 2, "rowmax": 50, "colmin": 40, "colmax": 50
            },
            'A4': {
                "rowmin": 50, "rowmax": 88, "colmin": 2, "colmax": 98
            },
            'A5': {
                "rowmin": 90, "rowmax": 100, "colmin": 0, "colmax": 100
            }
        },
        "radiators": {
            'R1': {
                "rowmin": 47, "rowmax": 48, "colmin": 20, "colmax": 27, "mask_values": 1
            },
            'R2': {
                "rowmin": 20, "rowmax": 30, "colmin": 97, "colmax": 98, "mask_values": 2
            },
            'R3': {
                "rowmin": 87, "rowmax": 88, "colmin": 30, "colmax": 45, "mask_values": 3
            },
            'R4': {
                "rowmin": 2, "rowmax": 3, "colmin": 44, "colmax": 46, "mask_values": 4
            }
        },
        "walls": {
            'W1': {
                "rowmin": 0, "rowmax": 2, "colmin": 0, "colmax": 100
            },
            'W2': {
                "rowmin": 2, "rowmax": 20, "colmin": 0, "colmax": 2
            },
            'W3': {
                "rowmin": 28, "rowmax": 60, "colmin": 0, "colmax": 2
            },
            'W4': {
                "rowmin": 70, "rowmax": 88, "colmin": 0, "colmax": 2
            },
            'W5': {
                "rowmin": 2, "rowmax": 20, "colmin": 98, "colmax": 100
            },
            'W6': {
                "rowmin": 28, "rowmax": 60, "colmin": 98, "colmax": 100
            },
            'W7': {
                "rowmin": 70, "rowmax": 88, "colmin": 98, "colmax": 100
            },
            'W8': {
                "rowmin": 88, "rowmax": 90, "colmin": 0, "colmax": 60
            },
            'W9': {
                "rowmin": 88, "rowmax": 90, "colmin": 65, "colmax": 100
            },
            'W10': {
                "rowmin": 48, "rowmax": 50, "colmin": 2, "colmax": 38
            },
            'W11': {
                "rowmin": 48, "rowmax": 50, "colmin": 52, "colmax": 98
            },
            'W12': {
                "rowmin": 2, "rowmax": 20, "colmin": 38, "colmax": 40
            },
            'W13': {
                "rowmin": 25, "rowmax": 50, "colmin": 38, "colmax": 40
            },
            'W14': {
                "rowmin": 2, "rowmax": 20, "colmin": 50, "colmax": 52
            },
            'W15': {
                "rowmin": 25, "rowmax": 50, "colmin": 50, "colmax": 52
            },
            'W16': {
                "rowmin": 48, "rowmax": 50, "colmin": 52, "colmax": 98
            }
        },
        "windows": {
            'O1': {
                "rowmin": 20, "rowmax": 28, "colmin": 0, "colmax": 2
            },
            'O2': {
                "rowmin": 60, "rowmax": 70, "colmin": 0, "colmax": 2
            },
            'O3': {
                "rowmin": 20, "rowmax": 28, "colmin": 98, "colmax": 100
            },
            'O4': {
                "rowmin": 60, "rowmax": 70, "colmin": 98, "colmax": 100
            }
        },
        "doors": {
            'D1': {
                "rowmin": 88, "rowmax": 90, "colmin": 60, "colmax": 65
            },
            'D2': {
                "rowmin": 20, "rowmax": 25, "colmin": 38, "colmax": 40
            },
            'D3': {
                "rowmin": 20, "rowmax": 25, "colmin": 50, "colmax": 52
            }
        },
        "domain": {
            "grid": np.meshgrid(np.linspace(-1,1,101),np.linspace(-1,1,101))[0], "dx": 1
        },
        "force_term": lambda x,t,mask: np.where(
            mask == 1, (np.sin(24*t/3600)**2 + 2)/10, np.where(
                mask == 2, (np.sin(24*t/3600)**2 + 1)/10, np.where(
                    mask == 3, (np.sin(24*t/3600)**2 + 1)/10, np.where(
                        mask == 4, (np.sin(24*t/3600)**2 + 1)/10, 0
                        )
                    )
                )
            ),
        "window_temp": lambda t: 280 - 10*np.sin(24*t/3600),
        "diffusion": 0.1,
        "current_time": 0.0
    }
    model = HeatingModel(apartment)
    jdhssjwcnic




