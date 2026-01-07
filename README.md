# Testcase-Generator
競技プログラミングの問題のテストケースを生成します。

main.pyを実行して必要事項を記入するとテストケースが生成されます。
out生成に使うコードは一応python/cpp/javaに対応しているはずですが、cpp/javaはまだ検証できていません。

例) 以下のような構造の入力例と出力例を8個ずつ生成するとします。

入力:
```
T
case1
case2
...
caseT
```

$i$ 個目のテストケース:
```
X_i Y_i L_i
A_i1 A_i2 A_i3 ... A_iX_i
S_i1 S_i2 S_i3 ... S_iY_i
```
・ Tは $1$ 以上 $100$ 以下の整数
・ X_iは $1$ 以上 $5000$ 以下の整数
・ A_ijは $1$ 以上 $2026$ 以下の整数

・ Y_iは $1$ 以上 $1000$ 以下の整数
・ L_iは $1$ 以上 $10$ 以下の整数
・ S_ijは $L_i$ 文字の小文字のアルファベット, `#`, `@` のみからなる文字列
・ それぞれのテストケースについて同じ数値は含まれてもよいが、同じ文字列は含まれてはならない。

このとき、まずは
![image](sample_images/01.png)
と書いて「数値を追加」ボタンを押す。

次に、
![image](sample_images/02.png)
と書いて、同様に「数値を追加」ボタンを押す。

そして、最後に解答のソースコードを選択し、「生成」ボタンを押す。

この手順で生成できます。

用意されたパターンでは表現しきれない場合は、同梱されている ![in_generate.py](https://github.com/Rapca1256/Testcase-Generator/blob/main/in_generate.py) 、 ![out_generate.py](https://github.com/Rapca1256/Testcase-Generator/blob/main/out_generate.py) などを使用してお好きにカスタマイズしてください。
