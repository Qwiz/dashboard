from app import app
from rrdtool import fetch
from os import listdir, getcwd
from time import time
import math
from flask import render_template, Response, request

def split_string(string,sep=' '):
    return string.strip().split(sep)

app.jinja_env.filters['split_string'] = split_string

@app.route('/')
def index():
    dblist = {  "plugin1":['subplugin1','subplugin2','subplugin3'],
                "plugin2":['subplugin1','subplugin2','subplugin3'],
                "plugin3":['subplugin1','subplugin2','subplugin3'],
                "plugin4":['subplugin1','subplugin2','subplugin3']
            }
    # if app.config['DEV'] == True:
    #     dblist = [app.config['DEV_FILE']]
    # else:
    #     for root, dir, files in os.walk(app.config['COLLECTD_DIR']):
            
    #     dblist = [f for f in listdir(app.config['COLLECTD_DIR']) if f.endswith('.rrd')]
    return render_template('index.html', graphs = dblist)

@app.route('/get_data')
def get_data():
    db = 'ping.rrd'
    data = ['Timestamp,Value\n']
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")
    interval = request.args.get("interval")
    values = fetch(db, 'AVERAGE', '-s', str(start_time), '-e', str(end_time), '-r', str(interval))
    start_time, end_time, interval = values[0]
    times = [str(x) for x in range(int(math.ceil(start_time/interval)*interval),end_time,interval)]
    values = [ str(v[0]) for v in values[2] if v[0] is not None ]
    data = data + ['{}\n'.format(str(','.join((t,v)))) for t,v in zip(times,values)]
    print(data)
    return Response(data, status=200, mimetype='text/html')