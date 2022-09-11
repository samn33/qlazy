量子回路実行(QCircクラス, Backendクラス)
========================================

## 量子回路実行の基本

量子コンピュータで量子計算を行うというのは、欲しい結果を得るように設計
された量子回路を量子コンピュータに投入して測定結果を取得するということ
です。qlazyでは量子コンピュータをBackendクラスで用意して、それにQCirc
クラスで作成した量子回路を指定することで量子計算を実行します。

### 量子コンピュータの用意

Backendクラスのインスタンスを生成する際に引数product(製品名)と引数
device(デバイス名)を指定することで量子計算させる量子コンピュータ(また
はシミュレータ)を設定します。例えば、qlazyというproductの
qstate_simulator(状態ベクトルシミュレータ)というdeviceで計算させたい場
合は、

    >>> from qlazy import Backend
	>>> bk = Backend(product='qlazy', device='qstate_simulator')

とします。qlazyのstabilizer_simulator(スタビライザーシミュレータ)で計
算させたい場合、

	>>> bk = Backend(product='qlazy', device='stabilizer_simulator')

とします。qlazyのmps_simulator(行列積状態シミュレータ)で計算させたい場
合、

	>>> bk = Backend(product='qlazy', device='mps_simulator')

とします。

	>>> bk = Backend()

のようにproductとdeviceを指定しない場合、qlazyのqstate_simulatorが指定
されます。

その他、現在のバージョンで対応しているバックエンドは、
[qulacs](https://github.com/qulacs/qulacs)と[IBM Quantum(IBMQ)](https://quantum-computing.ibm.com/)
と[Amazon Braket(LocalSimulator,AWS,IonQ,Rigetti,OQC)](https://aws.amazon.com/braket/?nc1=h_ls)です。
使用法などの詳細は「対応しているバックエンド」(後述)をご参照ください。

対応しているproductは、

    >>> print(Backend.products())
    ['qlazy', 'qulacs', 'ibmq', 'braket_local', 'braket_aws', 'braket_ionq', 'braket_rigetti', 'braket_oqc']

とすれば確認できます。各々のproductで使えるdeviceは、例えば、

	>>> print(Backend.devices('ibmq'))
    ['aer_simulator', 'qasm_simulator', 'least_busy', 'ibmq_armonk', 'ibmq_bogota', 'ibmq_lima', 'ibmq_belem', 'ibmq_quito', 'ibmq_manila']

とすれば確認できます。


### 量子回路の作成

#### ユニタリゲート

量子コンピュータが用意できたら、次に量子回路を作成します。QStateクラス
やDensopクラスと同じ記法でQCircクラスのインスタンスにゲートを追加して
いきます。例えば、Bell状態を作成する回路を作成したい場合は、

    >>> from qlazy import QCirc
    >>> qc = QCirc()
    >>> qc.h(0)
    >>> qc.cx(0,1)

のようにします。ここでhはアダマールゲート、cxはCNOTゲートを表します。
または、

    >>> qc = QCirc().h(0).cx(0,1)

のようにゲートをつなげて書いてもOKです。

これで、

    q[0] --H--*---
              |
    q[1] -----X---
    
という回路が作成されたことになります。ここで、q[0],q[1]は量子ビットの
番号（量子レジスタ番号）を表しています。

#### パウリ積ゲート

パウリ演算子X,Y,Zのテンソル積を定義して量子回路に追加することができま
す。パウリ積を扱うために、まず、

    >>> from qlazy import QCirc, PauliProduct
	
のようにPauliProductクラスをimportする必要があります。例えば、3量子ビッ
トの状態に対して、X2 Y0 Z1というパウリ積を演算したい場合、

	>>> pp = PauliProduct(pauli_str="XYZ", qid=[2,0,1])
	>>> qc = QCirc().operate(pp=pp)
	
のようにoperateメソッドのppオプションにPauliProductのインスタンスを指
定します。制御化されたパウリ積はoperateメソッドのctrlオプションに制御
量子ビット番号を指定することで実現できます。以下のようにします。

	>>> pp = PauliProduct(pauli_str="XYZ", qid=[0,1,2])
	>>> qc = QCirc().operate(pp=pp, ctlr=3)
	
#### 測定ゲート

測定する場合は、測定ゲートに測定する量子ビット番号のリストqidとその値
を格納するための古典ビット番号（古典メモリ番号または古典レジスタ番号）
のリストcidを指定します(qidとcidの長さは一致していなければなりません)。

    >>> qc = QCirc().h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])
	
図で書くと、以下のような量子回路が作成されたことになります。

    q[0] --H--*---M
              |   |
    q[1] -----X---|--M
                  |  |
    c[0] ---------*--|--
                     |
    c[1] ------------*--

ここで、c[0],c[1]は古典ビット番号を表しています。

古典ビットに格納されている測定結果に応じて、以降のゲート制御をしたい
ことがあります。そのような一例を以下に示します。

    >>> qc = QCirc()
    >>> qc.h(0).cx(0,1).measure(qid=[0],cid=[0])
    >>> qc.x(0, ctrl=0).x(1, ctrl=0).measure(qid=[0,1], cid=[0,1])

h(0).cx(0,1)を追加した後にmeasure(qid=[0],cid=[0])を追加しています。つ
まり、0番目の量子ビットの測定結果を0番目の古典レジスタに格納します。次
にx(0, ctrl=0)と続きます。xはQStateクラスやDensOpクラスと同様パウリXゲー
トを表しており、最初の引数は適用する量子ビット番号です。QCircクラスで
は、ctrlという引数も指定することができます。これはこのゲートを適用する
か否かをctrlで指定した古典ビット番号に格納されている測定値によって決め
るということを表すためのものです(qiskitのc_ifに対応)。いまの例の場合、
前段のmeasureで0番目の量子ビットの測定結果を0番目の古典レジスタに格納
していたので、その値が0であったか1であったかによってパウリXゲートが実
行されるかどうかが決まります。1だった場合パウリXゲートが実行されます。
次のx(1, ctrl=0)も同様の考え方で実行が制御されるパウリXゲートです。最
後に再びmeasureです。今度は0番目と1番目の量子ビットが測定され、結果が0
番目と1番目の古典レジスタに格納されます。図で書くと、以下のような量子
回路が作成されたことになります。

    q[0] --H--*---M---------X-------M
              |   |         |       |
    q[1] -----X---|--M------|---X---|--M
                  |  |      |   |   |  |
    c[0] ---------*--|------*---*---*--|--
                     |                 |
    c[1] ------------*-----------------*--


#### リセットゲート

特定の量子ビットを強制的に|0>にすることができます。例えば、以下のよう
にresetメソッドを使います。

    >>> qc = QCirc().h(0).cx(0,1).reset(qid=[0])

qidオプションには|0>にしたい量子ビット番号を指定します。


### 量子計算の実行

量子計算を実行するには、Backendクラスのrunメソッドを使います。

	>>> bk = Backend()  # qlazyの状態ベクトルシミュレータ(デフォルト)
    >>> qc = QCirc().h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])
	>>> result = bk.run(qcirc=qc, shots=100)

上記のようにrunメソッドの引数qcircに量子回路、引数shotsに測定回数を指
定します。結果はresult(Resultクラスのインスタンス)に格納されます。
Resultにはcidとfrequencyという2つのプロパティが定義されていて、各々、

    >>> print(result.cid)
	[0,1]
	>>> print(result.frequency)
	Counter({'00': 52, '11': 48})
	
のように値を取り出すことができます。cidは測定値が格納されている古典レ
ジスタの番号リストです。runのオプションとして頻度を取得したい古典レジ
スタ番号cidを指定することもできます。例えば、上の回路で、

	>>> result = bk.run(qcirc=qc, shots=100, cid=[0])

とすると、0番目の古典レジスタに入る値の頻度だけ取り出すことができて、

    >>> print(result.cid)
	[0]
    >>> print(result.frequency)
    Counter({'0': 52, '1': 48})

という結果を得ることができます(いわゆる周辺化ですね)。cidを省略した場
合、全古典レジスタにわたり頻度が計算されます。

その他、バックエンド情報、量子ビット数、古典ビット数、測定した回数、計
算開始時刻、計算終了時刻、計算時間がResultのプロパティとして定義されていて、
各々以下のように取得することができます。

    >>> print(result.backend)
    {'product': 'qlazy', 'device': 'qstate_simulator'}
    >>> print(result.qubit_num)
    2
    >>> print(result.cmem_num)
    2
    >>> print(result.shots)
    100
    >>> print(result.start_time)
    2022-03-05 13:32:33.837965
    >>> print(result.end_time)
    2022-03-05 13:32:33.842534
    >>> print(result.elapsed_time)
    0.004569

とりあえず測定値の頻度だけわかりやすく見たいという場合は、
showメソッドを使って、

    >>> result.show()

とすれば、

    freq[00] = 54 (0.5400) |+++++++++++++++++
    freq[11] = 46 (0.4600) |++++++++++++++

と棒グラフで頻度を可視化して見ることができます。
棒グラフだけでなく、すべてを一度に表示したい場合は、
verboseオプションをTrueにして、

    >>> result.show(verbose=True)

とすれば、

    [backend]
    - product      = qlazy
    - device       = qstate_simulator
    [qubit & cmem]
    - qubit_num    = 2
    - cmem_num     = 2
    [measurement]
    - cid          = [0, 1]
    - shots        = 100
    [time]
    - start_time   = 2022-03-15 23:05:41.249034
    - end_time     = 2022-03-15 23:05:41.254211
    - elassed time = 0.005177 [sec]
    [histogram]
    - freq[00] = 54 (0.5400) |+++++++++++++++++
    - freq[11] = 46 (0.4600) |++++++++++++++

のように表示させることができます。

この実行結果をファイルとして保存したり、保存したものを読み出すこともできます。
saveメソッドを使って、

    >>> result.save("hoge.res")

としてファイルhoge.resに保存しておいて、loadメソッド(classmethod)を使って、

    >>> from qlazy import Result
    >>> result_load = Result.load("hoge.res")
	
とすれば、保存しておいた計算結果をロードして結果データを再度取得することができます。

Pythonワンライナーで、以下のように結果データを見ることもできます。

    $ python -c "from qlazy import Result; Result.load('hoge.res').show(verbose=True)"



#### 行列積状態シミュレータでの測定に関する注意事項

数十〜数百量子ビットの量子回路でもそれほど深くない回路でエンタングルが
あまりないような場合は難なく量子回路の演算が実行できたりするのですが、
最後に多数の量子ビットに対して大量のショット数で測定するようなことをす
ると、測定結果取得に途方もない時間がかかる場合があります。

行列積状態を使ったシミュレーションの主な用途は、NISCデバイス上での量子
機械学習や量子化学計算や最適化問題の求解等のシミュレーションと思われま
すので、測定値を取得するのではなく、すぐ下で説明するように行列積状態
MPStateのインスタンスを取得しておいてから、MPStateクラスのexpectメソッ
ドで期待値計算することをとりあえずおすすめします。


### 量子状態の取得(qlazyおよびqulacsのみ)

qlazyの状態ベクトルシミュレータ(qstate_simulator)またはスタビライザー
シミュレータ(stabilizer_simulator)または行列積状態シミュレータ
(mps_simulator)でrunを実行するときにout_stateオプションをTrueにセット
すると、Resultのプロパティqstateまたはstabilizerまたはmpstateに各クラ
スで規定されている量子状態がセットされます。これらをもとにQState,
Stabilizer, MPStateで定義されている各種計算が実行できます(例えばオブザー
バブルに対する期待値計算など)。詳細については各クラスに関するドキュメ
ントご参照してください。

    >>> qc = QCirc().h(0).cx(0,1)
    >>> qs_sim = Backend(product='qlazy', device='qstate_simulator')
    >>> result = qs_sim.run(qcirc=qc, out_state=True)
    >>> qs = result.qstate
    >>> qs.show()
    c[00] = +0.7071+0.0000*i : 0.5000 |++++++
    c[01] = +0.0000+0.0000*i : 0.0000 |
    c[10] = +0.0000+0.0000*i : 0.0000 |
    c[11] = +0.7071+0.0000*i : 0.5000 |++++++

    >>> qc = QCirc().h(0).cx(0,1)
    >>> sb_sim = Backend(product='qlazy', device='stabilizer_simulator')
    >>> result = sb_sim.run(qcirc=qc, out_state=True)
    >>> sb = result.stabilizer
    >>> sb.show()
    g[0]:  XX
    g[1]:  ZZ

    >>> qc = QCirc().h(0).cx(0,1)
    >>> mps_sim = Backend(product='qlazy', device='mps_simulator')
    >>> result = mps_sim.run(qcirc=qc, out_state=True)
    >>> mps = result.mpstate
    >>> mps.show()
    c[00] = +0.7071+0.0000*i : 0.5000 |++++++
    c[01] = +0.0000+0.0000*i : 0.0000 |
    c[10] = +0.0000+0.0000*i : 0.0000 |
    c[11] = +0.7071+0.0000*i : 0.5000 |++++++

また、qulacsの状態ベクトルシミュレータ(cpu_simulator, gpu_simulator)で
も同様にして、qlazyの状態ベクトルを取得することができます。

    >>> qc = QCirc().h(0).cx(0,1)
    >>> qs_sim = Backend(product='qulacs', device='cpu_simulator')
    >>> result = qs_sim.run(qcirc=qc, out_state=True)
    >>> qs = result.qstate
    >>> qs.show()
    c[00] = +0.7071+0.0000*i : 0.5000 |++++++
    c[01] = +0.0000+0.0000*i : 0.0000 |
    c[10] = +0.0000+0.0000*i : 0.0000 |
    c[11] = +0.7071+0.0000*i : 0.5000 |++++++


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
- rxx,ryy,rzz: Ising coupling gate

#### 3量子ビットゲート(ユニタリゲート)

- ccx: toffoli gate (or CCX gate, controlled controlled X gate)
- csw: fredkin gate (or controlled swap gate)

#### 測定ゲート(非ユニタリゲート)

- measure: measurement gate (computational basis)

#### リセットゲート(非ユニタリゲート)

- reset: reset gate (computational basis)

#### 注意：スタビライザーシミュレータの場合

'qlazy_stabilizer_simulator'の場合、指定できるのはクリフォードゲート
(x,y,z,h,s,s_dg,cx,cy,cz)のみです。


## 量子回路の操作

### 量子回路の表示

作成した量子回路はprint関数で表示することができます。例えば、

    >>> qc = QCirc()
    >>> qc.h(0).cx(0,1).measure(qid=[0],cid=[0])
    >>> qc.x(0, ctrl=0).x(1, ctrl=0).measure(qid=[0,1], cid=[0,1])
	>>> print(qc)

とすると、

    h 0
    cx 0 1
    measure 0 -> 0
    x 0 , ctrl = 0
    x 1 , ctrl = 0
    measure 0 -> 0
    measure 1 -> 1

のように表示されます。また、showメソッドを使ってもう少しビジュアルに表
示することもできます。

    >>> qc.show()
    q[0] -H-*-M-X---M---
    q[1] ---X-|-|-X-|-M-
    c  =/=====v=^=^=v=v=
        2     0 0 0 0 1


#### 量子回路の同等性

2つの量子回路が全く同じものかどうか（同等性と呼ぶことにします）は
論理演算子'=='で判定できます。

    >>> qc_A = QCirc().h(0).cx(0,1)
	>>> qc_B = QCirc().h(0).cx(0,1)
	>>> qc_C = QCirc().h(0).cx(1,0)
	>>> print(qc_A == qc_B)
	True
	>>> print(qc_A == qc_C)
	False

量子回路の等価性（一見違うように見えていても実は同等の効果を及ぼす回路）
の判定については後述します。

#### 量子回路の連結

複数の量子回路を'+'でつなげることで連結させることができます。例えば、

    >>> qc_A = QCirc().h(0)
	>>> qc_B = QCirc().cx(0,1)
	>>> qc_C = QCirc().measure(qid=[0], cid=[0])

という3つの量子回路があったとき、

    >>> qc = qc_A + qc_B + qc_C

のようにすると、

    q[0] --H---*------
               |
    q[1] ------X---M
                   |
    c[0] ----------*--

という量子回路を作成することができます。また、

    >>> qc = qc_A
    >>> qc += qc_B
    >>> qc += qc_C

のようにインクリメント演算子を使って連結することも可能です。

### 量子回路の統計情報

ここまでの説明でお気づきかと思いますが、qlazyでは最初の量子回路生成

    >>> qc = QCirc()

の段階で使用する量子ビット数や古典ビット数を明示的に指定しておく必要はありません。
追加された量子ゲート情報から自動的に内部で都度更新・保持されます。

    >>> qubit_num = qc.qubit_num
    >>> cmem_num = qc.cmem_num
	
で、量子ビット数と古典ビット数を取得できます。
また、使用されている量子ゲートの数も、

    >>> gate_num = qc.gate_num
	
で取得できます。例えば、

    >>> qc = QCirc().h(0).cx(1,0)
    >>> print(qc.qubit_num)
    2
    >>> print(qc.cmem_num)
	0
    >>> print(qc.gate_num)
    2

となります。

ここで1点注意事項があります。QCircで利用可能な量子ゲートは上述の通りな
のですが、内部的に扱われている量子ゲートは、
x,z,h,s,s_dg,t,t_dg,rx,rz,cx,cz,ch,crz,measure,resetの15種類に限定され
ています。他の量子ゲートはこれらを組み合わせて内部的に表現されています。
例えば、swゲートは、

    >>> qc.cx(0,1).cx(1,0).cx(0,1)
	
のように3個のゲート演算の形に展開されています。crxは、

    >>> qc.h(1).crz(0,1).h(1)

のように展開されています。また、measureやresetは1量子ビットごとの演算に展開されます。
つまり、

    >>> qc.measure(qid=[0,1], cid=[0,1])
    >>> qc.reset(qid=[0,1])

は、

    >>> qc.measure(qid=[0], cid=[0]).measure(qid=[1], cid=[1])
    >>> qc.reset(qid=[0]).reset(qid=[1])

のように展開されます。なので、qc.gate_numで取得した値が自分の意図した
値よりも大きくなっていて、ん？となることがあるかもしれませんが、このよ
うな理由によるものです(どのように展開されたかはprint(qc)で確認できます)。

量子ビット数、古典ビット数、量子ゲート数に加えて、量子ゲートの頻度を知りたい場合、
get_statsメソッドを使えば、一気に取得することができます。
以下のような辞書データとして結果が得られます。

    >>> qc = QCirc().h(0).cx(1,0).t(1).measure(qid=[0,1], cid=[0,1])
	>>> print(qc.get_stats())
    {'qubit_num': 2, 'cmem_num': 2, 'gate_num': 5, 'gate_freq': Counter({'measure': 2, 'h': 1, 'cx': 1, 't': 1}), 'gatetype_freq': Counter({'unitary': 3, 'clifford': 2, 'non-unitary': 2, 'non-clifford': 1})}


### 量子回路の生成

量子計算の性能評価とか量子回路最適化の研究等でランダムな量子回路を作り
たくなることがあります。そんなときはget_random_gatesメソッド
(classmethod)が使えます。例えば、以下のようにします。

    >>> qc = QCirc.generate_random_gates(qubit_num=5, gate_num=100, phase=(0.0, 0.25, 0.5), prob={'h':7, 'cx':5, 'rx':3, 'crz':3})

ここで、qubit_numとgate_numは作成したい量子回路の量子ビット数と量子ゲー
ト数を指定します。

probは量子ゲートの出現確率を辞書形式で指定します。
上の例ではhとcxとrxとcrzを7:5:3:3の割合で出現させます。

    prob={'h':0.7, 'cx':0.5, 'rx':0.3, 'crz':0.3}

のように小数で指定しても良いです(足して1.0にしなくても内部で適当に処
理してくれます)。対応しているゲートは、
x,z,h,s,s_dg,t,t_dg,rx,rz,cx,cz,ch,crzの13種類です。
非ユニタリゲート(measure, reset)は指定できません。

phaseは回転系のゲートがある場合に有効になります(回転系がない場合、指定は無視されます)。
rxとかcrzなどの位相をどのようにバラけさせたいかをタプルで指定します(何個指定しても良いです)。

    phase=(0.0, 0.25, 0.5)

とすると、回転系のゲートが出現した場合、0.0*piか0.25*piか0.5*piかが均
等確率で設定されます。

以上、print(qc)すると、

    h 3
    h 4
    rx(0.25) 3
    h 2
    cx 2 4
    h 2
    h 2
    crz(0.0) 0 1
    cx 3 4
    h 4
    ...


のような回路が作成されていることが確認できます。


### 量子回路の保存と読み込み

作成した量子回路をファイルに書き出したり、書き出されたファイルを読み込むことができます。

まず、書き出す場合はsaveメソッドを使って、

    >>> qc_A = QCirc().h(0).cx(1,0).measure(qid=[0,1], cid=[0,1])
	>>> qc_A.save("hoge.qc")
	
のようにします。これでhoge.qcというファイルにqcの内容が書き出されます(内部でpickle使ってます)。

読み込む場合は、loadメソッド(classmethod)を使って、

    >>> qc_B = QCirc.load("hoge.qc")

のようにします。

### OpenQASMのエクスポートとインポート

qlazyで作成した量子回路をOpenQASM形式の文字列やファイルにエクスポート
したり、それらをインポートすることができます。

to_qasmメソッドを使って、以下のようにQpenQASM形式の文字列を出力するこ
とができます。

    >>> qc = QCirc().h(0).cx(0,1)
	>>> qasm = qc.to_qasm()
	>>> print(qasm)
    OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    h q[0];
    cx q[0],q[1];

to_qasm_fileメソッドを使って、以下のようにOpenQASM形式のファイルを出力
することができます。

	>>> qc.to_qasm_file("foo.qasm")

また、from_qasmメソッドおよびfrom_qasm_fileメソッド(staticmethod)を使って、
以下のようにOpenQASM(バージョン2.0)の文字列およびファイルからqlazyの量子回路を
作成することができます。

    >>> qc = QCirc.from_qasm(qasm)  # qasm: OpenQASM string
    >>> qc = QCirc.from_qasm_file("foo.qasm")  # foo.qasm: OpenQASM file

ただし、非ユニタリゲート(measure,reset)やユーザーがカスタマイズしたゲー
トには対応していません。対応しているゲートは、
x,y,z,h,s,sdg,t,tdg,cx,cz,ch,rx,rz,crzの14種類です。

### 量子回路の等価性(pyzx利用)

2つの量子回路が見た目は違っていても同じ効果を及ぼすユニタリゲートを表
している場合があります。ここでは、前述の「同等性」に対して「等価性」と呼ぶことにします。
qlazyでは、equivalentメソッドを使って等価であるかどうかを判断することができます
(ただし非ユニタリゲートは非対応)。
内部ではZX-calculusの計算ができるPythonモジュールである
[pyzx](https://github.com/Quantomatic/pyzx)を使っていますので、
この機能を使う場合、pyzxがインストールされていなければなりません。

というわけで、簡単な例ですが、

    --H--*--H--
         |
    --H--X--H--

と

    ---X---
       |
    ---*---

が等価であるということを確認してみます（知っておくと便利な公式です）。

    >>> qc_A = QCirc().h(0).h(1).cx(0,1).h(0).h(1)
    >>> qc_B = QCirc().cx(1,0)
    >>> print(qc_A == qc_B)
    False
    >>> print(qc_A.equivalent(qc_B))
    True

となり、確かに見た目が違うので同等ではないですが、
その意味するところは同じということで等価であることが確認できました。


### 量子回路の最適化

non-cliffordゲートであるTゲートはあらゆる量子アルゴリズムで活躍する重
要なゲートなのですが、ハードウェア的には難しいゲートなので、量子回路か
らなるべく追放したいのですが、単に追放しても意味のない回路になるだけなので、
等価性を保ったままTゲート数を削減できれば良いです。
このような意味での量子回路最適化はこれまでいろいろ研究がなされていて、
pyzxでもZX-calculusを使った手法が実装されています。
qlazyではこの機能(full_optimize)を使って最適化を実行することができます
(ただし非ユニタリゲートは非対応)。
以下のようにoptimizeメソッドを使います。

    >>> qc_opt = qc_ori.optimize()

試しに、h,cx,tを含んだ回路をランダムに発生させて、
optimeizeの効果をget_statsで見てみます。

    >>> qc = QCirc.generate_random_gates(qubit_num=10, gate_num=100, prob={'h':5, 'cx':5, 't':3})
    >>> qc_opt = qc.optimize()
	>>> print("== before ==")
    >>> print(qc.get_stats())
	>>> print("== after ==")
    >>> print(qc_opt.get_stats())

とすると、

    == before ==
    {'qubit_num': 10, 'cmem_num': 0, 'gate_num': 100, 'gate_freq': Counter({'cx': 45, 'h': 29, 't': 26}), 'gatetype_freq': Counter({'unitary': 100, 'clifford': 74, 'non-clifford': 26})}
    == after ==
    {'qubit_num': 10, 'cmem_num': 0, 'gate_num': 107, 'gate_freq': Counter({'cx': 55, 'h': 15, 'cz': 14, 'rz': 7, 's_dg': 5, 's': 4, 't': 3, 'z': 2, 'x': 2}), 'gatetype_freq': Counter({'unitary': 107, 'clifford': 97, 'non-clifford': 10})}

となりました。non-cliffordゲートは26個から10個に減りました(t:3個,rz:7個)。
その分、別のcliffordゲートが加わりますが、
non-cliffordゲートが減ったことの方がうれしいのです(と思います)。

### pyzxとのインターフェース

pyzxにはいろんな機能があって最適化に限ってみてもいろんな最適化ができるようになっています。
また、ZX-calculusのグラフを表示したり編集したりする機能もあったりします。諸々遊びたい人のために、
pyzxのCircuitを入出力する機能も用意しました。

    >>> zxqc = qc.to_pyzx()
	
でpyzxのCircuitインスタンスを吐き出すことができます。また、

    >>> qc = QCirc.from_pyzx(zxqc)
	
でCircuitインスタンスをqlazyのQCircインスタンスに変換できます。


### カスタムゲートの追加

QCircクラスを継承することで、自分専用の量子ゲートを簡単に作成・追加す
ることができます。ベル状態を作成する回路をbellメソッドとして、QCircを
継承したMyQCircクラスに追加する例を示します。

    >>> class MyQCirc(QCirc):
    >>>     def bell(self, q0, q1):
    >>>         self.h(q0).cx(q0,q1)
    >>>         return self
	>>> 
    >>> bk = Backend()
    >>> qc = MyQCirc().bell(0,1).measure(qid=[0,1], cid=[0,1])
    >>> result = bk.run(qcirc=qc, shots=10)
    >>> ...

これは非常に簡単な例なのであまりご利益を感じないかもしれませんが、大き
な量子回路を繰り返し使いたい場合など、便利に使える場面は多いと思います。


## 対応しているバックエンド

現在のバージョンで対応しているバックエンドは[qulacs](https://github.com/qulacs/qulacs)と
[IBM Quantum](https://quantum-computing.ibm.com/)と
[Amazon Braket](https://aws.amazon.com/braket/?nc1=h_ls)です。
各々の使い方について、以下で説明します。

### qulacs

[qulacs](https://github.com/qulacs/qulacs)は、[株式会社
QunaSys](https://qunasys.com/)が提供しているオープンソースの量子回路シ
ミュレータで、GPUを利用して高速計算が実行できるという特徴があります。

[qlazy](https://quantum-computing.ibm.com/)の簡単なインターフェースで
GPUを利用した高速計算を実行したい場合、このバックエンドがおすすめです。

#### 準備

まず、[Installation - Qulacs ドキュメント](http://docs.qulacs.org/ja/latest/intro/1_install.html)
あたりを参照しながらインストールしてください（v0.3.0で動作確認しています）。

### 使用法

GPUを利用しないシミュレータで計算させたい場合、

    >>> bk = Backend(product='qulacs', device='cpu_simulator')

GPUを利用したシミュレータで計算させたい場合、

    >>> bk = Backend(product='qulacs', device='gpu_simulator')

のように指定します(deviceを省略した場合のデフォルト値は'cpu_simulator'です)。

あとは上述したように、

	>>> qc = QCirc().h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])
	>>> result = bk.run(qcirc=qc, shots=100)

のようにすれば、qulacsを使った計算ができます。

### IBM Quantum

[IBM Quantum(IBMQ)](https://quantum-computing.ibm.com/)は、
[IBM](https://www.ibm.com/jp-ja)が開発した量子コンピュータ（およびシミュ
レータ）を利用するためのクラウドサービスです。

#### 準備

IBMQやローカルシミュレータをPythonから利用するためのライブラリである
[qiskit](https://qiskit.org/)をインストールして、量子計算を実行できる
環境を整えてください（v0.34.2で動作確認しています）。例えば、[Quantum Native
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

    >>> bk = Backend(product='ibmq', device='aer_simulator')

のように指定します。本物の量子コンピュータを利用したい場合は、例えば、

    >>> bk = Backend(product='ibmq', device='least_busy')

のように指定します。'least_busy'というのは、自分のアカウントで利用可能
な量子コンピュータシステムの中で、現在最も空いているシステムを自動選択
して実行するためのものです。実行するシステムを明示的に指定することもで
きます。例えば、'ibmq_athens'で実行したい場合、

    >>> bk = Backend(product='ibmq', device='ibmq_athens')
	
のように指定します(deviceを省略した場合のデフォルト値は'aer_simulator'です)。

あとは上述したように、

    >>> qc = QCirc().h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])
	>>> result = bk.run(qcic=qc, shots=100)

のようにすれば、IBMQを使った計算ができます。


### Amazon Braket

[Amazon Braket](https://aws.amazon.com/braket/?nc1=h_ls)は、
[IonQ](https://ionq.com/)、[Rigetti](https://www.rigetti.com/)、
[Oxford Quantum Circuits](https://oxfordquantumcircuits.com/)
などの量子コンピュータ（およびシミュレータ）を利用するためのクラウドサービスです。

#### 準備

[AWS](https://aws.amazon.com/jp/console/)のアカウントがまず必要です。
その上で、

- [amazon-braket-sdk-python](https://github.com/aws/amazon-braket-sdk-python)

などを参考にしながら、[Amazon Braket](https://aws.amazon.com/braket/?nc1=h_ls)
が利用できるようにします。以下の日本語の記事も参考になります。

- [Amazon Braketで量子コンピュータをはじめよう！](https://qiita.com/snuffkin/items/29bc6ee24bc2bff55df3)
- [Amazon Braket を利用して手軽に量子コンピュータを動かす](https://note.com/navitime_tech/n/n497cebbeccf3)

以下のようなコードが問題なく動くようになったら[Amazon Braket](https://aws.amazon.com/braket/?nc1=h_ls)
の利用環境が整ったと思って良いです（多分）。

    >>> import boto3
    >>> from braket.aws import AwsDevice
    >>> from braket.circuits import Circuit
    >>> 
    >>> device = AwsDevice("arn:aws:braket:::device/quantum-simulator/amazon/sv1")
    >>> s3_folder = ("amazon-braket-xxxx", "sv1") # Use the S3 bucket you created during onboarding
    >>> 
    >>> bell = Circuit().h(0).cnot(0, 1)
    >>> task = device.run(bell, s3_folder, shots=100)
    >>> result = task.result()
    >>> print(result.measurement_counts)

さらに、qlazyから[Amazon Braket](https://aws.amazon.com/braket/?nc1=h_ls)を利用できるようにするため、
ホームディレクトリに"~/.qlazy/"というディレクトリを作成して、その配下にconfig.iniというファイルを作り、
以下のように記述しておきます。'amazon-braket-xxxx'の部分はamazon braketを利用するために作成した
S3のbacket nameを書いておきます。

    $ cat ~/.qlazy/config.ini
    [backend_braket]
    backet_name = amazon-braket-xxxx

また、poll_timeout_secondsをデフォルト値(5日)から変えたい場合、
例えば1日にしたい場合、

    [backend_braket]
    backet_name = amazon-braket-xxxx
	poll_timeout_seconds = 86400

のように指定します。

ちなみに動作確認している[amazon-braket-sdk-python](https://github.com/aws/amazon-braket-sdk-python)
のバージョンはv1.18.0です。


#### 使用法

Backendのインスタンスを生成する際にproductとdeviceを指定します。
braket関連のproductは、braket_local(ローカルシミュレータ)、
braket_aws(AWS上で動作するシミュレータ)、braket_ionq(IonQの量子コンピュータ)、
braket_rigetti(Rigettiの量子コンピュータ)、
braket_oqc(Oxford Quantum Circuits)の5種類です。
各々で利用できるdeviceは以下の通りです。

- braket_local
    - braket_sv (状態ベクトルシミュレータ)
- braket_aws
    - sv1 (状態ベクトルシミュレータ)
    - tn1 (テンソルネットワークシミュレータ)
    - dm1 (密度行列シミュレータ)
- braket_ionq
    - ionq (IonQ)
- braket_rigetti
    - aspen_11 (Aspen-11)
    - aspen_m_1 (Aspen-M-1)
- braket_oqc
    - lucy (Lucy)

例えば、ローカルな状態ベクトルシミュレータを使う場合、

    >>> bk = Backend(product='braket_local', device='braket_sv')

AWSの状態ベクトルシミュレータを使う場合、

    >>> bk = Backend(product='braket_aws', device='sv1')

IonQの量子コンピュータを使う場合、

    >>> bk = Backend(product='braket_ionq', device='ionq')

RigettiのAspen-M-1を使う場合、

    >>> bk = Backend(product='braket_rigetti', device='aspnen_m_1')

OQCのLucyを使う場合、

    >>> bk = Backend(product='braket_oqc', device='lucy')

のように指定します。あとは、

    >>> qc = QCirc().h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])

のように量子回路を作成して、

    >>> result = bk.run(qcic=qc, shots=100)

のようにすれば、Amazon Braketを使った計算ができます。

#### 注意事項

測定が最後にある量子回路しか受け付けません。
したがって測定値に応じてオンオフするオプション(ctrl)も使えません。

また、braket_local以外のproductは有料になります。
以下のページに料金表がありますので参考にしてください。

[Amazon Braket Pricing](https://aws.amazon.com/jp/braket/pricing/)


## GPU版の利用

GPUを利用した高速な量子回路実行が可能です(v0.3.0より)。ただし、以下の
ようにGPU対応版をインストールする必要があります。

    $ git clone https://github.com/samn33/qlazy.git
    $ cd qlazy
    $ python setup_gpu.py install --user

インストールにあたりNVIDIA CUDA11の環境が整っていることが前提です。GPU
版がインストールされたかどうかは、

    $ qlazy -v

を実行して、

    * Version: 0.3.0-cuda

と表示されたら、とりあえずインストールされたのだと思って良いです。もし、

    * Version: 0.3.0

と表示されたとすると、あなたがお持ちのqlazyはCPU版です。

さて、無事GPU版がインストールされたとして、どうやって使うかを説明します。
CPU版の場合は、例えば、

    >>> from qlazy import QCirc, Backend
    >>> bk = Backend(product='qlazy', device='qstate_simulator')
    >>> qc = QCirc().h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])
	>>> result = bk.run(qcic=qc, shots=100)

でした。GPU版を使う場合は、Backendのインスタンス生成の時に、
deviceを'qstate_gpu_simulator'にするだけです。

    >>> from qlazy import QCirc, Backend
    >>> bk = Backend(product='qlazy', device='qstate_gpu_simulator')
    >>> qc = QCirc().h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])
	>>> result = bk.run(qcic=qc, shots=100)

これでOKです。GPU対応のモジュールをimportするようなことは必要ありません。

いまのところGPU対応版で計算できるのは、状態ベクトルシミュレータを利用
した量子回路計算だけです。QStateやDensOpやStabilizerクラスのGPU版はあ
りません（そのうち作るかどうかは未定です）。


以上
