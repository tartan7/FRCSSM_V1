import sys
import os

# src 内モジュールが相互インポートできるようにパスを追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main_optimized import main

if __name__ == '__main__':
    main()