# 設定ファイル - 迷路のパラメータと視覚化の設定

# 迷路のサイズ
MAZE_ROWS = 15  # 行数
MAZE_COLS = 20  # 列数

# 地形タイプとそれぞれのコスト
# ファンタジーRPGの設定: 冒険者の体力消費量
TERRAIN_TYPES = {
    'road': {
        'cost': 1,
        'color': '#E8E8E8',  # 明るいグレー - 石の通路
        'name': '石の通路'
    },
    'grass': {
        'cost': 3,
        'color': '#90EE90',  # ライトグリーン - 草むら
        'name': '草むらエリア'
    },
    'mud': {
        'cost': 5,
        'color': '#8B7355',  # ブラウン - 泥濘
        'name': '泥濘地帯'
    },
    'water': {
        'cost': 8,
        'color': '#87CEEB',  # スカイブルー - 浅瀬
        'name': '浅瀬の水路'
    }
}

# 視覚化の色設定
COLORS = {
    'wall': '#000000',          # 黒 - 壁
    'unvisited': '#FFFFFF',     # 白 - 未訪問
    'visited': '#D3D3D3',       # グレー - 訪問済み
    'frontier': '#4169E1',      # ロイヤルブルー - 探索中
    'start': '#00FF00',         # 緑 - スタート地点（入口）
    'goal': '#FF0000',          # 赤 - ゴール地点（宝物庫）
    'path': '#FFD700',          # ゴールド - 最終経路
    'generation': '#9370DB'     # ミディアムパープル - 迷路生成中
}

# アニメーション速度（秒）
ANIMATION_SPEED = {
    'fast': 0.001,
    'normal': 0.01,
    'slow': 0.05
}

# セルのサイズ（ピクセル）
CELL_SIZE = 30

# 壁の太さ
WALL_THICKNESS = 2
