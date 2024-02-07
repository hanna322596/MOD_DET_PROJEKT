import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import tqdm



class HeatingModel:
    def __init__(self, parameters: dict):
        self.parameters = parameters
        self.partial_matrix = {}
        self.result_matrix = np.zeros((100, 100))
        self.mask_matrix = np.zeros((100, 100))
        self.index = {"windows": 1, "walls": 2, "doors": 3, "radiators": 5}
        self.build_partial_matrix()
        self.build_result_matrix()
        self.heatingData = []

        for key, val in parameters['rooms'].items():
            self.partial_matrix[key] = np.zeros((val['rowmax'] - val['rowmin'], val['colmax'] - val['colmin']))
            mask = parameters["mask"][key]
            self.partial_matrix[key][mask == 1] = 4
            self.result_matrix[val['rowmin']:val['rowmax'], val['colmin']:val['colmax']] = self.partial_matrix[key]
        for i in self.index:
            for key, val in self.parameters[i].items():
                self.result_matrix[val['rowmin']:val['rowmax'], val['colmin']:val['colmax']] = self.index[i]

    def build_partial_matrix(self):
        for room in self.parameters["rooms"].keys():
            coord = self.parameters["rooms"][room]
            if room not in self.partial_matrix.keys():
                self.partial_matrix[room] = np.zeros((coord["rowmax"]-coord["rowmin"], coord["colmax"]-coord["colmin"]))
                self.partial_matrix[room] = coord["init_func"](self.partial_matrix[room])
            else:
                self.partial_matrix[room] = self.result_matrix[coord["rowmin"]: coord["rowmax"],
                                            coord["colmin"]: coord["colmax"]]


    def build_result_matrix(self):
        for room in self.parameters["rooms"].keys():
            coord = self.parameters["rooms"][room]
            self.result_matrix[coord["rowmin"]:coord["rowmax"], coord["colmin"]:coord["colmax"]] = (
                self.partial_matrix)[room]

    def build_mask_matrix(self):
        counter = 1
        for radiators in self.parameters["radiators"].keys():
            coord = self.parameters["radiators"][radiators]
            self.mask_matrix[coord["rowmin"]:coord["rowmax"], coord["colmin"]:coord["colmax"]] = counter
            counter += 1



    def evolve_in_unit_timestep(self, dt: float):
        coefficient = self.parameters["diffusion"] * dt / self.parameters["domain"]["dx"] ** 2
        force_term_full = self.parameters["force_term"](self.parameters["domain"]["grid"],
                                                    self.parameters["current_time"],
                                                    self.mask_matrix)

        for key in self.parameters["windows"].keys():
            self.result_matrix[
                self.parameters["windows"][key]["rowmin"]: self.parameters["windows"][key]["rowmax"],
                self.parameters["windows"][key]["colmin"]: self.parameters["windows"][key]["colmax"]
            ] = self.parameters["window_temp"](self.parameters["current_time"])
        self.build_partial_matrix()
        for key in self.parameters["rooms"].keys():
            if np.mean(self.partial_matrix[key]) > self.parameters["rooms"][key]["temp"]:
                force_term_full[
                    self.parameters["rooms"][key]["rowmin"] + 1: self.parameters["rooms"][key]["rowmax"] - 1,
                    self.parameters["rooms"][key]["colmin"] + 1: self.parameters["rooms"][key]["colmax"] - 1
                ] = 0
            self.partial_matrix[key][1:-1, 1:-1] += coefficient * (self.partial_matrix[key][0:-2, 1:-1] +
                                                     self.partial_matrix[key][2:, 1:-1] +
                                                     self.partial_matrix[key][1:-1, 0:-2] +
                                                     self.partial_matrix[key][1:-1, 2:] -
                                                     4*self.partial_matrix[key][1:-1, 1:-1]) + \
                                                    force_term_full[
                                                        self.parameters["rooms"][key]["rowmin"]+1:
                                                        self.parameters["rooms"][key]["rowmax"]-1,
                                                        self.parameters["rooms"][key]["colmin"]+1:
                                                        self.parameters["rooms"][key]["colmax"]-1
                                                    ]
            self.partial_matrix[key][0, :] = self.partial_matrix[key][1, :]
            self.partial_matrix[key][-1, :] = self.partial_matrix[key][-2, :]
            self.partial_matrix[key][:, 0] = self.partial_matrix[key][:, 1]
            self.partial_matrix[key][:, -1] = self.partial_matrix[key][:, -2]
        self.build_result_matrix()
        for key in self.parameters["doors"].keys():
            self.result_matrix[
                self.parameters["doors"][key]["rowmin"]: self.parameters["doors"][key]["rowmax"],
                self.parameters["doors"][key]["colmin"]: self.parameters["doors"][key]["colmax"]
            ] = np.mean(self.result_matrix[
                            self.parameters["doors"][key]["rowmin"]: self.parameters["doors"][key]["rowmax"],
                            self.parameters["doors"][key]["colmin"]: self.parameters["doors"][key]["colmax"]
                        ]
                        )
        self.build_partial_matrix()
        #self.heatingData.append(np.sum(force_term_full))
        self.parameters["current_time"] += dt
        return self

    def evolve(self, n_steps: int, dt: float):
        for _ in tqdm.tqdm(range(n_steps), desc="TIME STEPS"):
            self.evolve_in_unit_timestep(dt)
        self.heatingData = np.cumsum(self.heatingData)
        return self

    def build_apartment(self):
        return self.result_matrix




if __name__ == '__main__':
    apartment = {
        "rooms": { #rooms
            "A1": {
                "rowmin": 0, "rowmax": 50, "colmin": 0, "colmax": 40,
                "init_func": lambda x: 295 + np.random.random(x.shape), "temp": 296
            },
            "A2": {
                "rowmin": 0, "rowmax": 50, "colmin": 50, "colmax": 100,
                "init_func": lambda x: 298 + np.random.random(x.shape), "temp": 296
            },
            "A3": {
                "rowmin": 0, "rowmax": 50, "colmin": 40, "colmax": 50,
                "init_func": lambda x: 297 + np.random.random(x.shape), "temp": 296
            },
            "A4": {
                "rowmin": 50, "rowmax": 90, "colmin": 0, "colmax": 100,
                "init_func": lambda x: 296 + np.random.random(x.shape), "temp": 296
            },
            "A5": {
                "rowmin": 90, "rowmax": 100, "colmin": 0, "colmax": 100,
                "init_func": lambda x: 286 + np.random.random(x.shape), "temp": 290
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
        "force_term": lambda x, t, mask: np.where(
            mask == 1, (np.sin(24*t/3600)**2 + 0)/10, np.where(
                mask == 2, (np.sin(24*t/3600)**2 + 4)/10, np.where(
                    mask == 3, (np.sin(24*t/3600)**2 + 4)/10, np.where(
                        mask == 4, (np.sin(24*t/3600)**2 + 4)/10, 0
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


