from manim import *

# ============================================================
# CONFIG YOU SHOULD EDIT
# ============================================================

N = 6

# Put YOUR 6 permutations here (each must be a list of length 6 containing 0..5 exactly once).
# Interpretation: in slice z, we infect (row r, col perm[r], z).
PERMS = [
    [0, 1, 2, 3, 4, 5],  # identity
    [1, 2, 3, 4, 5, 0],  # shift
    [2, 3, 4, 5, 0, 1],
    [3, 4, 5, 0, 1, 2],
    [4, 5, 0, 1, 2, 3],
    [5, 0, 1, 2, 3, 4],
]

# Infection rule in 3D: a cell infects if it has >= THRESHOLD infected orthogonal neighbors.
# If you want the exact same rule as your 2D videos, set THRESHOLD = 2.
THRESHOLD = 3

RUN_INFECTION = True   # set False if you only want the stacking + voxel reveal
MAX_GENERATIONS = 50   # safety cap


# ============================================================
# HELPERS
# ============================================================

def check_perm(p):
    return sorted(p) == list(range(N))

def grid_xy_point(r, c, spacing):
    """Map (row, col) to a point in the XY plane centered at origin."""
    x = (c - (N - 1) / 2) * spacing
    y = (r - (N - 1) / 2) * spacing
    return np.array([x, y, 0.0])

def cube_xyz_point(r, c, z, spacing):
    """Map (row, col, z) to a 3D point centered at origin."""
    x = (c - (N - 1) / 2) * spacing
    y = (r - (N - 1) / 2) * spacing
    zz = (z - (N - 1) / 2) * spacing
    return np.array([x, y, zz])

def neighbors_3d(cell):
    r, c, z = cell
    for dr, dc, dz in [(-1,0,0),(1,0,0),(0,-1,0),(0,1,0),(0,0,-1),(0,0,1)]:
        rr, cc, zz = r+dr, c+dc, z+dz
        if 0 <= rr < N and 0 <= cc < N and 0 <= zz < N:
            yield (rr, cc, zz)

def next_infections(infected):
    to_fill = set()
    for r in range(N):
        for c in range(N):
            for z in range(N):
                cell = (r, c, z)
                if cell in infected:
                    continue
                cnt = 0
                for nb in neighbors_3d(cell):
                    if nb in infected:
                        cnt += 1
                        if cnt >= THRESHOLD:
                            to_fill.add(cell)
                            break
    return to_fill

def make_slice_group(z, perm, square_size, spacing, show_grid=True):
    """
    Build a 2D slice: optional faint 6x6 grid + the 6 infected squares from the permutation.
    Returned group is in the XY plane (z=0 initially).
    """
    g = VGroup()
    grid_squares = VGroup()

    if show_grid:
        for r in range(N):
            for c in range(N):
                sq = Square(side_length=square_size)
                sq.set_stroke(WHITE, width=1)
                sq.set_fill(BLACK, opacity=0)
                sq.move_to(grid_xy_point(r, c, spacing))
                grid_squares.add(sq)
        grid_squares.set_opacity(0.45)
        g.add(grid_squares)

    infected_squares = []
    for r in range(N):
        c = perm[r]
        sq = Square(side_length=square_size)
        sq.set_stroke(WHITE, width=1.2)
        sq.set_fill(BLUE, opacity=0.9)
        sq.move_to(grid_xy_point(r, c, spacing))
        infected_squares.append(sq)
        g.add(sq)

    label = Text(f"z = {z}", font_size=28)
    label.next_to(g, DOWN, buff=0.25)
    g.add(label)

    return g, infected_squares, grid_squares, label


def make_voxel(cell, voxel_size, spacing, color=BLUE):
    r, c, z = cell
    cube = Cube(side_length=voxel_size)
    cube.set_fill(color, opacity=0.9)
    cube.set_stroke(WHITE, width=0.6)
    cube.move_to(cube_xyz_point(r, c, z, spacing))
    return cube


# ============================================================
# MAIN SCENE
# ============================================================

class PermutationSlicesToCube(ThreeDScene):
    def construct(self):
        # Validate perms
        assert len(PERMS) == N, f"Need exactly {N} permutations (one per z-slice)."
        for p in PERMS:
            assert check_perm(p), f"Invalid permutation: {p} (must be a rearrangement of 0..{N-1})"

        # Visual parameters
        spacing = 0.65          # distance between grid cell centers
        square_size = spacing * 0.86
        voxel_size = spacing * 0.86
        layer_gap = spacing     # z-gap between slices when stacked

        # Title (fixed in frame so it doesn't rotate away)
        title = Text("6 permutation slices → stacked into a 6×6×6 cube", font_size=34)
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(title), run_time=0.6)

        # Start in a straight-on view (like 2D)
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.15)

        # Build the 6 slice groups in a 2×3 layout (fits screen nicely)
        slice_groups = []
        slice_infected_squares = []  # list of lists
        slice_labels = []
        slice_grids = []

        for z in range(N):
            g, infected_sq, grid_sq, label = make_slice_group(
                z=z,
                perm=PERMS[z],
                square_size=square_size,
                spacing=spacing,
                show_grid=True
            )
            slice_groups.append(g)
            slice_infected_squares.append(infected_sq)
            slice_grids.append(grid_sq)
            slice_labels.append(label)

        layout = VGroup(*slice_groups).arrange_in_grid(rows=2, cols=3, buff=(1.0, 0.9))
        layout.next_to(title, DOWN, buff=0.55)
        layout.scale(0.85)

        self.play(FadeIn(layout), run_time=0.9)
        self.wait(0.8)

        # Move all slices to the same XY position and stack in depth (z direction)
        # Also remove the per-slice label after stacking (optional).
        stack_center = ORIGIN + DOWN * 0.25
        stack_anims = []
        for z, g in enumerate(slice_groups):
            target = stack_center + OUT * (z - (N - 1) / 2) * layer_gap
            stack_anims.append(g.animate.move_to(target))

        self.play(*stack_anims, run_time=1.8)
        self.wait(0.4)

        # Fade the slice labels a bit so cube view is cleaner
        self.play(*[lbl.animate.set_opacity(0.25) for lbl in slice_labels], run_time=0.6)

        # Now rotate camera to reveal 3D
        self.move_camera(phi=70 * DEGREES, theta=-40 * DEGREES, run_time=2.0)
        self.wait(0.2)

        # Add a faint wireframe bounding cube
        side = (N - 1) * spacing + voxel_size
        frame = Cube(side_length=side)
        frame.set_fill(opacity=0)
        frame.set_stroke(WHITE, width=1.2, opacity=0.35)
        frame.move_to(stack_center)
        self.play(FadeIn(frame), run_time=0.7)

        # Transform infected squares → voxels
        # We'll also fade the faint 2D grids away for clarity.
        infected_cells = set()
        square_to_voxel_anims = []
        voxel_mobjects = {}  # cell -> Cube

        for z in range(N):
            perm = PERMS[z]
            for r in range(N):
                c = perm[r]
                cell = (r, c, z)
                infected_cells.add(cell)

        # Build a mapping from each infected SQUARE object to its voxel
        # (We know there are 6 squares per slice, in row order.)
        for z in range(N):
            perm = PERMS[z]
            for idx_r, sq in enumerate(slice_infected_squares[z]):
                r = idx_r
                c = perm[r]
                cell = (r, c, z)
                voxel = make_voxel(cell, voxel_size, spacing, color=BLUE)
                voxel.move_to(cube_xyz_point(r, c, z, spacing) + (stack_center - ORIGIN))
                voxel_mobjects[cell] = voxel
                square_to_voxel_anims.append(ReplacementTransform(sq, voxel))

        # Fade grids (optional)
        fade_grids = []
        for z in range(N):
            if slice_grids[z] is not None:
                fade_grids.append(slice_grids[z].animate.set_opacity(0.08))

        self.play(*fade_grids, run_time=0.6)
        self.play(*square_to_voxel_anims, run_time=1.6)

        # You can remove the slice containers entirely now (keep voxels + frame)
        # (Labels were still inside slice_groups, so let's fade them out cleanly.)
        self.play(*[FadeOut(lbl) for lbl in slice_labels], run_time=0.7)
        self.wait(0.4)

        # Add a fixed-in-frame generation counter
        gen_text = Text("Generation: 0", font_size=28, color=YELLOW).to_corner(DR)
        self.add_fixed_in_frame_mobjects(gen_text)

        # Slow ambient rotation for a nice 3D feel
        self.begin_ambient_camera_rotation(rate=0.12)

        # Optionally run infection in full 6x6x6 cube
        if RUN_INFECTION:
            gen = 0
            while gen < MAX_GENERATIONS and len(infected_cells) < N**3:
                new_cells = next_infections(infected_cells)
                if not new_cells:
                    break
                gen += 1

                # Update counter
                new_gen_text = Text(f"Generation: {gen}", font_size=28, color=YELLOW).move_to(gen_text)
                self.play(Transform(gen_text, new_gen_text), run_time=0.25)

                # Animate newly infected voxels
                anims = []
                for cell in sorted(new_cells):
                    infected_cells.add(cell)
                    if cell not in voxel_mobjects:
                        voxel = make_voxel(cell, voxel_size, spacing, color=BLUE)
                        voxel.move_to(cube_xyz_point(*cell, spacing) + (stack_center - ORIGIN))
                        voxel_mobjects[cell] = voxel
                        anims.append(FadeIn(voxel, scale=0.85))
                    else:
                        anims.append(voxel_mobjects[cell].animate.set_fill(BLUE, opacity=0.9))

                # If too many at once, it can look chaotic; but N=6 is fine.
                self.play(*anims, run_time=0.45)
                self.wait(0.15)

            # Finish message
            if len(infected_cells) == N**3:
                done = Text("Cube fully infected!", font_size=32, color=GREEN).to_corner(DL)
            else:
                done = Text("Stopped (no more infections)", font_size=30, color=RED).to_corner(DL)

            self.add_fixed_in_frame_mobjects(done)
            self.play(FadeIn(done), run_time=0.6)
            self.wait(2.0)

        else:
            self.wait(2.5)
