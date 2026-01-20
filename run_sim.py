from manim import *

class InfectionProblem(Scene):
    def construct(self):
        # Title
        title = Text("The Infection Spread Problem", font_size=48)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))
        
        # Problem statement
        problem = VGroup(
            Text("Problem: People stand in an n×n grid", font_size=36),
            Text("Rule: You get infected if 2+ neighbors are infected", font_size=32),
            Text("Question: How many people need to start infected", font_size=32),
            Text("for the infection to spread to everyone?", font_size=32)
        ).arrange(DOWN, buff=0.4)
        
        self.play(Write(problem[0]))
        self.wait(1)
        self.play(Write(problem[1]))
        self.wait(1)
        self.play(Write(problem[2]))
        self.wait(0.5)
        self.play(Write(problem[3]))
        self.wait(3)
        self.play(FadeOut(problem))


class PerimeterInvariance(Scene):
    def construct(self):
        title = Text("Key Insight: Perimeter Invariance", font_size=42)
        self.play(Write(title))
        self.wait(2)
        self.play(title.animate.to_edge(UP))
        
        # Show a 4x4 grid example
        grid_size = 4
        square_size = 1.0
        
        grid = VGroup()
        squares = {}
        
        for row in range(grid_size):
            for col in range(grid_size):
                sq = Square(side_length=square_size)
                sq.set_stroke(WHITE, width=2)
                sq.set_fill(BLACK, opacity=0)
                
                x = (col - grid_size/2 + 0.5) * square_size
                y = (row - grid_size/2 + 0.5) * square_size - 0.5
                sq.move_to([x, y, 0])
                
                grid.add(sq)
                squares[(row, col)] = sq
        
        self.play(Create(grid))
        self.wait(1)
        
        # Start with 2 diagonal squares
        filled = set()
        filled.add((0, 0))
        filled.add((1, 1))
        
        self.play(
            squares[(0, 0)].animate.set_fill(RED, opacity=0.8),
            squares[(1, 1)].animate.set_fill(RED, opacity=0.8)
        )
        self.wait(1)
        
        # Function to highlight perimeter
        def highlight_perimeter(filled_set, color=YELLOW):
            perimeter_edges = []
            for row, col in filled_set:
                sq = squares[(row, col)]
                # Check each edge
                # Top edge
                if (row + 1, col) not in filled_set:
                    edge = Line(
                        sq.get_corner(UL), sq.get_corner(UR),
                        color=color, stroke_width=6
                    )
                    perimeter_edges.append(edge)
                # Bottom edge
                if (row - 1, col) not in filled_set:
                    edge = Line(
                        sq.get_corner(DL), sq.get_corner(DR),
                        color=color, stroke_width=6
                    )
                    perimeter_edges.append(edge)
                # Left edge
                if (row, col - 1) not in filled_set:
                    edge = Line(
                        sq.get_corner(DL), sq.get_corner(UL),
                        color=color, stroke_width=6
                    )
                    perimeter_edges.append(edge)
                # Right edge
                if (row, col + 1) not in filled_set:
                    edge = Line(
                        sq.get_corner(DR), sq.get_corner(UR),
                        color=color, stroke_width=6
                    )
                    perimeter_edges.append(edge)
            return VGroup(*perimeter_edges)
        
        # Show initial perimeter
        perimeter = highlight_perimeter(filled)
        perimeter_text = Text("Perimeter = 8", font_size=28).to_edge(DOWN)
        self.play(Create(perimeter), Write(perimeter_text))
        self.wait(2)
        
        # Add a new square (orthogonally adjacent to both)
        explanation = Text("Adding a square with 2 infected neighbors...", font_size=24)
        explanation.next_to(perimeter_text, UP, buff=0.3)
        self.play(Write(explanation))
        self.wait(1)
        
        filled.add((0, 1))  # Orthogonally adjacent to both (0,0) and (1,1)
        new_perimeter = highlight_perimeter(filled)
        new_text = Text("Perimeter = 8 (stays the same!)", font_size=28).to_edge(DOWN)
        
        self.play(
            squares[(0, 1)].animate.set_fill(RED, opacity=0.8),
            Transform(perimeter, new_perimeter),
            Transform(perimeter_text, new_text),
            run_time=1.5
        )
        self.wait(2)
        
        # Show the key property
        self.play(FadeOut(explanation))
        key_property = VGroup(
            Text("Amazing Property:", font_size=36, color=YELLOW),
            Text("The perimeter never increases!", font_size=32),
            Text("Each infection step keeps perimeter ≤ initial", font_size=28)
        ).arrange(DOWN, buff=0.3).shift(DOWN * 0.5)
        
        self.play(
            FadeOut(grid),
            FadeOut(perimeter),
            FadeOut(perimeter_text)
        )
        self.play(Write(key_property))
        self.wait(3)
        self.play(FadeOut(key_property), FadeOut(title))


class DiagonalSolution(Scene):
    def construct(self):
        title = Text("The Solution: Diagonal Pattern", font_size=42)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))
        
        # Show why diagonal works
        explanation = VGroup(
            Text("For an 8×8 grid:", font_size=36),
            Text("Total perimeter = 4(8) = 32", font_size=32),
            Text("Diagonal has exactly 8 squares", font_size=32),
            Text("Each diagonal square touches 4 edges", font_size=32),
            Text("Diagonal perimeter = 8 × 4 = 32 ✓", font_size=32, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        self.play(Write(explanation))
        self.wait(4)
        self.play(FadeOut(explanation))
        
        # Show the diagonal animation
        grid_size = 8
        square_size = 0.6
        
        grid = VGroup()
        squares = {}
        
        for row in range(grid_size):
            for col in range(grid_size):
                sq = Square(side_length=square_size)
                sq.set_stroke(WHITE, width=1.5)
                sq.set_fill(BLACK, opacity=0)
                
                x = (col - grid_size/2 + 0.5) * square_size
                y = (row - grid_size/2 + 0.5) * square_size - 0.3
                sq.move_to([x, y, 0])
                
                grid.add(sq)
                squares[(row, col)] = sq
        
        self.play(Create(grid))
        self.wait(1)
        
        # Fill diagonal
        diagonal_text = Text("Start: Diagonal (8 infected)", font_size=28).to_edge(DOWN)
        self.play(Write(diagonal_text))
        
        filled = set()
        diagonal_squares = []
        for i in range(grid_size):
            filled.add((i, i))
            diagonal_squares.append(squares[(i, i)])
        
        self.play(*[sq.animate.set_fill(RED, opacity=0.8) for sq in diagonal_squares])
        self.wait(2)


class DiagonalRace(Scene):
    def construct(self):
        # Configuration
        grid_size = 8
        square_size = 0.35
        fill_interval = 0.6
        
        # Title
        title = Text("8×8 Diagonal Configuration Race", font_size=36)
        title.to_edge(UP)
        self.add(title)
        
        # Define all configurations (each has 8 squares total)
        configs = [
            {"name": "Two 4s", "diagonals": [(4, 0, 4), (0, 4, 4)]},
            {"name": "6 + 2", "diagonals": [(2, 0, 6), (0, 6, 2)]},
            {"name": "Full 8", "diagonals": [(0, 0, 8)]},
            {"name": "5 + 3", "diagonals": [(3, 0, 5), (0, 5, 3)]},
            {"name": "7 + 1", "diagonals": [(1, 0, 7), (0, 7, 1)]},
        ]
        
        # Create a grid for each configuration
        grids = []
        all_squares = []
        all_filled = []
        labels = []
        counters = []
        finished = []
        
        # Position grids in a layout (2 on top row, 3 on bottom row)
        positions = [
            [-3.5, 0.8, 0],
            [0.5, 0.8, 0],
            [-5, -2.2, 0],
            [-1.5, -2.2, 0],
            [2, -2.2, 0],
        ]
        
        for idx, config in enumerate(configs):
            grid = VGroup()
            squares = {}
            filled = set()
            
            for row in range(grid_size):
                for col in range(grid_size):
                    sq = Square(side_length=square_size)
                    sq.set_stroke(WHITE, width=1)
                    sq.set_fill(BLACK, opacity=0)
                    
                    x = (col - grid_size/2 + 0.5) * square_size
                    y = (row - grid_size/2 + 0.5) * square_size
                    sq.move_to([x, y, 0])
                    
                    grid.add(sq)
                    squares[(row, col)] = sq
            
            grid.move_to(positions[idx])
            
            diagonal_squares = []
            for diag_info in config["diagonals"]:
                if len(diag_info) == 4:
                    start_row, start_col, length, direction = diag_info
                else:
                    start_row, start_col, length = diag_info
                    direction = 1
                    
                for i in range(length):
                    row = start_row + (i * direction)
                    col = start_col + i
                    if 0 <= row < grid_size and 0 <= col < grid_size:
                        filled.add((row, col))
                        diagonal_squares.append(squares[(row, col)])
            
            label = Text(config["name"], font_size=20)
            label.next_to(grid, DOWN, buff=0.1)
            
            counter = Text("0", font_size=18, color=YELLOW)
            counter.next_to(label, DOWN, buff=0.1)
            
            grids.append(grid)
            all_squares.append(squares)
            all_filled.append(filled)
            labels.append(label)
            counters.append(counter)
            finished.append(False)
            
            self.add(grid, label, counter)
        
        all_initial_anims = []
        for idx in range(len(configs)):
            for pos in all_filled[idx]:
                all_initial_anims.append(
                    all_squares[idx][pos].animate.set_fill(BLUE, opacity=0.8)
                )
        
        self.play(*all_initial_anims, run_time=0.8)
        self.wait(1)
        
        def get_neighbors(row, col):
            neighbors = []
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < grid_size and 0 <= nc < grid_size:
                    neighbors.append((nr, nc))
            return neighbors
        
        def find_next_to_fill(filled):
            to_fill = []
            for row in range(grid_size):
                for col in range(grid_size):
                    if (row, col) not in filled:
                        filled_neighbors = sum(1 for n in get_neighbors(row, col) if n in filled)
                        if filled_neighbors >= 2:
                            to_fill.append((row, col))
            return to_fill
        
        generation = 1
        completion_order = []
        
        while not all(finished):
            animations = []
            counter_updates = []
            
            for idx in range(len(configs)):
                if finished[idx]:
                    continue
                
                next_to_fill = find_next_to_fill(all_filled[idx])
                
                if not next_to_fill:
                    finished[idx] = True
                    completion_order.append((idx, generation - 1))
                    labels[idx].set_color(GREEN)
                    continue
                
                for pos in next_to_fill:
                    all_filled[idx].add(pos)
                    animations.append(
                        all_squares[idx][pos].animate.set_fill(BLUE, opacity=0.8)
                    )
                
                new_counter = Text(str(generation), font_size=18, color=YELLOW)
                new_counter.move_to(counters[idx])
                counter_updates.append(Transform(counters[idx], new_counter))
            
            if animations:
                self.play(*animations, *counter_updates, run_time=0.3)
                self.wait(fill_interval - 0.3)
                generation += 1
        
        self.wait(1)
        
        # Blur/fade out the grids and counters
        fade_group = VGroup(*grids, *labels, *counters)
        self.play(fade_group.animate.set_opacity(0.2), run_time=0.5)
        
        ranking_title = Text("Final Rankings", font_size=32, color=GOLD)
        ranking_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(ranking_title))
        
        completion_order.sort(key=lambda x: x[1])
        
        rankings = VGroup()
        for rank, (idx, gens) in enumerate(completion_order, 1):
            medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"{rank}."
            rank_text = Text(
                f"{medal} {configs[idx]['name']}: {gens} generations",
                font_size=28
            )
            rankings.add(rank_text)
        
        rankings.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        rankings.move_to(ORIGIN)
        
        self.play(Write(rankings))
        self.wait(3)


class DiagonalRace9x9(Scene):
    def construct(self):
        grid_size = 9
        square_size = 0.32
        fill_interval = 0.6
        
        title = Text("9×9 Diagonal Configuration Race", font_size=36)
        title.to_edge(UP)
        self.add(title)
        
        configs = [
            {"name": "3+3+3", "diagonals": [(0, 0, 3), (5, 3, 3, -1), (6, 6, 3)]},
            {"name": "4+5", "diagonals": [(0, 0, 4), (8, 4, 5, -1)]},
            {"name": "Full 9", "diagonals": [(0, 0, 9)]},
            {"name": "6+3", "diagonals": [(3, 0, 6), (0, 6, 3)]},
            {"name": "7+2", "diagonals": [(2, 0, 7), (0, 7, 2)]},
            {"name": "8+1", "diagonals": [(1, 0, 8), (0, 8, 1)]},
        ]
        
        grids = []
        all_squares = []
        all_filled = []
        labels = []
        counters = []
        finished = []
        
        positions = [
            [-4.5, 0.5, 0],
            [-1, 0.5, 0],
            [2.5, 0.5, 0],
            [-4.5, -2.5, 0],
            [-1, -2.5, 0],
            [2.5, -2.5, 0],
        ]
        
        for idx, config in enumerate(configs):
            grid = VGroup()
            squares = {}
            filled = set()
            
            for row in range(grid_size):
                for col in range(grid_size):
                    sq = Square(side_length=square_size)
                    sq.set_stroke(WHITE, width=1)
                    sq.set_fill(BLACK, opacity=0)
                    
                    x = (col - grid_size/2 + 0.5) * square_size
                    y = (row - grid_size/2 + 0.5) * square_size
                    sq.move_to([x, y, 0])
                    
                    grid.add(sq)
                    squares[(row, col)] = sq
            
            grid.move_to(positions[idx])
            
            diagonal_squares = []
            for diag_info in config["diagonals"]:
                if len(diag_info) == 4:
                    start_row, start_col, length, direction = diag_info
                else:
                    start_row, start_col, length = diag_info
                    direction = 1
                    
                for i in range(length):
                    row = start_row + (i * direction)
                    col = start_col + i
                    if 0 <= row < grid_size and 0 <= col < grid_size:
                        filled.add((row, col))
                        diagonal_squares.append(squares[(row, col)])
            
            label = Text(config["name"], font_size=20)
            label.next_to(grid, DOWN, buff=0.1)
            
            counter = Text("0", font_size=18, color=YELLOW)
            counter.next_to(label, DOWN, buff=0.1)
            
            grids.append(grid)
            all_squares.append(squares)
            all_filled.append(filled)
            labels.append(label)
            counters.append(counter)
            finished.append(False)
            
            self.add(grid, label, counter)
        
        all_initial_anims = []
        for idx in range(len(configs)):
            for pos in all_filled[idx]:
                all_initial_anims.append(
                    all_squares[idx][pos].animate.set_fill(BLUE, opacity=0.8)
                )
        
        self.play(*all_initial_anims, run_time=0.8)
        self.wait(1)
        
        def get_neighbors(row, col):
            neighbors = []
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < grid_size and 0 <= nc < grid_size:
                    neighbors.append((nr, nc))
            return neighbors
        
        def find_next_to_fill(filled):
            to_fill = []
            for row in range(grid_size):
                for col in range(grid_size):
                    if (row, col) not in filled:
                        filled_neighbors = sum(1 for n in get_neighbors(row, col) if n in filled)
                        if filled_neighbors >= 2:
                            to_fill.append((row, col))
            return to_fill
        
        generation = 1
        completion_order = []
        
        while not all(finished):
            animations = []
            counter_updates = []
            
            for idx in range(len(configs)):
                if finished[idx]:
                    continue
                
                next_to_fill = find_next_to_fill(all_filled[idx])
                
                if not next_to_fill:
                    finished[idx] = True
                    completion_order.append((idx, generation - 1))
                    labels[idx].set_color(GREEN)
                    continue
                
                for pos in next_to_fill:
                    all_filled[idx].add(pos)
                    animations.append(
                        all_squares[idx][pos].animate.set_fill(BLUE, opacity=0.8)
                    )
                
                new_counter = Text(str(generation), font_size=18, color=YELLOW)
                new_counter.move_to(counters[idx])
                counter_updates.append(Transform(counters[idx], new_counter))
            
            if animations:
                self.play(*animations, *counter_updates, run_time=0.3)
                self.wait(fill_interval - 0.3)
                generation += 1
        
        self.wait(1)
        
        ranking_title = Text("Final Rankings", font_size=32, color=GOLD)
        ranking_title.to_edge(DOWN).shift(UP * 2.5)
        self.play(Write(ranking_title))
        
        completion_order.sort(key=lambda x: x[1])
        
        rankings = VGroup()
        for rank, (idx, gens) in enumerate(completion_order, 1):
            medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"{rank}."
            rank_text = Text(
                f"{medal} {configs[idx]['name']}: {gens} generations",
                font_size=24
            )
            rankings.add(rank_text)
        
        rankings.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        rankings.next_to(ranking_title, DOWN, buff=0.3)
        
        self.play(Write(rankings))
        self.wait(3)


# Full video combining all scenes
class FullVideo(Scene):
    def construct(self):
        InfectionProblem.construct(self)
        self.clear()
        PerimeterInvariance.construct(self)
        self.clear()
        DiagonalSolution.construct(self)
        self.clear()
        DiagonalRace.construct(self)
        self.clear()
        DiagonalRace9x9.construct(self)