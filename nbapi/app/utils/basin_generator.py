import json
from typing import Optional, Union
from enum import Enum
from timeit import default_timer as timer

import numpy as np
from PIL import Image
from pydantic import BaseModel, validator

from numba import jit, njit, prange


@jit
def polyval(p, x):
    y: float = 0.0
    for i, v in enumerate(p):
        y *= x
        y += v
    return y


@jit
def polyder(p):
    n = len(p)
    derivative = np.zeros(n - 1)
    for i in range(n - 1):
        derivative[i] = (n - 1 - i) * p[i]
    return derivative


@jit(parallel=True)
def basin(
    imw=31,
    imh=31,
    coefs=[1, 0, 0, 0, 0, 0, 1],
    crmin=-5.0,
    crmax=5.0,
    cimin=-5.0,
    cimax=5.0,
    itmax=30,
    tol=1e-6,
    roots=None,
):
    hsv_array = np.zeros((imh, imw, 3), dtype=np.float32)
    for x in prange(imw):
        for y in prange(imh):
            r = crmin + (crmax - crmin) / imw * x
            i = cimax - (cimax - cimin) / imh * y
            z = complex(r, i)
            k = 0
            while k < itmax:
                f = polyval(coefs, z)
                d = polyder(coefs)
                df = polyval(d, z)
                if df != 0.0:
                    z = z - f / df
                    f_curr = polyval(coefs, z)
                    if np.absolute(f_curr) <= tol:
                        root = np.abs(roots - z).argmin()
                        h = root / roots.size
                        s = 1
                        v = 1 - k / itmax
                        hsv_array[y, x] = np.asarray([h, s, v])
                        break
                k += 1
    return hsv_array


class Implementation(str, Enum):
    PYTHON = "python"
    NUMBA = "numba"


class BasinParams(BaseModel):
    imw: Optional[int] = 32
    imh: Optional[int] = 32
    coefs: Optional[Union[list[float], str]] = [1, 0, 0, 0, 0, 0, 1]
    crmin: Optional[float] = -5.0
    crmax: Optional[float] = 5.0
    cimin: Optional[float] = -5.0
    cimax: Optional[float] = 5.0
    itmax: Optional[int] = 30
    tol: Optional[float] = 1e-6
    implementation: Optional[Implementation] = Implementation.NUMBA

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
        self.impl = {
            Implementation.PYTHON: self.python_impl,
            Implementation.NUMBA: self.numba_impl,
        }

    def __iter__(self):
        return self.impl[self.params.implementation]()

    def python_impl(self):

        def polyval(p, x):
            y: float = 0.0
            for i, v in enumerate(p):
                y *= x
                y += v
            return y

        def polyder(p):
            n = len(p)
            derivative = np.zeros(n - 1)
            for i in range(n - 1):
                derivative[i] = (n - 1 - i) * p[i]
            return derivative

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
            f = polyval(p.coefs, z)
            while k < p.itmax:
                df = polyval(polyder(p.coefs), z)
                if df != 0.0:
                    z = z - f / df
                    f = polyval(p.coefs, z)
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

    def numba_impl(self):
        p = self.params
        total = p.imw * p.imh
        hsv = basin(
            imw=p.imw,
            imh=p.imh,
            coefs=np.array(p.coefs),
            crmin=p.crmin,
            crmax=p.crmax,
            cimin=p.cimin,
            cimax=p.cimax,
            itmax=p.itmax,
            tol=p.tol,
            roots=np.roots(p.coefs),
        )

        hsv_int = (hsv * 255).astype(np.uint8)
        hsv_im = Image.fromarray(hsv_int, mode="HSV")
        self.rgb_im = hsv_im.convert("RGB")

        yield (total, total)

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

    print("First")
    s1 = timer()
    basin_gen1 = BasinGenerator(
        params=BasinParams(
            imw=20,
            imh=20,
            coefs="[1, 0, 0, 0, 0, 0, 1]",
            implementation=Implementation.PYTHON,
        )
    )
    for pct in basin_gen1.pct_gen(step_threshold=100):
        print(pct)

    e1 = timer()
    print(f"{e1 - s1}")

    print("Second")
    s2 = timer()
    basin_gen2 = BasinGenerator(
        params=BasinParams(
            imw=256,
            imh=256,
            coefs="[1, 0, 0, 0, 0, 0, 1]",
            implementation=Implementation.NUMBA,
        )
    )
    for pct in basin_gen2.pct_gen(step_threshold=100):
        print(pct)

    e2 = timer()
    print(f"{e2 - s2}")
    basin_gen2.export_png()
