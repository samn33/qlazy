量子コンピュータ(QCompクラス, Backendクラスなど)
=================================================

## 量子コンピュータ操作の基本

量子コンピュータで量子計算を行うというのは、欲しい結果を得るように設計
された量子回路をユニタリゲートと測定の組み合わせという形で用意しておき、
それを量子コンピュータに投入して測定結果を取得するということです。
QCompクラスは、そのような一連の操作を実行できるように量子コンピュータ
そのものを抽象化したクラスです。このクラスを使って、どのように量子計算
を実行するかについて、以下で説明します。

### 量子コンピュータの生成・初期化

量子計算を実行するためには、当たり前ですが、まず量子コンピュータを用意
する必要があります。QCompのインスタンスを生成するときに、どの量子コン
ピュータのバックエンドで計算をさせるかをproduct(製品名)とdevice(デバイ
ス名)の組で指定します。例えば、qlazyというproductのqstate_simulatorと
いうdeviceで計算させたい場合、

    from qlazy import QComp
	qc = QComp(product='qlazy', device='qstate_simulator')

とします。qlazyのstabilizer_simulatorで計算させたい場合、

	qc = QComp(product='qlazy', device='stabilizer_simulator')

とします。

	qc = QComp()

のようにproductとdeviceを指定しない場合、qlazyのqstate_simulatorが指定
されます。その他、現在のバージョンで対応しているバックエンドは、
[qulacs](https://github.com/qulacs/qulacs)と[IBM Quantum(IBMQ)](https://quantum-computing.ibm.com/)です。
使用法などの詳細は「対応しているバックエンド」(後述)をご参照ください。


### 量子回路の設定と実行

#### 測定

量子コンピュータが用意できたら、次に量子回路を設定します。QStateクラス
やDensopクラスと同じ記法でゲートを追加していきます。例えば、Bell状態を
作成する回路を設定したい場合は、

    qc = QComp()
    qc.h(0)
    qc.cx(0,1)

のようにします。hはアダマールゲート、cxはCNOTゲートを表します。または、

    qc = QComp()
    qc.h(0).cx(0,1)

のようにゲートをつなげて書いてもOKです。これで量子コンピュータ内部に、

    q0 --H--*---
            |
    q1 -----X---
    
という回路が設定されたことになります。ここで、q0,q1は量子レジスタを表
しています。

QStateクラスやDensOpクラスやStabilizerクラスと違い、この段階ではまだゲー
ト演算は実行されていません。以下のようにrunメソッドを適用することでは
じめて実行されます(初期状態は常に|00...0>です。いまの例は2量子ビットな
ので|00>です)。

    qc.h(0).cx(0,1).run()

しかし、計算結果は測定をしないと得られないので、これでは意味がありませ
ん。測定を表すゲートmeasureを付加して、以下のようにすれば、測定結果を
取得することができます。

    qc.h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])
	result = qc.run(shots=10)
	
回路図で書くと、以下のような操作に相当します。

    q0 --H--*---M
            |   |
    q1 -----X---|--M
                |  |
    c0 ---------*--|--	
    c1 ------------*--

ここで、1行目のmeasureメソッドは計算基底で測定するためのゲートで、qid
に測定する量子ビット番号(量子レジスタ番号)を指定し、cidにその結果を格
納する古典レジスタ番号を指定します。ここでqidの長さとcidの長さは一致し
ている必要があります。cidをまったく指定しないということも許されますが、
その場合測定して状態は変化しますが測定値をどこにも格納しないという操作
を意味します。

測定を含んだ量子回路が設定できたらば、2行目に示すようにrunメソッドを呼
び出して実行します。runのオプションとして指定されているshotsは実行回数
(=測定回数)を表しています。これで測定結果がresult変数に格納されること
になります。resultにはcidとfrequencyという２つのプロパティが定義されて
いて、各々、

    print(result.cid)
	>>> [0,1]
	print(result.frequency)
	>>> Counter({'00': 6, '11': 4})
	
のように値を取り出すことができます。測定がない回路、あるいは測定しても
古典レジスタに測定値を格納しない（measureでcidを指定しない）回路の場合、
resultにはNoneが入ります。

runのオプションとして頻度を取得したい古典レジスタ番号cidを指定すること
もできます。例えば、上の回路で、

	result = qc.run(shots=10, cid=[1])

とすると、1番目の古典レジスタに入る値の頻度だけ取り出すことができて、

    print(result.cid)
	>>> [1]
    print(result.frequency)
    >>> Counter({'0': 6, '1': 4})

という結果を得ることができます（いわゆる周辺化ですね）。cidを省略した
場合、全古典レジスタにわたり頻度が計算されます。

#### 測定結果に応じたゲート演算制御

古典レジスタに格納されている測定結果に応じて、以降のゲート制御をしたい
ことがあります。そのような一例を以下に示します。

    qc = QComp()
    qc.h(0).cx(0,1).measure(qid=[0],cid=[0]).x(0, ctrl=0).x(1, ctrl=0).measure(qid=[0,1], cid=[0,1])
	result = qc.run(shots=10)
	print(result.frequency)

2行目の量子回路を設定する部分で、まずh(0).cx(0,1)を追加した後に
measure(qid=[0],cid=[0])を追加しています。つまり、0番目の量子ビットの
測定結果を0番目の古典レジスタに格納します。次にx(0, ctrl=0)と続きます。
xはQStateクラスやDensOpクラスと同様パウリXゲートを表しており、最初の引
数は適用する量子ビット番号です。QCompクラスでは、ctrlという引数も指定
することができます。これはこのゲートを適用するか否かをctrlで指定した古
典レジスタ番号に格納されている測定値によって決めるということを表すため
のものです。いまの例の場合、前段のmeasureで0番目の量子ビットの測定結果
を0番目の古典レジスタに格納していたので、その値が0であったか1であった
かによってパウリXゲートが実行されるかどうかが決まります。1だった場合パ
ウリXゲートが実行されます。次のx(1, ctrl=0)も同様の考え方で実行が制御
されるパウリXゲートです。最後に再びmeasureです。今度は0番目と1番目の量
子ビットが測定されます(cidが指定されていないので、古典レジスタに結果は
格納されません)。

3行目でrunによって、この回路が実行されます。shots=10と指定したので実行
回数は10回です。そして、その測定値の頻度がカウントされて、測定量子ビッ
ト番号リストとともにresultに格納されます。ここでご注意いただきたいので
すが、runで測定結果がカウントされるのは、一番最後のmeasureに対してです。
途中のmeasureの結果はカウントされません。

というわけで、この例の結果はどうなるかわかりますでしょうか？答えは、

    Counter({'00': 10})

です。最初のh(0).cx(0,1)で|00>+|11>というBell状態になり(規格化定数は省
略)、0番目の量子ビットを測定して結果が0だった場合は、以降何もしないの
で最終状態は|00>となり、1だった場合は全ビットをビット反転するので最終
状態は|11>のビット反転で|00>になります。これを最後に測定するので、100%
の確率で|00>になります。

#### リセット

特定の量子ビットを強制的に|0>にすることができます。例えば、以下のよう
にresetメソッドを使います。qidオプションには|0>にしたい量子ビット番号
を指定します。何も指定しなかった場合、すべての量子ビットが|0>にリセッ
トされます。

    qc = QComp()
    qc.h(0).cx(0,1).reset(qid=[0]).measure(qid=[0,1], cid=[0,1])
	result = qc.run(shots=10)
	print(result.frequency)

この実行結果は、

    Counter({'00': 6, '01': 4})

のようになります。

### 量子コンピュータの解放

生成・初期化した量子コンピュータのメモリ領域は使われなくなったら自動的
に解放されます。が、delで明示的に好きなタイミングで解放することもでき
ます。

    del qc

基本は以上です。

### 対応している量子ゲート

以下に利用可能な量子ゲートを示します。指定できる引数はQStateクラスや
DensOpクラスのものと同様で、さらに上で説明したctrlという引数がすべてユ
ニタリゲートで指定できます。

#### 1量子ビットゲート（ユニタリゲート）

- x,y,z: Pauli X/Y/Z gate
- h: Hadamard gate
- xr,xr_dg: root X and root X dagger gate
- s,s_dg: S and S dagger gate
- t,t_dg: T and T dagger gate
- p: phase shift gate
- rx,ry,rz: RX/RY/RZ (rotation around X/Y/Z-axis) gate
- u1,u2,u3: U1/U2/U3 gate (by IBM)

#### 2量子ビットゲート（ユニタリゲート）

- cx,cy,cz: controlled X/Y/Z gate
- cxr,cxr_dg: controlled XR and XR dagger gate
- ch: controlled Hadamard gate
- cs,cs_dg: controlled S and S dagger gate
- ct,ct_dg: controlled T and T dagger gate
- sw: swap gate
- cp: controlled P gate
- crx,cry,crz: controlled RX/RY/RZ gate
- cu1,cu2,cu3: controlled U1/U2/U3 gate

#### 3量子ビットゲート（ユニタリゲート）

- ccx: toffoli gate (or CCX gate, controlled controlled X gate)
- csw: fredkin gate (or controlled swap gate)

#### 測定ゲート（非ユニタリゲート）

- measure: measurement gate (computational basis)

#### リセットゲート（非ユニタリゲート）

- reset: reset gate (computational basis)

#### 注意：スタビライザーシミュレータの場合

'qlazy_stabilizer_simulator'の場合、実行できるのはクリフォードゲート
(x,y,z,h,s,s_dg,cx,cy,cz)のみです。


### パウリ積の演算

パウリ演算子X,Y,Zのテンソル積を定義して量子コンピュータに設定すること
ができます。パウリ積を扱うために、まず、

    from qlazy import QComp, PauliProduct
	
のようにPauliProductクラスをimportする必要があります。例えば、3量子ビッ
トの状態に対して、X2 Y0 Z1というパウリ積を演算したい場合、

    qs = QComp()
	pp = PauliProduct(pauli_str="XYZ", qid=[2,0,1])
	qc.operate(pp=pp)
	
のようにoperateメソッドのppオプションにPauliProductのインスタンスを指
定します。制御化されたパウリ積はoperateメソッドのctrlオプションに制御
量子ビット番号を指定することで実現できます。以下のようにします。

    qc = QComp()
	pp = PauliProduct(pauli_str="XYZ", qid=[0,1,2])
	qc.operate(pp=pp, ctlr=3)
	
量子ゲートの設定の場合と同様、operateメソッドを実行しただけでは実際の
演算は実行されていません。runメソッド（およびその前にmeasurementメソッ
ドがないと意味ある結果が得られません）を適用することではじめて実行され
ます。


## 少し高度な技

### 量子回路をクリアしない実行

上で説明した基本パターンを改めてまとめると、
- (1) バックエンドの定義
- (2) 量子コンピュータの初期化（バックエンドを指定）
- (3) 量子回路の設定(ユニタリゲートと非ユニタリゲートを次々に追加)
- (4) 量子回路の実行と結果取得
ということになります。

例えば、

    from qlazy import QComp, Backend
	bk = Backend(name='qlazy', device='qstate_simulator')
	qc = QComp(backend=bk)
    result = qc.x(0).measure(qid=[0], cid=[0]).run(shots=10)
    print(result.frequency)

という具合です。ここで、5行目のrunを実行したら、量子コンピュータ内部の
「量子回路」はクリアされる仕様になっています。なので、再びrunしても何
も起きません。しかし、同じ量子回路を保持したまま繰り返し何度も計算実行
したい場合やすでに設定済の量子回路にさらにゲートを追加して計算実行した
い場合があるかもしれません。そういった場合、runのオプションclear_qcirc
にFalseを指定することで量子回路をクリアしないようにできます。

上の例で、

    result = qc.x(0).measure(qid=[0], cid=[0]).run(shots=10)
    print(result.frequency)
    result = qc.x(0).measure(qid=[0], cid=[0]).run(shots=10)
    print(result.frequency)

を繰り返しても、結果は、

    Counter({'1': 10})
    Counter({'1': 10})

となり同じですが、以下のようにclear_qcircをFalseにすると、

    result = qc.x(0).measure(qid=[0], cid=[0]).run(shots=10, clear_qcirc=False)
    print(result.frequency)
    result = qc.x(0).measure(qid=[0], cid=[0]).run(shots=10)
    print(result.frequency)


結果は、

    Counter({'1': 10})
    Counter({'0': 10})

となります。2番めのrunではビット反転を2回やった結果に対して測定するの
で元の初期状態に戻るというわけです。


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
	qc = QComp(qubit_num=qubit_num)

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

    # 量子コンピュータの初期化
    bk = Backend('qlazy_stabilizer_simulator')
    qc = QComp(qubit_num=qubit_num, cmem_num=cmem_num)

    # 量子回路の設定と実行
    qc.h(qid[0]).cx(qid[0],qid[1]).measure(qid=qid[0], cid=cid[0])
    ...
    qc.run(shots=10)
    ...

とします。量子レジスタと古典レジスタの番号は別々に割り振りたいので、各々
でCreateRegisterとInitRegisterを実行します。

### カスタムゲートの追加

QCompクラスを継承することで、自分専用の量子ゲートを簡単に作成・追加す
ることができます。ベル状態を作成する回路をbellメソッドとして、QCompを
継承したMyQCompクラスに追加する例を示します。

    class MyQComp(QComp):

        def bell(self, q0, q1):
            self.h(q0).cx(q0,q1)
            return self

    qc = MyQComp(name='qlazy', device='qstate_simulator')
    result = qc.bell(0,1).measure(qid=[0,1], cid=[0,1]).run(shots=10)
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

    bk = Backend(name='qulacs', device='cpu_simulator')

GPUを利用したシミュレータで計算させたい場合、

    bk = Backend(name='qulacs', device='gpu_simulator')

のように指定します(deviceを省略した場合のデフォルト値は'cpu_simulator'です)。

あとは上述したように、

	qc = QComp(qubit_num=2, cmem_num=2, backend=bk)
    qc.h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])
	result = qc.run(shots=100)

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

    bk = Backend(name='ibmq', device='qasm_simulator')

のように指定します。本物の量子コンピュータを利用したい場合は、例えば、

    bk = Backend(name='ibmq', device='least_busy')

のように指定します。'least_busy'というのは、自分のアカウントで利用可能
な量子コンピュータシステムの中で、現在最も空いているシステムを自動選択して実行する
ためのものです。実行するシステムを明示的に指定することもできます。
例えば、'ibmq_athens'で実行したい場合、

    bk = Backend(name='ibmq', device='ibmq_athens')
	
のように指定します(deviceを省略した場合のデフォルト値は'qasm_simulator'です)。

あとは上述したように、

	qc = QComp(qubit_num=2, cmem_num=2, backend=bk)
    qc.h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])
	result = qc.run(shots=100)

のようにすれば、IBMQを使った計算ができます。

本物の量子コンピュータを使った計算に関して一点注意事項があります。量子
回路を設定してrunする際に、clear_qubits=Falseは指定できません。一度run
して結果が返ってきたら、IBMQ側の量子状態は有無を言わさず解放されるので
(少なくとも現在のIBMQでは...)、qlazy側でそれを保持しておく手段がないからです。


以上
