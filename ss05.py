# -*- coding: utf-8 -*-

import mwparserfromhell
import pywikibot
import requests
import re
import pprint
import datetime
import time
import regex
import sys
import kkt1
import kkt2

site = pywikibot.Site('ja', 'wikipedia')
asite=pywikibot.site.APISite('ja','wikipedia',user='Anakabot')

###　パラメーター　####

summary="Bot作業依頼#Cite webの和書引数追加"
tem1=['cite web']#小文字のみ、テンプレート、{{抜き英小文字のみ、全テンプレート抽出は''のみ


###　LIST、OLDNEW　####
args = sys.argv
a1=args[0]
a2=args[1]
list_0=kkt1.kk1[a1:a2]

###　必須関数　####


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

###　選択関数　####

def exturlusage(url): # 
    p1=asite.exturlusage(url,namespaces=0)
    p2=[ [m.title(),[g for g in m.extlinks() if url in g]] for m in p1]
    return p2
    
def record01(start0,list1): # 置換結果記録
    time.sleep(30)
    end0 = int(time.time() - start0)
    print(start0)
    print(end0)
    p1=len(list1)
    print('処理無し')  if p1==0 else print('処理件数',p1,'処理総時間',datetime.timedelta(seconds=end0),'　1件当たり',round(end0/p1),'秒')
    dt_end = datetime.datetime.utcnow().strftime('%Y/%m/%d%H:%M:%S')
    end1=str(dt_end).replace('/','').replace(':','')
    cprint("\n{{BOTREQ|済}}　作業終了。{{利用者の投稿記録リンク|Anakabot|"+"{}|{}|text=編集記録:{}件".format(p1,end1,p1)+"}}。[ <nowiki></nowiki>]0件により取りこぼし無しと判断。よろしければ{{t|確認}}の貼り付けをお願いします。", 'red')


def hantei01(title): # タイトルから記事種別判定検索
    try:
        page = pywikibot.page.BasePage(site, title)
        text = page.get()
        return 1,title
    except pywikibot.exceptions.NoPageError as ne:
        return 2,title
    except pywikibot.exceptions.IsRedirectPageError as ir:
        return 3,page.getRedirectTarget().title()
    except Exception as e:
        return e

def hantei02(list_0): # リストから記事種別判定検索
    set1=set()
    set2=set()
    set3=set()
    for i,title in enumerate(list_0):
        cprint(str(i)+ '—残り'+str(len(list_0)-i)+'   '+title+ '————', 'red')
        p1=hantei01(title)
        if int(p1[0])==1:
            set1.add(title)
        elif int(p1[0])==2:
            set2.add(title)
        elif int(p1[0])==3:
            set3.add(p1[1])
        else:
            cprint(p1, 'cyan')
    print('\n存在',len(set1),set1,sep="\n")
    print('\n存在しない',len(set2),set2,sep="\n")
    print('\nリダイレクト存在',len(set3),set3,sep="\n")
    return set1,set2,set3

def t01(n): # 英字以外
    g1=n.split('=',1)[1]
    p1 = re.compile('[\u3041-\u309F]+')#ひらがな
    p2 = re.compile('[\u30A1-\u30FF]+')#全角片仮名
    p3 = re.compile('[\uFF66-\uFF9F]+')#半角片仮名
    p4 = regex.compile(r'\p{Script=Han}+')#漢字
    #p5 = re.compile('[\uAC00-\uD7A0]+')#ハングル
    #p6 = re.compile('[\uFF66-\uFF9F]+')#中国語
    if p1.search(g1) is None and p2.search(g1) is None and p3.search(g1) is None and p4.search(g1) is None:
        print('英字のみ : ',n)
        return 0
    elif p1.search(g1) is None and p2.search(g1) is None and p3.search(g1) is None:
        cprint('漢字のみ : {}'.format(n),'on_grey')
        return 2
    else:
        cprint("ひら・カナ : {}".format(n), 'on_magenta')
        return 1

class Templistup: # テンプレートの検索と置換
    """テンプレートの検索と置換"""
    def tlistup02(self,list_0,tem1): # テンプレート内適合引数数調査
        list1=list2=list3=list4=list5=list6=list7=list8=list9=list10=list11=list13=list14=[]
        list20=list21=list22=[]
        par1='url='
        par2='language='
        par3='title='
        par4='和書'
        par5='website='
        par6='publisher='
        set1=set()
        set2=set()
        set3=set()
        set4=set()
        set5=set()
        set6=set()
        set7=set()
        set8=set()
        for i,title in enumerate(list_0):
            list_10=[]
            cprint('\n'+str(i)+ '—残り'+str(len(list_0)-i)+'   '+title+ '————', "on_red")
            try:
                page = pywikibot.Page(site, title)
                text = page.get(force=True, get_redirect=True)
                old_text=text
                wikicode = mwparserfromhell.parse(text)
                templates = wikicode.filter_templates()
                print([r for r in templates if 'dib.cambridge.org' in r])
                for te1 in tem1:
                    list_10=list_10+[r for r in templates if r.lower().startswith('{{'+te1)]+[r for r in templates if r.lower().startswith('{{ '+te1)]+[r for r in templates if r.lower().startswith('{{　'+te1)]
                list_9=[ r for r in list_10 if '和書' not in r ]
                list_1=[ r for r in list_9 if 'Cite web2' not in r and 'cite web2' not in r ]
                if list_1==[]:
                    print('対象テンプレート無し')
                    set2.add(title)
                else:
                    set1.add(title)
                #テンプレート分析
                for i,m in enumerate(list_1):
                    list14=[]
                    n1=str(m.name).strip()
                    cprint(str(i)+'-残り'+str(len(list_1)-i)+' - '+str(n1),'on_blue')
                    m0=str(m)
                    cprint(m0, 'yellow')
                    z0=m.params
                    print(z0)
                    z3=[n for n in z0 if "=".join([r.strip() for r in str(n).split('=',1)]).lower().startswith(par3)]
                    z4=[n for n in z0 if "=".join([r.strip() for r in str(n).split('=',1)]).lower().startswith(par4)]
                    z5=re.findall("language *= *(Japanese|ja|ja-jp|日本語)",m0)
                    z6=re.findall("url *= *.+?(ja\.|\.jp[^ego]|\.jp *\||\.jp *\/|\/jp\/|\/ja\/|ja_JP)",m0)
                    z7=re.findall("\{\{Category:中華人民共和国|\{\{Category:中国|\{\{Category:台湾", text)
                    q2="url *= *.+?(\.cn|\.tw|\.kr|\.baidu\.com|\.de\/|\.iaaf.org\/)"
                    z8=re.findall(q2,m0)
                    z10=re.findall("language *= *(zh|中国語|台湾語|韓国語|zw|kr|スペイン語|フランス語|ドイツ語|英語)",m0)
                    z11=[n for n in z0 if "=".join([r.strip() for r in str(n).split('=',1)]).lower().startswith(par5)]
                    z12=[n for n in z0 if "=".join([r.strip() for r in str(n).split('=',1)]).lower().startswith(par6)]
                    q1="url *= *.+?\.billboard-japan\.com|eiga\.com|smartnews\.com|netkeiba\.com|heroaca\.com|cdjournal\.com|artist\.cdjournal\.com|bleach-anime\.com|asahi\.com|hai-furi\.com|hypnosismic\.com|kakaku\.com\/tv|centforce\.com|s-manga\.net|www\.eiren\.org|\.getchu\.com|www\.equitation-japan\.com|nippon\.zaidan\.info|www\.train-media\.net"
                    z9=re.findall(q1,m0)
                    print("title : ",z3)
                    print("language : ",z5)
                    print("url : ",z6)
                    print("中台カテゴリ : ",z7)
                    print("url中台バイドウ : ",z8)
                    print("英字日本語 : ",z9)
                    print("台中韓国仏独英語 : ",z10)
                    print("ウエブサイト : ",z11)
                    print("publisher : ",z12)
                    kj1=kkt2.kk2
                    if z3[0] in kj1: # 履歴による除外
                        pass
                    else:
                        if z3!=[]:#タイトル
                            if len(str(z3[0]).split('=',1))==2:
                                k1=str(z3[0]).split('=',1)[0].strip()
                                v1=str(z3[0]).split('=',1)[1].strip()
                                f1=t01(z3[0])
                                #print('f1', f1)
                                if '{{lang' in v1 or '{{Lang' in v1 or '英文' in v1:
                                    set3.add(title)
                                    list8=list8+z3
                                    print('p31')
                                elif int(f1)==1: # ひらかな
                                        if '英語' in v1 or '中国語' in v1 or '韓国語' in v1 or 'フランス語' in v1 or 'ドイツ語' in v1:
                                            set3.add(title)
                                            list8=list8+z3
                                            print('p1')
                                        elif z8!=[]:
                                            set3.add(title)
                                            list8=list8+z3
                                            print('p1-1')
                                        else:
                                            m=re.sub("[\u3000 ]*[Cc]ite web *","Cite web|和書",str(m))
                                            list1=list1+[title,m0,m]
                                            list5=list5+z3
                                            set4.add(title)
                                            print('p2')
                                elif int(f1)==2: # 漢字のみ
                                    if  z7!=[] or z8!=[] or z10!=[]: # カテ･lan中台韓仏独英あり
                                        set3.add(title)
                                        list8=list8+z3
                                        print('p3')
                                    elif z5!=[] or z6!=[] or z9!=[] or z3[0] in inlist or '日本語' in v1: # lan・url日本 目視確認による追加
                                        m=re.sub("[\u3000 ]*[Cc]ite web *","Cite web|和書",str(m))
                                        list1=list1+[title,m0,m]
                                        set4.add(title)
                                        print('p4')
                                    else:
                                        if z11!=[]:#ウエブサイト
                                            if len(str(z11[0]).split('=',1))==2:
                                                k2=str(z11[0]).split('=',1)[0].strip()
                                                v2=str(z11[0]).split('=',1)[1].strip()
                                                f3=t01(z11[0])
                                                if int(f3)==1: # ひらかな
                                                    m=re.sub("[\u3000 ]*[Cc]ite web *","Cite web|和書",str(m))
                                                    list1=list1+[title,m0,m]
                                                    list5=list5+z3
                                                    set4.add(title)
                                                    print('p5')
                                                elif int(f3)==2:#漢字
                                                    m=re.sub("[\u3000 ]*[Cc]ite web *","Cite web|和書",str(m))
                                                    list22=list22+[title,m0,str(z3[0])]
                                                    set8.add(title)
                                                    print('p20')
                                                else:
                                                    set3.add(title)
                                                    list8=list8+z3
                                                    print('p11')
                                                    print('p6')
                                            else:
                                                m=re.sub("[\u3000 ]*[Cc]ite web *","Cite web|和書",str(m))
                                                list22=list22+[title,m0,str(z3[0])]
                                                set8.add(title)
                                                print('p7')
                                        else:
                                            if z12!=[]:#出版社
                                                if len(str(z12[0]).split('=',1))==2:
                                                    k3=str(z12[0]).split('=',1)[0].strip()
                                                    v3=str(z12[0]).split('=',1)[1].strip()
                                                    f4=t01(z12[0])
                                                    if int(f4)==1: # ひらかな
                                                        m=re.sub("[\u3000 ]*[Cc]ite web *","Cite web|和書",str(m))
                                                        list1=list1+[title,m0,m]
                                                        list5=list5+z3
                                                        set4.add(title)
                                                        print('p8')
                                                    else:
                                                        m=re.sub("[\u3000 ]*[Cc]ite web *","Cite web|和書",str(m))
                                                        list22=list22+[title,m0,str(z3[0])]
                                                        set8.add(title)
                                                        print('p9')
                                                else:
                                                    m=re.sub("[\u3000 ]*[Cc]ite web *","Cite web|和書",str(m))
                                                    list22=list22+[title,m0,str(z3[0])]
                                                    set8.add(title)
                                                    print('p10')
                                else:
                                    if z5!=[] : # lan日本 目視確認による追加
                                        m=re.sub("[\u3000 ]*[Cc]ite web *","Cite web|和書",str(m))
                                        list1=list1+[title,m0,m]
                                        list5=list5+z3
                                        set4.add(title)
                                        print('p12')
                                    else:
                                        set3.add(title)
                                        list8=list8+z3
                                        print('p11')
                            else:
                                pass
                            #text=text.replace(m0,str(m))
                        else: # その他
                            if z9!=[]:
                                m=re.sub("[\u3000 ]*[Cc]ite web *","Cite web|和書",str(m))
                                list1=list1+[title,m0,m]
                                list5=list5+z3
                                set4.add(title)
                                print('p41')
                            else:
                                set3.add(title)
                                list8=list8+z3
                                print('p42')
                            if z5!=[]:
                                m=re.sub("[\u3000 ]*[Cc]ite web *","Cite web|和書",str(m))
                                list2=list2+[title,m0,m]
                                list6=list6+z5
                                set4.add(title)
                                print('p43')
                            else:
                                if z6!=[]:
                                    m=re.sub("[\u3000 ]*[Cc]ite web *","Cite web|和書",str(m))
                                    list2=list2+[title,m0,m]
                                    list7=list7+z6
                                    set4.add(title)
                                    print('p44')
                                else:
                                    pass
                        text=text.replace(m0,str(m))
                #oldnew03(old_text,text)
                #list4=list4+[oldnew02(page,old_text,text)]
            except Exception as e:
                print('Exception : ',title, '—',e)
                set5.add(title)
        print('\n')
        print('\n')
        print('\n置換記事 : {}\n{}'.format(len(set4),set4))
        print('\n例外 : {}\n{}'.format(len(set5),set5))
        print('\n対象外記事 : {}\n{}'.format(len(set(list_0)-set4-set5),set(list_0)-set4-set5))
        cprint("\ntitle日本語：{} 個 - \t{}".format(len(list1),list1), 'yellow') 
        for n in list1:
            cprint(n, 'magenta')
        cprint("\nlanguage日本語：{} 個 - \t{}".format(len(list6),set(list6)), 'yellow') 
        for n in list2:
            cprint(n, 'magenta')
        cprint("\nurl日本語：{} 個 - \t{}".format(len(list7),set(list7)), 'yellow') 
        for n in list3:
            cprint(n, 'magenta')
        print("\ntitle")
        for n in list5:
            cprint(n, 'blue')
        print("\nタイトル英字",set3)
        for n in list8:
            cprint(n, 'yellow')
        print("\nタイトル日本英字目視判定2",set8)
        print(list22)
        for i in range(0,len(list22),3):
            cprint(repr(list22[i+2]), 'green')
            cprint("\t{}".format(repr(list22[i])), 'green')
            cprint("\t{}".format(repr(list22[i+1])), 'green')
        try:
            record01(start0,set4)
        except:
            pass
        return list1,list2,list3,list4
        
        

bz=Templistup()

##リスト読込　####
print("\nsummary："+str(summary))
print(datetime.datetime.now())
start0 = time.time()

bz.tlistup02(list_0,tem1)

cprint(datetime.datetime.now(), 'blue')
cprint('全終了', 'red')
