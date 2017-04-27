#/bin/bash

#=== test
#sed  -f rule.test input | tee output
#exit 0

unamestr=`uname`

if [[ "$unamestr" = MINGW32* ]]; then
    SED="sed"
elif [ "$unamestr" = "Linux" ]; then
    SED="sed"
else
    if [ "$unamestr" = "Darwin" ]; then
        SED="gsed"
    else
        echo "only Linux, MingW or Mac OS can be supported" &
        exit 1
    fi
fi

if [ $# -eq 0 ]; then
    echo "please enter the source directory"
    exit 0;
fi

echo "list java files..."
filelist=`find $FINDFLAG $1 -type f -name "*.java"`

function addImport {
    echo "" > temp
    cat imports | while read line
    do
        sed -e "/${line}/ "'i\
import com.hyphenate.chat.EMClient;' $1 > temp 
        grep -q "import com.hyphenate.chat.EMClient;" temp
        if [ $? == 0 ]; then
            mv temp $1
            return 0
        fi
    done
}

for file in $filelist; do
	echo "" > temp
	echo $file
	$SED -f rule $file > temp
	mv temp $file
    addImport $file
done

