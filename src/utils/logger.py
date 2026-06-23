"""
ログ管理クラス
アプリケーション全体のログ機能を提供
"""
import logging
import os
import sys
from datetime import datetime
from typing import Optional, Dict, Any
import traceback
import json

class Logger:
    """ログ管理クラス"""
    
    def __init__(self, name: str = "FRCSSM", log_level: str = "INFO"):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # ログディレクトリを exe / スクリプト横の logs フォルダに固定
        if getattr(sys, 'frozen', False):
            _base = os.path.dirname(sys.executable)
        else:
            _base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.log_dir = os.path.join(_base, "logs")
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        # ログファイルの設定
        self.log_file = os.path.join(self.log_dir, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")
        
        # ハンドラーの設定
        self._setup_handlers()
        
        # パフォーマンスログ
        self.performance_log = os.path.join(self.log_dir, "performance.log")
        
    def _setup_handlers(self):
        """ログハンドラーを設定"""
        # ファイルハンドラー
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # コンソールハンドラー
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # フォーマッター
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # ハンドラーを追加
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # 重複ログを防ぐ
        self.logger.propagate = False
    
    def debug(self, message: str, **kwargs):
        """デバッグログを出力"""
        self.logger.debug(self._format_message(message, **kwargs))
    
    def info(self, message: str, **kwargs):
        """情報ログを出力"""
        self.logger.info(self._format_message(message, **kwargs))
    
    def warning(self, message: str, **kwargs):
        """警告ログを出力"""
        self.logger.warning(self._format_message(message, **kwargs))
    
    def error(self, message: str, exception: Optional[Exception] = None, **kwargs):
        """エラーログを出力"""
        if exception:
            message += f" - 例外: {str(exception)}"
            message += f" - トレースバック: {traceback.format_exc()}"
        
        self.logger.error(self._format_message(message, **kwargs))
    
    def critical(self, message: str, exception: Optional[Exception] = None, **kwargs):
        """致命的エラーログを出力"""
        if exception:
            message += f" - 例外: {str(exception)}"
            message += f" - トレースバック: {traceback.format_exc()}"
        
        self.logger.critical(self._format_message(message, **kwargs))
    
    def _format_message(self, message: str, **kwargs) -> str:
        """メッセージをフォーマット"""
        if kwargs:
            context = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
            return f"{message} | {context}"
        return message
    
    def log_performance(self, function_name: str, execution_time: float, 
                       memory_usage: float, **kwargs):
        """パフォーマンスログを出力"""
        performance_data = {
            'timestamp': datetime.now().isoformat(),
            'function': function_name,
            'execution_time': execution_time,
            'memory_usage': memory_usage,
            **kwargs
        }
        
        with open(self.performance_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(performance_data, ensure_ascii=False) + '\n')
    
    def log_user_action(self, action: str, details: Dict[str, Any] = None):
        """ユーザーアクションをログ"""
        action_data = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'details': details or {}
        }
        
        user_log_file = os.path.join(self.log_dir, "user_actions.log")
        with open(user_log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(action_data, ensure_ascii=False) + '\n')
    
    def log_error_with_context(self, error: Exception, context: Dict[str, Any] = None):
        """コンテキスト付きでエラーをログ"""
        error_data = {
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'context': context or {}
        }
        
        error_log_file = os.path.join(self.log_dir, "errors.log")
        with open(error_log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(error_data, ensure_ascii=False) + '\n')
    
    def get_log_files(self) -> list:
        """ログファイルの一覧を取得"""
        if not os.path.exists(self.log_dir):
            return []
        
        return [f for f in os.listdir(self.log_dir) if f.endswith('.log')]
    
    def cleanup_old_logs(self, days: int = 30):
        """古いログファイルを削除"""
        if not os.path.exists(self.log_dir):
            return
        
        current_time = datetime.now().timestamp()
        cutoff_time = current_time - (days * 24 * 60 * 60)
        
        for filename in os.listdir(self.log_dir):
            file_path = os.path.join(self.log_dir, filename)
            if os.path.isfile(file_path):
                file_time = os.path.getmtime(file_path)
                if file_time < cutoff_time:
                    try:
                        os.remove(file_path)
                        self.info(f"古いログファイルを削除: {filename}")
                    except Exception as e:
                        self.error(f"ログファイル削除エラー: {filename}", e)

class ErrorHandler:
    """エラーハンドリングクラス"""
    
    def __init__(self, logger: Logger):
        self.logger = logger
    
    def handle_exception(self, exception: Exception, context: Dict[str, Any] = None):
        """例外を処理"""
        self.logger.error(f"例外が発生しました: {str(exception)}", exception, context=context)
        
        # エラーの種類に応じた処理
        if isinstance(exception, FileNotFoundError):
            return "ファイルが見つかりません。パスを確認してください。"
        elif isinstance(exception, PermissionError):
            return "ファイルへのアクセス権限がありません。"
        elif isinstance(exception, ValueError):
            return "入力値が正しくありません。"
        elif isinstance(exception, MemoryError):
            return "メモリが不足しています。アプリケーションを再起動してください。"
        else:
            return f"予期しないエラーが発生しました: {str(exception)}"
    
    def safe_execute(self, func, *args, **kwargs):
        """安全に関数を実行"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_message = self.handle_exception(e, {
                'function': func.__name__,
                'args': str(args),
                'kwargs': str(kwargs)
            })
            return None, error_message

# グローバルロガーインスタンス
app_logger = Logger("FRCSSM")
error_handler = ErrorHandler(app_logger)