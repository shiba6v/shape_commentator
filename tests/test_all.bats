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
    rm_if_exists $BATS_TEST_DIRNAME/result
}

rm_if_exists(){
    file_names=$1
    if [ -e $file_names ];then
        rm $file_names
    fi
}

get_script_path(){
    SCRIPT_NAME=$1

    if [ ! -e $BATS_TEST_DIRNAME/input_scripts/$SCRIPT_NAME ];then
        if [ $PYTHON_MAJOR_VERSION -eq "2" ];then
            SCRIPT_NAME="2/"$SCRIPT_NAME
        elif [ $PYTHON_MAJOR_VERSION -eq "3" ]; then
            SCRIPT_NAME="3/"$SCRIPT_NAME
        fi
    fi

    echo $SCRIPT_NAME
}


compare_module_result(){
    SCRIPT_NAME=$(get_script_path $1)

    # python $APP_DIRNAME/shape_commentator/main.py $BATS_TEST_DIRNAME/input_scripts/$SCRIPT_NAME
    python -m shape_commentator $BATS_TEST_DIRNAME/input_scripts/$SCRIPT_NAME

    file_commented=$BATS_TEST_DIRNAME/input_scripts/$SCRIPT_NAME.commented.py 
    file_correct=$BATS_TEST_DIRNAME/correct_scripts/$SCRIPT_NAME.commented.py
    diff $file_commented $file_correct
}

compare_method_result(){
    SCRIPT_NAME=$(get_script_path $1)
    python $BATS_TEST_DIRNAME/comment_method.py $BATS_TEST_DIRNAME/input_scripts/$SCRIPT_NAME > $BATS_TEST_DIRNAME/result
    file_commented=$BATS_TEST_DIRNAME/result
    file_correct=$BATS_TEST_DIRNAME/correct_scripts/$SCRIPT_NAME.commented.py
    diff $file_commented $file_correct
}

@test "NumPy (Module)" {
    compare_module_result "numpy_compute.py"
}

@test "NumPy (Method)" {
    compare_method_result "numpy_compute.py"
}

@test "Class (Module)" {
    compare_module_result "class_in_file.py"
}

@test "Class (Method)" {
    compare_method_result "class_in_file.py"
}

@test "Rewriting commented script (Module)" {
    compare_module_result "rewrite.py"
}

@test "Rewriting commented script (Method)" {
    compare_method_result "rewrite.py"
}

@test "Standard types (Module)" {
    compare_module_result "stdtypes.py"
}

@test "Standard types (Method)" {
    compare_method_result "stdtypes.py"
}

@test "Iterators (Module)" {
    compare_module_result "iters.py"
}

@test "Iterators (Method)" {
    compare_method_result "iters.py"
}
