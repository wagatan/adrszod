### インポート
import datetime
import time
import tkinter
import threading
import smbus

i2c = smbus.SMBus(1)
addr=0x68

Vref=2.048

def swap16(x):
    return (((x << 8) & 0xFF00) |
        ((x >> 8) & 0x00FF))

def sign16(x):
    return ( -(x & 0b1000000000000000) |
        (x & 0b0111111111111111) )

### 時刻取得関数
def get_time():

    ### 無限ループ
    while True:

        ### 現在時刻取得
        now = datetime.datetime.now()

        ### 時刻設定
        # tm = "{:02}:{:02}:{:02}".format(now.hour, now.minute, now.second)

        i2c.write_byte(addr, 0b10011000) #16bit
        time.sleep(0.2)
        data = i2c.read_word_data(addr,0x00)
        raw = swap16(int(hex(data),16))
        raw_s = sign16(int(hex(raw),16))
        tm = round((Vref * raw_s / 32767),5)

        ### キャンバス初期化
        canvas.delete("all")

        ### キャンバスに時刻表示
        canvas.create_text(100, 50, text=tm, font=(None,36))

        #### 待ち時間
        time.sleep(1)

### キャンバス作成
canvas = tkinter.Canvas(master=None, width=200, height=100)

### キャンバス表示
canvas.pack()

### スレッド作成
thread = threading.Thread(target=get_time, daemon=True)

### スレッド開始
thread.start()

### イベントループ
canvas.mainloop()
