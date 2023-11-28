# ESJ-novel-backup
ESJZone 小說的備份工具

## Python 版本
只支援 Python 3

## 與原版的差異
1. 解決章節沒展開下載不到的問題
2. 解決下載權限不足的問題（使用 cookie 登入）
3. 解決中文 cp950 編碼錯誤的問題
4. 增加下載時的進度提示

## 使用方法

### 必要：cookie 登入
本程式只支援登入後下載，將你的 cookie 存檔成 cookie.txt，放在程式主目錄下後，依照需求執行以下程式碼，cookie 會過期，如果有遇到找不到元素，可能是登入失效，更新 cookie 可解決
  
　
### 單部小說（從小說主頁備份）  

範例：https://www.esjzone.cc/detail/1599746513.html

`python esjbackup.py https://www.esjzone.cc/detail/1599746513.html`

讀取該小說的章節頁面，依序將該頁面內所有的「站內連結」來做備份，並把它寫成一個 txt 文字檔，檔案名為該小說的名稱。   
  
　
### 單部小說（從小說論壇備份）

範例：https://www.esjzone.cc/forum/1584679807/1599746513/

`python esjbackup3.py https://www.esjzone.cc/forum/1584679807/1599746513/`

生成該小說名稱的目錄，該目錄內有所有論壇內文章的 txt 文字檔，檔案名為該文章的標題名稱。


### 單篇文章

範例：https://www.esjzone.cc/forum/1599746513/121688.html

`python esjbackup.py https://www.esjzone.cc/forum/1599746513/121688.html`
  
　
僅保存該單篇的  txt 文字檔。
