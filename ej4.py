from copy import deepcopy
from aima.search import *
from copy import deepcopy

## grados.py
import csv
import sys
from collections import *



# diccionario de nombres de personas con ids
names = {}
# diccionario: name, birth, movies (conjunto de movie_ids)
people = {}
# movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Cargamos el archivo people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # cargamos el archivo movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # cargamos el archivo stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Para ejecutarlo en línea de comandos: python grados.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Cargando los datos...")
    load_data(directory)
    print("Datos cargados.")

    source = person_id_for_name(input("Nombre: "))
    if source is None:
        sys.exit("Esa persona no se encuentra.")
    target = person_id_for_name(input("Nombre: "))
    if target is None:
        sys.exit("Esa persona no se encuentra.")

    path = shortest_path(source, target)

    if path is None:
        print("No están conectados.")
    else:
        degrees = len(path) -1
        print(f"{degrees} grados de separacion.")
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} y {person2} participaron en {movie}")


def shortest_path(source, target):
    """
    Devuelve la lista de pares (movie_id, person_id) que conectan source y target o None si hay conexion.
    """
    camino = list()
    person_id = source
    node = Node(("", person_id))
    node2=None
    dest_id = target
    frontier = deque([node])
    explored = set()
    encontrado = False
    nodoFinal = None
    while frontier and encontrado==False:
        node = frontier.popleft()
        explored.add(node.state)
        for (movie_id, person_id) in neighbors_for_person(node.state[1]):
            node2 = Node((movie_id, person_id), node)
            if node2.state not in explored and node2.state not in frontier:
                if person_id == dest_id:
                    encontrado = True
                    nodoFinal = node2
                    break
                frontier.append(node2)

    node, path_back = nodoFinal, []
    while node:
        path_back.append(node.state)
        node = node.parent
    camino= list(reversed(path_back))
    return camino

    # TODO
    raise NotImplementedError


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    print("Grados.py")
    main()
    #p = CruzarPuente()



