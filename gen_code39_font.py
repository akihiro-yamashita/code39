#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import defcon
import ufo2ft


# フォント名、基本メトリックの設定
# 下4つのプロパティは「https://en.wikipedia.org/wiki/Mean_line」の画像を参照。
font = defcon.Font()
font.info.familyName = 'Code39'
font.info.styleName = ''
font.info.copyright = 'Akihiro Yamashita'
font.info.versionMajor = 1
font.info.versionMinor = 0
font.info.unitsPerEm = 1000 # よく分からん。
font.info.descender = -120
font.info.ascender = 880
font.info.xHeight = 500
font.info.capHeight = 800


# x座標を12マスに分割した時のストライプ位置
barcode_stripes_dict = {
    '0': 'B B  BB BB B',
    '1': 'BB B  B B BB',
    '2': 'B BB  B B BB',
    '3': 'BB BB  B B B',
    '4': 'B B  BB B BB',
    '5': 'BB B  BB B B',
    '6': 'B BB  BB B B',
    '7': 'B B  B BB BB',
    '8': 'BB B  B BB B',
    '9': 'B BB  B BB B',

    'A': 'BB B B  B BB',
    'B': 'B BB B  B BB',
    'C': 'BB BB B  B B',
    'D': 'B B BB  B BB',
    'E': 'BB B BB  B B',
    'F': 'B BB BB  B B',
    'G': 'B B B  BB BB',
    'H': 'BB B B  BB B',
    'I': 'B BB B  BB B',
    'J': 'B B BB  BB B',
    'K': 'BB B B B  BB',
    'L': 'B BB B B  BB',
    'M': 'BB BB B B  B',
    'N': 'B B BB B  BB',
    'O': 'BB B BB B  B',
    'P': 'B BB BB B  B',
    'Q': 'B B B BB  BB',
    'R': 'BB B B BB  B',
    'S': 'B BB B BB  B',
    'T': 'B B BB BB  B',
    'U': 'BB  B B B BB',
    'V': 'B  BB B B BB',
    'W': 'BB  BB B B B',
    'X': 'B  B BB B BB',
    'Y': 'BB  B BB B B',
    'Z': 'B  BB BB B B',

    '-': 'B  B B BB BB',
    '.': 'BB  B B BB B',
    ' ': 'B  BB B BB B',
    '*': 'B  B BB BB B',
    '$': 'B  B  B  B B',
    '/': 'B  B  B B  B',
    '+': 'B  B B  B  B', # 「+」じゃなくて「~（チルダ）」？
    '%': 'B B  B  B  B',
}

# 仕様と異なるが、小文字アルファベットもバーコード化
append_dict = dict()
for c, stripes in barcode_stripes_dict.items():
    if c.isupper():
        append_dict[c.lower()] = stripes
barcode_stripes_dict.update(append_dict)

x_unit = 50 # バー1マスあたりの幅
for c, stripes in barcode_stripes_dict.items():
    glyph = font.newGlyph(c)
    glyph.unicode = ord(c)
    glyph.width = 700 # 12マスなので(x_unit * 12)だが、右に2マス分の余白がないと読めない。
    for idx, stripe in enumerate(stripes):
        if stripe == 'B':
            contour = defcon.Contour()
            contour.appendPoint(defcon.Point((idx * x_unit, font.info.descender), 'line')) # 座標　左下
            contour.appendPoint(defcon.Point(((idx + 1) * x_unit, font.info.descender), 'line')) # 座標　右下
            contour.appendPoint(defcon.Point(((idx + 1) * x_unit, font.info.ascender), 'line')) # 座標　右上
            contour.appendPoint(defcon.Point((idx * x_unit, font.info.ascender), 'line')) # 座標　左上
            glyph.appendContour(contour)


otf = ufo2ft.compileOTF(font)
cur_dir = os.path.dirname(__file__)
font_file_path = os.path.join(cur_dir, '%s.otf' % font.info.familyName)
otf.save(font_file_path)
