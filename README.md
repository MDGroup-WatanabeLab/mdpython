# mdpython マニュアル

詳細な使い方は、各フォルダ内のREADMEと[チュートリアル](https://github.com/MDGroup-WatanabeLab/Tutorial)を参照してください。  
このREADMEでは、各フォルダにどのようなプログラムが入っているかを記載しています。


## 作成可能な構造（Structure フォルダ）
wyckoff positionはwyckoffの値，格子定数はDFTによる共役勾配法で決定。  
具体的な対応は下記の表のとおり。
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
SiO2_all.py|$\mathrm {SiO_2}$ の構造 | α-quartz, β-quartz, β-tridymite,  α-cristobalite, β-cristobalite, stishovite
trigonal.py|単体の三方晶系|$\mathrm {Sb, Te}$
wurtzite.py|ウルツ型構造|$\mathrm {ZnO, ZnS, BeO, BN, GaN}$


## ファイル形式変換（Converter フォルダ）
実行することでファイルの形式を変更できる。　　

    $ python convert_file.py

なお、変換できるファイル形式は  
  - mdl
  - lmp
  - xyz
  - POSCAR

の4形式である。

## MLFF用ツール（Tool4VASP フォルダ）
- calc_mlff.py  
  VASPの計算を繰り返す。計算内容はINCARに依存する。CONTCARをPOSCARに変換して、構造を継続して使用する。  
  プログラム上部の __mpi_num__ を変更すれば，並列計算のコア数を変更可能。下のようなEXAMPLEフォルダを用意する。  

      EXAMPLE       
          └── ICONST
          └── INCAR
          └── KPOINTS
          └── POSCAR
          └── POTCAR
          └── ML_ABN

    EXAMPLEディレクトリ内のターミナル上で

        $ nohup python calc_mlff.py -d [フォルダ名] -n [並列コア数] &

    を実行する．例えば，
    
        $ nohup python calc_mlff.py -d npt -n 50 &

    で実行すると，次のようにディレクトリが50個生成される．

      EXAMPLE       
          └── npt_1  
          └── npt_2
                :
                :
          └── npt_50
          └── ICONST
          └── INCAR
          └── KPOINTS
          └── POSCAR
          └── POTCAR
          └── ML_ABN



- calc_mlff_t.py  
  温度変化ありのときにVASPのML_MODE＝TRAINを繰り返す。  
  プログラム上部のTEBEGとTEENDを変更する必要がある。  
  &ensp; 例）TEBEG=300, TEEND=2000  
  &emsp;300Kから2000Kへ加熱，2000Kから300Kへの冷却を交互に行う．  
    INCARのNSWも調整する必要あり．

- calc_mlff_ctifor.py  
  一つ前の計算から、MLFFの閾値（ML_CTIFOR）を引き継ぐ。  
  __calc_mlff.pyよりもこちらを推奨__  
  使い方は通常のcalc_mlff.pyと同様

- calc_mlff_scale.py  
  プログラム内の"START", "END", "STEP"に応じ、POSCARのスケーリングを行い自動的に計算を行う。主に、E-V図を作成する際に有用。INCARおすすめ設定は次の通り。

      # Basic parameters for DFT 
      ISMEAR = 0
      SIGMA = 0.05
      LREAL = Auto
      ISYM = 0
      NELMIN = 4
      NELM = 100
      EDIFF = 1E-6
      LWAVE = .FALSE.
      LCHARG = .FALSE.
      ALGO = Normal
      PREC = Normal
      IBRION = -1
    
  または、

      # Basic parameters for DFT with MLFF
      ISMEAR = 0
      SIGMA = 0.05
      LREAL = Auto
      ISYM = 0
      NELMIN = 4
      NELM = 100
      EDIFF = 1E-6
      LWAVE = .FALSE.
      LCHARG = .FALSE.
      ALGO = Normal
      PREC = Normal

      # relaxation
      IBRION = 2
      NSW = 1
      ISIF = 3

      # MLFF
      ML_LMLFF = True
      ML_ISTART = 2



- data_sorting.py  
 calc_mlff.pyが存在するディレクトリと同じ場所に入れる。

      EXAMPLE       
          └── npt_1  
          └── npt_2
                :
                :
          └── npt_50
          └── ICONST
          └── INCAR
          └── KPOINTS
          └── POSCAR
          └── POTCAR
          └── ML_ABN
          └── calc_mlff.py
          └── data_sorting.py
          

  ターミナル上で，次のコマンドを実行する。  

        $ python data_sorting.py
    

    すると，次のようにExcelファイルが生成される。

      EXAMPLE       
          └── npt_1  
          └── npt_2
                :
                :
          └── npt_50
          └── ICONST
          └── INCAR
          └── KPOINTS
          └── POSCAR
          └── POTCAR
          └── ML_ABN
          └── calc_mlff.py
          └── data_sorting.py
          └── data.xlsx
    
  

- PVTE_graph.py  
  応力・体積・温度・エネルギーのタイムステップ変化をグラフ化する。  
  __なお、体積を出力するには、次の"ICONST"というファイルを用意する。__

      LR 1 7
      LR 2 7
      LR 3 7
      LA 2 3 7
      LA 1 3 7
      LA 1 2 7
      LV 7




