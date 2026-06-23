"""
シンプルなテストランナー
個別のテストファイルを順次実行
"""
import sys
import os
import subprocess
import time

def run_test_file(test_file):
    """個別のテストファイルを実行"""
    print(f"\n{'='*50}")
    print(f"実行中: {test_file}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, 
                              cwd=os.path.dirname(os.path.abspath(__file__)))
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        return result.returncode == 0, result.stdout, result.stderr
        
    except Exception as e:
        print(f"テスト実行エラー: {str(e)}")
        return False, "", str(e)

def main():
    """メインテスト実行関数"""
    print("FRCSSM テストスイート実行開始")
    print("="*60)
    
    # テストファイルのリスト
    test_files = [
        "test_models.py",
        "test_services.py", 
        "test_utils.py"
    ]
    
    results = []
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    start_time = time.time()
    
    for test_file in test_files:
        if os.path.exists(test_file):
            success, stdout, stderr = run_test_file(test_file)
            results.append({
                'file': test_file,
                'success': success,
                'stdout': stdout,
                'stderr': stderr
            })
            
            if success:
                passed_tests += 1
                print(f"✅ {test_file} - 成功")
            else:
                failed_tests += 1
                print(f"❌ {test_file} - 失敗")
        else:
            print(f"⚠️  {test_file} - ファイルが見つかりません")
            failed_tests += 1
    
    total_tests = len(test_files)
    end_time = time.time()
    execution_time = end_time - start_time
    
    # 結果サマリー
    print(f"\n{'='*60}")
    print("テスト結果サマリー")
    print(f"{'='*60}")
    print(f"総テストファイル数: {total_tests}")
    print(f"成功: {passed_tests}")
    print(f"失敗: {failed_tests}")
    print(f"成功率: {(passed_tests/total_tests*100):.1f}%")
    print(f"総実行時間: {execution_time:.4f}秒")
    
    # 詳細結果
    print(f"\n詳細結果:")
    for result in results:
        status = "✅ 成功" if result['success'] else "❌ 失敗"
        print(f"  {result['file']}: {status}")
        if not result['success'] and result['stderr']:
            print(f"    エラー: {result['stderr'][:100]}...")
    
    # 終了コード
    if failed_tests > 0:
        print(f"\n⚠️  {failed_tests}個のテストファイルが失敗しました")
        sys.exit(1)
    else:
        print(f"\n✅ すべてのテストファイルが成功しました")
        sys.exit(0)

if __name__ == "__main__":
    main()