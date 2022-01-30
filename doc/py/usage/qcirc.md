量子回路実行(QCircクラス, Backendクラス)
========================================

## 量子回路実行の基本

量子コンピュータで量子計算を行うというのは、欲しい結果を得るように設計
された量子回路を量子コンピュータに投入して測定結果を取得するということ
です。qlazyでは量子コンピュータはBackendクラスで用意して、それにQCirc
クラスで作成した量子回路を指定することで量子計算を実行します。

### 量子コンピュータの用意

Backendクラスのインスタンスを生成する際に引数product(製品名)と引数
device(デバイス名)を指定することで量子計算させる量子コンピュータ(また
はシミュレータ)を用意します。例えば、qlazyというproductの
qstate_simulator(状態ベクトルシミュレータ)というdeviceで計算させたい場
合、

    from qlazy import Backend
	bk = Backend(product='qlazy', device='qstate_simulator')

とします。qlazyのstabilizer_simulator(スタビライザーシミュレータ)で計
算させたい場合、

	bk = Backend(product='qlazy', device='stabilizer_simulator')

とします。

	bk = Backend()

のようにproductとdeviceを指定しない場合、qlazyのqstate_simulatorが指定
されます。

その他、現在のバージョンで対応しているバックエンドは、
[qulacs](https://github.com/qulacs/qulacs)と[IBM
Quantum(IBMQ)](https://quantum-computing.ibm.com/)です。使用法などの詳
細は「対応しているバックエンド」(後述)をご参照ください。


### 量子回路の作成

#### ユニタリゲート

量子コンピュータが用意できたら、次に量子回路を作成します。QStateクラス
やDensopクラスと同じ記法でQCircクラスのインスタンスにゲートを追加して
いきます。例えば、Bell状態を作成する回路を作成したい場合は、

    qc = QCirc()
    qc.h(0)
    qc.cx(0,1)

のようにします。hはアダマールゲート、cxはCNOTゲートを表します。または、

    qc = QCirc().h(0).cx(0,1)

のようにゲートをつなげて書いてもOKです。これで、

    q[0] --H--*---
              |
    q[1] -----X---
    
という回路が作成されたことになります。ここで、q[0],q[1]は量子ビットの
番号（量子レジスタ番号）を表しています。

#### パウリ積ゲート

パウリ演算子X,Y,Zのテンソル積を定義して量子回路に追加することができま
す。パウリ積を扱うために、まず、

    from qlazy import QCirc, PauliProduct
	
のようにPauliProductクラスをimportする必要があります。例えば、3量子ビッ
トの状態に対して、X2 Y0 Z1というパウリ積を演算したい場合、

	pp = PauliProduct(pauli_str="XYZ", qid=[2,0,1])
	qc = QCirc().operate(pp=pp)
	
のようにoperateメソッドのppオプションにPauliProductのインスタンスを指
定します。制御化されたパウリ積はoperateメソッドのctrlオプションに制御
量子ビット番号を指定することで実現できます。以下のようにします。

	pp = PauliProduct(pauli_str="XYZ", qid=[0,1,2])
	qc = QCirc().operate(pp=pp, ctlr=3)
	
#### 測定ゲート

測定する場合は、測定ゲートに測定する量子ビット番号のリストqidとその値
を格納するための古典ビット番号（古典メモリ番号または古典レジスタ番号）
のリストcidを指定します(qidの長さとcidは一致していなければなりません)。

    qc = QCirc().h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])
	
図で書くと、以下のような量子回路が作成されたことになります。

    q[0] --H--*---M
              |   |
    q[1] -----X---|--M
                  |  |
    c[0] ---------*--|--
                     |
    c[1] ------------*--

ここで、c[0],c[1]は古典ビット番号を表しています。

古典レジスタに格納されている測定結果に応じて、以降のゲート制御をしたい
ことがあります。そのような一例を以下に示します。

    qc = QCirc()
    qc.h(0).cx(0,1).measure(qid=[0],cid=[0])
    qc.x(0, ctrl=0).x(1, ctrl=0).measure(qid=[0,1], cid=[0,1])

h(0).cx(0,1)を追加した後にmeasure(qid=[0],cid=[0])を追加しています。つ
まり、0番目の量子ビットの測定結果を0番目の古典レジスタに格納します。次
にx(0, ctrl=0)と続きます。xはQStateクラスやDensOpクラスと同様パウリXゲー
トを表しており、最初の引数は適用する量子ビット番号です。QCircクラスで
は、ctrlという引数も指定することができます。これはこのゲートを適用する
か否かをctrlで指定した古典レジスタ番号に格納されている測定値によって決
めるということを表すためのものです。いまの例の場合、前段のmeasureで0番
目の量子ビットの測定結果を0番目の古典レジスタに格納していたので、その
値が0であったか1であったかによってパウリXゲートが実行されるかどうかが
決まります。1だった場合パウリXゲートが実行されます。次のx(1, ctrl=0)も
同様の考え方で実行が制御されるパウリXゲートです。最後に再びmeasureです。
今度は0番目と1番目の量子ビットが測定され、結果が0番目と1番目の古典レジ
スタに格納されます。図で書くと、以下のような量子回路が作成されたことに
なります。

    q[0] --H--*---M---------X------M
              |   |         |
    q[1] -----X---|--M------|---X--M
                  |  |      |   | 
    c[0] ---------*--|------*---*--
                     |
    c[1] ------------*-------------


#### リセットゲート

特定の量子ビットを強制的に|0>にすることができます。例えば、以下のよう
にresetメソッドを使います。

    qc = QCirc().h(0).cx(0,1).reset(qid=[0])

qidオプションには|0>にしたい量子ビット番号を指定します。

#### 量子回路の連結

複数の量子回路を'+'でつなげることで連結させることができます。例えば、

    qc_A = QCirc().h(0)
	qc_B = QCirc().cx(0,1)
	qc_C = QCirc().measure(qid=[0], cid=[0])

という3つの量子回路があったとき、

    qc = qc_A + qc_B + qc_C

のようにすると、

    q[0] --H---*------
               |
    q[1] ------X---M
                   |
    c[0] ----------*--

という量子回路を作成することができます。また、

    qc = qc_A
    qc += qc_B
    qc += qc_C

のようにインクリメント演算子を使って連結することも可能です。

#### 量子計算の実行

量子計算を実行するには、Backendクラスのrunメソッドを使います。

	bk = Backend()  # qlazyの状態ベクトルシミュレータ(デフォルト)
    qc = QCirc().h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])
	result = bk.run(qcirc=qc, shots=100)

上記のようにrunメソッドの引数qcircに量子回路、引数shotsに測定回数を指
定します。結果はresult(Resultクラスのインスタンス)に格納されます。
resultにはcidとfrequencyという2つのプロパティが定義されていて、各々、

    print(result.cid)
	>>> [0,1]
	print(result.frequency)
	>>> Counter({'00': 52, '11': 48})
	
のように値を取り出すことができます。cidは測定値が格納されている古典レ
ジスタの番号リストです。runのオプションとして頻度を取得したい古典レジ
スタ番号cidを指定することもできます。例えば、上の回路で、

	result = bk.run(qcirc=qc, shots=100, cid=[0])

とすると、0番目の古典レジスタに入る値の頻度だけ取り出すことができて、

    print(result.cid)
	>>> [0]
    print(result.frequency)
    >>> Counter({'0': 51, '1': 49})

という結果を得ることができます(いわゆる周辺化ですね)。cidを省略した場
合、全古典レジスタにわたり頻度が計算されます。


#### 量子状態の取得(qlazyの場合のみ)

qlazyの状態ベクトルシミュレータまたはスタビライザーシミュレータで量子
計算を実行した場合、resutlのinfoプロパティとして格納されている辞書デー
タから以下のようにして、量子状態またはスタビライザー状態を取り出すこと
ができます。

    qc = QCirc().h(0).cx(0,1)
    qs_sim = Backend(product='qlazy', device='qstate_simulator')
    result = qs_sim.run(qcirc=qc)
    qs = result.info['qstate']
    qs.show()
    >>> c[00] = +0.7071+0.0000*i : 0.5000 |++++++
    >>> c[01] = +0.0000+0.0000*i : 0.0000 |
    >>> c[10] = +0.0000+0.0000*i : 0.0000 |
    >>> c[11] = +0.7071+0.0000*i : 0.5000 |++++++

    qc = QCirc().h(0).cx(0,1)
    sb_sim = Backend(product='qlazy', device='stabilizer_simulator')
    result = sb_sim.run(qcirc=qc)
    sb = result.info['stabilizer']
    sb.show()
    >>> g[0]:  XX
    >>> g[1]:  ZZ


### 対応している量子ゲート

以下に利用可能な量子ゲートの一覧を示します。指定できる引数はQStateクラ
スやDensOpクラスのものと同様で、さらに上で説明したctrlという引数がすべ
てユニタリゲートで指定できます(非ユニタリゲートには指定できません)。

#### 1量子ビットゲート(ユニタリゲート)

- x,y,z: Pauli X/Y/Z gate
- h: Hadamard gate
- xr,xr_dg: root X and root X dagger gate
- s,s_dg: S and S dagger gate
- t,t_dg: T and T dagger gate
- p: phase shift gate
- rx,ry,rz: RX/RY/RZ (rotation around X/Y/Z-axis) gate

#### 2量子ビットゲート(ユニタリゲート)

- cx,cy,cz: controlled X/Y/Z gate
- cxr,cxr_dg: controlled XR and XR dagger gate
- ch: controlled Hadamard gate
- cs,cs_dg: controlled S and S dagger gate
- ct,ct_dg: controlled T and T dagger gate
- sw: swap gate
- cp: controlled P gate
- crx,cry,crz: controlled RX/RY/RZ gate

#### 3量子ビットゲート(ユニタリゲート)

- ccx: toffoli gate (or CCX gate, controlled controlled X gate)
- csw: fredkin gate (or controlled swap gate)

#### 測定ゲート(非ユニタリゲート)

- measure: measurement gate (computational basis)

#### リセットゲート(非ユニタリゲート)

- reset: reset gate (computational basis)

#### 注意：スタビライザーシミュレータの場合

'qlazy_stabilizer_simulator'の場合、実行できるのはクリフォードゲート
(x,y,z,h,s,s_dg,cx,cy,cz)のみです。


## 他形式との相互変換

qlazyで作成した量子回路をOpenQASM形式の文字列やファイルにエクスポート
したり、それらをインポートすることができます。

### OpenQASMへのエクスポート

to_qasmメソッドを使って、以下のようにQpenQASM形式の文字列を出力するこ
とができます。

    qc = QCirc().h(0).cx(0,1)
	qasm = qc.to_qasm()
	print(qasm)
    >> OPENQASM 2.0;
    >> include "qelib1.inc";
    >> qreg q[2];
    >> h q[0];
    >> cx q[0],q[1];

to_qasm_fileメソッドを使って、以下のようにOpenQASM形式のファイルを出力
することができます。

	qc.to_qasm_file("foo.qasm")

### OpenQASMからのインポート

from_qasmメソッドおよびfrom_qasm_fileメソッドを使って、以下のように
OpenQASM(バージョン2.0)の文字列およびファイルからqlazyの量子回路を作成
することができます。

    qc = QCirc.from_qasm(qasm)  # qasm: OpenQASM string
    qc = QCirc.from_qasm_file("foo.qasm")  # foo.qasm: OpenQASM file

ただし、非ユニタリゲート(measure,reset)やユーザーがカスタマイズしたゲー
トには対応していません。対応しているゲートは、'x', 'y', 'z', 'h', 's',
'sdg', 't', 'tdg', 'cx', 'cz', 'ch', 'rx', 'rz', 'crz'の14種類です。


## 少し高度な技

### レジスタの設定

大規模な量子回路を相手に量子プログラミングしたい場合、レジスタ関連ツー
ルを使うと便利です。

まず、

    from qlazy.tools.Register import CreateRegister,InitRegister

という具合に、CreateRegister関数とInitRegister関数をインポートします。
典型的な使い方は以下の通りです。

    dat = CreateRegister(3)
    anc = CreateRegister(2)
    qubit_num = InitRegister(dat, anc)

これは、3つのデータ量子ビットと2つの補助量子ビットを用意する例です。

    print(dat)
    >>> [0,1,2]
	print(anc)
    >>> [3,4]
    print(qubit_num)
    >>> 5

という具合にdatやancに量子ビット番号が順番に重ならないようにリストとし
て設定され、InitRegister関数の結果、合計のビット数がリターンされます。
レジスタを1次元配列としてではなく、多次元配列にして管理したい場合もあ
るかと思います。その場合は、

    qid = CreateRegister(3,3)
	qubit_num = InitRegister(qid)

とすると、3X3の2次元配列として、

    print(qid)
    >>> [[0,1,2],[3,4,5],[6,7,8]]
    print(qubit_num)
    >>> 9

のようにレジスタがセットされます。3次元以上の配列も同じように、

    qid = CreateRegister(2,3,4)
    qubit_num = InitRegister(qid)

    print(qid)
    >>> [[[0,1,2,3],[4,5,6,7],[8,9,10,11]],[[12,13,14,15],[16,17,18,19],[20,21,22,23]]]
    print(qubit_num)
    >>> 24

とできます。量子レジスタと古典レジスタの両方をセットする場合は、

    # 量子レジスタ
    qid = CreateRegister(2)
    qubit_num = InitRegister(qid)

    # 古典レジスタ
    cid = CreateRegister(2)
    cmem_num = InitRegister(cid)

    # 量子コンピュータ(バックエンド)の用意
    bk = Backend('qlazy_stabilizer_simulator')

    # 量子回路の設定と実行
    qc = QCirc().h(qid[0]).cx(qid[0],qid[1]).measure(qid=qid[0], cid=cid[0])
    ...
    result = bk.run(qcirc=qc, shots=10)
    ...

とします。量子レジスタと古典レジスタの番号は別々に割り振りたいので、各々
でCreateRegisterとInitRegisterを実行しています。

### カスタムゲートの追加

QCircクラスを継承することで、自分専用の量子ゲートを簡単に作成・追加す
ることができます。ベル状態を作成する回路をbellメソッドとして、QCircを
継承したMyQCircクラスに追加する例を示します。

    class MyQCirc(QCirc):

        def bell(self, q0, q1):
            self.h(q0).cx(q0,q1)
            return self

    bk = Backend()
    qc = MyQCirc().bell(0,1).measure(qid=[0,1], cid=[0,1])
    result = bk.run(qcirc=qc, shots=10)
    ...

これは非常に簡単な例なのであまりご利益を感じないかもしれませんが、大き
な量子回路を繰り返し使いたい場合など、便利に使える場面は多いと思います。


## 対応しているバックエンド

現在のバージョンで対応しているバックエンドは[qulacs](https://github.com/qulacs/qulacs)と
[IBM Quantum](https://quantum-computing.ibm.com/)です。
各々の使い方について、以下で説明します。

### qulacs

[qulacs](https://github.com/qulacs/qulacs)は、[株式会社
QunaSys](https://qunasys.com/)が提供しているオープンソースの量子回路シ
ミュレータで、GPUを利用して高速計算が実行できるという特徴があります。

[qlazy](https://quantum-computing.ibm.com/)の簡単なインターフェースで
GPUを利用した高速計算を実行したい場合、このバックエンドがおすすめです。

#### 準備

まず、[Installation - Qulacs ドキュメント](http://docs.qulacs.org/ja/latest/intro/1_install.html)
あたりを参照しながらインストールしてください。

### 使用法

GPUを利用しないシミュレータで計算させたい場合、

    bk = Backend(product='qulacs', device='cpu_simulator')

GPUを利用したシミュレータで計算させたい場合、

    bk = Backend(product='qulacs', device='gpu_simulator')

のように指定します(deviceを省略した場合のデフォルト値は'cpu_simulator'です)。

あとは上述したように、

	qc = QCirc().h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])
	result = bk.run(qcirc=qc, shots=100)

のようにすれば、qulacsを使った計算ができます。

### IBM Quantum

[IBM Quantum(IBMQ)](https://quantum-computing.ibm.com/)は、
[IBM](https://www.ibm.com/jp-ja)が開発した量子コンピュータ（およびシミュ
レータ）を利用するためのクラウドサービスです。

[qlazy](https://quantum-computing.ibm.com/)の簡単なインターフェースで
本物の量子コンピュータを利用した計算を実行したい場合、このバックエンドが
おすすめです。

#### 準備

IBMQやローカルシミュレータをPythonから利用するためのライブラリである
[qiskit](https://qiskit.org/)をインストールして、量子計算を実行できる
環境を整えてください。例えば、[Quantum Native
Dojo!](https://dojo.qulacs.org/ja/latest/)の[3-2. QiskitとIBM Q
Experienceの使い
方](https://dojo.qulacs.org/ja/latest/notebooks/3.2_Qiskit_IBMQ.html)
に一連の手続きからサンプルコードまで含めて日本語でやさしく書かれていま
すので、これを参考にやってみるのが早いと思います。ただし、IBMQへのリン
クが古いみたいです。正しくは
[https://quantum-computing.ibm.com/](https://quantum-computing.ibm.com/)
です。

#### 使用法

本物の量子コンピュータを利用しないでローカルなシミュレータで計算させたい場合、

    bk = Backend(product='ibmq', device='qasm_simulator')

のように指定します。本物の量子コンピュータを利用したい場合は、例えば、

    bk = Backend(product='ibmq', device='least_busy')

のように指定します。'least_busy'というのは、自分のアカウントで利用可能
な量子コンピュータシステムの中で、現在最も空いているシステムを自動選択
して実行するためのものです。実行するシステムを明示的に指定することもで
きます。例えば、'ibmq_athens'で実行したい場合、

    bk = Backend(product='ibmq', device='ibmq_athens')
	
のように指定します(deviceを省略した場合のデフォルト値は'qasm_simulator'です)。

あとは上述したように、

    qc = QCirc().h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])
	result = bk.run(qcic=qc, shots=100)

のようにすれば、IBMQを使った計算ができます。


以上
