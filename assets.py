import math


class Vec3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "({} {} {})".format(self.x, self.y, self.z)

    def __eq__(self, other):
        return (self.x == other.x) & (self.y == other.y) & (self.z == other.z)

    def __add__(self, other):
        out = Vec3()
        out.x = self.x + other.x
        out.y = self.y + other.y
        out.z = self.z + other.z
        return out

    def __sub__(self, other):
        out = Vec3()
        out.x = self.x - other.x
        out.y = self.y - other.y
        out.z = self.z - other.z
        return out

    def __mul__(self, other):
        out = Vec3()
        out.x = self.x * other
        out.y = self.y * other
        out.z = self.z * other
        return out

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        out = Vec3()
        out.x = self.x / other
        out.y = self.y / other
        out.z = self.z / other
        return out


class Ray:
    def __init__(self, o, d):
        self.o = o
        self.d = normalize(d)


class Light:
    def __init__(self, pos=Vec3(0, 0, 0), color=Vec3(1, 1, 1), strength=1, radius=10):
        self.pos = pos
        self.color = color
        self._strength = strength
        self.radius = radius

    def strength(self, point):
        dist = norm(self.pos - point)
        out = self._strength * min(self.radius * self.radius / (dist * dist), 1)
        return out


class Sphere:

    def __init__(self, pos, radius, color=Vec3(1, 0, 0)):
        self.pos = pos
        self.radius = radius
        self.color = color

    def normal(self, v):
        return normalize(v - self.pos)

    def intersect(self, ray):
        cam_sphere = self.pos - ray.o
        angle_ray_sphere = math.acos(dot(ray.d, cam_sphere) / norm(cam_sphere))
        dist_ray_sphere = math.sin(angle_ray_sphere) * norm(cam_sphere)
        if dist_ray_sphere <= self.radius:
            dist_cam_sphere = norm(cam_sphere)
            dist_ray_intersection = math.sqrt(
                dist_cam_sphere * dist_cam_sphere - dist_ray_sphere * dist_ray_sphere) - math.sqrt(
                self.radius * self.radius - dist_ray_sphere * dist_ray_sphere)
            i_point = ray.o + dist_ray_intersection * ray.d
            return True, i_point
        return False, None


class Camera:

    def __init__(self, res):
        self.res_width = res[0]
        self.res_height = res[1]
        self.width = 1
        self.height = 1
        self.focal = 1

    def camera_to_world(self, i, j):
        x = i * self.width / self.res_width - self.width / 2
        z = j * self.height / self.res_height - self.height / 2
        return x, z

    def shoot_ray(self, i, j):
        x, z = self.camera_to_world(i, j)
        ray = Ray(Vec3(0, 0, 0), Vec3(z, self.focal, -x))
        return ray


def norm(v):
    return math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z)


def normalize(u):
    if norm(u) == 0:
        return 0
    return u / norm(u)


def cross(u, v):
    out = Vec3()
    out.x = u.y * v.z - v.y * u.z
    out.y = u.z * v.x - v.z * u.x
    out.z = u.x * v.y - v.x * u.y
    return out


def dot(u, v):
    return u.x * v.x + u.y * v.y + u.z * v.z


def mul(u, v):
    out = Vec3()
    out.x = u.x * v.x
    out.y = u.y * v.y
    out.z = u.z * v.z
    return out


def float2uint8(value):
    return int(max(0, min(value * 255, 255)))
