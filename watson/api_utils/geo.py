import overpy
import numpy as np
from decimal import Decimal
import pickle

def get_campus_buildings():
    # TODO: generate building coords and other info, store them onto database
    api = overpy.Overpass()

    query = '''
        area[name='The University of Queensland']->.uq;
        (
            way(area.uq)[building="university"];
            node(area.uq)[building="univeristy"];
            relation(area.uq)[building="university"];
        );
        (._;>;);
        out;
    '''

    out = api.query(query)

    buildings = {}
    way: overpy.Way
    for way in out.ways:
        # only include buildings with proper IDs
        if "ref" in way.tags:
            # get coordinate of center
            coords = get_center_coords(way)

            buildings[way.tags["ref"]] = {"lat": coords[0], "lon": coords[1]}
            buildings[way.tags["ref"]].update(way.tags)

        else: continue
    
    relation: overpy.Relation
    for relation in out.relations:
        if "ref" in relation:
            coords = get_relation_center(relation)

            buildings[relation.tags["ref"]] = {"lat": coords[0], "lon": coords[1]}
            buildings[relation.tags["ref"]].update(relation.tags)

    return buildings

def save_building_data():
    # hacky as heck, should probably use the DB for this.
    data = get_campus_buildings()

    with open('buildings.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

def get_center_coords(way: overpy.Way) -> tuple[Decimal, Decimal]:
    # get coordinate of center
    coords = []
    node: overpy.Node
    for node in way.nodes:
        coords.append([node.lat, node.lon])
    return np.mean(coords, axis=0)

def get_relation_center(relation: overpy.Relation) -> tuple[Decimal, Decimal]:
    centers = []
    for way in relation.members:
        centers.append(get_center_coords)
    return np.mean(centers, axis=0)