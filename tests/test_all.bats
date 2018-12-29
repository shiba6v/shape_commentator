#!/usr/bin/env bats

setup(){
    echo "===== setup bats ====="
    APP_DIRNAME=$(cd $BATS_TEST_DIRNAME; cd ../; pwd)
    PYTHON_MAJOR_VERSION=$(python -c 'import sys; sys.stdout.write(str(sys.version_info.major))')
}

teardown(){
    echo "===== finish bats ====="
    # Comment out the line below, and you can get outputted scripts.
    remove_tested_scripts
}

remove_tested_scripts(){
    rm_if_exists $BATS_TEST_DIRNAME/input_scripts/*.commented.py
    rm_if_exists $BATS_TEST_DIRNAME/input_scripts/2/*.commented.py
    rm_if_exists $BATS_TEST_DIRNAME/input_scripts/3/*.commented.py

}

rm_if_exists(){
    file_names=$1
    if [ -e $file_names ];then
        rm $file_names
    fi
}

compare_result(){
    SCRIPT_NAME=$1

    if [ ! -e $BATS_TEST_DIRNAME/input_scripts/$SCRIPT_NAME ];then
        if [ $PYTHON_MAJOR_VERSION -eq "2" ];then
            SCRIPT_NAME="2/"$SCRIPT_NAME
        elif [ $PYTHON_MAJOR_VERSION -eq "3" ]; then
            SCRIPT_NAME="3/"$SCRIPT_NAME
        fi
    fi

    python $APP_DIRNAME/shape_commentator/main.py $BATS_TEST_DIRNAME/input_scripts/$SCRIPT_NAME

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

@test "Rewriting commented script" {
    compare_result "rewrite.py"
}
