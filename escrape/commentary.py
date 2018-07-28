import requests
from lxml import html
import io
import json
import os
import pickle
import funcy as fy
import html
from collections import OrderedDict


class Commentary:
    def __init__(self, sport, series_id, event_id):
        base = 'http://site.api.espn.com/apis/site/v2/sports/'
        self.base = base + sport + '/'+ series_id + '/playbyplay'
        self.base_args = {
            "contentorigin": "espn",
            "event": event_id,
            "section": "cricinfo"
        }
            
    def load(self):
        """
        Returns [<commentary items>], where each element 
        of the list is the commentary at a timestep, in order of 
        latest first.
        """
        innings = []
        for period in range(4):
            commentary = []
            page_number = 1
            complete = False
            while not complete:
                self.base_args.update({"page": page_number})
                api_response = requests.get(self.base, params=self.base_args)
                parsed = json.loads(api_response.text)           
                complete = parsed["commentary"]["pageCount"] == parsed["commentary"]["pageIndex"]
                commentary.append(parsed["commentary"]["items"])
                page_number += 1
            innings.append(commentary)
        
        return innings
    
    
class CachedCommentary(Commentary):
    def __init__(self, savepath, *args):
        fname = '_'.join(args) + '.pkl'
        self.fpath = os.path.join(savepath, fname)
        super().__init__(*args)
        
    def load(self):        
        if os.path.exists(self.fpath):
            with open(self.fpath, 'rb') as fp:
                return pickle.load(fp)
        else:
            content = super().load()
            with open(self.fpath, 'wb+') as fp:
                pickle.dump(content, fp)
            return content


def ESPNParse(dump):
    assert(len(dump) == 4)
    required = ['preText',  'text', 'postText', 'shortText']
                
    def _filter(item):
        values = []
        for key in required:
            decoded = html.unescape(item[key])
            values.append(decoded)
        return OrderedDict(zip(required, values))
    
    def _innings(innings):              
        items = fy.flatten(innings)
        exports = list(map(_filter, items))
        return exports
    
    return list(map(_innings, dump))