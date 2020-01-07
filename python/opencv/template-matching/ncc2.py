# -*- coding: utf-8 -*-
import cv2
import numpy as np


def template_matching_ncc(src, temp):
    # 画像の高さ・幅を取得
    h, w = src.shape
    ht, wt = temp.shape

    # スコア格納用の2次元リスト
    score = np.empty((h-ht, w-wt))

    # 配列のデータ型をuint8からfloatに変換
    src = np.array(src, dtype="float")
    temp = np.array(temp, dtype="float")

    # 走査
    for dy in range(0, h - ht):
        for dx in range(0, w - wt):
            # 窓画像
            roi = src[dy:dy + ht, dx:dx + wt]
            # NCCの計算式
            num = np.sum(roi * temp)
            den = np.sqrt((np.sum(roi ** 2))) * np.sqrt(np.sum(temp ** 2))
            if den == 0:
                score[dy, dx] = 0
            score[dy, dx] = num / den

    # スコアが最大(1に最も近い)の走査位置を返す
    pt = np.unravel_index(score.argmax(), score.shape)

    return (pt[1], pt[0])


# 入力画像の読み込み
img = cv2.imread("C:/github/sample/python/opencv/template-matching/input.png")
temp = cv2.imread("C:/github/sample/python/opencv/template-matching/temp.png")

# グレースケール変換
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)

# テンプレート画像の高さ・幅
h, w = temp.shape

# テンプレートマッチング（NumPyで実装）
pt = template_matching_ncc(gray, temp)

# テンプレートマッチングの結果を出力
cv2.rectangle(img, (pt[0], pt[1]), (pt[0] + w, pt[1] + h), (0, 0, 200), 3)

# 結果を出力
cv2.imwrite("C:/github/sample/python/opencv/template-matching/ncc2.png", img)
