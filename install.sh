#!/bin/sh

package_dir=$(cd `dirname $0` && pwd)

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

cp ./usr/share/unity/scopes/notes/nixnote.scope /usr/share/unity/scopes/notes/nixnote.scope 
cp ./usr/share/unity-scopes/nixnote /usr/share/unity-scopes/ 
cp ./usr/share/dbus-1/services/unity-scope-nixnote.service /usr/share/dbus-1/services/ 

echo "Install complete.  Please logoff & back on to enable scope"
