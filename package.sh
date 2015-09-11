#!/bin/sh
if [ $# -lt 1 ]; then
cat<<HELP
package -- zip a directory exclude .svn .git and .DS_Store.
USAGE: package DIRICTORY
HELP
	exit 0
fi

echo $0
echo $1

#zip -r -9 $1.zip $1 -x *.svn* *.DS_Store* *.git*
7za a -xr!*.svn* -xr!*.git* -xr!*.DS_store* $1.7z $1
