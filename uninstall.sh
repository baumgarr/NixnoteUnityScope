#!/bin/sh

package_dir=$(cd `dirname $0` && pwd)

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

rm /usr/share/unity/scopes/notes/nixnote.scope 
rm -rf /usr/share/unity-scopes/nixnote
rm /usr/share/dbus-1/services/unity-scope-nixnote.service  

echo "Uninstall complete"                                     
