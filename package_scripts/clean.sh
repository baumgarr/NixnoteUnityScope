#!/bin/sh

version="1.0"

#Do any parameter overrides
while [ -n "$*" ]
do
   eval $1
   shift
done

package_dir=$(cd `dirname $0` && pwd)
#destination="$package_dir/nixnote/share/nixnote"


# Check that we are runinng as root
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi


# Delete the tar.gz file if it exists
if [ -e "$package_dir/nixnote-unity-scope-${version}_noarch.tar.gz" ]
then
   rm $package_dir/nixnote-unity-scope-${version}_noarch.tar.gz
fi

#delete the debif it exists
if [ -e "$package_dir/nixnote-unity-scope-${version}_noarch.deb" ]
then
   rm $package_dir/nixnote-unity-scope-${version}_noarch.deb
fi

#delete the rpm if it exists
rpmversion=`echo $version | sed -e 's/[-]/_/g'`
if [ -e "$package_dir/nixnote-unity-scope-${rpmversion}-0.noarch.rpm" ]
then
   rm $package_dir/nixnote-unity-scope-${rpmversion}-0.noarch.rpm
fi

# Cleanup any directory info
if [ -d "$package_dir/nixnote-unity-scope" ]
then
   rm -rf $package_dir/nixnote-unity-scope
fi
