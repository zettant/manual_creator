マニュアル作成ツール
====

定型のマニュアルを作成するツールを作成する。

当初はUIは作らず、テキスト文と画像ファイルを指定のフォルダに入れてコマンドラインツールを実行することで、HTML形式のファイルを出力する。

HTML形式のページをPDFに出力して配布することを想定するが、HTMLをそのままマニュアルページとして表示してもいいかもしれない。


## 要件

* 入力は、mdファイルとjpeg/pngファイル群とする
* コマンドを実行するとhtmlファイルを出力する
* 画像はhtmlファイルにBase64で組み込む
* cssやフォントは外部から取得して良い
* HTMLからPDFに出力した時に、ページが正しく設定されること
* タイトルページや目次、索引ページも入れる


## 入力イメージ

```
doc_src/
  config.yml
  page_1/
   text.yml
   xx1.png/xx2.jpg 
  page_2/
   text.yml
   xx1.png/xx2.jpg 
  page_3/
   text.yml
   xx1.png/xx2.jpg 
```

```bash
# python create_manual.py -i doc_src -o manual.html
```

## マニュアルの構成

* マニュアル本体は、左右1:2に分けて、左の１にはイメージ、右の２には説明文とする
* イメージサイズは、1x1,1x2,2x1,2x2の４パターンのどれかとする
  * 1 = 180pxとする。なので、2x2 = 360x360px
* 


## ファイル構成

* package.json
* style.css
* tailwind.config.js
  -> これらは、開発する時にWebStormでCSSの補完ができる様にするために設置しているだけで、ツールの実際の動きには何も影響しない。

