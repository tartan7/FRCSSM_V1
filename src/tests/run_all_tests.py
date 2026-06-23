"""
全テストの実行スクリプト
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_framework import TestFramework
from test_models import run_model_tests, test_koden_model_creation, test_koden_model_validation, test_koden_model_display_name, test_flower_model_creation, test_flower_model_validation, test_condolence_model_creation, test_condolence_model_validation, test_condolence_model_message_count
from test_services import run_service_tests, test_validation_service_text_normalization, test_validation_service_furigana_conversion, test_validation_service_required_validation, test_validation_service_number_validation, test_validation_service_price_validation, test_file_service_path_operations, test_file_service_directory_operations, test_validation_service_koden_data_validation, test_validation_service_validation_summary
from test_utils import run_utils_tests, test_performance_optimizer_memory_monitoring, test_performance_optimizer_memory_cleanup, test_performance_optimizer_data_optimization, test_performance_optimizer_window_config_optimization, test_logger_creation, test_logger_logging, test_logger_performance_logging, test_logger_user_action_logging, test_error_handler_exception_handling, test_error_handler_safe_execute
from test_date_utils import (
    run_date_utils_tests,
    test_calc_age_normal, test_calc_age_before_birthday, test_calc_age_on_birthday, test_calc_age_none_inputs,
    test_convert_japanese_date_reiwa, test_convert_japanese_date_heisei, test_convert_japanese_date_showa,
    test_convert_japanese_date_with_afternoon_time, test_convert_japanese_date_invalid,
    test_convert_to_wareki_reiwa, test_convert_to_wareki_heisei, test_convert_to_wareki_showa,
    test_convert_to_wareki_with_afternoon_time, test_convert_to_wareki_none,
    test_increment_day_basic, test_increment_day_month_boundary, test_increment_day_year_boundary,
)
from test_funeral_model import (
    run_funeral_model_tests,
    test_funeral_model_creation, test_funeral_model_validate_required, test_funeral_model_validate_valid_data,
    test_funeral_model_validate_name_too_long, test_funeral_model_validate_age_negative,
    test_funeral_model_validate_age_over_150, test_funeral_model_validate_age_boundary,
    test_funeral_model_validate_date_western, test_funeral_model_validate_date_wareki,
    test_funeral_model_validate_date_invalid, test_funeral_model_validate_phone_valid,
    test_funeral_model_validate_phone_invalid, test_funeral_model_get_display_name,
    test_funeral_model_get_display_name_empty, test_funeral_model_get_summary,
    test_funeral_model_calculate_age_western, test_funeral_model_calculate_age_wareki,
    test_funeral_model_calculate_age_no_dates, test_funeral_model_is_valid,
    test_funeral_model_get_schedule_empty, test_funeral_model_get_schedule_full,
    test_funeral_model_to_dict, test_funeral_model_from_dict, test_funeral_model_to_json_from_json,
)
from test_base_controller import (
    run_base_controller_tests,
    test_base_controller_init, test_base_controller_update_values,
    test_base_controller_update_values_overwrites, test_base_controller_update_values_empty,
    test_base_controller_show_error_calls_popup, test_base_controller_show_error_default_title,
    test_base_controller_show_success_calls_popup, test_base_controller_show_confirm_returns_result,
    test_base_controller_show_confirm_cancel, test_base_controller_close_excel_safely,
    test_base_controller_close_excel_safely_on_exception, test_base_controller_switch_window_close,
    test_base_controller_switch_window_hide, test_base_controller_switch_window_updates_window,
)

def global_setup():
    """グローバルセットアップ"""
    print("テスト環境をセットアップ中...")
    # テスト用のディレクトリを作成
    if not os.path.exists("test_temp"):
        os.makedirs("test_temp")
    print("テスト環境のセットアップ完了")

def global_teardown():
    """グローバルティアダウン"""
    print("テスト環境をクリーンアップ中...")
    # テスト用のディレクトリを削除
    import shutil
    if os.path.exists("test_temp"):
        shutil.rmtree("test_temp")
    print("テスト環境のクリーンアップ完了")

def main():
    """メインテスト実行関数"""
    # テストフレームワークを初期化
    framework = TestFramework()
    
    # グローバルセットアップ・ティアダウンを設定
    framework.set_global_setup(global_setup)
    framework.set_global_teardown(global_teardown)
    
    # 各テストスイートを追加
    from test_framework import TestSuite
    
    # モデルテスト
    model_suite = TestSuite("データモデルテスト")
    model_results = run_model_tests()
    for test_func in [test_koden_model_creation, test_koden_model_validation, test_koden_model_display_name,
                     test_flower_model_creation, test_flower_model_validation,
                     test_condolence_model_creation, test_condolence_model_validation, test_condolence_model_message_count]:
        model_suite.add_test(test_func)
    framework.add_suite(model_suite)
    
    # サービステスト
    service_suite = TestSuite("サービステスト")
    service_results = run_service_tests()
    for test_func in [test_validation_service_text_normalization, test_validation_service_furigana_conversion,
                     test_validation_service_required_validation, test_validation_service_number_validation,
                     test_validation_service_price_validation, test_file_service_path_operations,
                     test_file_service_directory_operations, test_validation_service_koden_data_validation,
                     test_validation_service_validation_summary]:
        service_suite.add_test(test_func)
    framework.add_suite(service_suite)
    
    # ユーティリティテスト
    utils_suite = TestSuite("ユーティリティテスト")
    utils_results = run_utils_tests()
    for test_func in [test_performance_optimizer_memory_monitoring, test_performance_optimizer_memory_cleanup,
                     test_performance_optimizer_data_optimization, test_performance_optimizer_window_config_optimization,
                     test_logger_creation, test_logger_logging, test_logger_performance_logging,
                     test_logger_user_action_logging, test_error_handler_exception_handling,
                     test_error_handler_safe_execute]:
        utils_suite.add_test(test_func)
    framework.add_suite(utils_suite)

    # 日付ユーティリティテスト
    date_suite = TestSuite("日付ユーティリティテスト")
    run_date_utils_tests()
    for test_func in [
        test_calc_age_normal, test_calc_age_before_birthday, test_calc_age_on_birthday, test_calc_age_none_inputs,
        test_convert_japanese_date_reiwa, test_convert_japanese_date_heisei, test_convert_japanese_date_showa,
        test_convert_japanese_date_with_afternoon_time, test_convert_japanese_date_invalid,
        test_convert_to_wareki_reiwa, test_convert_to_wareki_heisei, test_convert_to_wareki_showa,
        test_convert_to_wareki_with_afternoon_time, test_convert_to_wareki_none,
        test_increment_day_basic, test_increment_day_month_boundary, test_increment_day_year_boundary,
    ]:
        date_suite.add_test(test_func)
    framework.add_suite(date_suite)

    # 葬儀モデルテスト
    funeral_model_suite = TestSuite("葬儀モデルテスト")
    run_funeral_model_tests()
    for test_func in [
        test_funeral_model_creation, test_funeral_model_validate_required, test_funeral_model_validate_valid_data,
        test_funeral_model_validate_name_too_long, test_funeral_model_validate_age_negative,
        test_funeral_model_validate_age_over_150, test_funeral_model_validate_age_boundary,
        test_funeral_model_validate_date_western, test_funeral_model_validate_date_wareki,
        test_funeral_model_validate_date_invalid, test_funeral_model_validate_phone_valid,
        test_funeral_model_validate_phone_invalid, test_funeral_model_get_display_name,
        test_funeral_model_get_display_name_empty, test_funeral_model_get_summary,
        test_funeral_model_calculate_age_western, test_funeral_model_calculate_age_wareki,
        test_funeral_model_calculate_age_no_dates, test_funeral_model_is_valid,
        test_funeral_model_get_schedule_empty, test_funeral_model_get_schedule_full,
        test_funeral_model_to_dict, test_funeral_model_from_dict, test_funeral_model_to_json_from_json,
    ]:
        funeral_model_suite.add_test(test_func)
    framework.add_suite(funeral_model_suite)

    # ベースコントローラーテスト
    controller_suite = TestSuite("ベースコントローラーテスト")
    run_base_controller_tests()
    for test_func in [
        test_base_controller_init, test_base_controller_update_values,
        test_base_controller_update_values_overwrites, test_base_controller_update_values_empty,
        test_base_controller_show_error_calls_popup, test_base_controller_show_error_default_title,
        test_base_controller_show_success_calls_popup, test_base_controller_show_confirm_returns_result,
        test_base_controller_show_confirm_cancel, test_base_controller_close_excel_safely,
        test_base_controller_close_excel_safely_on_exception, test_base_controller_switch_window_close,
        test_base_controller_switch_window_hide, test_base_controller_switch_window_updates_window,
    ]:
        controller_suite.add_test(test_func)
    framework.add_suite(controller_suite)

    # 全テストを実行
    results = framework.run_all_tests()
    
    # 結果を表示
    print("\n" + "="*60)
    print("最終テスト結果")
    print("="*60)
    print(f"総テスト数: {results['total_tests']}")
    print(f"成功: {results['passed_tests']}")
    print(f"失敗: {results['failed_tests']}")
    print(f"成功率: {results['success_rate']:.1f}%")
    print(f"総実行時間: {results['total_time']:.4f}秒")
    
    # 各スイートの結果
    print("\n各テストスイートの結果:")
    for suite_result in results['suite_summaries']:
        summary = suite_result['summary']
        print(f"  {suite_result['suite_name']}: {summary['passed']}/{summary['total']} 成功 ({summary['success_rate']:.1f}%)")
    
    # 終了コードを設定
    if results['failed_tests'] > 0:
        print(f"\n⚠️  {results['failed_tests']}個のテストが失敗しました")
        sys.exit(1)
    else:
        print("\n✅ すべてのテストが成功しました")
        sys.exit(0)

if __name__ == "__main__":
    main()