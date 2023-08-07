# Structure マニュアル

## 使い方 (stack.py以外) 
1. 下の表を参考に、作成したい構造のプログラムを実行する。  

        $ python *****.py

2. 原子種を入力する。対応する数字を入力する。
3. サイズを入力する。例は以下の通り。

        Input number :  2 3 4

    x, y, z方向それぞれが2, 3, 4倍された超格子が作成できる。

4. POSCARファイルが作成される。
5. [Converter](https://github.com/MDGroup-WatanabeLab/mdpython/tree/main/Converter)でファイル形式の変換を行う。

## 使い方（stack.py）
1. __同じファイル形式の__ くっつけたい構造を複数用意する。
2. 1つ目の構造を選択
   
        Please select 1st file :
3. 2つ目の構造を選択 
   
        Please select 2nd file : 
4. くっつける方向をx, y, z から指定。 __小文字で入力。__
     
        Please input direction to stack : 
5. 2つの構造間の距離を決定。単位はオングストローム。
   
        Please select distance among two structure : 
6. くっつけた後のファイル名を入力。
   
        Please input the name of the converted file: 

__なお、格子定数は、大きい方に揃えられるので、作成後に、アニールか、構造最適化することを忘れずに！__

## 作成可能な構造
wyckoff positionはwyckoffの値，格子定数はDFTによる共役勾配法で決定。  
具体的な対応は下記の表のとおり。
|プログラム名|結晶構造名|対応化合物|
---|---|---
SiO2_all.py|$\mathrm {SiO_2}$ の構造 | α-quartz, β-quartz, β-tridymite,  α-cristobalite, β-cristobalite, stishovite
aq-SiO2.py|α型クオーツ|α-quartz
bcc.py|体心立方構造|W, Cr, Fe
bq-SiO2.py|β型クオーツ|β-quartz
corundum.py|コランダム構造|$\mathrm {Al_2O_3}$
cubic.py|単体の立方晶系|Sb, Te
diamond.py|ダイヤモンド構造|$\mathrm {C, Si, Ge, Sn}$
diamond_mc.py|ダイヤモンド構造混晶|$\mathrm {SiC, SiGe, SiSn, GeSn}$
fcc.py|面心立方構造|Au, Ag, Cu, Fe, Al, Co
fluorite.py|蛍石型構造|$\mathrm {CaF_2, CeO_2}$
hcp.py|六方最密充填構造|Co, Ru
hexagonal.py|単体の六方晶系|$\mathrm {Co, Ru}$
perovskite.py|ペロブスカイト構造|$\mathrm {BaTiO_3, CaTiO_3}$
rocksalt.py|岩塩型構造|$\mathrm { GST, NaCl, MgO, CaO}$
sphalerite.py|閃亜鉛鉱型|$\mathrm {ZnS}$
rutile.py|ルチル型構造|$\mathrm {SiO_2, GeO_2}$
trigonal.py|単体の三方晶系|$\mathrm {Sb, Te}$
wurtzite.py|ウルツ型構造|$\mathrm {ZnO, ZnS, BeO, BN, GaN}$







