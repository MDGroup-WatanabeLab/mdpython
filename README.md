# mdpython 概要

詳細な使い方は、各フォルダ内のREADMEと[チュートリアル](https://github.com/MDGroup-WatanabeLab/Tutorial)を参照してください。  
このREADMEでは、各フォルダにどのようなプログラムが入っているかを記載しています。


## 作成可能な構造（Structure フォルダ）
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

２つの構造をくっつける。
- stack.py 
  
新規プログラム作成用のテンプレート
- template_cubic.py

## ファイル形式変換（Converter フォルダ）  
ファイルの形式を変換できる
- convert_file.py

## VASP用ツール（Tool4VASP フォルダ）  
VASPの出力ファイルの整理、繰り返し計算、データ処理用プログラム
- DOSCAR.py
- EIGENVAL
- PCDAT.py
- PVTE_graph.py
- calc_mlff.py  
- calc_mlff_ctifor.py
- calc_mlff_scale.py
- calc_mlff_t.py
- data_error.py
- data_rdf_lat.py
- data_sorting.py



