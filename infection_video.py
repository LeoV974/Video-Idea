from manim import *

# ---------------------------
# Helpers
# ---------------------------

def make_grid(grid_size, square_size, stroke_width=1.5, y_shift=0.0):
    """Return (grid VGroup, squares dict[(r,c)->Square])."""
    grid = VGroup()
    squares = {}
    for r in range(grid_size):
        for c in range(grid_size):
            sq = Square(side_length=square_size)
            sq.set_stroke(WHITE, width=stroke_width)
            sq.set_fill(BLACK, opacity=0)

            x = (c - grid_size / 2 + 0.5) * square_size
            y = (r - grid_size / 2 + 0.5) * square_size + y_shift
            sq.move_to([x, y, 0])

            grid.add(sq)
            squares[(r, c)] = sq
    return grid, squares


def seed_from_diagonals(diagonals, grid_size):
    """
    Encoding:
      (start_row, start_col, length) uses direction = +1
      (start_row, start_col, length, direction) with direction in {+1, -1}

    We always do: (row, col) = (start_row + i*direction, start_col + i)
    """
    filled = set()
    for info in diagonals:
        if len(info) == 4:
            start_r, start_c, length, direction = info
        else:
            start_r, start_c, length = info
            direction = 1

        for i in range(length):
            r = start_r + i * direction
            c = start_c + i
            if 0 <= r < grid_size and 0 <= c < grid_size:
                filled.add((r, c))
    return filled


def get_neighbors(pos, grid_size):
    r, c = pos
    out = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        rr, cc = r + dr, c + dc
        if 0 <= rr < grid_size and 0 <= cc < grid_size:
            out.append((rr, cc))
    return out


def find_next_to_fill(filled, grid_size):
    to_fill = []
    for r in range(grid_size):
        for c in range(grid_size):
            if (r, c) in filled:
                continue
            count = 0
            for nb in get_neighbors((r, c), grid_size):
                if nb in filled:
                    count += 1
                if count >= 2:
                    to_fill.append((r, c))
                    break
    return to_fill


# ---------------------------
# Scenes
# ---------------------------

class InfectionProblem(Scene):
    def construct(self):
        title = Text("The Infection Spread Problem", font_size=48)
        self.play(Write(title))
        self.wait(1.6)
        self.play(FadeOut(title))

        problem = VGroup(
            Text("Problem: People stand in an n×n grid", font_size=36),
            Text("Rule: You get infected if 2+ neighbors are infected", font_size=32),
            Text("Question: How many people need to start infected", font_size=32),
            Text("for the infection to spread to everyone?", font_size=32),
        ).arrange(DOWN, buff=0.35)

        for i, line in enumerate(problem):
            self.play(Write(line), run_time=0.8)
            self.wait(0.5 if i < 2 else 0.3)

        self.wait(1.6)
        self.play(FadeOut(problem))


class PerimeterInvariance(Scene):
    def construct(self):
        title = Text("Key Insight: Perimeter Never Increases", font_size=42)
        self.play(Write(title))
        self.wait(1.2)
        self.play(title.animate.to_edge(UP))

        # 4x4 grid, centered nicely under title
        grid_size = 4
        square_size = 1.0
        grid, squares = make_grid(grid_size, square_size, stroke_width=2.0, y_shift=-0.4)

        self.play(Create(grid))
        self.wait(0.6)

        # Start with TWO DIAGONAL squares IN THE CENTER:
        # (1,1) and (2,2) are central for a 4x4.
        filled = {(1, 1), (2, 2)}

        self.play(
            squares[(1, 1)].animate.set_fill(RED, opacity=0.85),
            squares[(2, 2)].animate.set_fill(RED, opacity=0.85),
            run_time=0.8
        )
        self.wait(0.6)

        def highlight_perimeter(filled_set, color=YELLOW):
            perimeter_edges = []
            for row, col in filled_set:
                sq = squares[(row, col)]
                # Top edge
                if (row + 1, col) not in filled_set:
                    perimeter_edges.append(Line(sq.get_corner(UL), sq.get_corner(UR), color=color, stroke_width=6))
                # Bottom edge
                if (row - 1, col) not in filled_set:
                    perimeter_edges.append(Line(sq.get_corner(DL), sq.get_corner(DR), color=color, stroke_width=6))
                # Left edge
                if (row, col - 1) not in filled_set:
                    perimeter_edges.append(Line(sq.get_corner(DL), sq.get_corner(UL), color=color, stroke_width=6))
                # Right edge
                if (row, col + 1) not in filled_set:
                    perimeter_edges.append(Line(sq.get_corner(DR), sq.get_corner(UR), color=color, stroke_width=6))
            return VGroup(*perimeter_edges)

        perimeter = highlight_perimeter(filled)
        perimeter_text = Text("Perimeter = 8", font_size=28).to_edge(DOWN)
        self.play(Create(perimeter), Write(perimeter_text))
        self.wait(1.2)

        explanation = Text("Add a square with 2 infected neighbors…", font_size=24)
        explanation.next_to(perimeter_text, UP, buff=0.25)
        self.play(Write(explanation))
        self.wait(0.6)

        # Add (1,2): it is orthogonally adjacent to BOTH (1,1) and (2,2)
        new_square = (1, 2)
        filled.add(new_square)

        new_perimeter = highlight_perimeter(filled)
        new_text = Text("Perimeter = 8 (stays the same!)", font_size=28).to_edge(DOWN)

        self.play(
            squares[new_square].animate.set_fill(RED, opacity=0.85),
            Transform(perimeter, new_perimeter),
            Transform(perimeter_text, new_text),
            run_time=1.1
        )
        self.wait(1.5)

        self.play(FadeOut(explanation))

        key_property = VGroup(
            Text("Rule of thumb:", font_size=36, color=YELLOW),
            Text("Infection can only keep or reduce perimeter.", font_size=30),
            Text("So you must START with enough perimeter.", font_size=30),
        ).arrange(DOWN, buff=0.25).shift(DOWN * 0.4)

        self.play(
            FadeOut(grid),
            FadeOut(perimeter),
            FadeOut(perimeter_text),
            FadeIn(key_property),
        )
        self.wait(2.2)
        self.play(FadeOut(key_property), FadeOut(title))


class LowerBoundN(Scene):
    def construct(self):
        title = Text("Why you need at least n infected to start", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.4)

        lines = VGroup(
            Text("Key idea: the perimeter never increases", font_size=30, color=YELLOW),
            Text("Perimeter of the full n×n grid = 4n", font_size=34),
            Text("Each infected square contributes at most 4 perimeter", font_size=32),
            Text("So with k infected squares: start perimeter ≤ 4k", font_size=32),
            Text("To ever reach 4n: 4k ≥ 4n  ⇒  k ≥ n", font_size=38, color=GREEN),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT)

        lines.next_to(title, DOWN, buff=0.6)
        self.play(Write(lines), run_time=2.5)
        self.wait(2.0)
        self.play(FadeOut(lines), FadeOut(title))



class DiagonalSolution(Scene):
    def construct(self):
        title = Text("The Solution: Start with the diagonal", font_size=42)
        self.play(Write(title))
        self.wait(0.7)
        self.play(title.animate.to_edge(UP))

        grid_size = 8
        square_size = 0.55
        grid, squares = make_grid(grid_size, square_size, stroke_width=1.4, y_shift=-0.2)

        self.play(Create(grid))
        self.wait(0.4)

        filled = set((i, i) for i in range(grid_size))
        label = Text("Start: n infected (diagonal)", font_size=26).to_edge(DOWN)
        gen_counter = Text("Generation: 0", font_size=26, color=YELLOW).next_to(label, UP, buff=0.25)

        self.play(Write(label), Write(gen_counter))
        self.play(*[squares[p].animate.set_fill(RED, opacity=0.85) for p in filled], run_time=0.8)
        self.wait(0.6)

        gen = 0
        while len(filled) < grid_size * grid_size:
            nxt = find_next_to_fill(filled, grid_size)
            if not nxt:
                break

            gen += 1
            anims = []
            for p in nxt:
                filled.add(p)
                anims.append(squares[p].animate.set_fill(BLUE, opacity=0.85))

            new_counter = Text(f"Generation: {gen}", font_size=26, color=YELLOW).move_to(gen_counter)
            self.play(*anims, Transform(gen_counter, new_counter), run_time=0.35)
            self.wait(0.22)

        punch = Text(f"Diagonal finishes in {gen} generations", font_size=34, color=GREEN)
        punch.next_to(title, DOWN, buff=0.5)
        self.play(Write(punch))
        self.wait(2.0)

        self.play(FadeOut(punch), FadeOut(label), FadeOut(gen_counter), FadeOut(grid), FadeOut(title))


class DiagonalRace(Scene):
    def construct(self):
        grid_size = 8
        square_size = 0.35
        fill_interval = 0.55

        title = Text("8×8: Different n-square diagonals race", font_size=36)
        title.to_edge(UP)
        self.add(title)

        configs = [
            {"name": "Two 4s", "diagonals": [(4, 0, 4), (0, 4, 4)]},
            {"name": "6 + 2", "diagonals": [(2, 0, 6), (0, 6, 2)]},
            {"name": "Full 8", "diagonals": [(0, 0, 8)]},
            {"name": "5 + 3", "diagonals": [(3, 0, 5), (0, 5, 3)]},
            {"name": "7 + 1", "diagonals": [(1, 0, 7), (0, 7, 1)]},
        ]

        panels = []
        all_squares = []
        all_filled = []
        labels = []
        counters = []
        finished = []
        times = []

        for config in configs:
            grid, squares = make_grid(grid_size, square_size, stroke_width=1.0, y_shift=0.0)
            filled = seed_from_diagonals(config["diagonals"], grid_size)

            label = Text(config["name"], font_size=20)
            counter = Text("Gen: 0", font_size=18, color=YELLOW)

            meta = VGroup(label, counter).arrange(DOWN, buff=0.1)
            panel = VGroup(grid, meta).arrange(DOWN, buff=0.15)

            panels.append(panel)
            all_squares.append(squares)
            all_filled.append(filled)
            labels.append(label)
            counters.append(counter)
            finished.append(False)
            times.append(None)

        # Centered layout: 2 on top, 3 on bottom
        top_row = VGroup(*panels[:2]).arrange(RIGHT, buff=1.2)
        bot_row = VGroup(*panels[2:]).arrange(RIGHT, buff=1.2)
        layout = VGroup(top_row, bot_row).arrange(DOWN, buff=0.9)

        layout.next_to(title, DOWN, buff=0.5)
        layout.move_to(layout.get_center() + DOWN * 0.1)
        self.add(layout)

        init_anims = []
        for idx in range(len(configs)):
            for p in all_filled[idx]:
                init_anims.append(all_squares[idx][p].animate.set_fill(BLUE, opacity=0.85))
        self.play(*init_anims, run_time=0.8)
        self.wait(0.6)

        generation = 0
        while not all(finished):
            generation += 1
            anims = []
            counter_updates = []

            for idx in range(len(configs)):
                if finished[idx]:
                    continue

                if len(all_filled[idx]) == grid_size * grid_size:
                    finished[idx] = True
                    labels[idx].set_color(GREEN)
                    times[idx] = generation - 1
                    continue

                nxt = find_next_to_fill(all_filled[idx], grid_size)
                if not nxt:
                    finished[idx] = True
                    labels[idx].set_color(RED)
                    times[idx] = float("inf")
                    continue

                for p in nxt:
                    all_filled[idx].add(p)
                    anims.append(all_squares[idx][p].animate.set_fill(BLUE, opacity=0.85))

                new_counter = Text(f"Gen: {generation}", font_size=18, color=YELLOW).move_to(counters[idx])
                counter_updates.append(Transform(counters[idx], new_counter))

            if anims:
                self.play(*anims, *counter_updates, run_time=0.3)
                self.wait(max(0.0, fill_interval - 0.3))

        self.wait(0.5)
        self.play(VGroup(*panels).animate.set_opacity(0.18), run_time=0.5)

        ranking_title = Text("Final Rankings (fastest wins)", font_size=30, color=GOLD)
        ranking_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(ranking_title))

        pairs = [(i, t) for i, t in enumerate(times) if t != float("inf")]
        pairs.sort(key=lambda x: x[1])

        rankings = VGroup()
        for rank, (idx, gens) in enumerate(pairs, 1):
            rankings.add(Text(f"{rank}. {configs[idx]['name']}: {gens} generations", font_size=26))

        rankings.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        rankings.move_to(ORIGIN + DOWN * 0.2)

        self.play(Write(rankings))
        self.wait(2.3)


class DiagonalRace9x9(Scene):
    def construct(self):
        grid_size = 9
        square_size = 0.32
        fill_interval = 0.55

        title = Text("9×9: Different n-square diagonals race", font_size=36)
        title.to_edge(UP)
        self.add(title)

        configs = [
            {"name": "3+3+3", "diagonals": [(0, 0, 3), (5, 3, 3, -1), (6, 6, 3)]},
            {"name": "4+5",   "diagonals": [(0, 0, 4), (8, 4, 5, -1)]},
            {"name": "Full 9","diagonals": [(0, 0, 9)]},
            {"name": "6+3",   "diagonals": [(3, 0, 6), (0, 6, 3)]},
            {"name": "7+2",   "diagonals": [(2, 0, 7), (0, 7, 2)]},
            {"name": "8+1",   "diagonals": [(1, 0, 8), (0, 8, 1)]},
        ]

        panels = []
        all_squares = []
        all_filled = []
        labels = []
        counters = []
        finished = []
        times = []

        for config in configs:
            grid, squares = make_grid(grid_size, square_size, stroke_width=1.0, y_shift=0.0)
            filled = seed_from_diagonals(config["diagonals"], grid_size)

            label = Text(config["name"], font_size=20)
            counter = Text("Gen: 0", font_size=18, color=YELLOW)

            meta = VGroup(label, counter).arrange(DOWN, buff=0.1)
            panel = VGroup(grid, meta).arrange(DOWN, buff=0.15)

            panels.append(panel)
            all_squares.append(squares)
            all_filled.append(filled)
            labels.append(label)
            counters.append(counter)
            finished.append(False)
            times.append(None)

        layout = VGroup(*panels).arrange_in_grid(rows=2, cols=3, buff=(1.2, 0.9))
        layout.next_to(title, DOWN, buff=0.5)
        self.add(layout)

        init_anims = []
        for idx in range(len(configs)):
            for p in all_filled[idx]:
                init_anims.append(all_squares[idx][p].animate.set_fill(BLUE, opacity=0.85))
        self.play(*init_anims, run_time=0.8)
        self.wait(0.6)

        generation = 0
        while not all(finished):
            generation += 1
            anims = []
            counter_updates = []

            for idx in range(len(configs)):
                if finished[idx]:
                    continue

                if len(all_filled[idx]) == grid_size * grid_size:
                    finished[idx] = True
                    labels[idx].set_color(GREEN)
                    times[idx] = generation - 1
                    continue

                nxt = find_next_to_fill(all_filled[idx], grid_size)
                if not nxt:
                    finished[idx] = True
                    labels[idx].set_color(RED)
                    times[idx] = float("inf")
                    continue

                for p in nxt:
                    all_filled[idx].add(p)
                    anims.append(all_squares[idx][p].animate.set_fill(BLUE, opacity=0.85))

                new_counter = Text(f"Gen: {generation}", font_size=18, color=YELLOW).move_to(counters[idx])
                counter_updates.append(Transform(counters[idx], new_counter))

            if anims:
                self.play(*anims, *counter_updates, run_time=0.3)
                self.wait(max(0.0, fill_interval - 0.3))

        self.wait(0.5)

        ranking_title = Text("Final Rankings", font_size=30, color=GOLD)
        ranking_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(ranking_title))

        pairs = [(i, t) for i, t in enumerate(times) if t != float("inf")]
        pairs.sort(key=lambda x: x[1])

        rankings = VGroup()
        for rank, (idx, gens) in enumerate(pairs, 1):
            rankings.add(Text(f"{rank}. {configs[idx]['name']}: {gens} generations", font_size=24))

        rankings.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        rankings.next_to(ranking_title, DOWN, buff=0.25)

        self.play(Write(rankings))
        self.wait(2.3)


class ExtraSeedsSpeedup(Scene):
    def construct(self):
        title = Text("Adding just 2 extra seeds can speed things up a lot", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        n = 10
        s = 0.32

        gridL, squaresL = make_grid(n, s, stroke_width=1.0, y_shift=0.0)
        filledL = set((i, i) for i in range(n))

        gridR, squaresR = make_grid(n, s, stroke_width=1.0, y_shift=0.0)
        filledR = set((i, i) for i in range(n))
        # add two squares to create a 2x2 block with the diagonal at the center
        filledR.add((4, 5))
        filledR.add((5, 4))

        labelL = Text("k = n", font_size=26)
        labelR = Text("k = n + 2", font_size=26)
        genL = Text("Gen: 0", font_size=22, color=YELLOW)
        genR = Text("Gen: 0", font_size=22, color=YELLOW)

        panelL = VGroup(gridL, VGroup(labelL, genL).arrange(DOWN, buff=0.12)).arrange(DOWN, buff=0.2)
        panelR = VGroup(gridR, VGroup(labelR, genR).arrange(DOWN, buff=0.12)).arrange(DOWN, buff=0.2)

        layout = VGroup(panelL, panelR).arrange(RIGHT, buff=1.4)
        layout.next_to(title, DOWN, buff=0.6)
        self.add(layout)

        self.play(
            *[squaresL[p].animate.set_fill(RED, opacity=0.85) for p in filledL],
            *[squaresR[p].animate.set_fill(RED, opacity=0.85) for p in filledR],
            run_time=0.9
        )
        self.wait(0.5)

        tL = 0
        tR = 0

        while len(filledL) < n * n or len(filledR) < n * n:
            anims = []

            nxtL = []
            if len(filledL) < n * n:
                nxtL = find_next_to_fill(filledL, n)
                if nxtL:
                    tL += 1
                    for p in nxtL:
                        filledL.add(p)
                    anims += [squaresL[p].animate.set_fill(BLUE, opacity=0.85) for p in nxtL]
                    new_genL = Text(f"Gen: {tL}", font_size=22, color=YELLOW).move_to(genL)
                    anims += [Transform(genL, new_genL)]

            nxtR = []
            if len(filledR) < n * n:
                nxtR = find_next_to_fill(filledR, n)
                if nxtR:
                    tR += 1
                    for p in nxtR:
                        filledR.add(p)
                    anims += [squaresR[p].animate.set_fill(BLUE, opacity=0.85) for p in nxtR]
                    new_genR = Text(f"Gen: {tR}", font_size=22, color=YELLOW).move_to(genR)
                    anims += [Transform(genR, new_genR)]

            if anims:
                self.play(*anims, run_time=0.28)
                self.wait(0.18)
            else:
                break

        result = Text(f"Done!  k=n took {tL} gens   |   k=n+2 took {tR} gens",
                      font_size=30, color=GREEN)
        result.next_to(layout, DOWN, buff=0.4)
        self.play(Write(result))
        self.wait(2.0)

        self.play(FadeOut(result), FadeOut(layout), FadeOut(title))


class TimeVsSeedsConcept(Scene):
    def construct(self):
        title = Text("How fast can you finish with k seeds?", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.4)

        axes = Axes(
            x_range=[0, 100, 10],
            y_range=[0, 40, 5],
            x_length=10,
            y_length=5.2,
            tips=False
        )
        axes_labels = axes.get_axis_labels(
            x_label=Text("k (initial infected)", font_size=24),
            y_label=Text("T(k) (generations)", font_size=24)
        )
        group = VGroup(axes, axes_labels).next_to(title, DOWN, buff=0.6)
        self.play(Create(group))
        self.wait(0.3)

        # Landmark points (conceptual)
        n = 30
        p1 = axes.c2p(n, n - 1)
        p2 = axes.c2p(2 * n, int(n / 2))
        p3 = axes.c2p(n * n, 0)

        d1, d2, d3 = Dot(p1), Dot(p2), Dot(p3)
        self.play(FadeIn(d1), FadeIn(d2), FadeIn(d3))

        l1 = Text("k = n", font_size=20).next_to(d1, UP, buff=0.1)
        l2 = Text("k = 2n", font_size=20).next_to(d2, UP, buff=0.1)
        l3 = Text("k = n²", font_size=20).next_to(d3, UP, buff=0.1)
        self.play(FadeIn(l1), FadeIn(l2), FadeIn(l3))
        self.wait(0.4)

        msg = VGroup(
            Text("Big picture:", font_size=28, color=YELLOW),
            Text("T(n) = n − 1  (diagonal is very slow)", font_size=30),
            Text("T(k) drops sharply just above k = n", font_size=30),
            Text("Then roughly:  T(k) ~ n / sqrt(k)", font_size=32, color=GREEN),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).to_edge(DOWN)

        self.play(Write(msg), run_time=2.2)
        self.wait(2.0)

        self.play(
            FadeOut(msg), FadeOut(group),
            FadeOut(d1), FadeOut(d2), FadeOut(d3),
            FadeOut(l1), FadeOut(l2), FadeOut(l3),
            FadeOut(title)
        )


# ---------------------------
# Full video
# ---------------------------

class FullVideo(Scene):
    def construct(self):
        InfectionProblem.construct(self)
        self.clear()

        PerimeterInvariance.construct(self)
        self.clear()

        LowerBoundN.construct(self)
        self.clear()

        DiagonalSolution.construct(self)
        self.clear()

        DiagonalRace.construct(self)
        self.clear()

        DiagonalRace9x9.construct(self)
        self.clear()

        ExtraSeedsSpeedup.construct(self)
        self.clear()

        TimeVsSeedsConcept.construct(self)
        self.clear()
