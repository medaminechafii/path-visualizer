# 5.6 創造(50点)
# 問題: ファンタジーRPG迷宮探索シミュレーター
#
# 【問題文】
# 冒険者が古代遺跡の迷宮を探索しています。迷宮内には様々な地形があり、
# それぞれ通過するための体力消費量が異なります:
# - 石の通路: 体力1消費
# - 草むらエリア: 体力3消費（移動が遅い）
# - 泥濘地帯: 体力5消費（足を取られる）
# - 浅瀬の水路: 体力8消費（泳ぐ必要がある）
#
# 冒険者は迷宮の入口（左上）から宝物庫（右下）まで移動したいが、
# 体力を最小限に抑えたいです。ダイクストラ法を使って、
# 最も体力消費が少ない経路を見つけましょう。
#
# 【ダイクストラ法を使う理由】
# この問題では各地形に異なるコスト（重み）があります。
# BFSは最短ステップ数しか考慮しませんが、ダイクストラ法は
# 各エッジの重みを考慮して最小コストの経路を見つけることができます。
# 体力消費量という実際のコストを最小化する必要があるため、
# ダイクストラ法が最適なアルゴリズムです。
#
# 【評価ポイント】
# - 独創性: RPGの迷宮探索という独自のストーリー設定
# - 実用性: 体力というリソース管理が必要な現実的な問題
# - 視覚化: 地形ごとに色分けして探索過程を表示

class Cell:
    """
    迷路の各セル（マス）を表すクラス
    
    Attributes:
        row (int): 行番号
        col (int): 列番号
        walls (dict): 上下左右の壁の有無 {'top': bool, 'right': bool, 'bottom': bool, 'left': bool}
        visited (bool): 訪問済みフラグ（迷路生成時に使用）
        cost (float): このセルに入るための体力消費量（地形コスト）
        terrain (str): 地形タイプ ('road', 'grass', 'mud', 'water')
    """
    
    def __init__(self, row: int, col: int):
        """
        セルを初期化
        
        Args:
            row: 行番号
            col: 列番号
        """
        self.row = row
        self.col = col
        # 初期状態では全ての壁が存在（完全に閉じた状態）
        self.walls = {
            'top': True,
            'right': True,
            'bottom': True,
            'left': True
        }
        self.visited = False  # 迷路生成アルゴリズムで使用
        self.cost = 1.0  # デフォルトコスト
        self.terrain = 'road'  # デフォルト地形
    
    def remove_wall(self, direction: str):
        """
        指定方向の壁を取り除く
        
        Args:
            direction: 'top', 'right', 'bottom', 'left' のいずれか
        """
        if direction in self.walls:
            self.walls[direction] = False
    
    def has_wall(self, direction: str) -> bool:
        """
        指定方向に壁があるかチェック
        
        Args:
            direction: チェックする方向
            
        Returns:
            壁がある場合True
        """
        return self.walls.get(direction, True)
    
    def set_terrain(self, terrain_type: str, cost: float):
        """
        地形タイプとコストを設定
        
        Args:
            terrain_type: 地形の種類
            cost: その地形に入るためのコスト
        """
        self.terrain = terrain_type
        self.cost = cost
    
    def __repr__(self):
        return f"Cell({self.row}, {self.col}, terrain={self.terrain}, cost={self.cost})"
