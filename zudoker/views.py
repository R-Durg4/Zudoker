# zudoker/views.py
from django.shortcuts import render
from django.http import JsonResponse
import numpy as np

def index(request):
    context = {'range_9': range(9)}
    return render(request, 'zudoker/index.html', context)

def solve_sudoku(request):
    if request.method == 'POST':
        try:
            puzzle = request.POST.get('puzzle', '')
            if not puzzle:
                return JsonResponse({'error': 'Empty puzzle'}, status=400)

            # Split the puzzle into rows
            rows = puzzle.strip().split('\n')
            if len(rows) != 9:
                return JsonResponse({'error': 'Puzzle must have 9 rows'}, status=400)

            # Convert rows into a numpy array
            grid = np.zeros((9, 9), dtype=int)
            for i, row in enumerate(rows):
                values = row.split()
                if len(values) != 9:
                    return JsonResponse({'error': 'Each row must have 9 values'}, status=400)
                grid[i] = [int(v) if v.isdigit() else 0 for v in values]

            # Solve the puzzle
            solution = solve(grid)
            return JsonResponse({'solution': solution.tolist()})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

def solve(grid):
    def is_valid(num, pos, grid):
        for i in range(len(grid[0])):
            if grid[pos[0]][i] == num and pos[1] != i:
                return False
        for i in range(len(grid)):
            if grid[i][pos[1]] == num and pos[0] != i:
                return False
        box_x = pos[1] // 3
        box_y = pos[0] // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if grid[i][j] == num and (i, j) != pos:
                    return False
        return True

    def solve_backtrack(grid):
        find = find_empty(grid)
        if not find:
            return True
        else:
            row, col = find
        for i in range(1, 10):
            if is_valid(i, (row, col), grid):
                grid[row][col] = i
                if solve_backtrack(grid):
                    return True
                grid[row][col] = 0
        return False

    def find_empty(grid):
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 0:
                    return(i,j)
        return None
    solve_backtrack(grid)
    return grid