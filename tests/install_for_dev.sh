if [ $(pip list | grep shape-commentator | wc -l) -gt 0 ];then
    pip uninstall -y shape_commentator
fi
BASEDIR=$(dirname $0)
SETUPDIR=$(cd $BASEDIR/../;pwd)
python $SETUPDIR/setup.py develop
