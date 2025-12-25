# 迷路とアルゴリズムの視覚化システム
# Matplotlibを使用してアニメーション表示

# 迷路とアルゴリズムの視覚化システム
# Matplotlibを使用してアニメーション表示

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import japanize_matplotlib  # 日本語フォントの設定
from typing import List, Tuple, Optional
import time

from maze import Maze
from config import COLORS, TERRAIN_TYPES, CELL_SIZE, WALL_THICKNESS

class MazeVisualizer:
    """
    迷路の生成と探索を視覚化するクラス
    Matplotlibを使用してリアルタイムでアニメーション表示
    """
    
    def __init__(self, maze: Maze, cell_size: int = CELL_SIZE):
        """
        ビジュアライザーを初期化
        
        Args:
            maze: 表示する迷路
            cell_size: 各セルの表示サイズ（ピクセル）
        """
        self.maze = maze
        self.cell_size = cell_size
        
        # Matplotlibの図とaxesを作成
        self.fig, self.ax = plt.subplots(
            figsize=(maze.cols * 0.4, maze.rows * 0.4)
        )
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        
        # タイトル用のテキストオブジェクト
        self.title_text = self.fig.suptitle('', fontsize=14, fontweight='bold')
        
    def draw_maze_static(self, title: str = "迷宮マップ"):
        """
        迷路を静的に描画（アニメーションなし）
        
        Args:
            title: 表示するタイトル
        """
        self.ax.clear()
        self.ax.set_xlim(0, self.maze.cols)
        self.ax.set_ylim(0, self.maze.rows)
        self.ax.invert_yaxis()  # Y軸を反転（上が0）
        
        self.title_text.set_text(title)
        
        # 各セルを描画
        for row in self.maze.grid:
            for cell in row:
                self._draw_cell(cell)
        
        # スタートとゴールをマーク
        self._mark_special_cells()
        
        plt.draw()
        plt.pause(0.001)
    
    def _draw_cell(self, cell, state: str = 'normal', show_cost: bool = True):
        """
        個別のセルを描画
        
        Args:
            cell: 描画するセル
            state: セルの状態 ('normal', 'visiting', 'visited', 'path', 'generating')
            show_cost: コスト表示の有無
        """
        x, y = cell.col, cell.row
        
        # セルの背景色を決定
        if state == 'normal':
            # 地形に応じた色
            color = TERRAIN_TYPES[cell.terrain]['color']
        elif state == 'generating':
            color = COLORS['generation']
        elif state == 'visiting':
            color = COLORS['frontier']
        elif state == 'visited':
            color = COLORS['visited']
        elif state == 'path':
            color = COLORS['path']
        else:
            color = TERRAIN_TYPES[cell.terrain]['color']
        
        # セルの背景を描画
        rect = patches.Rectangle(
            (x, y), 1, 1,
            linewidth=0,
            facecolor=color,
            alpha=0.8
        )
        self.ax.add_patch(rect)
        
        # コスト表示（ダイクストラ法用）
        if show_cost and state == 'normal' and cell.cost > 1:
            self.ax.text(
                x + 0.5, y + 0.5,
                f'{int(cell.cost)}',
                ha='center', va='center',
                fontsize=6,
                color='black',
                alpha=0.6
            )
        
        # 壁を描画
        wall_color = COLORS['wall']
        if cell.has_wall('top'):
            self.ax.plot(
                [x, x + 1], [y, y],
                color=wall_color,
                linewidth=WALL_THICKNESS
            )
        if cell.has_wall('right'):
            self.ax.plot(
                [x + 1, x + 1], [y, y + 1],
                color=wall_color,
                linewidth=WALL_THICKNESS
            )
        if cell.has_wall('bottom'):
            self.ax.plot(
                [x, x + 1], [y + 1, y + 1],
                color=wall_color,
                linewidth=WALL_THICKNESS
            )
        if cell.has_wall('left'):
            self.ax.plot(
                [x, x], [y, y + 1],
                color=wall_color,
                linewidth=WALL_THICKNESS
            )
    
    def _mark_special_cells(self):
        """
        スタート（入口）とゴール（宝物庫）をマーク
        """
        # スタート地点（緑の円）
        start_circle = patches.Circle(
            (0.5, 0.5), 0.3,
            color=COLORS['start'],
            zorder=10
        )
        self.ax.add_patch(start_circle)
        self.ax.text(0.5, 0.5, 'S', ha='center', va='center',
                    fontsize=10, fontweight='bold', color='white', zorder=11)
        
        # ゴール地点（赤の円）
        goal_circle = patches.Circle(
            (self.maze.cols - 0.5, self.maze.rows - 0.5), 0.3,
            color=COLORS['goal'],
            zorder=10
        )
        self.ax.add_patch(goal_circle)
        self.ax.text(self.maze.cols - 0.5, self.maze.rows - 0.5, 'G',
                    ha='center', va='center',
                    fontsize=10, fontweight='bold', color='white', zorder=11)
    
    def animate_maze_generation(self, delay: float = 0.01):
        """
        迷路生成過程をアニメーション表示
        
        Args:
            delay: 各ステップ間の遅延時間（秒）
        """
        self.draw_maze_static("迷路生成中...")
        
        for row, col, status in self.maze.generate_maze_step():
            cell = self.maze.get_cell(row, col)
            self._draw_cell(cell, state='generating', show_cost=False)
            plt.draw()
            plt.pause(delay)
        
        # 生成完了後、地形コストを割り当て
        self.maze.assign_terrain_costs()
        self.draw_maze_static("迷路生成完了 - 地形コスト割り当て済み")
        plt.pause(1)
    
    def animate_solving(self, solver_generator, algorithm_name: str, delay: float = 0.01):
        """
        探索アルゴリズムをアニメーション表示
        
        Args:
            solver_generator: ソルバーのジェネレーター
            algorithm_name: アルゴリズム名（表示用）
            delay: 各ステップ間の遅延時間（秒）
            
        Returns:
            探索結果の辞書（経路、コスト、探索ノード数など）
        """
        self.draw_maze_static(f"{algorithm_name} - 探索中...")
        
        result = None
        path = []
        
        for state, pos, data in solver_generator:
            if state == 'visiting' and pos:
                cell = self.maze.get_cell(*pos)
                self._draw_cell(cell, state='visiting')
                plt.draw()
                plt.pause(delay)
                
            elif state == 'visited' and pos:
                cell = self.maze.get_cell(*pos)
                self._draw_cell(cell, state='visited')
                
            elif state == 'found' and data:
                result = data
                path = data['path']
                self.title_text.set_text(f"{algorithm_name} - 経路発見！")
                plt.draw()
                plt.pause(0.5)
                
            elif state == 'complete':
                break
        
        # 最終経路を描画
        if path:
            for r, c in path:
                if (r, c) != (0, 0) and (r, c) != (self.maze.rows - 1, self.maze.cols - 1):
                    cell = self.maze.get_cell(r, c)
                    self._draw_cell(cell, state='path')
            
            self._mark_special_cells()
            plt.draw()
        
        return result
    
    def display_results(self, results: dict):
        """
        探索結果を図に表示
        
        Args:
            results: アルゴリズムごとの結果辞書
        """
        result_text = "探索結果比較:\n\n"
        
        for algo_name, data in results.items():
            if data:
                result_text += f"{algo_name}:\n"
                result_text += f"  経路長: {data['path_length']} ステップ\n"
                result_text += f"  総コスト: {data['path_cost']:.1f} 体力\n"
                result_text += f"  探索ノード数: {data['nodes_explored']}\n\n"
        
        self.ax.text(
            0.02, 0.98, result_text,
            transform=self.fig.transFigure,
            fontsize=9,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        )
        plt.draw()
    
    def show(self):
        """
        ウィンドウを表示（ブロッキング）
        """
        plt.show()
    
    def close(self):
        """
        ウィンドウを閉じる
        """
        plt.close(self.fig)
