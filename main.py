from assets import *
import numpy as np
from PIL import Image

ambient_power = 2
ambient = ambient_power * Vec3(1, 1, 1)

materials = {
    "metal": {"k_ambient": 0.1, "k_diffuse": 0.4, "k_specular": 0.6, "n_specular": 101.0},
    "drewno": {"k_ambient": 0.5, "k_diffuse": 0.6, "k_specular": 0.1, "n_specular": 11.0},
    "plastik": {"k_ambient": 0.45, "k_diffuse": 0.9, "k_specular": 0.2, "n_specular": 51.0},
    "tynk": {"k_ambient": 0.8, "k_diffuse": 0.9, "k_specular": 0.01, "n_specular": 26.0}
}


def render_pixel(x, y, camera, light, asset, mat):
    c = Vec3(0, 0, 0)
    ray = camera.shoot_ray(x, y)
    intersect, i = asset.intersect(ray)
    if intersect:
        n = asset.normal(i)
        l = light.pos - i
        r = normalize(2 * n - l)

        l_intensity = light.strength(i) * light.color
        i_ambient = mat["k_ambient"] * ambient
        i_diffuse = mat["k_diffuse"] * max(dot(n, normalize(l)), 0) * l_intensity
        i_specular = mat["k_specular"] * pow(max(dot(r, normalize(-1 * i)), 0), mat["n_specular"]) * l_intensity

        c = mul(asset.color, i_ambient + i_diffuse + i_specular)
    return [float2uint8(c.x), float2uint8(c.y), float2uint8(c.z)]


def main():
    res = 500
    camera = Camera((res, res))
    sphere = Sphere(pos=Vec3(0, 2, 0), radius=0.5, color=Vec3(0.5, 0.5, 0.5))
    spotlight_power = 3
    light = Light(pos=Vec3(1, 0.5, 1), color=Vec3(0.6, 0.6, 0.6), strength=spotlight_power, radius=1)

    asset = sphere

    for key in materials:
        data = np.zeros((camera.res_width, camera.res_width, 3), dtype=np.uint8)
        for x in range(camera.res_width):
            for y in range(camera.res_height):
                data[x, y] = render_pixel(x, y, camera, light, asset, materials[key])

        img = Image.fromarray(data)
        img.show(f"Materiał: {key.capitalize()}")
        img.save(f"images/{key}__ambient_{ambient_power}__spotlight_{spotlight_power}.png")
        print(f"Done: {key}")


if __name__ == "__main__":
    main()
