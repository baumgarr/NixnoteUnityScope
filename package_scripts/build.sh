#!/bin/sh
#version="2.0-alpha5"

####################################################
# Make sure we are running as root
####################################################
#if [ "$(id -u)" != "0" ]; then
#  echo "This script must be run as root" 1>&2
#   exit 1
#fi

package_dir=$(cd `dirname $0` && pwd)

#Do any parameter overrides
while [ -n "$*" ]
do
   eval $1
   shift
done

sl="s"

read -p "Enter version for build: " version

sudo $package_dir/clean.sh version=$version
sudo $package_dir/copy_files.sh version=$version 

read -p "Build tar.gz (y/n): " yn
if [ "$yn" = "y" ] 
then
  sudo $package_dir/tar.sh version=$version 
fi

read -p "Build deb (y/n): " yn
if [ "$yn" = "y" ]  
then
   sudo $package_dir/dpkg.sh version=$version 
   echo "**********************************"
   echo "* Checking deb for errors"
   echo "**********************************"
   lintian $package_dir/nixnote-unity-scope-${version}_noarch.deb 
fi
#read -p "Build rpm (y/n): " yn
#if [ "$yn" = "y" ] 
#then
#  sudo $package_dir/rpm.sh arch=$arch version=$version
#fi

# Cleanup
echo "Cleaning up"
sudo rm -rf $package_dir/nixnote-unity-scope

echo "****************************************"
echo "Build complete"
echo "****************************************" 
