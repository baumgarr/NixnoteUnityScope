#! /usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright(C) 2013 Mark Tully <markjtully@gmail.com>
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import GLib, Gio
from gi.repository import Unity
import gettext
import os
import webbrowser
import sqlite3
import hashlib

APP_NAME = 'unity-scope-nixnote'
LOCAL_PATH = '/usr/share/locale/'
gettext.bindtextdomain(APP_NAME, LOCAL_PATH)
gettext.textdomain(APP_NAME)
_ = gettext.gettext

GROUP_NAME = 'com.canonical.Unity.Scope.Notes.NixNote'
UNIQUE_PATH = '/com/canonical/unity/scope/notes/nixnote'

SEARCH_HINT = _('Search NixNote')
NO_RESULTS_HINT = _('Sorry, there are no notes that match your search.')
PROVIDER_CREDITS = _('')
SVG_DIR = '/usr/share/icons/unity-icon-theme/places/svg/'
DEFAULT_RESULT_ICON = SVG_DIR + 'group-notes.svg'
DEFAULT_RESULT_MIMETYPE = 'application-x/desktop'
DEFAULT_RESULT_TYPE = Unity.ResultType.DEFAULT
NIXNOTE_EXECUTABLE = '/usr/bin/nixnote2'
BOOKMARKS_PATH = os.getenv("HOME") + "/.nixnote/db-1/"

c1 = {'id': 'recent',
      'name': _('Notes'),
      'icon': SVG_DIR + 'group-notes.svg',
      'renderer': Unity.CategoryRenderer.VERTICAL_TILE}

CATEGORIES = [c1]

FILTERS = []

m1 = {'id'   :'dateCreated',
      'type' :'s',
      'field':Unity.SchemaFieldType.OPTIONAL}
m2 = {'id'   :'dateUpdated',
      'type' :'s',
      'field':Unity.SchemaFieldType.OPTIONAL}
m3 = {'id'   :'tags',
      'type' :'s',
      'field':Unity.SchemaFieldType.OPTIONAL}
m4 = {'id'   :'notebook',
      'type' :'s',
      'field':Unity.SchemaFieldType.OPTIONAL}   
m5 = {'id'   :'lid',
      'type' :'s',
      'field':Unity.SchemaFieldType.OPTIONAL}   

EXTRA_METADATA = [m1, m2, m3, m4, m5]

def trace(text) :
#  f = open('/tmp/output.txt','a')
#  print(text, file=f)
#  f.close();
   print(text)  



def search(search, filters) :
  DB_PATH = os.getenv("HOME") + "/.nixnote/db-1/nixnote.db"
  BASE_QUERY = "SELECT lid, datetime(dateCreated/1000, 'unixepoch', 'localtime'), datetime(dateUpdated/1000, 'unixepoch', 'localtime'), title, tags, notebook from notetable where lid in (SELECT lid from SearchIndex where content like '%s' and weight>30) order by dateUpdated desc limit 10"
  searchtext = '%'+search+'%'
  SQL_SEARCH = BASE_QUERY % searchtext
  retval = []
 
  try:
    conn = sqlite3.connect(DB_PATH)
    connection = conn.cursor()
    connection.execute(SQL_SEARCH)
    results = connection.fetchall()
    for row in results:
       lid = row[0]
       created = row[1]
       updated = row[2]
       title = row[3]
       tags = row[4]
       notebook = row[5]
       icon = os.getenv("HOME")+"/.nixnote/db-1/tdba/"+str(lid)+".png"
       if not os.path.exists(icon):
          icon = None
       retval.append({'uri': '--openNote='+str(lid),
                        'icon': icon,
                        'category': 0,
                        'title': title,
                        'dateCreated': created,
                        'dateUpdated': updated,
                        'tags': tags,
                        'notebook':notebook,
                        'lid': lid
                    })
  except sqlite3.DatabaseError as e :
    pass 
  connection.close()
  return retval



def activate(result, metadata, id):
    trace('activate')
    trace(metadata)
    note = result.uri
    parameters = [NIXNOTE_EXECUTABLE, '--accountId=1', '--startMinimized', note]
    trace(parameters)
    trace('spawning')
    GLib.spawn_async(parameters)
    return Unity.ActivationResponse(handled=Unity.HandledType.HIDE_DASH, goto_uri=None)


class Preview(Unity.ResultPreviewer):
    def do_run(self):
        trace('preview.do_run')
        trace(self.result.metadata)
        preview = Unity.GenericPreview.new(self.result.title, '', None)
        subtitle = _('Notebook:  ') 
        if self.result.metadata and 'notebook' in self.result.metadata:
           subtitle += self.result.metadata['notebook'].get_string() + '\n'
        if self.result.metadata and 'tags' in self.result.metadata:
           subtitle = subtitle + _('Tags:  ') +self.result.metadata['tags'].get_string() + '\n'
        if self.result.metadata and 'dateCreated' in self.result.metadata and self.result.metadata['dateCreated'].get_string() != '':
           subtitle = subtitle + _('Created:  ') + self.result.metadata['dateCreated'].get_string() +'\n'
        if self.result.metadata and 'dateUpdated' in self.result.metadata and self.result.metadata['dateUpdated'].get_string() != '':
           subtitle = subtitle + _('Updated:  ') + self.result.metadata['dateUpdated'].get_string() + '\n'
        preview.props.subtitle = subtitle 

        if os.path.exists(self.result.icon_hint):
            preview.props.image_source_uri = 'file://' + self.result.icon_hint
        else:
            preview.props.image = Gio.ThemedIcon.new('gtk-about')
        show_action = Unity.PreviewAction.new("show", _("Open"), None)
        preview.add_action(show_action)
        return preview

# Classes below this point establish communication
# with Unity, you probably shouldn't modify them.


class MySearch(Unity.ScopeSearchBase):
    def __init__(self, search_context):
        trace('mysearch.init')
        super(MySearch, self).__init__()
        self.set_search_context(search_context)

    def do_run(self):
        trace('search.do_run')
        try:
            result_set = self.search_context.result_set
            for i in search(self.search_context.search_query,
                            self.search_context.filter_state):
                if not 'uri' in i or not i['uri'] :
                    i['uri'] = '' 
                if not 'icon' in i or not i['icon'] or i['icon'] == '':
                    i['icon'] = DEFAULT_RESULT_ICON
                if not 'mimetype' in i or not i['mimetype'] or i['mimetype'] == '':
                    i['mimetype'] = DEFAULT_RESULT_MIMETYPE
                if not 'result_type' in i or not i['result_type'] or i['result_type'] == '':
                    i['result_type'] = DEFAULT_RESULT_TYPE
                if not 'category' in i or not i['category'] or i['category'] == '':
                    i['category'] = 0
                if not 'title' in i or not i['title']:
                    i['title'] = ''
                if not 'comment' in i or not i['comment']:
                    i['comment'] = ''
                if not 'dnd_uri' in i or not i['dnd_uri'] or i['dnd_uri'] == '':
                    i['dnd_uri'] = i['uri']
                if not 'tags' in i or not i['tags'] :
                    i['tags'] = ''
                i['provider_credits'] = GLib.Variant('s', PROVIDER_CREDITS)
                result_set.add_result(**i)
        except Exception as error:
            trace('error in search_do_run')


class Scope(Unity.AbstractScope):
    def __init__(self):
        Unity.AbstractScope.__init__(self)

    def do_get_search_hint(self):
        return SEARCH_HINT

    def do_get_schema(self):
        trace('do_get_schema')
        schema = Unity.Schema.new()
        if EXTRA_METADATA:
            for m in EXTRA_METADATA:
                schema.add_field(m['id'], m['type'], m['field'])
        #FIXME should be REQUIRED for credits
        schema.add_field('provider_credits', 's', Unity.SchemaFieldType.OPTIONAL)
        return schema

    def do_get_categories(self):
        trace('do_get_categories')
        '''
        Adds categories
        '''
        cs = Unity.CategorySet.new()
        if CATEGORIES:
           for c in CATEGORIES:
               cat = Unity.Category.new(c['id'], c['name'],
                                        Gio.ThemedIcon.new(c['icon']),
                                        c['renderer'])
               cs.add(cat)
        return cs

    def do_get_filters(self):
        trace('do_get_filters')
        '''
        Adds filters
        '''
        fs = Unity.FilterSet.new()
        #if FILTERS:
        #
        return fs

    def do_get_group_name(self):
        trace('return group name')
        return GROUP_NAME

    def do_get_unique_name(self):
        trace('do_get_unique_name')
        return UNIQUE_PATH

    def do_create_search_for_query(self, search_context):
        trace('do_create_search_for_query')
        se = MySearch(search_context)
        return se

    def do_activate(self, result, metadata, id):
        trace('do_activate')
        return activate(result, metadata, id)

    def do_create_previewer(self, result, metadata):
        trace('do_create_preview')
        '''
        Creates a preview when a resut is right-clicked
        '''
        result_preview = Preview()
        result_preview.set_scope_result(result)
        result_preview.set_search_metadata(metadata)
        return result_preview


def load_scope():
    return Scope()
