import json

import numpy as np
from PIL import Image
from pydantic import BaseModel, validator


class BasinParams(BaseModel):
    imw: int | None = 32
    imh: int | None = 32
    coefs: list[float] | str | None = [1, 0, 0, 0, 0, 0, 1]
    crmin: float | None = -5.0
    crmax: float | None = 5.0
    cimin: float | None = -5.0
    cimax: float | None = 5.0
    itmax: int | None = 30
    tol: float | None = 1e-6

    @validator("coefs")
    def coefs_list_or_str(cls, v):
        if isinstance(v, str):
            ret = json.loads(v)
        elif isinstance(v, list):
            ret = v
        else:
            raise ValueError(
                "BasinParams.coefs must be list of numbers or a json valid"
            )
        return ret


class BasinGenerator:

    params: BasinParams
    rgb_im: Image

    def __init__(self, params: BasinParams):
        self.params = params

    def __iter__(self):
        p = self.params
        total = p.imw * p.imh
        progress = 0
        roots = np.roots(p.coefs)
        hsv = np.zeros((p.imh, p.imw, 3), dtype=np.float32)
        for idx, _ in np.ndenumerate(hsv[:, :, 0]):
            y, x = idx
            r = p.crmin + (p.crmax - p.crmin) / p.imw * x
            i = p.cimax - (p.cimax - p.cimin) / p.imh * y
            z = complex(r, i)
            k = 0
            f = np.polyval(p.coefs, z)
            while k < p.itmax:
                df = np.polyval(np.polyder(p.coefs), z)
                if df != 0.0:
                    z = z - f / df
                    f = np.polyval(p.coefs, z)
                    if np.absolute(f) <= p.tol:
                        root = np.abs(roots - z).argmin()
                        h, s, v = root / roots.size, 1, 1 - k / p.itmax
                        hsv[y, x] = np.asarray([h, s, v])
                        break
                k += 1
            progress += 1
            yield (progress, total)

        hsv_int = (hsv * 255).astype(np.uint8)
        hsv_im = Image.fromarray(hsv_int, mode="HSV")
        self.rgb_im = hsv_im.convert("RGB")

    def pct_gen(self, step_threshold: int = 10):
        step_threshold = max(min(100, step_threshold), 1)  # clamp
        th = 0
        for (p, t) in self:
            pct = int(p * 100 / t)
            if pct >= th:
                yield pct
                th += step_threshold

    def export_png(self, file="out.png"):
        if not self.rgb_im:
            raise ValueError(
                "Image was not generated. Did you forget to run the computation?"
            )
        self.rgb_im.save(file, "PNG")


if __name__ == "__main__":
    basin_gen = BasinGenerator(
        params=BasinParams(imw=201, imh=201, coefs="[-1, 1, -1, 1, -1, 1, -1, 1]")
    )
    for pct in basin_gen.pct_gen(step_threshold=10):
        print(pct)
    basin_gen.export_png()
