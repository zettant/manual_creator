トピックの詳細情報を記述してください。


* マニュアルページのトピックの冒頭に説明文を記述する（記述する内容がなければ放置でOK）
* newManual/トピック１/description.md に記述する。
  * htmlファイルでも記述できる。ファイル名をfileで指定しているので、description.mdをdescription.htmlに変更すれば良い。
  * 簡単なものであれば newManual/トピック１/config.ymlのdescriptionの下に、fileではなくtextというキーを書いて、その下に配列で文字列を書くことも可能
    ```yaml
    description: # このページのトピックの詳細記述
    text: # このコンフィグファイルに直接記述を書く場合 (textかfileのどちらか一方を指定する(両方指定されたらtext優先))
     - トピックの説明の行１
     - トピックの説明の行２
     - トピックの説明の行３
    ```
