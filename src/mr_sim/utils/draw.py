from matplotlib.patches import Polygon as MatplotlibPolygon
from matplotlib.collections import PatchCollection
from shapely.geometry import Polygon, MultiPolygon, LineString, Point
import numpy as np

def draw_geometry(ax, geometry, **kwargs):

    color = kwargs.get('color', 'blue')
    alpha = kwargs.get('alpha', 0.6)
    edgecolor = kwargs.get('edgecolor', 'black')
    linewidth = kwargs.get('linewidth', 1)
   
    if geometry.geom_type == 'Polygon':
        x, y = geometry.exterior.xy
        coords = np.vstack((x, y)).T
        patch = MatplotlibPolygon(coords, closed=True, facecolor=color, 
                                   edgecolor=edgecolor, alpha=alpha, 
                                   linewidth=linewidth, zorder=kwargs.get('zorder', 1))
        return ax.add_patch(patch)

    elif geometry.geom_type == 'MultiPolygon':
        patches = []
        for poly in geometry.geoms:
            x, y = poly.exterior.xy
            coords = np.vstack((x, y)).T
            patches.append(MatplotlibPolygon(coords, closed=True))
        
        collection = PatchCollection(patches, facecolor=color, edgecolor=edgecolor, 
                                     alpha=alpha, linewidth=linewidth, zorder=kwargs.get('zorder', 1))
        return ax.add_collection(collection)

    elif geometry.geom_type == 'LineString':
        x, y = geometry.xy
        return ax.plot(x, y, color=color, alpha=alpha, linewidth=linewidth, 
                       zorder=kwargs.get('zorder', 2))

    elif geometry.geom_type == 'Point':
        return ax.scatter([geometry.x], [geometry.y], color=color, alpha=alpha, 
                          zorder=kwargs.get('zorder', 3))


def draw_heading(ax, pose, length=0.5, **kwargs):

    x, y, theta = pose
    dx = length * np.cos(theta)
    dy = length * np.sin(theta)
    
    arrow_params = {
        'width': kwargs.get('width', 0.05),       
        'head_width': kwargs.get('head_width', 0.2), 
        'head_length': kwargs.get('head_length', 0.2), 
        'fc': kwargs.get('color', 'red'),         
        'ec': kwargs.get('color', 'red'),         
        'zorder': kwargs.get('zorder', 10),       
        'length_includes_head': True              
    }
    
    arrow_params.update({k: v for k, v in kwargs.items() if k not in ['color', 'width']})

    return ax.arrow(x, y, dx, dy, **arrow_params)