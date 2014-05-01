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
echo "****************************************************"
echo "Copying files for NixNote Scope $version "
echo "****************************************************"

############################
# Copy the things we need  #
############################

# Create directories
echo "Building directories"
mkdir $package_dir/nixnote-unity-scope
mkdir $package_dir/nixnote-unity-scope/usr
mkdir $package_dir/nixnote-unity-scope/usr/share
mkdir $package_dir/nixnote-unity-scope/usr/share/dbus-1
mkdir $package_dir/nixnote-unity-scope/usr/share/dbus-1/services
mkdir $package_dir/nixnote-unity-scope/usr/share/unity
mkdir $package_dir/nixnote-unity-scope/usr/share/unity/scopes
mkdir $package_dir/nixnote-unity-scope/usr/share/unity/scopes/notes
mkdir $package_dir/nixnote-unity-scope/usr/share/unity-scopes/
mkdir $package_dir/nixnote-unity-scope/usr/share/doc/
mkdir $package_dir/nixnote-unity-scope/usr/share/doc/nixnote-unity-scope

# Copy binary, configs, & man pages
echo "Copying files"
cp $source_dir/copyright $package_dir/nixnote-unity-scope/usr/share/doc/nixnote-unity-scope/
cp $source_dir/changelog.txt $package_dir/nixnote-unity-scope/usr/share/doc/nixnote-unity-scope/changelog.Debian
gzip -c -9 $package_dir/nixnote-unity-scope/usr/share/doc/nixnote-unity-scope/changelog.Debian > $package_dir/nixnote-unity-scope/usr/share/doc/nixnote-unity-scope/changelog.gz
rm $package_dir/nixnote-unity-scope/usr/share/doc/nixnote-unity-scope/changelog.Debian
 

# Copy subdirectories
cp -r $source_dir/daemon $package_dir/nixnote-unity-scope/usr/share/unity-scopes/nixnote
cp -r $source_dir/nixnote.scope $package_dir/nixnote-unity-scope/usr/share/unity/scopes/notes/
cp -r $source_dir/unity-scope-nixnote.service $package_dir/nixnote-unity-scope/usr/share/dbus-1/services/


# Reset user permissions
echo "Resetting ownership & permissions"
chown -R root:root $package_dir/nixnote-unity-scope/

