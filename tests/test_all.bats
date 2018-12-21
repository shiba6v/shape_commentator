#!/usr/bin/env bats

setup(){
    echo "===== setup bats ====="
    APP_DIRNAME=$(cd $BATS_TEST_DIRNAME; cd ../; pwd)
}

teardown(){
    echo "===== finish bats ====="
    # Comment out the line below, and you can get outputted scripts.
    rm $BATS_TEST_DIRNAME/input_scripts/*.commented.py
}

compare_result(){
    SCRIPT_NAME=$1
    python $APP_DIRNAME/shape_commentator/shape_commentator.py $BATS_TEST_DIRNAME/input_scripts/$SCRIPT_NAME

    file_commented=$BATS_TEST_DIRNAME/input_scripts/$SCRIPT_NAME.commented.py 
    file_correct=$BATS_TEST_DIRNAME/correct_scripts/$SCRIPT_NAME.commented.py
    diff $file_commented $file_correct
}

@test "NumPy in CLI" {
    compare_result "numpy_compute.py"
}

# @test "NumPy in IPython" {
# 
# }

@test "Class in CLI" {
    compare_result "class_in_file.py"
}
