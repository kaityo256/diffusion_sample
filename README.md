# LAMMPSを使った拡散係数の計算サンプル

## 使い方

最初に初期配置を作る。

```sh
$ python3 generate_config.py 
Generated diffusion.atoms
```

すると、`diffusion.atoms`が作成される。

LAMMPSを実行する。

```sh
lmp_serial < diffusion.input 
```

トラジェクトリファイル(ダンプファイル)として`diffusion.lammpstrj`が作成される。

これをつかって拡散係数を計算するのが`diffusion.py`。実行すると標準出力に平均自乗変位の時間依存性を出力するので、リダイレクトでファイルに保存する。

```sh
python diffusion.py > diffusion.dat
```

それをgnuplotでプロットする。

```sh
gnuplot diffusion.plt
```

すると、以下のような図が出力され、たしかに拡散していることがわかる。

