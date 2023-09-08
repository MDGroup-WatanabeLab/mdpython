# Tool4VASP マニュアル
## MLFF用ツール 
- calc_mlff.py  
  VASPのML_MODE＝TRAINを繰り返す。
    プログラム上部の __mpi_num__ を変更すれば，並列計算のコア数を変更可能。下のようなEXAMPLEフォルダを用意する。  

      EXAMPLE
          ├── ICONST
          ├── INCAR
          ├── KPOINTS
          ├── POSCAR
          ├── POTCAR
          └── ML_ABN

    EXAMPLEディレクトリ内のターミナル上で

      nohup python calc_mlff.py -d [フォルダ名] -n [計算回数] &

    を実行する．例えば，
    
      nohup python calc_mlff.py -d npt -n 50 &

    で実行すると，次のようにディレクトリが50個生成される．
    
      EXAMPLE
          ├── npt_1
          ├── npt_2
          ├── ：
          ├── ：
          ├── npt_50
          ├── ICONST
          ├── INCAR
          ├── KPOINTS
          ├── POSCAR
          ├── POTCAR
          └── ML_ABN


- calc_mlff_t.py  
  温度変化ありのときにVASPのML_MODE＝TRAINを繰り返す。  
  プログラム上部のTEBEGとTEENDを変更する必要がある。  
  &ensp; 例）TEBEG=300, TEEND=2000  
  &emsp;300Kから2000Kへ加熱，2000Kから300Kへの冷却を交互に行う．  
    INCARのNSWも調整する必要あり．
  <br>

- calc_mlff_ctifor.py
  一つ前の計算から、MLFFの閾値（ML_CTIFOR）を引き継ぐ。  
  __calc_mlff.pyよりもこちらを推奨__  
  使い方は通常のcalc_mlff.pyと同様
  <br>

- calc_mlff_scale.py
  プログラム内の"START", "END", "STEP"に応じ、POSCARのスケーリングを行い自動的に計算を行う。主に、E-V図を作成する際に有用。
  __INCARの設定を変更すればMLFF以外にも流用可能であり、このプログラムを実行した後にEV_graph.pyを実行すればE-V図が作成できる。__  
  INCARおすすめ設定は次の通り。

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
  <br>

- data_error.py
  ML_LOGFILEの中から、ERR(力のRMSE)とBEER(Bayesian error estimations of force)を取り出し、data_err.xlsxを生成する。以下のようなグラフを作成する。
  ![image](https://github.com/MDGroup-WatanabeLab/image_for_mdpython/assets/139113059/1bbc0174-4018-44b3-b501-67e8e4ced998)
  <br>

- data_rdf_lat.py
  REPORTファイルから格子定数と体積を取り出す。
  <br>

- data_sorting.py  
 calc_mlff.pyが存在するディレクトリと同じ場所に入れる。  

      EXAMPLE
          ├── npt_1
          ├── npt_2
          ├── ：
          ├── ：
          ├── npt_50
          ├── ICONST
          ├── INCAR
          ├── KPOINTS
          ├── POSCAR
          ├── POTCAR
          ├── ML_ABN
          └── data_sorting.py
 
  ターミナル上で，次のコマンドを実行する。  

       python data_sorting.py
    

    実行後はdata.xlsxファイルが生成される。Excelファイルには計算回数、原子種、合計ステップ数、計算時間、構造数のデータに加え、以下のように計算時間と構造数のグラフが作成される。日付を記入することも可能。
    ![image](https://github.com/MDGroup-WatanabeLab/image_for_mdpython/assets/139113059/6723afca-6228-4e55-9c7e-c344e0eb7791)
  <br>

- PVTE_graph.py  
  応力・体積・温度・エネルギーのタイムステップ変化をグラフ化する。
  __第一原理MD計算を実行した際に使用可能。体積とエネルギーを出力するには、ICONSTファイルを用意する。中身は以下の通り。__

      LR 1 7
      LR 2 7
      LR 3 7
      LA 2 3 7
      LA 1 3 7
      LA 1 2 7
      LV 7
  <br>

## VASP出力ファイル用のプログラム
- DOSCAR.py  
  VASPの出力ファイルDOSCARからExcelを用いてDOS(状態密度)をグラフ化する。DOSCARと同じディレクトリ内で実行する。  

  - 実行時には以下のような図が作成される  
  ![dos_image](https://github.com/MDGroup-WatanabeLab/image_for_mdpython/assets/139113059/a8f080ba-b236-4760-8be1-34c682b3298b)
  <br>

- EIGENVAL.py  
  VASPの出力ファイルEIGENVALからExcelを用いてバンド構造(バンド分散)をグラフ化する。EIGENVALと同じディレクトリ内で実行する。  
  
  - 実行時には以下のような図が作成される  
  ![band_image](https://github.com/MDGroup-WatanabeLab/image_for_mdpython/assets/139113059/55796f50-9bdb-4de4-868d-0436cdba520f)
  <br>

- EV_graph.py
  体積に対するエネルギーのグラフを作成する。calc_mlff_scale.pyを実行した後に、このプログラムを実行すると以下のようにE-V図が作成できる。
  ![image](https://github.com/MDGroup-WatanabeLab/image_for_mdpython/assets/139113059/73fc5a90-1068-42c0-a254-fafd662915e6)
  <br>

- PCDAT.py  
  VASPの出力ファイルPCDATからペア相関関数(動径分布関数と同じ)をExcelを用いてグラフ化する。PCDATと同じディレクトリ内で実行する。  

  - 実行時には以下のような図が作成される  
  ![rdf_image](https://github.com/MDGroup-WatanabeLab/image_for_mdpython/assets/139113059/1e925344-e336-4aef-850a-c0e8a78e9b2d)
