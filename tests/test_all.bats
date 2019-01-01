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
    rm_if_exists $BATS_TEST_DIRNAME/tmp_result*
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

# python -m shape_commentator script_name
compare_module_result(){
    SCRIPT_NAME=$(get_script_path $1)

    # python $APP_DIRNAME/shape_commentator/main.py $BATS_TEST_DIRNAME/input_scripts/$SCRIPT_NAME
    python -m shape_commentator $BATS_TEST_DIRNAME/input_scripts/$SCRIPT_NAME

    file_commented=$BATS_TEST_DIRNAME/input_scripts/$SCRIPT_NAME.commented.py 
    file_correct=$BATS_TEST_DIRNAME/correct_scripts/$SCRIPT_NAME.commented.py
    diff $file_commented $file_correct
}

# shape_commentator.comment(src, globals())
compare_method_comment_result(){
    SCRIPT_NAME=$(get_script_path $1)
    python $BATS_TEST_DIRNAME/method_comment.py $BATS_TEST_DIRNAME/input_scripts/$SCRIPT_NAME > $BATS_TEST_DIRNAME/tmp_result

    file_commented=$BATS_TEST_DIRNAME/tmp_result
    file_correct=$BATS_TEST_DIRNAME/correct_scripts/$SCRIPT_NAME.commented.py
    diff $file_commented $file_correct
}

# shape_commentator.clear(src)
compare_method_clear_result(){
    SCRIPT_NAME=$(get_script_path $1)
    python $BATS_TEST_DIRNAME/method_clear.py $BATS_TEST_DIRNAME/input_scripts/$SCRIPT_NAME > $BATS_TEST_DIRNAME/tmp_result

    file_commented=$BATS_TEST_DIRNAME/tmp_result
    file_correct=$BATS_TEST_DIRNAME/correct_scripts/$SCRIPT_NAME.commented.py
    diff $file_commented $file_correct
}

# python -m shape_commentator.print_clear script_name
compare_module_print_clear_result(){
    SCRIPT_NAME=$(get_script_path $1)
    python -m shape_commentator.print_clear $BATS_TEST_DIRNAME/input_scripts/$SCRIPT_NAME > $BATS_TEST_DIRNAME/tmp_result
    
    file_commented=$BATS_TEST_DIRNAME/tmp_result
    file_correct=$BATS_TEST_DIRNAME/correct_scripts/$SCRIPT_NAME.commented.py
    diff $file_commented $file_correct
}

# python -m shape_commentator.print_comment script_name
compare_module_print_comment_result(){
    SCRIPT_NAME=$(get_script_path $1)
    python -m shape_commentator.print_comment $BATS_TEST_DIRNAME/input_scripts/$SCRIPT_NAME > $BATS_TEST_DIRNAME/tmp_result
    
    file_commented=$BATS_TEST_DIRNAME/tmp_result
    file_correct=$BATS_TEST_DIRNAME/correct_scripts/$SCRIPT_NAME.commented.py
    diff $file_commented $file_correct
}

# 
compare_print_result(){
    SCRIPT_NAME=$(get_script_path $1)
    python -m shape_commentator $BATS_TEST_DIRNAME/input_scripts/$SCRIPT_NAME > $BATS_TEST_DIRNAME/tmp_result1
    python $BATS_TEST_DIRNAME/input_scripts/$SCRIPT_NAME > $BATS_TEST_DIRNAME/tmp_result2

    file_commented=$BATS_TEST_DIRNAME/tmp_result1
    file_correct=$BATS_TEST_DIRNAME/tmp_result2
    diff $file_commented $file_correct

}

@test "NumPy (Module)" {
    compare_module_result "numpy_compute.py"
}

@test "NumPy (Method)" {
    compare_method_comment_result "numpy_compute.py"
}

@test "Class (Module)" {
    compare_module_result "class_in_file.py"
}

@test "Class (Method)" {
    compare_method_comment_result "class_in_file.py"
}

@test "Rewriting commented script (Module)" {
    compare_module_result "rewrite.py"
}

@test "Rewriting commented script (Method)" {
    compare_method_comment_result "rewrite.py"
}

@test "Standard types (Module)" {
    compare_module_result "stdtypes.py"
}

@test "Standard types (Method)" {
    compare_method_comment_result "stdtypes.py"
}

@test "Iterators (Module)" {
    compare_module_result "iters.py"
}

@test "Iterators (Method)" {
    compare_method_comment_result "iters.py"
}

@test "Long and complex list and tuple (Module)" {
    compare_module_result "long_list.py"
}

@test "Long and complex list and tuple (Method)" {
    compare_method_comment_result "long_list.py"
}

@test "Module print_clear" {
    compare_module_print_clear_result "print_clear.py"
}

@test "Module print_comment" {
    compare_module_print_comment_result "print_comment.py"
}

@test "Method shape_commentator.clear(src)" {
    compare_method_clear_result "print_clear.py"
}

@test "__file__ __package__ __name__ is same" {
    compare_print_result "filepath.py"
}