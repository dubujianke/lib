import numpy as np
import open3d as o3d

import numpy as np
import math
def ray_triangle_intersection(ray_origin, ray_dir, v0, v1, v2):
    # 计算平面法向量
    N = np.cross(v1 - v0, v2 - v0)
    denom = np.dot(ray_dir, N)
    if np.abs(denom) < 1e-6:
        return None  # 光线与平面平行

    # 计算t参数
    t = np.dot(v0 - ray_origin, N) / denom
    if t < 0:
        return None  # 交点在光线起点的反方向

    # 计算交点
    P = ray_origin + t * ray_dir

    # 使用重心坐标法判断P是否在三角形内
    u = v1 - v0
    v = v2 - v0
    w = P - v0

    denom = np.dot(u, u) * np.dot(v, v) - np.dot(u, v) ** 2
    if denom == 0:
        return None  # 三角形退化

    s = (np.dot(u, u) * np.dot(w, v) - np.dot(u, v) * np.dot(w, u)) / denom
    t_param = (np.dot(v, v) * np.dot(w, u) - np.dot(u, v) * np.dot(w, v)) / denom

    if (s >= 0) and (t_param >= 0) and (s + t_param <= 1):
        return P  # 交点在三角形内部
    else:
        return None  # 交点在三角形外部

# 示例使用
ray_origin = np.array([0.0, 0.0, 0.0])
ray_dir = np.array([0.0, 0.0, 1.0])
v0 = np.array([1.0, 1.0, 5.0])
v1 = np.array([-1.0, 1.0, 5.0])
v2 = np.array([0.0, -1.0, 5.0])

def distance(dir):
    x = dir[0]
    y = dir[1]
    z = dir[2]
    return math.sqrt(pow(x,2)+pow(y,2)+pow(z,2))
def getInstance(ray_origin, ray_dir, vs):
    intersection = ray_triangle_intersection(ray_origin, ray_dir, vs[0], vs[1], vs[2])
    if intersection is not None:
        print("交点坐标:", intersection)
        dlt = intersection - ray_origin
        dlt = distance(dlt)
        print(dlt)
    else:
        print("没有交点或交点不在三角形内部")
getInstance(ray_origin, ray_dir, [v0, v1, v2])

def show(path_obj):
    mesh = o3d.io.read_triangle_mesh(path_obj, enable_post_processing=True)
    # print(np.asarray(mesh.vertices))
    mesh.compute_vertex_normals()
    return mesh


mesh = show('./fit_scan_result.obj')
mesh2 = show('./scan_scaled.obj')
vertices = np.asarray(mesh.vertices)
triangles = np.asarray(mesh.triangles)

def getTringle(idx):
    ary = triangles[idx]
    ret = np.asarray([vertices[ary[0]], vertices[ary[1]], vertices[ary[2]]])
    print(ret)

# def getTringles(idxs):
#     ary = mesh.triangles[idx]
#     ret = np.asarray([vertices[ary[0]], vertices[ary[1]], vertices[ary[2]]])
#     print(ret)

getTringle(0)

print('Vertices:')
print(np.asarray(mesh.vertices[0]))
print(np.asarray(mesh.triangle_normals[0]))
print('Triangles:')
print(np.asarray(mesh.triangles[0]))

mesh.paint_uniform_color([1, 0.706, 0])

mesh2Out= mesh2.filter_smooth_simple()
# mesh2Out.compute_vertex_normals()
mesh2Out.paint_uniform_color([1, 0.706, 0])
axis_aligned_bounding_box = mesh2.get_axis_aligned_bounding_box()
axis_aligned_bounding_box.color = (1, 0, 0)
print(axis_aligned_bounding_box.max_bound - axis_aligned_bounding_box.min_bound)
# mesh.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
o3d.visualization.draw_geometries([mesh, mesh2], point_show_normal=True)

