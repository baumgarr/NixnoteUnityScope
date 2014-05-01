#!/bin/sh

version="1.0"


package_dir=$(cd `dirname $0` && pwd)

source_dir=".."


####################################################
# Make sure we are running as root
####################################################
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi


#Do any parameter overrides
while [ -n "$*" ]
do
   eval $1
   shift
done


##################################################
# Banner page              
##################################################
echo "**************************************************"
echo "Building tar.gz for  NixNote Unity Scope $version "
echo "**************************************************"

# Cleanup any old stuff

if [ -e "$package_dir/nixnote-unity-scope-${version}_noarch.tar.gz" ] 
then
   rm $package_dir/nixnote-unity-scope-${version}_noarch.tar.gz
fi

cd $package_dir
echo "Building tar"
cp $source_dir/install.sh $package_dir/nixnote-unity-scope/
cp $source_dir/uninstall.sh $package_dir/nixnote-unity-scope/
tar -czf $package_dir/nixnote-unity-scope-${version}_noarch.tar.gz ./nixnote-unity-scope
rm $package_dir/nixnote-unity-scope/install.sh
rm $package_dir/nixnote-unity-scope/uninstall.sh
cd -

