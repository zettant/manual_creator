ステップごとの内容を記述してください。


* 画像ファイルをおく。デフォルトでは、step1.pngのようにステップ番号と同じ名前のファイル名であることを期待している。
    * どのファイルを読み込むかは、config.ymlに書かれているので、読み込むファイル名を変えたければconfig.ymlを直接修正すればよい
    * 画像ファイルのサイズは、後述する様に1x1、1x2、2x1、2x2の４パターンを想定しており、どのサイズにしたいかはconfig.ymlの中の**imgSize**という項目に記述する。
　* 説明文を書く。デフォルトでは、step1.html（newManual/トピック１/step1.html） のようにステップ番号と同じ名前のファイル名であることを期待している。
    * どのファイルを読み込むかは、config.ymlに書かれているので、読み込むファイル名を変えたければconfig.ymlを直接修正すればよい
    * 簡単なものであれば newManual/トピック１/config.ymlのdescriptionの下に、fileではなくtextというキーを書いて、その下に配列で文字列を書くことも可能
      ```yaml
      caption: ステップタイトルを変更したければここも編集可能
      text: # 説明文をこのコンフィグファイルに直接書く場合 (textかfileのどちらか一方を指定する(両方指定されたらtext優先))
        - 説明記述の行１
        - 説明記述の行２
        - 説明記述の行３
      ```
