import numpy as np
import open3d as o3d
from open3d.visualization import RenderOption
import numpy as np
import math
import open3d.visualization.gui as gui
import open3d.visualization.rendering as rendering

def load_model(filename):
    vs = []
    fs = []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('#'): continue
            values = line.strip().split()
            if not values: continue
            if values[0] == 'v':
                vs.append([float(x) for x in values[1:4]])
            elif values[0] == 'f':
                xs = [int(x) - 1 for x in values[1:4]]
                fs.append(xs)
    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(np.asarray(vs))
    mesh.triangles = o3d.utility.Vector3iVector(np.asarray(fs))
    mesh.compute_vertex_normals()
    return mesh


def normals_lineset(pcd, normal_scale=0.002, color=[1, 0, 0]):
    # vertex_normals = np.asarray(mesh.vertex_normals)
    line_set = o3d.geometry.LineSet()
    start = np.asarray(pcd.points)
    end = np.asarray(pcd.points) + (np.asarray(mesh.vertex_normals) * normal_scale)
    points = np.concatenate((start, end))
    line_set.points = o3d.utility.Vector3dVector(points)
    size = len(start)
    line_set.lines = o3d.utility.Vector2iVector(np.asarray([[i, i + size] for i in range(0, size)]))
    line_set.paint_uniform_color(color)
    return line_set


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
    return math.sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2))


def getInstance(ray_origin, ray_dir, vs, idx):
    intersection = ray_triangle_intersection(ray_origin, ray_dir, vs[0], vs[1], vs[2])
    if intersection is not None:
        print("交点坐标:", idx, intersection)
        dlt = intersection - ray_origin
        dlt = distance(dlt)
        print('distance', dlt)
    else:
        pass


def rayMesh(ray_origin, ray_dir, mesh):
    triLen = len(mesh.triangles)
    for i in range(0, triLen):
        tringle = getTringle(mesh, i)
        getInstance(ray_origin, ray_dir, tringle, i)

# getInstance(ray_origin, ray_dir, [v0, v1, v2])

mesh = load_model('./fit_scan_result.obj')
mesh2 = load_model('./scan_scaled.obj')
vertices = np.asarray(mesh.vertices)
vertex_normals = np.asarray(mesh.vertex_normals)


def getTringle(mesh, idx):
    triangles = np.asarray(mesh.triangles)
    vertices = np.asarray(mesh.vertices)
    ary = triangles[idx]
    ret = np.asarray([vertices[ary[0]], vertices[ary[1]], vertices[ary[2]]])
    # print(ret)
    return ret

for i in range(0, 20):
    aPoint = vertices[2000+i]
    aNormal = vertex_normals[2000+i]
    rayMesh(aPoint, aNormal, mesh2)



mesh.paint_uniform_color([0.706, 0.706, 0.706])
mesh2.paint_uniform_color([0.706, 0.906, 0.706])

axis_aligned_bounding_box = mesh.get_axis_aligned_bounding_box()
axis_aligned_bounding_box.color = (1, 1, 0)
print(axis_aligned_bounding_box.max_bound - axis_aligned_bounding_box.min_bound)
# mesh.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

pts = np.asarray(mesh.vertices)
render_option = RenderOption()
render_option.background_color = [0.5, 0.5, 0.5]
render_option.point_show_normal = True
points = pts
ptLen = len(points)
colors = [[1, 1, 0] for i in range(0, ptLen)]
for i in range(2000, 2100):
    colors[i] = [1, 0, 0]
test_pcd = o3d.geometry.PointCloud()
test_pcd.points = o3d.utility.Vector3dVector(points)
test_pcd.colors = o3d.utility.Vector3dVector(colors)

normals = normals_lineset(test_pcd)

def visualize():
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name='32line Lidar', width=1080, height=720, left=300, top=150, visible=True)
    # vis.add_geometry(mesh)
    # vis.add_geometry(mesh2)
    vis.add_geometry(test_pcd)
    vis.add_geometry(normals)
    vis.get_render_option().point_size = 2  # 点云大小
    vis.get_render_option().background_color = np.asarray([0, 0, 0])  # 背景颜色
    vis.run()

def make_point_cloud(pts):
    cloud = o3d.geometry.PointCloud()
    cloud.points = o3d.utility.Vector3dVector(pts)
    colors = np.random.uniform(0.0, 1.0, size=[len(pts), 3])
    cloud.colors = o3d.utility.Vector3dVector(colors)
    return cloud

def high_level():
    app = gui.Application.instance
    app.initialize()

    points = make_point_cloud(pts)

    vis = o3d.visualization.O3DVisualizer("Open3D - 3D Text", 1024, 768)
    vis.show_settings = True
    vis.add_geometry("mesh", mesh)
    vis.add_geometry("pt", test_pcd)
    vis.add_geometry("normal", normals)
    # vis.add_geometry("Points", points)
    idx = 705
    # for idx in range(0, len(points.points)):
        # vis.add_3d_label(points.points[idx], "{}".format(idx))
    vis.add_3d_label(points.points[idx], "{}".format(idx))
    vis.reset_camera_to_default()

    app.add_window(vis)
    app.run()



# if __name__ == "__main__":
#     high_level()


if __name__ == "__main__":
    visualize()
