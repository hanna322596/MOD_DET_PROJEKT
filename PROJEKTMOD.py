import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap



class HeatingModel:
    def __init__(self, parameters: dict):
        self.parameters = parameters
        self.partial_matrix = {}
        self.result_matrix = np.zeros((100, 100))
        self.mask_matrix = np.zeros((100, 100))

        for key, val in parameters['rooms'].items():
            row_min = val['rowmin']
            row_max = val['rowmax']
            col_min = val['colmin']
            col_max = val['colmax']
            self.partial_matrix[key] = np.zeros((row_max - row_min, col_max - col_min))
            mask = parameters["mask"][key]
            self.partial_matrix[key][mask == 1] = 4
            self.result_matrix[row_min:row_max, col_min:col_max] = self.partial_matrix[key]

        index = {'windows': 1, 'walls': 2, 'doors': 3, 'radiators': 5}

        for i in index:
            for key, val in parameters[i].items():
                row_min = val['rowmin']
                row_max = val['rowmax']
                col_min = val['colmin']
                col_max = val['colmax']
                self.result_matrix[row_min:row_max, col_min:col_max] = index[i]



    def build_apartment(self):
        return self.result_matrix

    def evolve_in_unit_timestep(self, dt: float):
        hx=1
        ht=1/4
        force_term_full = self.parameters["force_term"](self.parameters["domain"]["grid"],
                                                     self.parameters["current_time"],
                                                     self.mask_matrix)
        for key in self.parameters["windows"].keys():
            self.result_matrix[
                self.parameters["windows"][key]["rowmin"]: self.parameters["windows"][key]["rowmax"],
                self.parameters["windows"][key]["colmin"]: self.parameters["windows"][key]["colmax"]
            ] = self.parameters["window_temp"](self.parameters["current_time"])


        self.parameters["current_time"] += dt
        return self

    def evolve(self, n_steps: int, dt: float):
        for _ in tqdm.tqdm(range(n_steps), desc="TIME STEPS"):
            self.evolve_in_unit_timestep(dt)
        self.build_apartment()
        return self


if __name__ == '__main__':
    apartment = {
        "rooms": { #rooms
            "A1": {
                "rowmin": 2, "rowmax": 48, "colmin": 2, "colmax": 38, "init_func": lambda x: 295 + np.random.random(x.shape)
            },
            "A2": {
                "rowmin": 2, "rowmax": 48, "colmin": 52, "colmax": 98, "init_func": lambda x: 298 + np.random.random(x.shape)
            },
            "A3": {
                "rowmin": 2, "rowmax": 50, "colmin": 40, "colmax": 50, "init_func": lambda x: 297 + np.random.random(x.shape)
            },
            "A4": {
                "rowmin": 50, "rowmax": 88, "colmin": 2, "colmax": 98, "init_func": lambda x: 296 + np.random.random(x.shape)
            },
            "A5": {
                "rowmin": 90, "rowmax": 100, "colmin": 0, "colmax": 100
            }
        },
        "mask": {"A1": 1, "A2": 1, "A3": 1, "A4": 1, "A5": 0},
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
        "walls": { #walls
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
    cmap = ListedColormap(['white', 'blue', 'black', 'brown', 'floralwhite', 'red'])

    model = HeatingModel(apartment)
    plt.imshow(model.build_apartment(), cmap=cmap)
    plt.show()
    plt.imshow(model.build_apartment(), cmap=plt.get_cmap("coolwarm"))
    plt.title(f"t = {model.parameters['current_time']}")
    plt.colorbar().set_label("Temperature[K]")
    plt.show()