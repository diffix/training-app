from gevent import monkey; monkey.patch_all()
import gevent
from bottle import get, post, route, run, template, request, response, static_file, redirect
import logging
import decimal
import simplejson
import hashlib
import sqlite3
import io
import pprint
import os
import random
import datetime
import socket    
import time
import psycopg2
import copy
from demoConfig import getExampleList
pp = pprint.PrettyPrinter(indent=4)

# Env variables
'''
PORT (defaults to 8080)
DATA_DIR (holds the database 'training.db', defaults to .)
LOG_DIR (holds the log file 'training.log', defaults to .)
NATIVE_USER (user name for native postgres, defaults to 'direct_user'
NATIVE_PASS (password for native postgres, defaults to 'demo')
NATIVE_PORT (defaults to 5432)
NATIVE_HOST (defaults to db001.gda-score.org)
TRUSTED_USER (user name for diffix postgres, defaults to 'trusted_user'
TRUSTED_PASS (password for diffix postgres, defaults to 'demo')
TRUSTED_PORT (defaults to NATIVE_PORT)
TRUSTED_HOST (defaults to db001.gda-score.org)
UNTRUSTED_USER (user name for diffix postgres, defaults to 'untrusted_user'
UNTRUSTED_PASS (password for diffix postgres, defaults to 'demo')
UNTRUSTED_PORT (defaults to NATIVE_PORT)
UNTRUSTED_HOST (defaults to db001.gda-score.org)
'''


# Layout parameters main page
margin = 0.1    # cm
padding = 5     # px
gap = 0.5
fullParWd = 26
fullParHt = 150
listParWd = 5
logoWd = 5
pRightDescHt = 6
listHt = 16
pRightQueriesHt = 6
queryBoxGap = 1
minColWd = 1.8
pRightAnsHt = fullParHt - pRightDescHt - pRightQueriesHt
queryHt = pRightQueriesHt - (4 * gap)
rightTopParHt = queryHt + (3 * gap)
rightParWd = fullParWd - listParWd - gap
rightParHt = fullParHt
descParWd = rightParWd - (2 * gap)
resultsHt = pRightAnsHt - (2 * margin)
dbParWd = (rightParWd / 2) - gap
dbParHt = rightParHt
tabWid = dbParWd
descWd = descParWd - (3 * gap)
descHt = pRightDescHt - gap
listWd = listParWd - (2 * margin)
#queryWd = dbParWd + (2 * margin)
queryWd = dbParWd
#zzzz
spaceWd = queryWd - 1.2
resultsWd = dbParWd - (2 * margin)

rightArrowLeft = queryWd
leftArrowLeft = queryWd - (1.5 * gap)
rightArrowTop = queryHt/2
leftArrowTop = queryHt/1.2

# Layout parameters consent page
consentParHt = 10
logoParWd = 7
msgParWd = fullParWd - logoParWd - (3 * gap)

maxNumRows = 100

initClientState = {
    'example' : 0,
    'exampleHtml' : '',
    'exampleList' : [],
    'description' : '',
    'dbList' : [],
    'dbHtml' : '',
    'modeHtml' : '',
    'dbname' : '',
    'mode' : '',
    'native': {
        'sql' : '',
        'runSql' : '',
        'ans' : [],
        'err' : None,
        'notices' : '',
        'ansHtml' : '',
        'cached' : False,
        'colInfo' : None,
        'conn' : None,
        'numRows' : 0,
        'duration': 0
    },
    'trusted': {
        'sql' : '',
        'runSql' : '',
        'ans' : [],
        'err' : None,
        'notices' : '',
        'ansHtml' : '',
        'cached' : False,
        'colInfo' : None,
        'conn' : None,
        'numRows' : 0,
        'duration': 0
    },
    'untrusted': {
        'sql' : '',
        'runSql' : '',
        'ans' : [],
        'err' : None,
        'notices' : '',
        'ansHtml' : '',
        'cached' : False,
        'colInfo' : None,
        'conn' : None,
        'numRows' : 0,
        'duration': 0
    },
}

# global user state
us = {
}

# global other system state
ss = {
    'conn' : None,
    'cursor' : None,
    'dbPath' : '',
    'logPath' : '',
    'native': {
        'host': 'db001.gda-score.org',
        'port': 5432,
        'user': 'direct_user',
        'password': 'demo',
    },
    'trusted': {
        'host': 'db001.gda-score.org',
        'port': 5432,
        'user': 'trusted_user',
        'password': 'demo',
    },
    'untrusted': {
        'host': 'db001.gda-score.org',
        'port': 5432,
        'user': 'untrusted_user',
        'password': 'demo',
    },
}

def makePulldowns():
    user = getCookie()
    s = loadUserState(user)
    s['dbList'] = ['']
    for ex in s['exampleList']:
        if len(ex['dbname']) > 0 and ex['dbname'] not in s['dbList']:
            s['dbList'].append(ex['dbname'])
    s['dbHtml'] = ''' <select name="database">
                 <option value=" "> </option> '''
    for db in s['dbList']:
        if len(db) < 3:
            continue
        if db == s['dbname']:
            s['dbHtml'] += f'''<option value="{db}" selected>{db}</option>'''
        else:
            s['dbHtml'] += f'''<option value="{db}">{db}</option>'''
    s['dbHtml'] += '''</select>'''

    s['modeHtml'] = ''' <select name="mode">
                 <option value=" "> </option> '''
    for mode in ['trusted','untrusted']:
        if mode == s['mode']:
            s['modeHtml'] += f'''<option value="{mode}" selected>{mode}</option>'''
        else:
            s['modeHtml'] += f'''<option value="{mode}">{mode}</option>'''
    s['modeHtml'] += '''</select>'''
    return

def makeWelcomeHtml():
    html = f'''
    <style>
    * {{
        font-family: "Arial", helvetica, sans-serif;
    }}  
    .par {{
        margin: auto;
        height: {consentParHt}cm;
        width: {fullParWd}cm;
    }}
    .par-left {{
        float: left;
        height: {consentParHt}cm;
        width: {logoParWd}cm;
    }}
    .par-right {{
        float: right;
        height: {consentParHt}cm;
        width: {msgParWd}cm;
    }}
    .button {{
      border: none;
      font-size: 32;
      cursor: pointer;
      border-radius: 8px;
    }}
    .button-consent {{
      background-color: #3498DB;
      color: white;
    }}
    img {{
      width: {logoParWd}cm
    }}
    </style>
    <br><br><br>
    <div class="par">
      <div class="par-left">
           <img src="logos.png" alt="" style="vertical-align:top">
      </div>
      <div class="par-right">
          <font size="5">
          Welcome to the training app for Diffix for PostgreSQL anonymization.
          </font>
          <br><br>
          <font size="4">
          This app requires cookies for correct operation. This app may
          record statistics about how the app is used. These statistics are
          used to improve the app.
          </font>
          <br><br>
          <form method="get" action="/consent">
              <button class="button button-consent" type="submit">
                I Agree
              </button>
          </form>
      </div>
    </div>
    '''
    return html

def makeHtml():
    user = getCookie()
    s = loadUserState(user)
    diffixSys = s['mode']
    if s['native']['colInfo'] is None:
        nativeTabWd = tabWid
    else:
        nativeCols = len(s['native']['colInfo'])
        if nativeCols <= 5:
            nativeTabWd = tabWid
        else:
            nativeTabWd = minColWd * nativeCols
    if s[diffixSys]['colInfo'] is None:
        diffixTabWd = tabWid
    else:
        diffixCols = len(s[diffixSys]['colInfo'])
        if diffixCols <= 5:
            diffixTabWd = tabWid
        else:
            diffixTabWd = minColWd * diffixCols
    html = f'''
    <style>
    * {{
        font-family: "Arial", helvetica, sans-serif;
    }}  
    .par {{
        margin: auto;
        height: {fullParHt}cm;
        width: {fullParWd}cm;
    }}
    .par-left {{
        float: left;
        height: {fullParHt}cm;
        width: {listParWd}cm;
    }}
    .par-right {{
        float: right;
        height: {rightParHt}cm;
        width: {rightParWd}cm;
    }}
    .par-right-desc {{
        margin: auto;
        height: {pRightDescHt}cm;
        width: {descParWd}cm;
    }}
    .par-right-queries {{
        /*margin-left: -20px;*/
        float: left;
        height: {pRightQueriesHt}cm;
        width: {rightParWd}cm;
    }}
    .par-right-answers {{
        float: left;
        /*margin-left: -20px;*/
        height: {pRightAnsHt}cm;
        width: {rightParWd}cm;
    }}
    .par-diffix {{
        float: left;
        height: {dbParHt}cm;
        width: {dbParWd}cm;
        font-size: 14px;
        overflow: auto;
        border-style: none;
    }}
    .par-native {{
        float: right;
        height: {dbParHt}cm;
        width: {dbParWd}cm;
        font-size: 14px;
        overflow: auto;
        border-style: none;
    }}
    .items-list {{
        overflow: auto;
        white-space: wrap;
        float: left;
        flex-wrap: wrap;
        height: {listHt}cm;
        width: {listWd}cm;
        border-style: groove;
        padding: {padding}px;
    }}
    textarea {{
        font-family: "Courier New", Courier, monospace;
        font-size: 14px;
        font-weight: bold;
        overflow: auto;
        resize: none;
        height: {queryHt}cm;
        width: {queryWd}cm;
    }}
    .ta-diffix {{
        background-color: #e6f7ff;
    }}
    .ta-native {{
        background-color: #f7ffe6;
    }}
    .desc-box {{
        white-space: normal;
        font-size: 18px;
        overflow:auto;
        flex-wrap:nowrap;
        height: {descHt}cm;
        width: {descWd}cm;
        margin: auto;
        border-style: none;
        background-color: #f0f0f5;
        padding: {padding}px;
        padding-left: 20px;
        text-indent: -20px
    }}
    dd {{
      margin-left: 10px;
      padding-left: 20px;
      text-indent: -20px
    }}
    img {{
      width: {logoWd}cm;
      vertical-align:top;
    }}
    .arrow-button-right {{
      color: black;
      position: relative;
      left: {rightArrowLeft}cm;
      top: {rightArrowTop}cm;
      background-color: white;
      border-style: none;
      font-size: 24px;
      font-weight: bold;
    }}
    .arrow-button-left {{
      color: black;
      position: relative;
      left: {leftArrowLeft}cm;
      top: {leftArrowTop}cm;
      background-color: white;
      border-style: none;
      font-size: 24px;
      font-weight: bold;
    }}
    .button {{
      border: none;
      font-size: 20;
      cursor: pointer;
      border-radius: 8px;
      box-shadow: 0 4px #999;
    }}
    .button:hover {{background-color: DarkGreen}}
    .button:active {{
      background-color: #0000FF;
      box-shadow: 0 5px #666;
      transform: translateY(4px);
    }}
    .button-run {{
      background-color: #39C629;
      color: white;
    }}
    .button-cancel {{
      background-color: #D1D1E0;
      color: black;
    }}
    p.desc {{
      margin-top: 0;
      margin-bottom: 0;
      padding-left: 10px;
      test-indent: -10px;
    }}
    a.list {{
      text-decoration: none;
      target: none;
    }}
    a:link {{
      color: black;
    }}
    a:visited {{
      color: black;
    }}
    a:hover {{
      color: red;
    }}
    a:active {{
      color: red;
    }}
    table.trusted {{
      table-layout: fixed;
      width: {diffixTabWd}cm;
      border: 1px solid blue;
      text-overflow: clipped;
    }}
    table.untrusted {{
      table-layout: fixed;
      width: {diffixTabWd}cm;
      border: 1px solid blue;
      text-overflow: clipped;
    }}
    table.native {{
      table-layout: fixed;
      width: {nativeTabWd}cm;
      border: 1px solid green;
      text-overflow: clipped;
    }}
    tr.error {{
      background-color: #ffcccc;
      border-left: 2px solid black;
    }}
    tr.native:nth-child(even) {{
      background-color: #f7ffe6;
    }}
    td.trusted {{
      font-size: 14px;
      border-bottom: 1px solid #1aa3ff;
      text-overflow: clipped;
    }}
    td.untrusted {{
      font-size: 14px;
      border-bottom: 1px solid #1aa3ff;
      text-overflow: clipped;
    }}
    td.native {{
      font-size: 14px;
      border-bottom: 1px solid #99e600;
      text-overflow: clipped;
    }}
    td.error {{
      font-size: 14px;
      border-bottom: 1px solid #99e600;
      background-color: #ffcccc;
      text-overflow: clipped;
      border-left: 2px solid black;
      border-bottom: 1px solid #e60000;
      border-top: 1px solid #e60000;
    }}
    th.trusted {{
      white-space: wrap;
      text-align: left;
      font-size: 16px;
      background-color: #e6f7ff;
    }}
    th.untrusted {{
      white-space: wrap;
      text-align: left;
      font-size: 16px;
      background-color: #e6f7ff;
    }}
    th.native {{
      white-space: wrap;
      text-align: left;
      font-size: 16px;
      background-color: #f7ffe6;
    }}
    th.error {{
      white-space: wrap;
      text-align: left;
      font-size: 16px;
      background-color: #ffcccc;
      border-left: 2px solid black;
      border-bottom: 1px solid #e60000;
      border-top: 1px solid #e60000;
    }}
    </style>

    <br><br><br>
    <div class="par">
      <div class="par-left">
           <center>
           <a target=_self href="/refresh">
               <img src="logos.png" alt="" style="vertical-align:top">
           </a>
           <font size="6" color="#0099cc"> 
           Training App
           </font>
           </center>
           <div class="items-list">{s['exampleHtml']}</div>
      </div>
      <div class="par-right">
        <div class="par-right-desc">
          <div class="desc-box">{s['description']}</div>
        </div>
        <div class="par-right-queries">
            <button class="arrow-button-right" type="submit">
              &#62;
            </button>
            <button class="arrow-button-left" type="submit">
              &#60;
            </button>
            <br>
            Diffix SQL
            <span style="display:inline-block; width: {spaceWd}cm;"></span>
            Native SQL
            <form action = "/run" method="POST"
              enctype="multipart/form-data">
              <textarea class="ta-diffix" name = "diffix"
                  wrap="hard">{s[diffixSys]['sql']}</textarea>
              &nbsp; &nbsp; &nbsp;
              <textarea class="ta-native" name = "native"
                  wrap="hard">{s['native']['sql']}</textarea>
               <br>
               <button class="button button-run" type="submit">
                 Run
               </button>
               &nbsp&nbsp&nbsp&nbsp
               &nbsp&nbsp&nbsp&nbsp
               Database:{s['dbHtml']}
               &nbsp&nbsp&nbsp&nbsp
               &nbsp&nbsp&nbsp&nbsp
               Trust Mode:{s['modeHtml']}
            </form>
        </div>
        <div class="par-right-answers">
          <div class="par-diffix">
              {s[diffixSys]['ansHtml']}
          </div>
          <div class="par-native">
              {s['native']['ansHtml']}
          </div>
        </div>
      </div>
    </div>
    '''
    return html

def getHeaderList(exList):
    headerList = []
    for i in range(len(exList)):
        ex = exList[i]
        if len(ex['diffix']['sql']) == 0:
            headerList.append(i)
    headerList.append(10000000000)
    return headerList

def makeExamplesHtml():
    user = getCookie()
    s = loadUserState(user)
    headerList = getHeaderList(s['exampleList'])
    html = '''<dl>'''
    curHead = 0
    blue = s['example']
    for i in range(len(s['exampleList'])):
        if i == headerList[curHead+1]:
            curHead += 1
        ex = s['exampleList'][i]
        if (len(ex['diffix']['sql']) > 0 and
                (blue < headerList[curHead] or
                    blue >= headerList[curHead+1])):
            # This is not a header, and we don't want to list it
            continue
        end = ''
        if len(ex['diffix']['sql']) == 0:
            start = '''<dt><strong>'''
            end = '''</strong>'''
        else:
            start = '''<dd>'''
        html += f'''{start}<a class="list" href="/example/{i}">'''
        if i == s['example']:
            html += '''<font color="blue">'''
        html += f'''{ex['heading']}'''
        if i == s['example']:
            html += '''</font>'''
        html += f'''</a>{end}'''
    html += '''</dl>'''
    s['exampleHtml'] = html
    return

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def computeErrors():
    user = getCookie()
    s = loadUserState(user)
    diffixSys = s['mode']
    # This routine assume that the last native column is the measure, and the
    # previous columns are the values
    if s['native']['colInfo'] is None or s[diffixSys]['colInfo'] is None:
        return
    if s['native']['colInfo'][0] != s[diffixSys]['colInfo'][0]:
        return
    numValCols = len(s['native']['colInfo']) - 1
    #if numValCols <= 0:
        #return
    for i in range(numValCols):
        if s['native']['colInfo'][i] != s[diffixSys]['colInfo'][i]:
            return
    measureIndex = numValCols
    diffixDict = {}
    for row in s[diffixSys]['ans']:
        key = ''
        for i in range(numValCols):
            key += str(row[i]) + ':::'
        if is_number(row[measureIndex]) is False:
            return
        diffixDict[key] = row[measureIndex]
    newAns = []
    for i in range(len(s['native']['ans'])):
        row = s['native']['ans'][i]
        newRow = []
        for val in row:
            newRow.append(val)
        key = ''
        for i in range(numValCols):
            key += str(row[i]) + ':::'
        if key in diffixDict:
            cVal = diffixDict[key]
            nVal = row[measureIndex]
            if is_number(row[measureIndex]) is False:
                return
            absError = round((nVal - cVal),2)
            maxVal = max([abs(nVal),abs(cVal)])
            if maxVal == 0:
                relError = '---'
            else:
                relError = round((abs(nVal-cVal) / maxVal)*100,2)
            newRow.append(f'''{absError}, {relError}%''')
        else:
            newRow.append('')
        newAns.append(newRow)
    # Now add new column to native table
    colInfo = list(s['native']['colInfo'])
    colInfo.append('abs,rel')
    s['native']['colInfo'] = colInfo
    s['native']['ans'] = newAns
    return

def makeAnswerHtml(sys):
    user = getCookie()
    s = loadUserState(user)
    html = "<br>"
    html += f'''{s[sys]['numRows']} rows in {s[sys]['duration']} seconds'''
    if s[sys]['cached'] is True:
        html += ''' (Cached result)<br>'''
    else:
        html += '''<br>'''
    if s[sys]['err'] is not None and len(s[sys]['err']) > 5:
        errMsg = str(s[sys]['err'])
        errMsg = errMsg.replace('\n','<br>')
        html += f'''<hr><font color="red">{errMsg}</font>'''
        s[sys]['ansHtml'] = html
        return
    if s[sys]['colInfo'] is None:
        s[sys]['ansHtml'] = ''
        return
    print(f"{sys}: {html}")
    html += f'''<table class="{sys}">'''
    html += '''<tr>'''
    for col in s[sys]['colInfo']:
        if col == 'abs,rel':
            html += f'''<th class="error">{col}</th>'''
        else:
            html += f'''<th class="{sys}">{col}</th>'''
    html += '''</tr>'''
    for row in s[sys]['ans']:
        html += '''<tr>'''
        for i in range(len(row)):
            val = row[i]
            if s[sys]['colInfo'][i] == 'abs,rel':
                html += f'''<td class="error">{val}</td>'''
            else:
                html += f'''<td class="{sys}">{val}</td>'''
            pass
        html += '''</tr>'''
    html += '''</table>'''
    if len(s[sys]['notices']) > 5:
        html += f'''<hr><font color="red">{s[sys]['notices']}</font>'''
    s[sys]['ansHtml'] = html
    return

def readFromCache(s,user):
    (conn,c) = validateAndGetCursor()
    for sys in ['native','trusted','untrusted']:
        s[sys]['cached'] = False
        sql = s[sys]['sql']
        key = makeKeyFromSql(sql)
        query = f'''SELECT ans, err, colInfo, rows, duration, notices
                FROM cache
                WHERE query = '{key}' AND sys = '{sys}';'''
        c.execute(query)
        ans = c.fetchall()
        if len(ans) == 0:
            # no hit, do nothing
            continue
        # add 'err'
        s[sys]['ans'] = simplejson.loads(ans[0][0])
        s[sys]['err'] = ans[0][1]
        s[sys]['colInfo'] = simplejson.loads(ans[0][2])
        s[sys]['numRows'] = ans[0][3]
        s[sys]['duration'] = ans[0][4]
        s[sys]['notices'] = ans[0][5]
        s[sys]['cached'] = True
        global us
        #pp.pprint(us[user])
    return

def smartRound(val):
    for i in [2,3,4,5,6]:
        rounded = round(val,i)
        asString = str(rounded)
        if asString[-2:] == '00':
            rounded = round(val,i-1)
            return rounded
    return rounded

def setPrecision(ans):
    newAns = []
    for row in ans:
        newRow = []
        for cell in row:
            if isinstance(cell, float) or isinstance(cell, decimal.Decimal):
                newRow.append(smartRound(cell))
            elif isinstance(cell, datetime.datetime):
                newRow.append(str(f"{cell}"))
            else:
                newRow.append(cell)
        newAns.append(newRow)
    return newAns

def makeKeyFromSql(sql):
    sql = sql.replace('\n',' ')
    sql = sql.replace('\r',' ')
    return hashlib.sha1(sql.encode('utf-8')).hexdigest()

def entryIsInCache(sys,key):
    (conn,c) = validateAndGetCursor()
    check = f'''SELECT count(*) FROM cache
            WHERE query = '{key}' AND
                  sys = '{sys}'; '''
    c.execute(check)
    ans = c.fetchall()
    if ans[0][0] == 1:
        # already in cache
        return True
    return False

def deleteCacheEntry(ex,sys):
    if len(ex[sys]['sql']) == 0:
        return
    sql = ex[sys]['sql']
    key = makeKeyFromSql(sql)
    if not entryIsInCache(sys,key):
        return
    (conn,c) = validateAndGetCursor()
    check = f'''DELETE FROM cache
            WHERE query = '{key}' AND
                  sys = '{sys}'; '''
    c.execute(check)
    conn.commit()
    return

def addExampleToCache(s,ex,sys):
    (conn,c) = validateAndGetCursor()
    html = ''
    job = []
    s['dbname'] = ex['dbname']
    s['mode'] = ex['mode']
    if len(ex[sys]['sql']) == 0:
        return html
    sql = ex[sys]['sql']
    html += f'''Check sql {sql}<br>'''
    key = makeKeyFromSql(sql)
    if entryIsInCache(sys,key):
        html += f'''   Already in cache<br>'''
        return html
    # Not in cache, so do lookup
    job.append(gevent.spawn(doQuery,[sys,sql,s]))
    gevent.wait(job)
    newAns = setPrecision(s[sys]['ans'])
    ansStr = simplejson.dumps(newAns)
    colInfoStr = simplejson.dumps(s[sys]['colInfo'])
    if s[sys]['err']:
        errMsg = s[sys]['err'].replace("'","''")
        if 'expectErr' not in ex or ex['expectErr'] == False:
            # We don't expect to get an error, so don't cache anything.
            # In this way, we will try this cache entry again next time.
            html += f'''    <font color="red">FAILED</font><br>'''
            return html
    else:
        errMsg = s[sys]['err']
    insert = f'''INSERT INTO cache VALUES (
              '{key}',
              '{sys}',
              '{ansStr}',
              '{errMsg}',
              '{colInfoStr}',
              {s[sys]['numRows']},
              {s[sys]['duration']},
              '{s[sys]['notices']}');
            '''
    print(insert)
    c.execute(insert)
    conn.commit()
    html += '''   Committed<br>'''
    return html

def populateCache():
    # make a fake user from which to run the queries
    html = ''
    s = copy.deepcopy(initClientState)
    s['exampleList'] = getExampleList()
    for ex in s['exampleList']:
        for sys in ['native','trusted','untrusted']:
            html += addExampleToCache(s,ex,sys)
    return html

def doQuery(params):
    sys = params[0]
    sql = params[1]
    s = params[2]
    print(f"doQuery: {sys}")
    print("SQL is:")
    print(sql)
    # Not 100% sure why the following is necessary. Without it, though,
    # there isn't white-space between SQL objects and so the query fails
    sql = sql.replace('\n','\n ')
    sql = sql.replace('\r','\n ')
    connStr = f'''
            host={ss[sys]['host']}
            port={ss[sys]['port']}
            dbname={s['dbname']}
            user={ss[sys]['user']}
            password={ss[sys]['password']}
            '''
    #print(connStr)
    conn = psycopg2.connect(connStr, async_=1)
    while True:
        try:
            state = conn.poll()
        except (psycopg2.Error, psycopg2.ProgrammingError, psycopg2.OperationalError) as e:
            end = time.perf_counter()
            error = str(f"{e}")
            s[sys]['err'] = error
            s[sys]['duration'] = 0
            if s[sys]['conn']:
                s[sys]['conn'].close()
            s[sys]['conn'] = None
            return
        if state == psycopg2.extensions.POLL_OK:
            break
        gevent.sleep(0.05)
    s[sys]['conn'] = conn
    cur = conn.cursor()
    start = time.perf_counter()
    s[sys]['ans'] = []
    s[sys]['numRows'] = 0
    s[sys]['colInfo'] = None
    s[sys]['err'] = None
    try:
        cur.execute(sql)
    except (psycopg2.Error, psycopg2.ProgrammingError, psycopg2.OperationalError) as e:
        end = time.perf_counter()
        print(f"Error is '{e}'")
        s[sys]['err'] = e
        s[sys]['duration'] = round(end - start,3)
        s[sys]['conn'].close()
        s[sys]['conn'] = None
        return
    while True:
        try:
            state = conn.poll()
        except (psycopg2.Error, psycopg2.ProgrammingError) as e:
            end = time.perf_counter()
            error = str(f"{e}")
            s[sys]['err'] = error
            s[sys]['duration'] = round(end - start,3)
            s[sys]['conn'].close()
            s[sys]['conn'] = None
            return
        if state == psycopg2.extensions.POLL_OK:
            break
        gevent.sleep(0.05)
    s[sys]['numRows'] = cur.rowcount
    s[sys]['colInfo'] = [desc[0] for desc in cur.description]
    cur.itersize = maxNumRows
    cnt = 0
    for row in cur:
        s[sys]['ans'].append(row)
        cnt += 1
        if cnt >= maxNumRows:
            break
        pass
    #pp.pprint(s[sys]['ans'])
    #pp.pprint(s[sys]['colInfo'])
    end = time.perf_counter()
    s[sys]['notices'] = ''
    if len(s[sys]['conn'].notices):
        # There are notices
        for notice in s[sys]['conn'].notices:
            if '[Debug]' in notice:
                continue
            s[sys]['notices'] += notice
    s[sys]['ans'] = setPrecision(s[sys]['ans'])
    s[sys]['duration'] = round(end - start,3)
    s[sys]['conn'].close()
    s[sys]['conn'] = None
    return

def reloadExamples():
    user = getCookie()
    s = loadUserState(user)
    from demoConfig import getExampleList
    s['exampleList'] = getExampleList()
    makePulldowns()
    makeExamplesHtml()
    return

def clearCache():
    global ss
    db = ss['dbPath']
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS cache''')
    conn.close()
    buildDatabase()
    return

def buildDatabase():
    global ss
    db = ss['dbPath']
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cache
             (query text, 
             sys text,
             ans text,
             err text,
             colInfo text,
             rows integer, 
             duration real,
             notices text);
             ''')
    c.execute('''CREATE TABLE IF NOT EXISTS users
             (cookie text, example int, name text, org text)''')
    conn.close()
    return

def makeDbConnection():
    global ss
    db = ss['dbPath']
    ss['conn'] = sqlite3.connect(db)
    ss['cursor'] = ss['conn'].cursor()
    return

def connectDatabase():
    global ss
    db = ss['dbPath']
    conn = sqlite3.connect(db)
    c = conn.cursor()
    ss['conn'] = conn
    ss['cursor'] = c
    if (not isinstance(ss['conn'], sqlite3.Connection) or
            not isinstance(ss['cursor'], sqlite3.Cursor)):
        # Should absolutely never happen....
        print("Failed to connect to training.db")
        quit()
    return

def loadUserState(user):
    global us
    if user is None:
        redirect('/')
    if user in us:
        # already loaded
        return us[user]
    s = copy.deepcopy(initClientState)
    s['example'] = getUserExample(user)
    if s['example'] is None:
        s['example'] = 0
    us[user] = s
    return s

def validateAndGetCursor():
    global ss
    if (not isinstance(ss['conn'], sqlite3.Connection) or
            not isinstance(ss['cursor'], sqlite3.Cursor)):
        connectDatabase()
    return(ss['conn'],ss['cursor'])

def getUserExample(user):
    (conn,c) = validateAndGetCursor()
    sql = f'''SELECT example FROM users WHERE cookie = '{user}';'''
    try:
        c.execute(sql)
    except sqlite3.Error as er:
        print('er:', er.message)
        return None
    ans = c.fetchall()
    if len(ans) == 0:
        return None
    return ans[0][0]

def putUserExample(user,example):
    (conn,c) = validateAndGetCursor()
    sql = f'''UPDATE users SET example = '{example}' WHERE cookie = '{user}';'''
    try:
        c.execute(sql)
    except sqlite3.Error as er:
        print('er:', er.message)
    conn.commit()
    return

def makeNewCookieValue():
    while True:
        user = str(f"{random.randint(0,100000000000000000)}")
        example = getUserExample(user)
        if example is None:
            break
        else:
            print(f"Never expected to get a collision! ({user})")
    return user

def getCookie():
    # This is called after the cookie has been set, so we either expect
    # a cookie, or (if cookies disabled or no consent) we'll use the IP
    # address
    cookie = request.get_cookie("user_id")
    if cookie is None:
        ip = request.environ.get('REMOTE_ADDR')
        cookie = hashlib.sha512(ip.encode('utf-8')).hexdigest()
    return cookie

def getEnvVars():
    global ss
    dir_path = os.path.dirname(os.path.realpath(__file__))
    env = os.environ.get('DATA_DIR')
    if env is not None:
        dir_path = env
    ss['dbPath'] = os.path.join(dir_path,'training.db')
    dir_path = os.path.dirname(os.path.realpath(__file__))
    env = os.environ.get('LOG_DIR')
    if env is not None:
        dir_path = env
    ss['logPath'] = os.path.join(dir_path,'training.log')
    env = os.environ.get('NATIVE_USER')
    if env is not None:
        ss['native']['user'] = env
    env = os.environ.get('NATIVE_PASS')
    if env is not None:
        ss['native']['password'] = env
    env = os.environ.get('NATIVE_PORT')
    if env is not None:
        ss['native']['port'] = int(env)
    env = os.environ.get('NATIVE_HOST')
    if env is not None:
        ss['native']['host'] = env
    env = os.environ.get('TRUSTED_USER')
    if env is not None:
        ss['trusted']['user'] = env
    env = os.environ.get('TRUSTED_PASS')
    if env is not None:
        ss['trusted']['password'] = env
    env = os.environ.get('TRUSTED_PORT')
    if env is not None:
        ss['trusted']['port'] = env
    env = os.environ.get('TRUSTED_HOST')
    if env is not None:
        ss['trusted']['host'] = env
    env = os.environ.get('UNTRUSTED_USER')
    if env is not None:
        ss['untrusted']['user'] = env
    env = os.environ.get('UNTRUSTED_PASS')
    if env is not None:
        ss['untrusted']['password'] = env
    env = os.environ.get('UNTRUSTED_PORT')
    if env is not None:
        ss['untrusted']['port'] = env
    env = os.environ.get('UNTRUSTED_HOST')
    if env is not None:
        ss['untrusted']['host'] = env

@route('/refresh')
def doRefresh():
    user = getCookie()
    s = loadUserState(user)
    s['example'] = 0
    s['exampleHtml'] = ''
    s['exampleList'] = []
    redirect("/example/0")

@route('/consent')
def doConsent():
    user = getCookie()
    msg = str(f"Consent with cookie: {user}")
    logging.info(msg)
    (conn,c) = validateAndGetCursor()
    name = ''
    org = ''
    sql = f'''INSERT INTO users VALUES('{user}', 0, '{name}', '{org}');'''
    c.execute(sql)
    conn.commit()
    s = loadUserState(user)
    redirect("/training")

@route('/populateCache')
def doPop():
    return populateCache()

@route('/clearCache')
def doClear():
    clearCache()
    return("Cache cleared")

@route('/training')
def doDemo():
    # It can happen that a user starts with the '/training' URL because it was
    # cut-and-pasted from another user. So we want to check if there is a cookie
    # already and if not send the user to the consent page
    cookie = request.get_cookie("user_id")
    if cookie is None:
        redirect("/")
    user = getCookie()
    s = loadUserState(user)
    if len(s['exampleHtml']) == 0:
        reloadExamples()
        redirect("/example/0")
    return(makeHtml())

@route('/cache/<index>')
def doCache(index):
    index = int(index)
    html = ''
    s = copy.deepcopy(initClientState)
    s['exampleList'] = getExampleList()
    if index < 0 or index >= len(s['exampleList']):
        return("Bad example number")
    ex = s['exampleList'][index]
    for sys in ['native','trusted','untrusted']:
        deleteCacheEntry(ex,sys)
        html += addExampleToCache(s,ex,sys)
    return html

@route('/example/<index>')
def updateExample(index):
    user = getCookie()
    s = loadUserState(user)
    index = int(index)
    s['example'] = index
    putUserExample(user,index)
    makeExamplesHtml()
    if len(s['exampleList']) == 0:
        reloadExamples()
    ex = s['exampleList'][index]
    diffixSys = ex['mode']
    s[diffixSys]['ansHtml'] = ''
    s['native']['ansHtml'] = ''
    s[diffixSys]['ans'] = []
    s['native']['ans'] = []
    s[diffixSys]['colInfo'] = None
    s['native']['colInfo'] = None
    s[diffixSys]['err'] = None
    s['native']['err'] = None
    s['description'] = f'''<strong>{ex['heading']}</strong><br>'''
    s['description'] += ex['description']
    s[diffixSys]['sql'] = ex['diffix']['sql']
    s['dbname'] = ex['dbname']
    s['mode'] = ex['mode']
    makePulldowns()
    s['native']['sql'] = ex['native']['sql']
    readFromCache(s,user)
    computeErrors()
    makeAnswerHtml(diffixSys)
    makeAnswerHtml('native')
    redirect("/training")
    return

@route('/run', method='POST')
def doRun():
    user = getCookie()
    s = loadUserState(user)
    s['dbname'] = str(request.POST.get('database'))
    print(s['dbname'])
    s['mode'] = str(request.POST.get('mode'))
    print(s['mode'])
    diffixSys = s['mode']
    s[diffixSys]['ans'] = []
    s[diffixSys]['ansHtml'] = ''
    s[diffixSys]['cached'] = False
    s['native']['ans'] = []
    s['native']['ansHtml'] = ''
    s['native']['cached'] = False
    print(f"Example index is {s['example']}")
    jobs = []
    makePulldowns()
    for sys in ['native',s['mode']]:
        if sys == 'native':
            sql = str(request.POST.get(sys))
        else:
            sql = str(request.POST.get('diffix'))
        s[sys]['sql'] = sql
        if len(sql) > 0:
            jobs.append(gevent.spawn(doQuery,[sys,sql,s]))
    if len(jobs) > 0:
        gevent.wait(jobs)
    computeErrors()
    makeAnswerHtml(diffixSys)
    makeAnswerHtml('native')
    #print(f"Process answers, diffix {s[diffixSys]['numRows']} rows,  native {s['native']['numRows']} rows")
    #print(f"Durations, diffix {s[diffixSys]['duration']} secs,  native {s['native']['duration']} secs")
    redirect("/training")

@route('/logos.png')
def send_image():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(dir_path,'logos.png')
    return static_file("logos.png", root=dir_path)

@route('/')
def welcome():
    cookie = request.get_cookie("user_id")
    if cookie is None:
        # We'll try setting a cookie here, and after the consent click
        # we'll know if the client allows cookies or not
        cookie = makeNewCookieValue()
        msg = str(f"New user with no cookie: {cookie}")
        logging.info(msg)
        # expires in about one year....
        response.set_cookie("user_id", cookie, max_age=32000000)
        return makeWelcomeHtml()
    # already has cookie, so jump right in
    loadUserState(cookie)
    redirect("/training")

getEnvVars()
# Set to DEBUG for more detail
logging.basicConfig(filename=ss['logPath'],level=logging.INFO,
        format='%(asctime)s %(message)s')
random.seed()
buildDatabase()
connectDatabase()
hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)    
port = os.environ.get('PORT')
print(port)
if port is None:
    port = 8080
else:
    port = int(port)
print("Your Computer Name is:" + hostname)    
print("Your Computer IP Address is:" + IPAddr)
trainDev = os.environ.get('TRAIN_DEV')
if trainDev is None:
    reloader = False
else:
    reloader = True
if __name__ == "__main__":
    run(host='0.0.0.0', port=port, reloader=reloader, server='gevent')
