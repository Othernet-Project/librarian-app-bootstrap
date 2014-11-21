#!/usr/bin/env python

import os
import sys
import json

import bottle
from bottle import (view, request, static_file, abort, run, default_app,
                    redirect)

import files

script = os.path.dirname(os.path.abspath(__file__))
statics = os.path.join(script, 'static')
views = os.path.join(script, 'views')
app = default_app()

bottle.TEMPLATE_PATH.insert(0, views)


class AppInfo(object):
    """ Class that wraps application metadata """
    def __init__(self, appid, title, author, version, descriptions={}, behavior=False):
        self.appid = appid
        self.title = title
        self.author = author
        self.version = version
        self.descriptions = descriptions
        self.url = '/en/apps/%s/' % appid
        self.icon_behavior = behavior

    @property
    def description(self):
        return self.descriptions['en']


@app.get('/')
def redir():
    redirect('/en/')


@app.get('/en/')
@view('list')
def show_apps():
    appdir = request.app.config['appdir']
    meta = os.path.join(appdir, 'app.json')
    try:
        with open(meta, 'r') as f:
            meta = f.read()
    except (OSError, IOError):
        abort(501, "Missing or malformed app.json metadta file")
    meta = json.loads(meta)
    try:
        app_info = AppInfo(
            appid=meta['id'],
            title=meta['title'],
            author=meta['author'],
            version=meta['version'],
            descriptions=meta['description'],
            behavior=meta['icon_behavior'])
    except KeyError as err:
        abort(501, "Missing metadata key: '%s'" % err.args[0])
    return dict(app=app_info)


@app.get('/en/app/')
@app.get('/en/app/<path:path>')
def show_app(path='index.html'):
    appdir = request.app.config['appdir']
    full_path = os.path.join(appdir, path)
    if os.path.isdir(full_path):
        abort(404)
    return static_file(path, root=appdir)


@app.get('/en/files/<path:path>')
def handle_ajax(path):
    path = request.params.get('p', path)
    resp_format = request.params.get('f', '')
    try:
        path, relpath, dirs, file_list, readme = files.get_dir_contents(path)
    except files.DoesNotExist:
        if path == '.':
            if resp_format == 'json':
                response.content_type = 'application/json'
                return json.dumps(dict(
                    dirs=dirs,
                    files=dictify_file_list(file_list),
                    readme=readme
                ))
            return dict(path='.', dirs=[], files=[], up='.', readme='')
        abort(404)
    except files.IsFileError as err:
        if resp_format == 'json':
            fstat = os.stat(path)
            response.content_type = 'application/json'
            return json.dumps(dict(
                name=os.path.basename(path),
                size=fstat[stat.ST_SIZE],
            ))
        return static_file(err.path, root=files.get_file_dir())
    up = os.path.normpath(os.path.join(path, '..'))
    if resp_format == 'json':
        response.content_type = 'application/json'
        return json.dumps(dict(
            dirs=dirs,
            files=dictify_file_list(file_list),
            readme=readme
        ))
    return dict(path=relpath, dirs=dirs, files=file_list, up=up, readme=readme)


@app.get('/static/<path:path>')
def send_static(path):
    return static_file(path, root=statics)


def main(files_dir, app_dir):
    print('App directory:   %s' % app_dir)
    print('Files directory: %s' % files_dir)
    app.config.update({
        'appdir': app_dir,
        'filesdir': files_dir
    })
    run(app)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='application bootstrapper')
    parser.add_argument('--files', metavar='PATH',
                        help='path to files directory (default: ./data)',
                        default='data')
    parser.add_argument('--app', metavar='PATH',
                        help='path to app directory (default: .)',
                        default='.')

    args = parser.parse_args(sys.argv[1:])

    main(args.files, args.app)
