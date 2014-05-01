NixnoteUnityScope
=================

A rough Unity scope for use with NixNote2 and Unity.

This project is designed to give a Unity search interface into NixNote2.  The general idea is 
for you to be able to see your notes when searching through Unity's search bar.  This initial bulid
has several restrictions.

Thesse restrictions are:
- You must have NixNote2 beta 2 or later installed.
- Only the last 10 notes will ever be presented in a search.  If more than 10 match a search, 
  the last 10 which have been updated most recently are returned.
- Thumbails of your notes will only be shown after they are generated by NixNote.  If no 
  thumbnail exists, you'll get a generic "note" picture.
- Searching is NOT done by default.  You must use "evernote:" or "nixnote:" as the start of
  your search to use this feature.
  
Most of these restrictions are because this is new and I have some reservations about the performance
(or lack of performance) this may cause.  

If this proves useful, please let me know.  I'm not a big Unity user so this was more of an 
experiment.  

Thanks.
