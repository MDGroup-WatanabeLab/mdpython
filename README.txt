＜mdpython 使い方＞
1. $ python *****.py
2. 原子種に応じた番号入力（選択肢が無い場合は飛ばしてください）
3. サイズの入力
　 例）2*2*5方向に拡張　→　2 2 5
4. POSCARファイルが生成される
5. $ python conert_file.py
   場合に応じ，ファイル形式をPOSCARから変換する


＜構造作成＞　☑マークはVASPでの動作確認済み
格子定数は基本的にwycoffの本参考（研究室に１・２巻あり）
POSCARファイルを作成する

☑aq-SiO2.py
    α型クオーツ

☑bq-SiO2.py
    β型クオーツ

☑corundum.py
    コランダム構造
    Al2O3

☑diamond_mc.py
    Ⅳ族のダイヤモンド構造混晶（mixed crystal）
    SiC
    SiGe

☑diamond.py
    Ⅳ族のダイヤモンド構造
    C
    Si
    Ge
    Sn

☑fluorite.py
    蛍石型構造
    CaF2
    CeO2

  hexagonal.py
  　六方晶系の単体の構造
  　Co
  　Ru

☑perovskite.py
    ペロブスカイト構造
    BaTiO3
    CaTiO3

☑rocksalt.py
    岩塩型構造
    GST(その2体系も含む)
    NaCl
    MgO
    CaO

☑sphalerite.py
    閃亜鉛鉱型
    ZnS

☑rutile.py
    ルチル型構造
    SiO2
    GeO2

  SiO2_all.py
    α-石英
    β-石英
    β-トリディマイト
    α-クリストバライト
　  β-クリストバライト
    スティショバイト 

☑trigonal.py
    三方晶系の単体
    Sb
    Te

☑wurtzite.py
    ウルツ型構造
    ZnO
    ZnS
    BeO
    BN
    GaN

＜その他＞
  convert_file.py
    ファイル形式を変換する


