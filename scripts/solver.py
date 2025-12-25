# 迷路探索アルゴリズム: BFS, DFS, Dijkstra
# 各アルゴリズムの違いと特性を比較するための実装

from collections import deque
import heapq
from typing import List, Tuple, Dict, Set, Optional, Generator
from cell import Cell
from maze import Maze

class MazeSolver:
    """
    迷路を解くための各種アルゴリズムを提供するクラス
    BFS（幅優先探索）、DFS（深さ優先探索）、ダイクストラ法を実装
    """
    
    def __init__(self, maze: Maze):
        """
        ソルバーを初期化
        
        Args:
            maze: 解くべき迷路オブジェクト
        """
        self.maze = maze
        self.start = (0, 0)  # スタート位置（入口）
        self.goal = (maze.rows - 1, maze.cols - 1)  # ゴール位置（宝物庫）
    
    def get_walkable_neighbors(self, cell: Cell) -> List[Cell]:
        """
        指定セルから壁なしで移動できる隣接セルを取得
        
        Args:
            cell: 現在のセル
            
        Returns:
            移動可能な隣接セルのリスト
        """
        neighbors = []
        directions = [
            (-1, 0, 'top'),
            (0, 1, 'right'),
            (1, 0, 'bottom'),
            (0, -1, 'left')
        ]
        
        for dr, dc, direction in directions:
            # その方向に壁がなければ移動可能
            if not cell.has_wall(direction):
                neighbor = self.maze.get_cell(cell.row + dr, cell.col + dc)
                if neighbor:
                    neighbors.append(neighbor)
        
        return neighbors
    
    def reconstruct_path(self, parent: Dict[Tuple[int, int], Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        親マップから最終経路を再構築
        
        Args:
            parent: {(row, col): (parent_row, parent_col)} の辞書
            
        Returns:
            スタートからゴールまでの経路（座標のリスト）
        """
        path = []
        current = self.goal
        
        while current in parent:
            path.append(current)
            current = parent[current]
        
        path.append(self.start)
        path.reverse()
        
        return path
    
    def bfs_solve(self) -> Generator[Tuple[str, Tuple[int, int], Optional[Dict]], None, None]:
        """
        BFS（幅優先探索）で迷路を解く
        
        【アルゴリズムの特徴】
        - キューを使用して、近い場所から順に探索
        - 最短ステップ数の経路を保証
        - コストは考慮しない（全てのエッジ重み = 1として扱う）
        
        Yields:
            ('state', (row, col), data) のタプル
            state: 'visiting', 'visited', 'found', 'complete'
        """
        self.maze.reset_visited()
        
        queue = deque([self.start])
        visited: Set[Tuple[int, int]] = {self.start}
        parent: Dict[Tuple[int, int], Tuple[int, int]] = {}
        nodes_explored = 0
        
        while queue:
            current_pos = queue.popleft()
            current_cell = self.maze.get_cell(*current_pos)
            nodes_explored += 1
            
            yield ('visiting', current_pos, None)
            
            if current_pos == self.goal:
                path = self.reconstruct_path(parent)
                path_cost = sum(self.maze.get_cell(r, c).cost for r, c in path)
                
                yield ('found', current_pos, {
                    'path': path,
                    'nodes_explored': nodes_explored,
                    'path_length': len(path),
                    'path_cost': path_cost
                })
                yield ('complete', None, None)
                return
            
            # 隣接セルを探索
            for neighbor in self.get_walkable_neighbors(current_cell):
                neighbor_pos = (neighbor.row, neighbor.col)
                
                if neighbor_pos not in visited:
                    visited.add(neighbor_pos)
                    parent[neighbor_pos] = current_pos
                    queue.append(neighbor_pos)
            
            yield ('visited', current_pos, None)
    
    def dfs_solve(self) -> Generator[Tuple[str, Tuple[int, int], Optional[Dict]], None, None]:
        """
        DFS（深さ優先探索）で迷路を解く
        
        【アルゴリズムの特徴】
        - スタックを使用して、深い経路を優先的に探索
        - 最短経路を保証しない
        - メモリ効率が良い（一本道を深く探索）
        
        Yields:
            ('state', (row, col), data) のタプル
        """
        self.maze.reset_visited()
        
        stack = [self.start]
        visited: Set[Tuple[int, int]] = {self.start}
        parent: Dict[Tuple[int, int], Tuple[int, int]] = {}
        nodes_explored = 0
        
        while stack:
            current_pos = stack.pop()
            current_cell = self.maze.get_cell(*current_pos)
            nodes_explored += 1
            
            yield ('visiting', current_pos, None)
            
            if current_pos == self.goal:
                path = self.reconstruct_path(parent)
                path_cost = sum(self.maze.get_cell(r, c).cost for r, c in path)
                
                yield ('found', current_pos, {
                    'path': path,
                    'nodes_explored': nodes_explored,
                    'path_length': len(path),
                    'path_cost': path_cost
                })
                yield ('complete', None, None)
                return
            
            # 隣接セルを探索（ランダム順で探索）
            neighbors = self.get_walkable_neighbors(current_cell)
            for neighbor in neighbors:
                neighbor_pos = (neighbor.row, neighbor.col)
                
                if neighbor_pos not in visited:
                    visited.add(neighbor_pos)
                    parent[neighbor_pos] = current_pos
                    stack.append(neighbor_pos)
            
            yield ('visited', current_pos, None)
    
    def dijkstra_solve(self) -> Generator[Tuple[str, Tuple[int, int], Optional[Dict]], None, None]:
        """
        ダイクストラ法で迷路を解く
        
        【アルゴリズムの特徴】
        - 優先度付きキュー（ヒープ）を使用
        - 各エッジの重み（コスト）を考慮
        - 最小コスト経路を保証
        - RPG問題では体力消費量を最小化
        
        【なぜダイクストラ法が最適か】
        この問題では各地形に異なるコスト（体力消費量）があります:
        - 石の通路: 1
        - 草むら: 3
        - 泥濘: 5
        - 水路: 8
        
        BFSは「最短ステップ数」しか考慮しませんが、
        ダイクストラ法は「最小コスト」を見つけます。
        
        例: 
        - ルートA: 石の通路を5歩 → コスト5
        - ルートB: 石の通路3歩 + 水路1歩 → コスト11
        BFSはルートBを選ぶ可能性がありますが、
        ダイクストラ法は正しくルートAを選びます。
        
        Yields:
            ('state', (row, col), data) のタプル
        """
        self.maze.reset_visited()
        
        # 優先度付きキュー: (累積コスト, (行, 列))
        pq = [(0, self.start)]
        # 各ノードへの最小コストを記録
        distances: Dict[Tuple[int, int], float] = {self.start: 0}
        parent: Dict[Tuple[int, int], Tuple[int, int]] = {}
        visited: Set[Tuple[int, int]] = set()
        nodes_explored = 0
        
        while pq:
            current_cost, current_pos = heapq.heappop(pq)
            
            if current_pos in visited:
                continue
            
            visited.add(current_pos)
            nodes_explored += 1
            current_cell = self.maze.get_cell(*current_pos)
            
            yield ('visiting', current_pos, {'cost': current_cost})
            
            if current_pos == self.goal:
                path = self.reconstruct_path(parent)
                path_cost = sum(self.maze.get_cell(r, c).cost for r, c in path)
                
                yield ('found', current_pos, {
                    'path': path,
                    'nodes_explored': nodes_explored,
                    'path_length': len(path),
                    'path_cost': path_cost
                })
                yield ('complete', None, None)
                return
            
            # 隣接セルを探索
            for neighbor in self.get_walkable_neighbors(current_cell):
                neighbor_pos = (neighbor.row, neighbor.col)
                
                if neighbor_pos not in visited:
                    # 新しい累積コスト = 現在のコスト + 次のセルのコスト
                    new_cost = current_cost + neighbor.cost
                    
                    # より良い経路が見つかった場合のみ更新
                    if neighbor_pos not in distances or new_cost < distances[neighbor_pos]:
                        distances[neighbor_pos] = new_cost
                        parent[neighbor_pos] = current_pos
                        heapq.heappush(pq, (new_cost, neighbor_pos))
            
            yield ('visited', current_pos, None)
