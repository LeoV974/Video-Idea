from manim import *

class DiagonalRace(Scene):
    def construct(self):
        # Configuration
        grid_size = 8
        square_size = 0.35
        fill_interval = 0.6
        
        # Title
        title = Text("Diagonal Configuration Race", font_size=36)
        title.to_edge(UP)
        self.add(title)
        
        # Define all configurations (each has 8 squares total)
        configs = [
            {"name": "Two 4s", "diagonals": [(4, 0, 4), (0, 4, 4)]},  # (start_row, start_col, length)
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
            [-3.5, 1.2, 0],   # Top left
            [0.5, 1.2, 0],    # Top middle
            [-5, -1.8, 0],    # Bottom left
            [-1.5, -1.8, 0],  # Bottom middle
            [2, -1.8, 0],     # Bottom right
        ]
        
        for idx, config in enumerate(configs):
            # Create grid
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
            
            # Position the grid
            grid.move_to(positions[idx])
            
            # Fill initial diagonals
            diagonal_squares = []
            for diag_info in config["diagonals"]:
                if len(diag_info) == 4:  # Has direction specified
                    start_row, start_col, length, direction = diag_info
                else:  # Default up-right direction
                    start_row, start_col, length = diag_info
                    direction = 1
                    
                for i in range(length):
                    row = start_row + (i * direction)
                    col = start_col + i
                    if 0 <= row < grid_size and 0 <= col < grid_size:
                        filled.add((row, col))
                        diagonal_squares.append(squares[(row, col)])
            
            # Label
            label = Text(config["name"], font_size=20)
            label.next_to(grid, DOWN, buff=0.1)
            
            # Counter
            counter = Text("0", font_size=18, color=YELLOW)
            counter.next_to(label, DOWN, buff=0.1)
            
            grids.append(grid)
            all_squares.append(squares)
            all_filled.append(filled)
            labels.append(label)
            counters.append(counter)
            finished.append(False)
            
            self.add(grid, label, counter)
        
        # Animate initial fill
        all_initial_anims = []
        for idx in range(len(configs)):
            for pos in all_filled[idx]:
                all_initial_anims.append(
                    all_squares[idx][pos].animate.set_fill(BLUE, opacity=0.8)
                )
        
        self.play(*all_initial_anims, run_time=0.8)
        self.wait(1)
        
        # Helper function
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
        
        # Run simulation
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
                    # Mark as complete
                    labels[idx].set_color(GREEN)
                    continue
                
                # Add new filled squares
                for pos in next_to_fill:
                    all_filled[idx].add(pos)
                    animations.append(
                        all_squares[idx][pos].animate.set_fill(BLUE, opacity=0.8)
                    )
                
                # Update counter
                new_counter = Text(str(generation), font_size=18, color=YELLOW)
                new_counter.move_to(counters[idx])
                counter_updates.append(Transform(counters[idx], new_counter))
            
            if animations:
                self.play(*animations, *counter_updates, run_time=0.3)
                self.wait(fill_interval - 0.3)
                generation += 1
        
        self.wait(1)
        
        # Show rankings
        ranking_title = Text("Final Rankings", font_size=32, color=GOLD)
        ranking_title.to_edge(DOWN).shift(UP * 2.5)
        self.play(Write(ranking_title))
        
        # Sort by completion time
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


class DiagonalRace9x9(Scene):
    def construct(self):
        # Configuration
        grid_size = 9
        square_size = 0.32
        fill_interval = 0.6
        
        # Title
        title = Text("9×9 Diagonal Configuration Race", font_size=36)
        title.to_edge(UP)
        self.add(title)
        
        # Define all configurations (each has 9 squares total)
        configs = [
            {"name": "3+3+3", "diagonals": [(0, 0, 3), (5, 3, 3, -1), (6, 6, 3)]},  # (start_row, start_col, length, direction)
            {"name": "4+5", "diagonals": [(0, 0, 4), (8, 4, 5, -1)]},
            {"name": "Full 9", "diagonals": [(0, 0, 9)]},
            {"name": "6+3", "diagonals": [(3, 0, 6), (0, 6, 3)]},
            {"name": "7+2", "diagonals": [(2, 0, 7), (0, 7, 2)]},
            {"name": "8+1", "diagonals": [(1, 0, 8), (0, 8, 1)]},
        ]
        
        # Create a grid for each configuration
        grids = []
        all_squares = []
        all_filled = []
        labels = []
        counters = []
        finished = []
        
        # Position grids in a layout (3 on top row, 3 on bottom row)
        positions = [
            [-4.5, 1.2, 0],   # Top left
            [-1, 1.2, 0],     # Top middle
            [2.5, 1.2, 0],    # Top right
            [-4.5, -1.8, 0],  # Bottom left
            [-1, -1.8, 0],    # Bottom middle
            [2.5, -1.8, 0],   # Bottom right
        ]
        
        for idx, config in enumerate(configs):
            # Create grid
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
            
            # Position the grid
            grid.move_to(positions[idx])
            
            # Fill initial diagonals
            diagonal_squares = []
            for diag_info in config["diagonals"]:
                if len(diag_info) == 4:  # Has direction specified
                    start_row, start_col, length, direction = diag_info
                else:  # Default up-right direction
                    start_row, start_col, length = diag_info
                    direction = 1
                    
                for i in range(length):
                    row = start_row + (i * direction)
                    col = start_col + i
                    if 0 <= row < grid_size and 0 <= col < grid_size:
                        filled.add((row, col))
                        diagonal_squares.append(squares[(row, col)])
            
            # Label
            label = Text(config["name"], font_size=20)
            label.next_to(grid, DOWN, buff=0.1)
            
            # Counter
            counter = Text("0", font_size=18, color=YELLOW)
            counter.next_to(label, DOWN, buff=0.1)
            
            grids.append(grid)
            all_squares.append(squares)
            all_filled.append(filled)
            labels.append(label)
            counters.append(counter)
            finished.append(False)
            
            self.add(grid, label, counter)
        
        # Animate initial fill
        all_initial_anims = []
        for idx in range(len(configs)):
            for pos in all_filled[idx]:
                all_initial_anims.append(
                    all_squares[idx][pos].animate.set_fill(BLUE, opacity=0.8)
                )
        
        self.play(*all_initial_anims, run_time=0.8)
        self.wait(1)
        
        # Helper function
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
        
        # Run simulation
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
                    # Mark as complete
                    labels[idx].set_color(GREEN)
                    continue
                
                # Add new filled squares
                for pos in next_to_fill:
                    all_filled[idx].add(pos)
                    animations.append(
                        all_squares[idx][pos].animate.set_fill(BLUE, opacity=0.8)
                    )
                
                # Update counter
                new_counter = Text(str(generation), font_size=18, color=YELLOW)
                new_counter.move_to(counters[idx])
                counter_updates.append(Transform(counters[idx], new_counter))
            
            if animations:
                self.play(*animations, *counter_updates, run_time=0.3)
                self.wait(fill_interval - 0.3)
                generation += 1
        
        self.wait(1)
        
        # Show rankings
        ranking_title = Text("Final Rankings", font_size=32, color=GOLD)
        ranking_title.to_edge(DOWN).shift(UP * 2.5)
        self.play(Write(ranking_title))
        
        # Sort by completion time
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