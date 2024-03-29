---
tags: 天文社
---
# 臺灣南十字可見地點分析

![Alt](./CruxByNebula0.jpg)
PC: @nebula0
偷來修了一下> <

[Github Repo連結](https://github.com/xiguaakako/CruxVisibilityTaiwan)

## 緣起

某一天月全食小隊群組在閒聊
> 好想做一個台灣南十字可見地圖
> [name=煜翔 2023.02.09]

然後就開始了。

## 程式碼使用方法

1. [下載QGIS](https://www.qgis.org/en/site/forusers/download.html)
2. [下載內政部20公尺網格數值地形模型資料](https://data.gov.tw/dataset/35430)，解壓縮。
3. 在QGIS內按Ctrl+Alt+P開啟Python主控台，按上方紙張按鈕「顯示編輯器」。
4. 按「打開腳本資料」開啟CruxVisibilityMap.py。
5. 更改第6行的DEM .tif檔路徑、第129行的列印範圍。
6. 執行。

## 假設

原問題：**臺灣哪些地方看得到南十字？**

1. **看見十字架二就可以 → 看見南十字。**
    ※ 由於在臺灣十字架二最難看到也最南看到，暫且假設看到了十字架二就看到了南十字。
2. **某地（下稱分析點）沒有人為建築物只有地形起伏，且正南方遮蔽高度（角）小於十字架二 → 看見南十字**
    ※ 南十字二高度最高的時候剛好在正南方，相對容易觀測。因此，只要做視域分析，計算分析點正南方的高山遮蔽高度（角）是否小於十字架二即可。

## 實作

### 在一個特定分析點

#### 計算分析點南方遮蔽高度（角）

1. 載入數值高程模型（下稱DEM），建立該欄（地圖南北向）所有位置的高度陣列（下稱欄高陣列）。
    ※ 將欄高陣列建置為全域變數，可以重複使用。
2. 第一次陣列切片：切出欄高陣列中分析點南方的部分。
3. 第二次陣列切片：切出分析地以南，南方最高峰（最高處）以北的部分。
    ※ 南方最高峰以南的任何地形起伏無法造成任何更高的遮蔽。
4. 將上一步所得的陣列每一項除以與分析地的距離，得到坡度（斜率）。
5. 取上一步所得的陣列的最大值，得到坡度最大值，換算成高度角輸出，即南方遮蔽高度（角）。

### 計算分析點十字架二高度

#### 初步想法

應該是先把 TWD97 轉成 WGS84，得到地點緯度 `position_De`

### 輸出分析點南十字可見性

比較分析點 **十字架二高度角** 及 **南方遮蔽高度角**，如果前者大於後者則輸出「可見」，以1代表；否則輸出「不可見」，以0代表。

### 地圖繪製

1. 引入一個新的同樣大小的DEM（同一張地圖即可）。
2. 由北向南（第一層迴圈）、由西向東（第二層迴圈）對一個DEM的每一格利用上述演算法分析可見性。
3. 覆寫該格數值，如果在該格可見南十字覆寫以1，否則複寫以0。
4. 渲染上不同的顏色，輸出地圖。

## 閒聊

> 內容要打什麼呀？全部的過程嗎？還是剪精華就好？途中其實碰壁很多次。
>[name=巖盛 2023.02.10][color=#ffc854]
> 都可以？我最初的想法只是怕之後找資料要從訊息裡翻，或是有些東西忘記了。就，開心怎樣使用這個文件就怎樣用，之後可以整理。東西不見了 QQ。[name=張家昀 2023.02.10][color=#99cad9]

<!-- ## 簡化概念
> credit：邱巖盛

今天先不論南十字，先討論十字架二的可見度，假設十字架二就看到了整個南十字。
![](https://i.imgur.com/ldIQDzD.png)
這個是我們所在的地圖，是一個4×4的網格，每個網格中間的數字是當地的高度。
如果要討論十字架二的可見度，應該只要討論十字架二升到最高點，也就是面向正南方的時候，南方最高的高山遮掉多少視野就行了。
因此演算法大概可以這樣寫
![](https://i.imgur.com/uV8Kux1.png)
如果要探討這個位置的十字架二可見度，往南找山高的最大值，找到是10
![](https://i.imgur.com/0xvmEXH.png)
看那個角度有沒有比十字架二的最大高度小
每一個緯度的十字架二的最大高度應該很好算 -->
