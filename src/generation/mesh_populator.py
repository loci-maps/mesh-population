import os
import sys
import pathlib

import geopandas as gpd
import numpy as np
import pyvista as pv

from enum import Enum

weather = ['sunny', 'snowy', 'windy', 'rainy', 'overcast']
class weather(Enum):
    SUNNY = 0,
    SNOWY = 1,
    WINDY = 2,
    RAINY = 3,
    OVERCAST = 4,

biome = ['aquatic', 'forest', 'grassland', 'desert', 'tundra']
class biome(Enum):
    AQUATIC = 0,
    FOREST = 1,
    GRASSLAND = 2,
    DESERT = 3,
    TUNDRA = 4,

def get_segment():
    """ Gets a segment of the mesh """
	
    return

def gdf_to_mesh(mesh_fpath):
	gdf = gpd.read_file(mesh_fpath)
	vertices = []
	faces = []
	poly_ids = []

	for index, row in gdf.iterrows():
		polygon = row['geometry']
		if not polygon.is_valid:
			continue 

		exterior = np.array(polygon.exterior.coords)
		exterior_3d = np.hstack([exterior, np.zeros((len(exterior), 1))])  # Add z-coordinate of zero
		vertices.append(exterior_3d)

		face = np.arange(len(exterior), dtype=np.int64) + len(np.vstack(vertices)[:-len(exterior)])
		faces.append(face)

		# Assign an ID to each polygon
		poly_ids.extend([index] * len(face))
		
	# Combine vertices and face connectivity lists
	vertices = np.vstack(vertices)
	faces = np.hstack([np.hstack([[len(face)], face]) for face in faces])

	mesh = pv.PolyData(vertices, faces)

	# Add polygon IDs as a scalar array
	mesh["PolyIDs"] = np.array(poly_ids) 
	return mesh

# Debug/Sample Code: displays multiple objects on a flat mesh
def debug_place_objs():
	objs = [
		'tetrahedron',
		'cube',
		'octahedron',
		'dodecahedron',
		'icosahedron',
	]
	centers = [
		(0, 1, 0),
		(0, 0, 0),
		(0, 2, 0),
		(-1, 0, 0),
		(-1, 2, 0),
	]
	colors = [
		'red',
		'silver',
		'white',
		'blue',
		'gray',
	]
	
	solids = [pv.PlatonicSolid(obj, radius=0.4, center=center) for obj, center in zip(objs, centers)]
	
	p = pv.Plotter(window_size=[1000, 1000])
	for ind, solid in enumerate(solids):
		p.add_mesh(
			solid, color=colors[ind], specular=1.0, specular_power=10
		)
	p.view_vector((5.0, 2, 3))
	p.add_floor('-z', lighting=True, color='tan', pad=1.0)
	p.enable_shadows()
	p.show()

if __name__ == "__main__":
	# DEBUG USAGE
	# debug_place_objs()

	triangles_fname = ""
	if os.uname().sysname == "Windows":
		triangles_fname = f"{pathlib.Path(__file__).parent.absolute()}\\..\\..\\assets\\triangles.geojson"
	else:
		triangles_fname = f"{pathlib.Path(__file__).parent.absolute()}/../../assets/triangles.geojson"
	
	mesh = gdf_to_mesh(triangles_fname)
	

	sys.exit()