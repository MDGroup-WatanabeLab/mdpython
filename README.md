# mdpython マニュアル
## 使い方
① 使いたいプログラムを実行

    $ python *****.py

② 原子種に応じた番号入力（選択肢が無い場合は飛ばしてください）  
③ サイズを入力する  
&ensp; 例）2×2×5方向に拡張

    2 2 5

④ POSCARファイルが生成される  
⑤ 場合に応じ，ファイル形式をPOSCARから変換する  

    $ python convert_file.py  

※convert_file.py は Converter フォルダ内にあり　　

   


## 作成可能な構造（Structure フォルダ）
wyckoff positionはwyckoffの値，格子定数はDFTによる共役勾配法で決定。  具体的な対応は下記の表のとおり。
|プログラム名|結晶構造名|対応化合物|
---|---|---
aq-SiO2.py|α型クオーツ|α-quartz
bq-SiO2.py|β型クオーツ|β-quartz
corundum.py|コランダム構造|$\mathrm {Al_2O_3}$
diamond_mc.py|ダイヤモンド構造混晶|$\mathrm {SiC, SiGe, SiSn, GeSn}$
diamond.py|ダイヤモンド構造|$\mathrm {C, Si, Ge, Sn}$
fluorite.py|蛍石型構造|$\mathrm {CaF_2, CeO_2}$
hexagonal.py|単体の六方晶系|$\mathrm {Co, Ru}$
perovskite.py|ペロブスカイト構造|$\mathrm {BaTiO_3, CaTiO_3}$
rocksalt.py|岩塩型構造|$\mathrm { GST, NaCl, MgO, CaO}$
sphalerite.py|閃亜鉛鉱型|$\mathrm {ZnS}$
rutile.py|ルチル型構造|$\mathrm {SiO_2, GeO_2}$
SiO2_all.py|$\mathrm {SiO_2}$ の構造 | α-$\mathrm {quartz}$, β-$\mathrm {quartz}$, β-$\mathrm {tridymite}$,  α-$\mathrm {cristobalite}$, β-$\mathrm {cristobalite}$, $\mathrm {stishovite}$
trigonal.py|単体の三方晶系|$\mathrm {Sb, Te}$
wurtzite.py|ウルツ型構造|$\mathrm {ZnO, ZnS, BeO, BN, GaN}$


## ファイル形式変換（Converter フォルダ）
実行することでファイルの形式を変更できる。非直交基底の構造には今後対応予定　　

    $ python convert_file.py


## MLFF用ツール（Tool4MLFF フォルダ）
- calc_mlff.py  
  VASPのML_MODE＝TRAINを繰り返す。
    プログラム上部の __mpi_num__ を変更すれば，並列計算のコア数を変更可能。下のようなEXAMPLEフォルダを用意する。  
    - EXAMPLE
      - ICONST
      - INCAR
      - KPOINTS
      - POSCAR
      - POTCAR
      - ML_ABN

    EXAMPLEディレクトリ内のターミナル上で

        $ nohup python calc_mlff.py -d [フォルダ名] -n [並列コア数] &

    を実行する．例えば，
    
        $ nohup python calc_mlff.py -d npt -n 50 &

    で実行すると，次のようにディレクトリが50個生成される．
    - EXAMPLE
      - npt_1
      - npt_2
      - ：
      - ：
      - npt_50
      - ICONST
      - INCAR
      - KPOINTS
      - POSCAR
      - POTCAR
      - ML_ABN


- calc_mlff_t.py  
  温度変化ありのときにVASPのML_MODE＝TRAINを繰り返す。  
  プログラム上部のTEBEGとTEENDを変更する必要がある。  
  &ensp; 例）TEBEG=300, TEEND=2000  
  &emsp;300Kから2000Kへ加熱，2000Kから300Kへの冷却を交互に行う．  
    INCARのNSWも調整する必要あり．


- data_sorting.py  
 calc_mlff.pyが存在するディレクトリと同じ場所に入れる。  
   - EXAMPLE
      - npt_1
      - npt_2
      - ：
      - ：
      - npt_50
      - ICONST
      - INCAR
      - KPOINTS
      - POSCAR
      - POTCAR
      - ML_ABN  
      - data_sorting.py
 
  ターミナル上で，次のコマンドを実行する。  

        $ python data_sorting.py
    

    すると，次のようにExcelファイルが生成される。
    - EXAMPLE
      - npt_1
      - npt_2
      - ：
      - ：
      - npt_50
      - ICONST
      - INCAR
      - KPOINTS
      - POSCAR
      - POTCAR
      - ML_ABN  
      - data_sorting.py
      - data.xlsx

  



