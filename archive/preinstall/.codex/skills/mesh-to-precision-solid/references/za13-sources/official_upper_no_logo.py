"""SOURCE OF TRUTH: TEXT-TO-CAD. Smoothly fill the upper-shell logo only.

Millimetres, original assembly coordinates. Keep the exact pilot fit input,
inner shell, rims and mounting details. The isolated logo island is replaced
by the surrounding B-spline support surface, without adding a new seam.
"""
from pathlib import Path
import hashlib
from cadgen import step,build123d as bd

OUT=Path('V:/mouse/outputs/ZA13_UPPER_NO_LOGO_01')
SOURCE=Path('V:/mouse/outputs/ZA13_OFFICIAL_PRECISION_REPAIR_02/exact_boundary_66853.brep')
SOURCE_SHA256='fac7ad9170a468302b4d9f2a5ef4c11e06be62b28a201930d8c365226f8059bd'

@step(out='../outputs/ZA13_UPPER_NO_LOGO_01/ZA13_upper_no_logo.step')
def upper_no_logo():
    from official_upper_hybrid_rebuild import main
    with SOURCE.open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()==SOURCE_SHA256
    shape=bd.Solid(main(output_dir=OUT,remove_logo=True))
    shape.label='ZA13 upper shell - smooth no-logo';return shape

if __name__=='__main__':upper_no_logo()
