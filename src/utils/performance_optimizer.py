"""
パフォーマンス最適化クラス
メモリ使用量と処理速度の改善
"""
import gc
import psutil
import time
from typing import Dict, List, Any, Optional, Callable
import threading
from functools import wraps
import weakref

class PerformanceOptimizer:
    """パフォーマンス最適化のためのユーティリティクラス"""
    
    def __init__(self):
        self.memory_threshold = 80  # メモリ使用率の閾値（%）
        self.cache = {}
        self.weak_refs = weakref.WeakValueDictionary()
        
    def monitor_memory(self) -> Dict[str, float]:
        """メモリ使用状況を監視"""
        process = psutil.Process()
        memory_info = process.memory_info()
        
        return {
            'rss': memory_info.rss / 1024 / 1024,  # MB
            'vms': memory_info.vms / 1024 / 1024,  # MB
            'percent': process.memory_percent(),
            'available': psutil.virtual_memory().available / 1024 / 1024  # MB
        }
    
    def check_memory_usage(self) -> bool:
        """メモリ使用率をチェック"""
        memory_info = self.monitor_memory()
        return memory_info['percent'] > self.memory_threshold
    
    def cleanup_memory(self) -> None:
        """メモリをクリーンアップ"""
        # ガベージコレクションを実行
        collected = gc.collect()
        print(f"ガベージコレクション: {collected}個のオブジェクトを回収")
        
        # キャッシュをクリア
        self.cache.clear()
        
        # 弱参照をクリア
        self.weak_refs.clear()
    
    def cache_result(self, max_size: int = 100):
        """結果をキャッシュするデコレータ"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                # キャッシュキーを生成
                cache_key = f"{func.__name__}_{hash(str(args) + str(kwargs))}"
                
                # キャッシュサイズをチェック
                if len(self.cache) >= max_size:
                    # 古いエントリを削除
                    oldest_key = next(iter(self.cache))
                    del self.cache[oldest_key]
                
                # キャッシュから取得を試行
                if cache_key in self.cache:
                    return self.cache[cache_key]
                
                # 関数を実行して結果をキャッシュ
                result = func(*args, **kwargs)
                self.cache[cache_key] = result
                return result
            
            return wrapper
        return decorator
    
    def measure_time(self, func: Callable) -> Callable:
        """実行時間を測定するデコレータ"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            
            execution_time = end_time - start_time
            print(f"{func.__name__}の実行時間: {execution_time:.4f}秒")
            
            return result
        
        return wrapper
    
    def async_operation(self, func: Callable, callback: Optional[Callable] = None) -> threading.Thread:
        """非同期操作を実行"""
        def run_async():
            try:
                result = func()
                if callback:
                    callback(result)
            except Exception as e:
                print(f"非同期操作でエラーが発生: {str(e)}")
        
        thread = threading.Thread(target=run_async)
        thread.daemon = True
        thread.start()
        return thread
    
    def batch_process(self, items: List[Any], batch_size: int = 100, 
                     process_func: Callable = None) -> List[Any]:
        """バッチ処理を実行"""
        results = []
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            
            if process_func:
                batch_results = process_func(batch)
                results.extend(batch_results)
            else:
                results.extend(batch)
            
            # メモリ使用率をチェック
            if self.check_memory_usage():
                self.cleanup_memory()
        
        return results
    
    def optimize_data_structures(self, data: Any) -> Any:
        """データ構造を最適化"""
        if isinstance(data, list):
            # リストの最適化
            return [self.optimize_data_structures(item) for item in data]
        elif isinstance(data, dict):
            # 辞書の最適化
            return {k: self.optimize_data_structures(v) for k, v in data.items()}
        elif isinstance(data, str):
            # 文字列の最適化（不要な空白を削除）
            return data.strip()
        else:
            return data
    
    def create_weak_reference(self, obj: Any, key: str) -> None:
        """弱参照を作成"""
        self.weak_refs[key] = obj
    
    def get_weak_reference(self, key: str) -> Optional[Any]:
        """弱参照を取得"""
        return self.weak_refs.get(key)
    
    def optimize_window_creation(self, window_config: Dict[str, Any]) -> Dict[str, Any]:
        """ウィンドウ作成の最適化"""
        optimized_config = window_config.copy()
        
        # 不要な設定を削除
        unnecessary_keys = ['grab_anywhere', 'keep_on_top', 'modal']
        for key in unnecessary_keys:
            if key in optimized_config and not optimized_config[key]:
                del optimized_config[key]
        
        # デフォルト値を設定
        if 'resizable' not in optimized_config:
            optimized_config['resizable'] = True
        
        if 'finalize' not in optimized_config:
            optimized_config['finalize'] = True
        
        return optimized_config
    
    def optimize_layout_rendering(self, layout: List[List]) -> List[List]:
        """レイアウトのレンダリングを最適化"""
        optimized_layout = []
        
        for row in layout:
            optimized_row = []
            for element in row:
                # 要素の最適化
                if hasattr(element, 'key') and element.key:
                    # キーが重複していないかチェック
                    pass
                
                optimized_row.append(element)
            optimized_layout.append(optimized_row)
        
        return optimized_layout
    
    def monitor_performance(self, func: Callable) -> Callable:
        """パフォーマンスを監視するデコレータ"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 開始時のメモリ使用量
            start_memory = self.monitor_memory()
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                
                # 終了時のメモリ使用量
                end_memory = self.monitor_memory()
                end_time = time.time()
                
                # パフォーマンス情報を出力
                print(f"=== パフォーマンス監視: {func.__name__} ===")
                print(f"実行時間: {end_time - start_time:.4f}秒")
                print(f"メモリ使用量変化: {end_memory['rss'] - start_memory['rss']:.2f}MB")
                print(f"現在のメモリ使用率: {end_memory['percent']:.1f}%")
                
                return result
                
            except Exception as e:
                print(f"パフォーマンス監視中にエラーが発生: {str(e)}")
                raise
        
        return wrapper
    
    def get_system_info(self) -> Dict[str, Any]:
        """システム情報を取得"""
        return {
            'cpu_count': psutil.cpu_count(),
            'memory_total': psutil.virtual_memory().total / 1024 / 1024 / 1024,  # GB
            'memory_available': psutil.virtual_memory().available / 1024 / 1024 / 1024,  # GB
            'disk_usage': psutil.disk_usage('/').percent if hasattr(psutil, 'disk_usage') else 0
        }
    
    def optimize_for_system(self) -> None:
        """システムに応じて最適化"""
        system_info = self.get_system_info()
        
        # メモリが少ない場合の最適化
        if system_info['memory_total'] < 4:  # 4GB未満
            self.memory_threshold = 70
            print("低メモリシステムのため、メモリ閾値を70%に設定")
        
        # CPUコア数に応じた最適化
        if system_info['cpu_count'] >= 8:
            print("マルチコアシステムのため、並列処理を有効化")
        else:
            print("シングルコアシステムのため、シーケンシャル処理を使用")