# メインプログラム - 迷路生成と探索アルゴリズムのデモンストレーション
# 
# 【プログラムの目的】
# ファンタジーRPGの迷宮探索シミュレーターとして、
# 異なる探索アルゴリズム（BFS、DFS、ダイクストラ法）の
# 動作と効率を視覚的に比較する教育用プログラム
#
# 【実行方法】
# python main.py
#
# 【操作方法】
# コンソールでアルゴリズムを選択し、Enterキーで実行
# ウィンドウを閉じると次のアルゴリズムまたはメニューに進む

import time
from maze import Maze
from solver import MazeSolver
from visualization import MazeVisualizer
from config import MAZE_ROWS, MAZE_COLS, ANIMATION_SPEED

def print_header():
    """
    プログラムのヘッダーを表示
    """
    print("=" * 70)
    print("  ファンタジーRPG 迷宮探索シミュレーター")
    print("  Maze Generator & Pathfinding Algorithm Visualizer")
    print("=" * 70)
    print()
    print("【問題設定】")
    print("冒険者が古代遺跡の迷宮を探索します。")
    print("迷宮内には様々な地形があり、それぞれ体力消費量が異なります：")
    print("  • 石の通路: 体力1消費")
    print("  • 草むらエリア: 体力3消費")
    print("  • 泥濘地帯: 体力5消費")
    print("  • 浅瀬の水路: 体力8消費")
    print()
    print("目標: 入口（左上）から宝物庫（右下）まで、")
    print("      体力消費を最小限に抑えて移動する経路を見つける")
    print("=" * 70)
    print()

def print_algorithm_comparison():
    """
    アルゴリズムの比較説明を表示
    """
    print("\n【アルゴリズムの特徴】")
    print()
    print("1. BFS（幅優先探索）")
    print("   • 最短ステップ数の経路を保証")
    print("   • コストは考慮しない")
    print("   • 近い場所から順に探索")
    print()
    print("2. DFS（深さ優先探索）")
    print("   • 深い経路を優先的に探索")
    print("   • 最短経路を保証しない")
    print("   • メモリ効率が良い")
    print()
    print("3. Dijkstra（ダイクストラ法）★推奨")
    print("   • 最小コスト経路を保証")
    print("   • 各地形のコストを考慮")
    print("   • 体力消費を最小化（この問題に最適！）")
    print()

def run_algorithm(maze: Maze, visualizer: MazeVisualizer, 
                 algorithm: str, speed: str = 'normal') -> dict:
    """
    指定されたアルゴリズムを実行
    
    Args:
        maze: 迷路オブジェクト
        visualizer: ビジュアライザー
        algorithm: 'bfs', 'dfs', 'dijkstra' のいずれか
        speed: アニメーション速度 'fast', 'normal', 'slow'
        
    Returns:
        探索結果の辞書
    """
    solver = MazeSolver(maze)
    delay = ANIMATION_SPEED[speed]
    
    print(f"\n[{algorithm.upper()}] アルゴリズム実行中...")
    start_time = time.time()
    
    if algorithm == 'bfs':
        result = visualizer.animate_solving(
            solver.bfs_solve(),
            "BFS（幅優先探索）",
            delay
        )
    elif algorithm == 'dfs':
        result = visualizer.animate_solving(
            solver.dfs_solve(),
            "DFS（深さ優先探索）",
            delay
        )
    elif algorithm == 'dijkstra':
        result = visualizer.animate_solving(
            solver.dijkstra_solve(),
            "Dijkstra（ダイクストラ法）",
            delay
        )
    else:
        print(f"エラー: 不明なアルゴリズム '{algorithm}'")
        return None
    
    elapsed_time = time.time() - start_time
    
    if result:
        print(f"✓ 経路発見！")
        print(f"  経路長: {result['path_length']} ステップ")
        print(f"  総コスト: {result['path_cost']:.1f} 体力")
        print(f"  探索ノード数: {result['nodes_explored']}")
        print(f"  実行時間: {elapsed_time:.2f} 秒")
        result['execution_time'] = elapsed_time
    
    return result

def interactive_mode():
    """
    インタラクティブモード - ユーザーがアルゴリズムを選択
    """
    print_header()
    print_algorithm_comparison()
    
    # 迷路を生成
    print("\n迷路を生成中...")
    maze = Maze(MAZE_ROWS, MAZE_COLS)
    visualizer = MazeVisualizer(maze)
    
    # 迷路生成をアニメーション表示
    visualizer.animate_maze_generation(delay=0.001)
    print("✓ 迷路生成完了！")
    
    results = {}
    
    while True:
        print("\n" + "=" * 70)
        print("アルゴリズムを選択してください:")
        print("  1. BFS（幅優先探索）")
        print("  2. DFS（深さ優先探索）")
        print("  3. Dijkstra（ダイクストラ法）★推奨")
        print("  4. 全てのアルゴリズムを比較実行")
        print("  5. 新しい迷路を生成")
        print("  0. 終了")
        print("=" * 70)
        
        choice = input("\n選択 (0-5): ").strip()
        
        if choice == '0':
            print("\nプログラムを終了します。")
            visualizer.close()
            break
            
        elif choice == '1':
            result = run_algorithm(maze, visualizer, 'bfs')
            if result:
                results['BFS'] = result
            input("\nEnterキーで続ける...")
            
        elif choice == '2':
            result = run_algorithm(maze, visualizer, 'dfs')
            if result:
                results['DFS'] = result
            input("\nEnterキーで続ける...")
            
        elif choice == '3':
            result = run_algorithm(maze, visualizer, 'dijkstra')
            if result:
                results['Dijkstra'] = result
            input("\nEnterキーで続ける...")
            
        elif choice == '4':
            print("\n全アルゴリズムを実行します...")
            
            # BFS実行
            result = run_algorithm(maze, visualizer, 'bfs', 'fast')
            if result:
                results['BFS'] = result
            input("\nEnterキーで次のアルゴリズムへ...")
            
            # DFS実行
            result = run_algorithm(maze, visualizer, 'dfs', 'fast')
            if result:
                results['DFS'] = result
            input("\nEnterキーで次のアルゴリズムへ...")
            
            # Dijkstra実行
            result = run_algorithm(maze, visualizer, 'dijkstra', 'fast')
            if result:
                results['Dijkstra'] = result
            
            # 結果比較を表示
            print("\n" + "=" * 70)
            print("【アルゴリズム比較結果】")
            print("=" * 70)
            
            for algo_name, data in results.items():
                print(f"\n{algo_name}:")
                print(f"  経路長: {data['path_length']} ステップ")
                print(f"  総コスト: {data['path_cost']:.1f} 体力 ", end="")
                if algo_name == 'Dijkstra':
                    print("★最小！")
                else:
                    print()
                print(f"  探索ノード数: {data['nodes_explored']}")
                print(f"  実行時間: {data['execution_time']:.2f} 秒")
            
            print("\n【結論】")
            print("ダイクストラ法が体力消費を最小化する最適な経路を見つけました！")
            print("BFS/DFSはステップ数を考慮しますが、地形コストは無視します。")
            
            # ビジュアルに結果を表示
            visualizer.display_results(results)
            
            input("\nEnterキーで続ける...")
            
        elif choice == '5':
            print("\n新しい迷路を生成中...")
            visualizer.close()
            maze = Maze(MAZE_ROWS, MAZE_COLS)
            visualizer = MazeVisualizer(maze)
            visualizer.animate_maze_generation(delay=0.001)
            print("✓ 新しい迷路生成完了！")
            results = {}  # 結果をリセット
            
        else:
            print("\n無効な選択です。もう一度選んでください。")

def demo_mode():
    """
    デモモード - 全アルゴリズムを自動実行
    """
    print_header()
    print("【デモモード】全アルゴリズムを自動実行します\n")
    
    # 迷路を生成
    print("迷路を生成中...")
    maze = Maze(MAZE_ROWS, MAZE_COLS)
    visualizer = MazeVisualizer(maze)
    visualizer.animate_maze_generation(delay=0.001)
    print("✓ 迷路生成完了！\n")
    
    results = {}
    
    # 各アルゴリズムを実行
    for algo in ['bfs', 'dfs', 'dijkstra']:
        result = run_algorithm(maze, visualizer, algo, 'normal')
        if result:
            algo_name = algo.upper()
            results[algo_name] = result
        time.sleep(2)
    
    # 結果表示
    print("\n" + "=" * 70)
    print("【最終結果】")
    print("=" * 70)
    
    visualizer.display_results(results)
    
    print("\nウィンドウを閉じて終了してください。")
    visualizer.show()

def main():
    """
    メインエントリーポイント
    """
    # モード選択
    print("=" * 70)
    print("  迷宮探索シミュレーター")
    print("=" * 70)
    print("\nモードを選択してください:")
    print("  1. インタラクティブモード（推奨）")
    print("  2. デモモード（全自動実行）")
    print("=" * 70)
    
    mode = input("\n選択 (1-2): ").strip()
    
    if mode == '2':
        demo_mode()
    else:
        interactive_mode()

if __name__ == "__main__":
    main()
