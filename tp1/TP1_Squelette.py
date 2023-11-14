import tkinter as tk
from tkinter import ttk
import csv
import random
from queue import Queue
from queue import LifoQueue
from queue import PriorityQueue
import math
import time


search_algorithms = ('Parcours en largeur', 'Parcours en profondeur', 'Parcours en profondeur itératif', 'Recherche à coût Uniforme', 'Recherche gloutonne', 'A*', "Distance à vol d'oiseau")
costs = ('distance', 'temps')

town_color = 'lightcoral'
road_color = 'lightgreen'
path_color = 'red'




class Town:

    def __init__(self, dept_id, name, latitude, longitude):
        self.dept_id = dept_id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.neighbours = dict()


class Road:

    def __init__(self, town1, town2, distance, time):
        self.town1 = town1
        self.town2 = town2
        self.distance = distance
        self.time = time

class Node:

    def __init__(self, state, parent, cost, depth, road_to_parent):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.depth = depth
        self.road_to_parent = road_to_parent
    
    def __lt__(self, other):
        return self.cost < other.cost
    
    def __eq__(self, other):
        return self.state == other.state

# Distance vol d'oiseau
def crowfliesdistance(town1, town2):
    # use orthodromic distance and latitude and longitude of the two towns
    
    # convert degrees to radians
    lat1 = math.radians(town1.latitude)
    lon1 = math.radians(town1.longitude)
    lat2 = math.radians(town2.latitude)
    lon2 = math.radians(town2.longitude)

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # calculate the result
    canvas1.create_line(longitude_to_pixel(town1.longitude), latitude_to_pixel(town1.latitude),
                        longitude_to_pixel(town2.longitude), latitude_to_pixel(town2.latitude), fill=path_color,
                        width=road_width)
    print("Distance à vol d'oiseau: ", c*r)
    

# A-Star
def a_star(start_town, end_town):
    # À remplir !
    return None

# Recherche gloutonne
def greedy_search(start_town, end_town):

    node = Node(state=start_town, parent=None, cost=0, depth=0, road_to_parent=None)
    frontier = PriorityQueue()
    frontier.put((node.cost, node))
    explored = set()

    while not frontier.empty():
        state = frontier.get()[1]
        explored.add(state.state)
        if state.state == end_town: return state
        for neighbour, road in state.state.neighbours.items():
            child = Node(state=neighbour, parent=state, cost=road.distance, depth=state.depth+1, road_to_parent=road)
            if child.state not in explored and child.state not in frontier.queue:
                frontier.put((child.cost, child))
            elif child.state in frontier.queue:
                for item in frontier.queue:
                    if item[1].state == child.state and item[1].cost > child.cost:
                        frontier.get(item)
                        frontier.put((child.cost, child))
    return None

# Parcours à coût uniforme
def ucs(start_town, end_town):
    
    node = Node(state=start_town, parent=None, cost=0, depth=0, road_to_parent=None)
    frontier = PriorityQueue()
    frontier.put((node.cost, node))
    explored = set()

    while True:
        if frontier.empty(): return "Failure"
        node = frontier.get()[1]
        if node.state == end_town: return node
        explored.add(node.state)
        for neighbour, road in node.state.neighbours.items():
            child = Node(state=neighbour, parent=node, cost=node.cost+road.distance, depth=node.depth+1, road_to_parent=road)
            if child.state not in explored and child.state not in frontier.queue:
                frontier.put((child.cost, child))
            elif child.state in frontier.queue:
                for item in frontier.queue:
                    if item[1].state == child.state and item[1].cost > child.cost:
                        frontier.get(item)
                        frontier.put((child.cost, child))

# Parcours en profondeur itératif
def dfs_iter(start_town, end_town):
    # À remplir !
    return None

# Parcours en profondeur
def dfs(start_town, end_town):
    
    node = Node(state=start_town, parent=None, cost=0, depth=0, road_to_parent=None)
    explored = LifoQueue()
    explored.put(node.state)
    return dfs_recursive(node=node, end_town=end_town, explored=explored, limit=200000)

def dfs_recursive(node, end_town, explored, limit):
    if node.state == end_town: return node
    if limit == 0: return "cutoff"
    cutoff_occurred = False
    for neighbour, road in node.state.neighbours.items():
        if neighbour not in explored.queue:
            child = Node(state=neighbour, parent=node, cost=node.cost+road.distance, depth=node.depth+1, road_to_parent=road)
            explored.put(neighbour)
            result = dfs_recursive(child, end_town, explored, limit)
            if result == "cutoff": cutoff_occurred = True
            elif result != "failure": return result
    if cutoff_occurred: return "cutoff"
    return "failure"

# Parcours en largeur
def bfs(start_town, end_town):

    node = Node(state=start_town, parent=None, cost=0, depth=0, road_to_parent=None)
    if end_town == node.state: return node

    frontier = Queue()
    frontier.put(node)
    explored = set()

    while True:
        if frontier.empty(): return None
        node = frontier.get()
        explored.add(node.state)
        for neighbour, road in node.state.neighbours.items():
            child = Node(state=neighbour, parent=node, cost=node.cost+road.distance, depth=node.depth+1, road_to_parent=road)
            if child.state not in explored and child.state not in frontier.queue:
                if child.state == end_town: return child
                frontier.put(child)

def display_path(path):
    current_node = path
    while current_node.parent is not None:
        canvas1.itemconfig(road_lines[current_node.road_to_parent], fill=path_color)
        print(current_node.road_to_parent.town1.name, current_node.road_to_parent.town2.name)
        current_node = current_node.parent


def run_search():
    button_run['state'] = tk.DISABLED
    # put all the roads in normal
    for road in roads:
        canvas1.itemconfig(road_lines[road], fill=road_color)
    start_city = towns[combobox_start.current() + 1]
    end_city = towns[combobox_end.current() + 1]
    search_method = combobox_algorithm.current()
    cost = combobox_cost.current()
    computing_time = time.time()
    if search_method == 0:  # Parcours en largeur
        path = bfs(start_city, end_city)
    elif search_method == 1:  # Parcours en profondeur
        path = dfs(start_city, end_city)
    elif search_method == 2:  # Parcours en profondeur itératif
        path = dfs_iter(start_city, end_city)
    elif search_method == 3:  # Parcours à coût uniforme
        path = ucs(start_city, end_city)
    elif search_method == 4:  # Recherche gloutonne
        path = greedy_search(start_city, end_city)
    elif search_method == 5:  # A*
        path = a_star(start_city, end_city)
    elif search_method == 6:  # Crowflies
        path = crowfliesdistance(start_city, end_city)
    else:
        path = None
    computing_time = time.time() - computing_time
    if path is not None:
        label_path_title['text'] = "Itinéraire de "+start_city.name+" à "+end_city.name+" avec "+search_algorithms[search_method]
        label_distance['text'] = "Distance: "+str(path.cost)+"km"
        label_computing_time['text'] = "Temps de calcul: "+str(computing_time)+"s"
        display_path(path)
    button_run['state'] = tk.NORMAL


def longitude_to_pixel(longitude):
    return (longitude-map_W) * diff_W_E

def latitude_to_pixel(latitude):
    return (map_N - latitude) * diff_N_S


# Read towns and roads csv and create relative objects
towns = dict()
roads = list()
with open('data/towns.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        towns[int(row['dept_id'])] = Town(dept_id=int(row['dept_id']), name=row['name'], latitude=float(row['latitude']), longitude=float(row['longitude']))
with open('data/roads.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        road = Road(town1=towns[int(row['town1'])], town2=towns[int(row['town2'])], distance=int(row['distance']), time=int(row['time']))
        roads.append(road)
        road.town1.neighbours[road.town2] = road
        road.town2.neighbours[road.town1] = road


window = tk.Tk()
window.title("Itineria")

# Décommenter la carte pour choisir la bonne taille pour votre machine
# map_image = tk.PhotoImage(file="img/France_map_admin_1066_1024.png")
map_image = tk.PhotoImage(file="img/France_map_admin_799_768.png")
# map_image = tk.PhotoImage(file="img/France_map_admin_499_480.png")



width = map_image.width()
height = map_image.height()
canvas1 = tk.Canvas(window, width=width, height=height)

background_map = canvas1.create_image(0, 0, anchor=tk.NW, image=map_image)

# Dessin des routes et villes
map_N = 51.5
map_S = 41
map_W = -5.8
map_E = 10
diff_W_E = width / (map_E - map_W)
diff_N_S = height / (map_N - map_S)
town_radius = 4
road_width = 3

road_lines = dict()
for road in roads:
    road_lines[road] = canvas1.create_line(longitude_to_pixel(road.town1.longitude), latitude_to_pixel(road.town1.latitude),
                        longitude_to_pixel(road.town2.longitude), latitude_to_pixel(road.town2.latitude), fill=road_color,
                        width=road_width)

for town in towns.values():
    canvas1.create_oval(longitude_to_pixel(town.longitude) - town_radius, latitude_to_pixel(town.latitude) - town_radius,
                        longitude_to_pixel(town.longitude) + town_radius, latitude_to_pixel(town.latitude) + town_radius,
                        fill=town_color)


canvas1.grid(row=0, column=0, columnspan=4)
label_start = tk.Label(window, text="Départ")
label_start.grid(row=1, column=0)
combobox_start = ttk.Combobox(window, state='readonly')
combobox_start.grid(row=1, column=1)

label_end = tk.Label(window, text="Arrivée")
label_end.grid(row=1, column=2)
combobox_end = ttk.Combobox(window, state='readonly')
combobox_end.grid(row=1, column=3)

town_list = []
for town in towns.values():
    town_list.append(str(town.dept_id)+" - "+town.name)
combobox_start['values'] = town_list
combobox_end['values'] = town_list
combobox_start.current(random.randint(0, len(town_list)-1))
combobox_end.current(random.randint(0, len(town_list)-1))

label_algorithm = tk.Label(window, text="Algorithme")
label_algorithm.grid(row=2, column=0)
combobox_algorithm = ttk.Combobox(window, state='readonly')
combobox_algorithm.grid(row=2, column=1)
combobox_algorithm['values'] = search_algorithms
combobox_algorithm.current(random.randint(0, len(combobox_algorithm['values'])-1))

label_cost = tk.Label(window, text="Coût")
label_cost.grid(row=2, column=2)
combobox_cost = ttk.Combobox(window, state='readonly')
combobox_cost.grid(row=2, column=3)
combobox_cost['values'] = costs
combobox_cost.current(random.randint(0, len(combobox_cost['values']) - 1))

label_path_title = tk.Label(window, text="")
label_path_title.grid(row=3, column=0, columnspan=4)

label_distance = tk.Label(window, text="")
label_distance.grid(row=4, column=0)

label_computing_time = tk.Label(window, text="")
label_computing_time.grid(row=4, column=3)

button_run = tk.Button(window, text='Calculer', command=run_search)
button_run.grid(row=5, column=0)

button_quit = tk.Button(window, text='Quitter', command=window.destroy)
button_quit.grid(row=5, column=3)
window.mainloop()
