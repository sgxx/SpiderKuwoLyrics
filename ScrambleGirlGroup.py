#coding=utf-8

#@time:2019/4/17 7:42
#@author: Sheng Guangxiao

import time,traceback,random,datetime,re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from multiprocessing import Pool

options = webdriver.ChromeOptions()
options.binary_location = r'C:\Program Files\Opera\58.0.3135.127\opera.exe'
dirpath=r'LyricsSet'
exceptionList=['词：','曲：','词:','曲:','吉他：','录音：','混音：','制作人：','吉他:','录音:','混音:','制作人:','和声：','和声:','录音棚：','录音棚:','推广：','推广:','作曲:','作曲：','监制:','监制：']

def is_element_exist(css):
    s=driver.find_elements_by_css_selector(css_selector=css)
    if len(s)==0:
        return False
    return True

def getlyrics(ids):
    for id in ids:
        print('read',id)
        filepath=dirpath+"\\{}.txt".format(id)
        url='http://www.kuwo.cn/yinyue/{}'.format(id)

        j=requests.get(url).text

        pat=re.compile('class="lrcItem">.*</p>')
        result=pat.findall(str(j))

        f=open(filepath,'w+',encoding='utf-8')
        for item in result:
            flag=True

            for exceptionitem in exceptionList:
                if exceptionitem in item:
                    flag=False
                    break

            if flag:
                tmpItem=str(item).replace('</p>','').replace('class="lrcItem">','').replace('（','').replace('）','').replace('(','').replace(')','')
                f.write(tmpItem+"\n")
        f.close()
        time.sleep(0.2)

if __name__ == '__main__':
    driver=webdriver.Opera(options=options,executable_path=r'D:ChromeDownload\operadriver_win64\operadriver_win64\operadriver.exe')

    driver.maximize_window()
    driver.implicitly_wait(3)

    singerlist=['t-ara','少女时代','aoa','twice','sistar','exid','gfriend','4minute','stellar','after%20school']

    for singer in singerlist:
        try:
            songlist = []

            driver.get('http://www.kuwo.cn/artist/content?name={}'.format(singer))
            driver.find_element_by_xpath('//*[@id="tab_music"]/span').click()

            while is_element_exist('#song > div.page > a.next'):
                r=driver.page_source
                bs_obj=BeautifulSoup(r,'lxml')

                patten=re.compile(r'href="/yinyue/\d+"')
                result=patten.findall(str(bs_obj))

                for music in result:
                    songlist.append(music.replace('"','').replace('href=/yinyue/',''))

                time.sleep(0.1)
                print(len(songlist))
                element=driver.find_element_by_css_selector('#song > div.page > a.next')
                driver.execute_script("arguments[0].click();",element)

            part=int(len(songlist)/6)

            newlist=[songlist[:part],songlist[part:2*part],songlist[2*part:3*part],songlist[3*part:4*part],songlist[4*part:5*part],songlist[5*part:]]

            pool=Pool(6)
            pool.map(getlyrics,newlist)
            pool.close()
            pool.join()

            time.sleep(5)

        except:
            print(traceback.format_exc())

    driver.quit()

