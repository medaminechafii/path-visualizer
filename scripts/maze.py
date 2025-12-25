# 迷路生成ロジック - DFS（深さ優先探索）を使った再帰的バックトラッキング法

import random
from typing import List, Tuple, Optional, Generator
from cell import Cell
from config import TERRAIN_TYPES

class Maze:
    """
    迷路を生成・管理するクラス
    DFS（深さ優先探索）を使った再帰的バックトラッキング法で完全迷路を生成
    """
    
    def __init__(self, rows: int, cols: int):
        """
        迷路を初期化
        
        Args:
            rows: 迷路の行数
            cols: 迷路の列数
        """
        self.rows = rows
        self.cols = cols
        # 2次元グリッドでセルを作成
        self.grid: List[List[Cell]] = [
            [Cell(r, c) for c in range(cols)]
            for r in range(rows)
        ]
        
    def get_cell(self, row: int, col: int) -> Optional[Cell]:
        """
        指定位置のセルを取得
        
        Args:
            row: 行番号
            col: 列番号
            
        Returns:
            セルオブジェクト。範囲外の場合はNone
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None
    
    def get_neighbors(self, cell: Cell) -> List[Tuple[Cell, str]]:
        """
        指定セルの隣接セル（上下左右）を取得
        
        Args:
            cell: 対象セル
            
        Returns:
            (隣接セル, 方向)のタプルのリスト
        """
        neighbors = []
        directions = [
            (-1, 0, 'top'),      # 上
            (0, 1, 'right'),     # 右
            (1, 0, 'bottom'),    # 下
            (0, -1, 'left')      # 左
        ]
        
        for dr, dc, direction in directions:
            neighbor = self.get_cell(cell.row + dr, cell.col + dc)
            if neighbor:
                neighbors.append((neighbor, direction))
        
        return neighbors
    
    def get_opposite_direction(self, direction: str) -> str:
        """
        反対方向を取得（壁を取り除く際に使用）
        
        Args:
            direction: 現在の方向
            
        Returns:
            反対方向の文字列
        """
        opposites = {
            'top': 'bottom',
            'bottom': 'top',
            'left': 'right',
            'right': 'left'
        }
        return opposites[direction]
    
    def generate_maze_step(self, start_row: int = 0, start_col: int = 0) -> Generator[Tuple[int, int, str], None, None]:
        """
        DFS再帰的バックトラッキングで迷路を生成（ジェネレーター版）
        各ステップをyieldして視覚化可能にする
        
        Args:
            start_row: 生成開始行
            start_col: 生成開始列
            
        Yields:
            (row, col, status) のタプル - 現在処理中のセル情報
        """
        stack = [(self.grid[start_row][start_col], None, None)]
        
        while stack:
            current_cell, came_from_cell, came_from_direction = stack.pop()
            
            if current_cell.visited:
                continue
                
            current_cell.visited = True
            yield (current_cell.row, current_cell.col, 'visiting')
            
            # 来た方向の壁を取り除く
            if came_from_cell and came_from_direction:
                current_cell.remove_wall(self.get_opposite_direction(came_from_direction))
                came_from_cell.remove_wall(came_from_direction)
            
            # 未訪問の隣接セルを取得
            unvisited_neighbors = [
                (neighbor, direction)
                for neighbor, direction in self.get_neighbors(current_cell)
                if not neighbor.visited
            ]
            
            if unvisited_neighbors:
                # ランダムに隣接セルを選択
                random.shuffle(unvisited_neighbors)
                for neighbor, direction in unvisited_neighbors:
                    if not neighbor.visited:
                        stack.append((neighbor, current_cell, direction))
    
    def assign_terrain_costs(self):
        """
        各セルにランダムな地形タイプとコストを割り当てる
        RPGの迷宮設定: 様々な地形による体力消費量の違い
        """
        terrain_list = list(TERRAIN_TYPES.keys())
        weights = [0.4, 0.3, 0.2, 0.1]  # 石の通路が最も多く、水路が最も少ない
        
        for row in self.grid:
            for cell in row:
                # スタートとゴールは常に石の通路（コスト1）にする
                if (cell.row == 0 and cell.col == 0) or \
                   (cell.row == self.rows - 1 and cell.col == self.cols - 1):
                    terrain = 'road'
                else:
                    terrain = random.choices(terrain_list, weights=weights)[0]
                
                cell.set_terrain(terrain, TERRAIN_TYPES[terrain]['cost'])
    
    def reset_visited(self):
        """
        全セルの訪問フラグをリセット（探索アルゴリズム実行前に呼ぶ）
        """
        for row in self.grid:
            for cell in row:
                cell.visited = False
