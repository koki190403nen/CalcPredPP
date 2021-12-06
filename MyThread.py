# %%
import numpy as np
from matplotlib import pyplot as plt
import threading
from scipy import stats



# %%
class MyThread(threading.Thread):
    def __init__(self, h=320, w=300, product='chirps25', 
                in_dir='D:/ResearchData/Level3/CHIRPS25_RAW_f64/',
                out_dir='D:/ResearchData/Level4/ClimaticNormal_RAW/RRnnpp_test/',
                start_row=0, end_row = 320, thread_num = None):

        super().__init__()


        self.out_arr = None

        self.start_row = int(start_row)
        self.end_row = int(end_row)
        self.h = h
        self.w = w
        self.product=product  # プロダクト名
        self.in_dir = in_dir  # 入力元ディレクトリ
        self.out_dir = out_dir  # 出力先ディレクトリ
        self.get_img_arr=None  # 取得画像(縦×横×時間)

        self.now_working = ''  # 現在動かしているメソッド名を記録
        self.thread_num = thread_num

        self.param1_img = np.zeros((self.end_row-self.start_row, self.w))
        self.param2_img = np.zeros((self.end_row-self.start_row, self.w))
        self.param3_img = np.zeros((self.end_row-self.start_row, self.w))

        self.RR95_img = np.zeros((self.end_row-self.start_row, self.w))
        self.RR99_img = np.zeros((self.end_row-self.start_row, self.w))



    def run(self):
        print('run')
        self.GetTimeSeries()
        self.fit_gamma()



    def GetTimeSeries(self, meta=''):

        self.now_working = f'GetTimeSeries thread:{self.thread_num}|'

        self.get_img_arr = np.zeros((10958,self.end_row - self.start_row, self.w), dtype=np.float64)

        
        c = 0  # カウンタ
        for year in np.arange(1991, 2020+1):
            for doy in np.arange(1, 366+1):

                # DOY366に対する処理
                if (year%4!=0)&(doy==366):
                    continue
        
            # 画像を取得
                get_img = np.fromfile(
                    ###### ここでパス変更!!!!!
                    f'{self.in_dir}/{self.product}.A{year}{str(doy).zfill(3)}.float64_h{self.h}w{self.w}.raw',
                    count=self.h*self.w, dtype=np.float64).reshape(self.h, self.w)
        
                self.get_img_arr[c, 0:(self.end_row-self.start_row), :]=get_img[self.start_row:self.end_row, :]
                del get_img  # メモリの解放
                print(self.now_working + f'{year}/{doy}\n')

                c+=1
    
    def fit_gamma(self, meta='fit_gamma'):
        print(f'start Fitting Thread:{self.thread_num}\n')
        self.now_working = f'{meta} thread:{self.thread_num}|'
        for row in np.arange(0, self.end_row-self.start_row):
            for column in range(self.w):
                target_ts = self.get_img_arr[:, row, column]

                # Null値が含まれていた場合の処理
                if np.sum(np.isnan(target_ts))!=0:
                    params = [np.nan,np.nan,np.nan]
                    RR95 = np.nan
                    RR99 = np.nan

                # 含まれていなければfitting
                else:
                    params = stats.gamma.fit(target_ts)
                    RR95 = stats.gamma.ppf(0.95, *params)
                    RR99 = stats.gamma.ppf(0.99, *params)

                self.param1_img[row, column] = params[0]
                self.param2_img[row, column] = params[1]
                self.param3_img[row, column] = params[2]

                self.RR95_img[row, column] = RR95
                self.RR99_img[row, column] = RR99

                print(self.now_working + f'row:{self.start_row + row} column:{column}, RR95:{str(np.round(RR95,2)).rjust(6)} RR99:{str(np.round(RR99,2)).rjust(6)}\n')

# %%
def FitGamma_multi(n, h=320, w=300, span=10, out_dir='./img/'):
    RR95_img = np.zeros((4*span, w), dtype=np.float64)  # 400×1500
    RR99_img = np.zeros((4*span, w), dtype=np.float64)  # 400×1500

    for i in range(4):
        t1 = MyThread(start_row=(4*n + i)*span, end_row=(4*n + (i+1))*span, thread_num=4*n +i+1)  # 1セットで 0~100

        t1.start()
        t1.join()


        RR95_img[i*span:(i+1)*span , :] = t1.RR95_img
        RR99_img[i*span:(i+1)*span , :] = t1.RR99_img

        RR95_img.tofile(out_dir+f'/RR95_n{n}.A1900001.h{span*4}w{w}.raw')
        RR99_img.tofile(out_dir+f'/RR95_n{n}.A1900001.h{span*4}w{w}.raw')


    del t1
    return RR95_img, RR99_img
