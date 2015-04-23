import random
import string

import cherrypy
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))

class Qrube(object):

    @cherrypy.expose
    def watch(self,v,*args,**kwargs):
        import youtube_dl

        ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

        with ydl:
            result = ydl.extract_info(
                'http://www.youtube.com/watch?v={}'.format(v),
                download=False # We just want to extract the info
            )
        if 'entries' in result:
            # Can be a playlist or a list of videos
            video = result['entries'][0]
        else:
            # Just a video
            video = result

        video_url   = video['url']
        video_title = video['title']
        tmpl = env.get_template('index.html')
        return tmpl.render(dlurl=video_url, title=video_title)

if __name__ == '__main__':
    cherrypy.quickstart(Qrube(),'/','cherry.conf')