# -*- coding: utf-8 -*-

import mwparserfromhell
import pywikibot
from pywikibot import pagegenerators
from pywikibot import textlib
import pandas as pd
import numpy as np
import requests
import re
import pickle
import pprint
import datetime
import time
import collections
import kkt3

site = pywikibot.Site('ja', 'wikipedia')
#asite=pywikibot.site.APISite('ja','wikipedia',user='Anakabot')
asite=pywikibot.site.APISite('ja','wikipedia',user='Anaka Satamiya')

###　パラメーター　####
class Pt:
    #テンプレート・パラメーター
    tem1=['cite web|和書','cite web |和書','cite web| 和書','cite web | 和書']#小文字のみ、テンプレート、{{抜き英小文字のみ、全テンプレート抽出は''のみ
    #tem1=['defaultsort','デフォルトソート']#小文字のみ、テンプレート、{{抜き英小文字のみ、全テンプレート抽出は''のみ
    par1=['language=']#固定引数リストアップ・ふるい分けする引数英小文字のみ
    par2=['deadlink=','deadlinkdate=','coauthors=','website=','ref=','date=','accessdate=']#変動引数リストアップ・引数英小文字のみ
    par3=par1+par2
    tempa1=[tem1, par3] # テンプレート、引数用
    tempa2=[tem1, par1, par2] # テンプレート、固定・変動引数用

list_00=kkt3.kk3[70000:70050]

###　必須関数　####
c_d = {'cyan':'\033[96m', 'magenta':'\033[95m', 'yellow':'\033[33m', 'green':'\033[92m', 'red':'\033[91m', 'blue':'\033[94m', 'on_cyan':'\033[37m\033[46m', 'on_magenta':'\033[37m\033[45m', 'on_yellow':'\033[37m\033[43m', 'on_green':'\033[37m\033[42m', 'on_red':'\033[37m\033[41m', 'on_blue':'\033[37m\033[44m','on_grey':'\033[30m\033[47m', 'end':'\033[0m'}

def cprint(word,k):  # カラー印刷
    if k=='red':
        k1= '\033[31m' # (文字)赤
    elif k=='green':
        k1= '\033[32m' # (文字)緑
    elif k=='yellow':
        k1= '\033[33m' # (文字)黄
    elif k=='blue':
        k1= '\033[34m' # (文字)青 
    elif k=='magenta':
        k1= '\033[35m' # (文字)マゼンタ
    elif k=='cyan':
        k1= '\033[36m' # (文字)シアン
    elif k=='on_cyan':
        k1='\033[37m\033[46m' # (文字)白背景シアン
    elif k=='on_magenta':
        k1='\033[37m\033[45m' # (文字)白背景シアン
    elif k=='on_yellow':
        k1='\033[37m\033[43m' # (文字)白背景イエロー
    elif k=='on_green':
        k1='\033[37m\033[42m' # (文字)白背景グリーン
    elif k=='on_red':
        k1='\033[37m\033[41m' # (文字)白背景レッド
    elif k=='on_blue':
        k1='\033[37m\033[44m' # (文字)白背景ブルー
    elif k=='on_grey':
        k1='\033[30m\033[47m' # (文字)白背景グレー
    else:
        k1='\033[30m' # 黒
    print(k1+str(word)+'\033[0m')

def col(word,k):  # カラー印刷
    if k=='red':
        k1= '\033[31m' # (文字)赤
    elif k=='green':
        k1= '\033[32m' # (文字)緑
    elif k=='yellow':
        k1= '\033[33m' # (文字)黄
    elif k=='blue':
        k1= '\033[34m' # (文字)青 
    elif k=='magenta':
        k1= '\033[35m' # (文字)マゼンタ
    elif k=='cyan':
        k1= '\033[36m' # (文字)シアン
    elif k=='on_cyan':
        k1='\033[37m\033[46m' # (文字)白背景シアン
    elif k=='on_magenta':
        k1='\033[37m\033[45m' # (文字)白背景シアン
    elif k=='on_yellow':
        k1='\033[37m\033[43m' # (文字)白背景イエロー
    elif k=='on_green':
        k1='\033[37m\033[42m' # (文字)白背景グリーン
    elif k=='on_red':
        k1='\033[37m\033[41m' # (文字)白背景レッド
    elif k=='on_blue':
        k1='\033[37m\033[44m' # (文字)白背景ブルー
    elif k=='on_grey':
        k1='\033[30m\033[47m' # (文字)白背景グレー
    else:
        k1='\033[30m' # 黒
    return k1+word+'\033[0m'

def get_unique_list(seq): # 1・2次元配列リストタプルの重複した要素を削除し、元のリストの順番を保持するリストを生成
    seen = []
    return [x for x in seq if x not in seen and not seen.append(x)]

def get_duplicate_list(seq):# 1・2次元配列リストタプルの重複した要素を抽出し、それを元に元のリストの順番を保持する新しいリストを生成
    seen = []
    return [x for x in seq if not seen.append(x) and seen.count(x) == 2]

def get_duplicate_list_order(seq): # 1・2次元配列リストタプルの重複した要素を抽出し、それを元に元のリストの順番を保持する新しいリストを生成
    seen = []
    return [x for x in seq if seq.count(x) > 1 and not seen.append(x) and seen.count(x) == 1]

###　選択関数　####

def temp1(templates,tem,par): # テンプレート引数検索
        list2=[]
        #print(templates)
        for tem0 in tem:
            list1=[r for r in templates if r.lower().startswith('{{'+tem0)]+[r for r in templates if r.lower().startswith('{{ '+tem0)]+[r for r in templates if r.lower().startswith('{{　'+tem0)]
            for m in list1:
                z2=[]
                z0=m.params
                for pa in par:
                    z2=z2+[m for m in z0 if "=".join([r.strip() for r in str(m).split('=',1)]).startswith(pa)] 
                list2=list2+[[str(m)]+z2]
        return list2

def fprint1(s0,text,a,b,c1,c2): # 復数行位置検索
    list1=[]
    m_0=re.finditer(s0,text)
    #m_0=re.finditer(s0,text,flags=re.DOTALL)
    if m_0==[]:
        pass
    else:
        for i,m in enumerate(m_0):
            if m.start()-int(a)<0: # aよりも対象文字が前にある
                if m.end()+int(a)>len(text):
                    x1=c_d[c1]+text[0:m.start()]+ c_d["end"]
                    x2=c_d[c2]+m.group()+ c_d["end"]
                    x3=c_d[c1]+text[m.end():len(text)]+ c_d["end"]
                    list1=list1+[[m.group(),text[0:m.start()]+m.group()+text[m.end():len(text)] ,x1+x2+x3 ]]
                else:
                    x1=c_d[c1]+text[0:m.start()]+ c_d["end"]
                    x2=c_d[c2]+m.group()+ c_d["end"]
                    x3=c_d[c1]+text[m.end():m.end()+int(b)]+ c_d["end"]
                    list1=list1+[[m.group(),text[0:m.start()]+m.group()+text[m.end():m.end()+int(b)] ,x1+x2+x3 ]]
            else:
                if m.end()+int(a)>len(text):
                    x1=c_d[c1]+text[m.start()-int(a):m.start()]+ c_d["end"]
                    x2=c_d[c2]+m.group()+ c_d["end"]
                    x3=c_d[c1]+text[m.end():len(text)]+ c_d["end"]
                    list1=list1+[[m.group(),text[m.start()-int(a):m.start()]+m.group()+text[m.end():len(text)] ,x1+x2+x3 ]]
                else:
                    x1=c_d[c1]+text[m.start()-int(a):m.start()]+ c_d["end"]
                    x2=c_d[c2]+m.group()+ c_d["end"]
                    x3=c_d[c1]+text[m.end():m.end()+int(b)]+ c_d["end"]
                    list1=list1+[[m.group(),text[m.start()-int(a):m.start()]+m.group()+text[m.end():m.end()+int(b)] ,x1+x2+x3 ]]
        return list1

def diffprint1(a,b): # 差分内部表示
        listo1=[]
        listn1=[]
        listz1=[]
        p=pywikibot.PatchManager(a,b,context=0, by_letter=True, replace_invisible=False)
        p1=p.get_blocks()
        if int(p1[0][0])==-1 and int(p1[-1][0])==-1:
            for tag,o9,n9 in p1[1:-1]:
                if int(tag)==-1:
                    listo1=listo1+[c_d['yellow']+a[o9[0]:o9[1]]+c_d["end"]]
                    listn1=listn1+[c_d['yellow']+a[o9[0]:o9[1]]+c_d["end"]]
                    listz1=listz1+[c_d['yellow']+a[o9[0]:o9[1]]+c_d["end"]]
                elif int(tag)==0:
                    listo1=listo1+[c_d['red']+a[o9[0]:o9[1]]+c_d["end"]]
                    listn1=listn1+[c_d['red']+b[n9[0]:n9[1]]+c_d["end"]]
                    listz1=listz1+[c_d['red']+a[o9[0]:o9[1]]+c_d["end"]]
                elif int(tag)==1:
                    listo1=listo1+[c_d['green']+a[o9[0]:o9[1]]+c_d["end"]]
                    listn1=listn1+[c_d['green']+b[n9[0]:n9[1]]+c_d["end"]]
                    listz1=listz1+[c_d['green']+b[n9[0]:n9[1]]+c_d["end"]]
                else:
                    print(4)
        elif int(p1[0][0])==-1 and int(p1[-1][0])!=-1:
            for tag,o9,n9 in p1[1:]:
                if int(tag)==-1:
                    listo1=listo1+[c_d['yellow']+a[o9[0]:o9[1]]+c_d["end"]]
                    listn1=listn1+[c_d['yellow']+a[o9[0]:o9[1]]+c_d["end"]]
                    listz1=listz1+[c_d['yellow']+a[o9[0]:o9[1]]+c_d["end"]]
                elif int(tag)==0:
                    listo1=listo1+[c_d['red']+a[o9[0]:o9[1]]+c_d["end"]]
                    listn1=listn1+[c_d['red']+b[n9[0]:n9[1]]+c_d["end"]]
                    listz1=listz1+[c_d['red']+a[o9[0]:o9[1]]+c_d["end"]]
                elif int(tag)==1:
                    listo1=listo1+[c_d['green']+a[o9[0]:o9[1]]+c_d["end"]]
                    listn1=listn1+[c_d['green']+b[n9[0]:n9[1]]+c_d["end"]]
                    listz1=listz1+[c_d['green']+b[n9[0]:n9[1]]+c_d["end"]]
                else:
                    print(3)
        elif int(p1[0][0])!=-1 and int(p1[-1][0])==-1:
            for tag,o9,n9 in p1[0:-1]:
                if int(tag)==-1:
                    listo1=listo1+[c_d['yellow']+a[o9[0]:o9[1]]+c_d["end"]]
                    listn1=listn1+[c_d['yellow']+a[o9[0]:o9[1]]+c_d["end"]]
                    listz1=listz1+[c_d['yellow']+a[o9[0]:o9[1]]+c_d["end"]]
                elif int(tag)==0:
                    listo1=listo1+[c_d['red']+a[o9[0]:o9[1]]+c_d["end"]]
                    listn1=listn1+[c_d['red']+b[n9[0]:n9[1]]+c_d["end"]]
                    listz1=listz1+[c_d['red']+a[o9[0]:o9[1]]+c_d["end"]]
                elif int(tag)==1:
                    listo1=listo1+[c_d['green']+a[o9[0]:o9[1]]+c_d["end"]]
                    listn1=listn1+[c_d['green']+b[n9[0]:n9[1]]+c_d["end"]]
                    listz1=listz1+[c_d['green']+b[n9[0]:n9[1]]+c_d["end"]]
                else:
                    print(2)
        else:
            for tag,o9,n9 in p1:
                if int(tag)==-1:
                    listo1=listo1+[c_d['yellow']+a[o9[0]:o9[1]]+c_d["end"]]
                    listn1=listn1+[c_d['yellow']+a[o9[0]:o9[1]]+c_d["end"]]
                    listz1=listz1+[c_d['yellow']+a[o9[0]:o9[1]]+c_d["end"]]
                elif int(tag)==0:
                    listo1=listo1+[c_d['red']+a[o9[0]:o9[1]]+c_d["end"]]
                    listn1=listn1+[c_d['red']+b[n9[0]:n9[1]]+c_d["end"]]
                    listz1=listz1+[c_d['red']+a[o9[0]:o9[1]]+c_d["end"]]
                elif int(tag)==1:
                    listo1=listo1+[c_d['green']+a[o9[0]:o9[1]]+c_d["end"]]
                    listn1=listn1+[c_d['green']+b[n9[0]:n9[1]]+c_d["end"]]
                    listz1=listz1+[c_d['green']+b[n9[0]:n9[1]]+c_d["end"]]
                else:
                    print(1)
        print('置換前\n',"".join(listo1))
        print('置換後\n',"".join(listn1))
        print('置換前後\n',"".join(listz1))

def asite_search(word_1,a): # SR複数検索
    list1=[]
    list2=[]
    list3=[]
    for w1 in word_1:
        val1=input(str(w1)+'\n何番？　1: 標準のみ　2: 標準・テンプレート　3: 標準・テンプレート・カテゴリ　4：すべて　5：カテゴリのみ　6：テンプレートのみ　7：カテゴリ/テンプレートのみ　8：標準・テンプレート・カテゴリ・ポータル・索引(Wikipedia)　9：パス  ')
        if int(val1)==1:
            gen=asite.search(w1,namespaces=[0],total=int(a))
            t1=[ page.title() for page in gen ]
        elif int(val1)==2:
            gen=asite.search(w1,namespaces=[0,10],total=int(a))
            t1=[ page.title() for page in gen ]
        elif int(val1)==3:
            t2=[]
            gen=asite.search(w1,namespaces=[0,10,14],total=int(a))
            t3=[ page.title() for page in gen ]
            for r in t3:
                t2=t2+[r.title() for r in pywikibot.page.BasePage(site,r).backlinks(filter_redirects=True)]
            cprint("通常：{}".format(t3), 'green')
            cprint("リダイレクト：{}".format(t2), 'cyan')
            t1=t2+t3
        elif int(val1)==4:
            gen=asite.search(w1)
            t1=[ page.title() for page in gen ]
        elif int(val1)==5:
            gen=asite.search(w1,namespaces=[14],total=int(a))
            t1=[ page.title() for page in gen ]
        elif int(val1)==6:
            gen=asite.search(w1,namespaces=[10],total=int(a))
            t1=[ page.title() for page in gen ]
        elif int(val1)==7:
            t2=[]
            gen=asite.search(w1,namespaces=[10,14],total=int(a))
            t3=[ page.title() for page in gen ]
            for r in t3:
                t2=t2+[r.title() for r in pywikibot.page.BasePage(site,r).backlinks(filter_redirects=True)]
            cprint("通常：{}".format(t3), 'green')
            cprint("リダイレクト：{}".format(t2), 'cyan')
            t1=t2+t3
        elif int(val1)==8:
            gen1=asite.search(w1,namespaces=[0,10,14],total=int(a))
            gen3=asite.search(w1,namespaces=[100],total=int(a))
            gen2=asite.search(w1,namespaces=[4],total=int(a))
            t3=[ r for r in [ page.title() for page in gen3  if '過去ログ' not in page.title()]]
            t2=[ r for r in [ page.title() for page in gen2 ] if 'Wikipedia:索引' in r]
            cprint("Wikipedia:Potal　{}\nWikipedia:索引　{}".format(t3,t2),'red')
            t1=[ page.title() for page in gen1]+t2+t3
        else:
            gen=[]
            t1=[]
        cprint('{}個 - {}'.format(len(t1),w1), 'red')
        print(t1)
        list1=list1+t1
        nn0=record02(w1,len(t1))
        list2=list2+nn0[0]
        list3=list3+nn0[1]
    set1=set(list1)
    
    cprint("置換対象{}件。".format(len(set1)), 'red')
    for g in list2:
        cprint(g, 'red')
    for g in list3:
        cprint(g, 'red')
    return set1

def csearch01(searchpart): # ワード検索1 ランダム
    a=input('読込数指定　しない：0　　何個を入力？　')
    b=input('1　編集日時の新しい順　2　作成日時の古い順　3　リンク元の少ない順　4　ランダム　？')
    c=["last_edit_desc", "create_timestamp_asc", "incoming_links_asc", "random"][int(b)-1]

    #last_edit_desc　編集日時の新しい順
    #create_timestamp_asc　作成日時の古い順
    #incoming_links_asc　リンク元の少ない順
    #random ランダム
    S = requests.Session()
    URL = "https://ja.wikipedia.org/w/api.php"
    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srlimit":a,
        "srsearch": searchpart,
        "srsort": c,
        "srprop": "redirecttitle"
    }
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    #pprint.pprint(DATA)
    print('API個数 : ',DATA['query']['searchinfo']['totalhits'])
    pages=DATA['query']['search']
    ptitle=[ r['title'] for r in pages ]
    return ptitle

def listupold(oldnew): # oldからリストアップ
    list_0=[]
    list2=[]
    for r in oldnew:
        old0=r[0]
        word='insource:"{}" insource:/"{}"/'.format(old0,old0.replace("/","\/").replace('"','\"').replace(".","\.").replace('+','\+').replace('?','\?'))
        word='insource:"{}" '.format(old0)
        lis01=[page.title() for page in asite.search(word,namespaces=[0,10,14])]
        cprint('個数：{}  {}'.format(len(lis01),word), 'red')
        list_0=list_0+lis01
        set1=set(list_0)
        list2=list2+["{}件[https://ja.wikipedia.org/w/index.php?search={}&title=特別%3A検索&profile=advanced&fulltext=1&ns0=1&ns10=1&ns14=1 <nowiki>{}</nowiki>]。".format(len(lis01),urllib.parse.quote(word),word)]
    print('oldリスト：',[r[0] for r in oldnew])
    cprint("{{BOTREQ|調査中}}　対象記事"+",".join(list2), 'red')
    return list(set1), [ r[0].replace("/","\/").replace('"','\"').replace(".","\.").replace('+','\+').replace('?','\?') for r in oldnew ]

def move01(oldnew): # 移動リダイレクト有り
    for i,r in enumerate(oldnew):
        old=r[0]
        browser1(old)
        new=r[1]
        cprint(str(i)+ '—残り'+str(len(oldnew)-i)+'   '+str(old)+ '————', 'red')
        try:
            page6 = pywikibot.page.BasePage(site,old,ns=0)
            page6.move(new, summary, movetalk=True, noredirect=False)
        except Exception as e:
            print(old, '—',e)
    time.sleep(120)
    for i,r in enumerate(oldnew):
        old=r[0]
        new=r[1]
        cprint(str(i)+ '—残り'+str(len(oldnew)-i)+'   '+str(old)+ '————', 'red')
        try:
            page6 = pywikibot.page.BasePage(site,old,ns=0)
            page6.moved_target()
            cprint('\t移動成功', 'on_red')
        except Exception as e:
            print(new, '—',e)
    print('終了')

def result01(list_0): # result検索
    for i,title in enumerate(list_0):
        cprint(str(i)+ '—残り'+str(len(list_0)-i)+'   '+title+ '————', 'red')
        try:
            page = pywikibot.page.BasePage(site, title)
            text = page.get(force=True, get_redirect=True)
            #text=page.getOldVersion(98608713, force=False)
            result = textlib.extract_sections(text, site)
            #cprint(result.header, 'green')
            #cprint(result.sections, 'yellow')
            #cprint(result.footer, 'cyan')
            md=[[re.sub("^=*|=*$","",m[0]).strip(), m[1]] for m in result.sections ]
            print(md[-1])
            print(str(result.footer))
        except Exception as e:
            print(title, '—',e)
    print('終了')

def result02(list_0): # result検索
    for i,title in enumerate(list_0):
        cprint(str(i)+ '—残り'+str(len(list_0)-i)+'   '+title+ '————', 'red')
        try:
            page = pywikibot.page.BasePage(site, title)
            text = page.get(force=True, get_redirect=True)
            #text=page.getOldVersion(98608713, force=False)
            result = textlib.extract_sections(text, site)
            cprint(result.header, 'green')
            cprint(result.sections, 'yellow')
            cprint(result.footer, 'cyan')
            md=[re.sub("^=*|=*$","",m[0]).strip() for m in result.sections ]
            md1=[m[1] for m in result.sections ]
            for i,d1 in enumerate(md):
                print(i,' - ',d1)
            vv1=input('何番の節文章を選択？　')
            mdtext1=md1[int(vv1)]
            old_mdtext1=mdtext1
            print(mdtext1)
            p1=re.findall("\|\|-[0-9]*\.[0-9]*",mdtext1)
            p2=[[r,'{{Hs|'+r[2:]+'}}▲'+r[3:] ] for r in p1]
            for m in p2:
                old=m[0]
                new=m[1]
                mdtext1=OLDNEW01(mdtext1.P2)
            text=text.replace(old_text1,mdtext1)
            oldnew02(old_text,text)
        except Exception as e:
            print(title, '—',e)
    print('終了')

    

class Templistup: # テンプレートの検索と置換
    
    """テンプレートの検索と置換"""
    def listup(self,list_0,tem1):
        list1=[]
        set1=set()
        set2=set()
        for i,title in enumerate(list_0):
            list_2=[]
            #cprint('\n'+str(i)+ '—残り'+str(len(list_0)-i)+'   '+title+ '————', "on_red")
            try:
                page = pywikibot.Page(site, title)
                text = page.get(force=True, get_redirect=True)
                old_text=text
                wikicode = mwparserfromhell.parse(text)
                templates = wikicode.filter_templates()
                for te1 in tem1:
                    list_2=list_2+[r for r in templates if r.lower().startswith('{{'+te1)]+[r for r in templates if r.lower().startswith('{{ '+te1)]+[r for r in templates if r.lower().startswith('{{　'+te1)]
                list_k1=[g for g in list_2 if not '和書' in g ]
                list_k2=[g for g in list_2 if '和書' in g ]
                list_1=list_k1+list_k2
                if list_1==[]:
                    set2.add(title)
                else:
                    list1=list1+list_1
            except Exception as e:
                print(title, '—',e)
        cprint("\n対象テンプレート無し：{} 個 - \t{}".format(len(set2),set2), 'yellow')
        cprint("\n対象テンプレートあり：{} 個 - \t{}".format(len(set1),set1), 'yellow')
        return set1,list1
    
    def tlistup03(self,list_0,tempa2): # {{テンプレート}}親引数子引数抽出
        list1=list2=list3=list4=list5=list6=list7=list8=list9=list10=[]
        set1=set()
        set3=set()
        tem1=tempa2[0]
        pa1=tempa2[1]
        pa2=tempa2[2]
        t1=bz.listup(list_0,tem1)
        title=t1[0]
        list_1=t1[1]
        #テンプレート分析
        for i,m in enumerate(list_1):
            list7=list9=[]
            m0=str(m)
            #cprint(m0, 'yellow')
            n1=str(m.name).strip()
            list2=list2+[n1]
            #cprint(str(i)+'-残り'+str(len(list_1)-i)+' - '+str(n1),'on_blue')
            z0=m.params
            #print(z0)
            list1=list1+[[title,m0,n1,z0]]
            for r in z0:
                
                if len(str(r).split('=',1))==2:
                    k1=str(r).split('=',1)[0].strip() # キー
                    v1=str(r).split('=',1)[1].strip() # 値
                    if v1=="":
                        list3=list3+[k1]
                    else:
                        list4=list4+[k1]
                        for p in pa1:
                            #print(p,pa1)
                            if p==k1+'=':
                                if 'ja' in v1 or 'ja-JP' in v1 or '日本語' in v1 or 'jp' in v1 or 'Japanese' in v1:
                                    list7=list7+[]
                                    #print('nasi')
                                else:
                                    list7=list7+[r]
                                    set3.add(str(r))
                                    #print('ari')
                    for p in pa2:
                        if p==k1+'=':
                            list9=list9+[r]
                        else:
                            pass
                elif str(r).strip()=='和書':
                    list5=list5+[ str(r) ]
                else:
                    list6=list6+[ str(r) ]
            #print('list7',list7)
            if list7==[]:
                list10=list10+[m,list9]
            else:
                list8=list8+[m,list7+list9]

        #for k in list1:
        #    cprint(k[0], 'red')
        #    cprint(k[1], 'yellow')
        #    cprint(k[2], 'cyan')
        #    cprint(k[3], 'blue')
        print('')
        print('テンプ全数：',len(list1),' 和書：',len(list5),' 洋書：',len(list1)-len(list5))
        print('\n--不明引数 : ', list6)
        # ひな形テンプレート作成
        set1=set(list2) # name
        set2=set(list3+list4) # parametor
        pprint.pprint(collections.Counter(list2)) # テンプ名別
        pprint.pprint(collections.Counter(list4)) # 引数（キー）別
        print('\n--空白引数の数')
        pprint.pprint(collections.Counter(list3)) # 引数（キー）別
        print('language : ')
        pprint.pprint(sorted(set3)) # 引数（キー値）別
        #for m in sorted(set3):
        #    cprint(m, 'yellow')
        #for i in range(0,len(list10),2):
        #    cprint(list10[i], 'green')
        #    cprint(list10[i+1], 'cyan')
        for i in range(0,len(list8),2):
            cprint(list8[i], 'yellow')
            cprint(list8[i+1], 'blue')
        print('終了')
        return list1


##プログラム開始　####
bz=Templistup()
bz.tlistup03(list_00,Pt.tempa2)

cprint(datetime.datetime.now(), 'blue')
cprint('全終了', 'red')
