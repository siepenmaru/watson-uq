import overpy
import numpy as np

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
            coords = []
            node: overpy.Node
            for node in way.nodes:
                coords.append([node.lat, node.lon])
            coords = np.mean(coords, axis=0)

            buildings[way.tags["ref"]] = {"lat": coords[0], "lon": coords[1]}
            buildings[way.tags["ref"]].update(way.tags)

        else: continue

    return buildings