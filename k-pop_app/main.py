import PySimpleGUI as sg
from meta import meta
import glob
import subprocess
import os
import shutil

def main():
    
    # ウィンドウに配置するパーツ
    layout = [[sg.Text('bingで画像検索し、嘘つきk-popを見破ります。')],
              [sg.Text('検索ワード:'),sg.Input(key="-key")],
              [sg.Text('上から何番目までを調べる?:'),sg.Input(key="-index")],
              [sg.Button('OK',key="-OK"), sg.Button('キャンセル')]]
    # ウィンドウの生成
    window = sg.Window('嘘つきk-popを許さない卍', layout,finalize=True) 

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'キャンセル':
            break
        elif event == '-OK':
            # 第2ウィンドウを起動
            layout2 = [[sg.Text(' … なうろーでぃんぐ … ')]]
            window2 = sg.Window("進捗状況",layout2,finalize=True)  
            # ファイルの削除
            for file in glob.glob("./read/*.jpg"):
                os.remove(file)
            for file in glob.glob("./result/*.jpg"):
                os.remove(file)          
            # 検索をする            
            keyword=values['-key']
            index=int(values['-index'])
            meta.search(keyword,index)
            # 顔認証を行う。            
            l=glob.glob("./read/*.jpg")         
            for i,jpg in enumerate(l):
                meta.read_img( jpg , keyword+"_"+str(i) )
            # エクスプローラーを開く
            path = os.getcwd()
            path = path+r"\result"
            print(path)
            window2.close()
            subprocess.Popen(['explorer', path ], shell=True)
    window.close()


if __name__=="__main__":
    main()