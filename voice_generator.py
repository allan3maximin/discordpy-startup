import subprocess
import re

# ************************************************
# remove_custom_emoji
# 絵文字IDは読み上げない
# ************************************************
def remove_custom_emoji(text):
    
    #pattern = r'<:[a-zA-Z0-9_]+:[0-9]+>'    # カスタム絵文字のパターン
    pattern = r'<:'    # カスタム絵文字のパターン
    text = re.sub(pattern,'',text)   # 置換処理
    pattern = r':[0-9]+>'    # カスタム絵文字のパターン
    return re.sub(pattern,'',text)   # 置換処理

# ************************************************
# exclude_url
# URLなら省略
# ************************************************
def exclude_url(text):
    pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    return re.sub(pattern,'URL',text)   # 置換処理

# ************************************************
# remove_picture
# 画像ファイルなら読み上げない
# ************************************************
def remove_picture(text):
    pattern = r'.*(\.jpg|\.jpeg|\.gif|\.png|\.bmp)'
    return re.sub(pattern,'画像',text)   # 置換処理

# ************************************************
# remove_command
# コマンドは読み上げない
# ************************************************
def remove_command(text):
    pattern = r'^\!.*'
    return re.sub(pattern,'',text)   # 置換処理

# ************************************************
# remove_log
# 参加ログは読み上げない
# ************************************************
def remove_log(text):
    pattern = r'(\【VC参加ログ\】.*)'
    return re.sub(pattern,'',text)   # 置換処理

# ************************************************
# user_custam
# ユーザ登録した文字を読み替える
# ************************************************
def user_custam(text):

    f = open('user_dictionary.txt', 'r')
    line = f.readline()

    while line:
        pattern = line.strip().split(',')
        if pattern[0] in text:
            text = text.replace(pattern[0], pattern[1])
            print('置換後のtext:'+text)
            break
        else:
            line = f.readline()
    f.close()

    return text



# ************************************************
# creat_WAV
# message.contentをテキストファイルと音声ファイルに書き込む
# 引数：inputText
# 書き込みファイル：input.txt、output.wav
# ************************************************
def creat_WAV(text):
    text = remove_custom_emoji(text)   # 絵文字IDは読み上げない
    text = exclude_url(text)   # URLなら省略

    open_jtalk = ['jtalk/bin/open_jtalk']
    mech = ['-x', 'jtalk/dic']
    htsvoice = ['-m', 'jtalk/mei/mei_normal.htsvoice']
    speed = ['-r', '1.0']
    outwav = ['-ow', 'output.wav']
    cmd = open_jtalk + mech + htsvoice + speed + outwav
    c = subprocess.Popen(' '.join(cmd), stdin=subprocess.PIPE, shell=True)
    c.stdin.write(text.encode())
    c.stdin.close()
    c.wait()


if __name__ == '__main__':
    creat_WAV('hello world')
