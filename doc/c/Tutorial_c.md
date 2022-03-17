Command Line Tool
=================

## 量子回路ファイルの実行

まず、簡単な使用例を示します。以下のようなファイル(foo.qc)を用意し、

    init 2
    h 0
    cx 0 1
    m

実行すると、

    $ qlazy -qc foo.qc
    direction of measurement: z-axis
    frq[00] = 49
    frq[11] = 51
    last state => 00

となります。foo.qcで何をやっているかと言うと、

* 1行目:量子ビットを2つ用意
* 2行目:0番目の量子ビットにアダマールゲートを作用
* 3行目:0番目と1番目の量子ビットに制御NOTゲートを作用
* 4行目:全量子ビットを測定

実行結果として表示されるのは、この場合、測定結果です。
はじめの行「direction of measurement: z-axis」は、
Z軸方向の測定をしています、ということ表しています。
デフォルトの測定の方向はZ軸方向です。他の大抵のシミュレータと違い、
qlazyでは任意方向の測定もオプション等で簡単に実行できるので、
区別できるように測定方向を一応表示するようにしています。
frq[xx]は、測定の結果、|xx>だった回数を表しています。測定の回数は、
何も指定しなければ、デフォルトで100回です。上の例では、
|00>だった回数は49回、|11>だった回数は51回だったということを表しています。
内部で乱数を発生させることで確率的な測定をシミュレートしていますので、
実行のたびにこの回数は変わります。last stateは、
最後の測定の結果が何だったかを表しています。上の例では|00>でした。
ということを意味しています。

また、制御NOTゲートの後に、

    show

を挿入すると、この時点の量子状態を以下のように表示することができます。

    c[00] = +0.7071+0.0000*i : 0.5000 |++++++
    c[01] = +0.0000+0.0000*i : 0.0000 |
    c[10] = +0.0000+0.0000*i : 0.0000 |
    c[11] = +0.7071+0.0000*i : 0.5000 |++++++

2量子ビットで実行しているので、量子状態は|00>,|01>,|10>,|11>の重ね合わ
せです。各々に対応した係数（複素数）をc[00],c[01],c[10],c[11]と定義し
ており、それを表示しています。量子ビットオーダーは左から右に向かって0
番目,1番目...と定義しています。複素数の右に表示されている実数値
（0.5000とか0.0000）は各々の絶対値の２乗、すなわちその状態が観測される
確率を表しています。一番右に表示されている「++++++」は、その確率の大き
さを視覚的にわかりやすくするための、棒グラフです。

## 対話モードでの実行（量子電卓）

対話モードで実行することもできます。

    $ qlazy
	
	>> init 2
	>> h 0
	>> cx 0 1
	>> show
    c[00] = +0.7071+0.0000*i : 0.5000 |++++++
    c[01] = +0.0000+0.0000*i : 0.0000 |
    c[10] = +0.0000+0.0000*i : 0.0000 |
    c[11] = +0.7071+0.0000*i : 0.5000 |++++++
	>> m
    direction of measurement: z-axis
    frq[00] = 49
    frq[11] = 51
    last state => 00
	>> quit

対話モード中で、helpすると、

	>> help
    [commands]
    * initialize quantum state: %,init
    * print quantum circuitt:   &,circ                                                       
    * print quantum gates:      !,gates
    * print quantum state:      -,show
    * print bloch angles:       |,bloch
    * echo input string:        @,echo
    * output quantum gates:     >,output
    * quit:                     .,quit
    * help:                     ?,help
    [quantum gates]
    * 1-qubit gates:            x,y,z,xr,xr_dg,h,s,s_dg,t,t_dg,p,rx,ry,rz
    * 2-qubit gates:            cx,cy,cz,cxr,cxr_dg,ch,cs,cs_dg,cp,crx,cry,crz,sw,rxx,ryy,rzz
    * measurement:              m,mx,my,mz,mb
    * reset:                    reset
    [notes]
    * see 'help <item>', for more information

のように、定義されているコマンドや使用可能な量子ゲートのリストを表示できます。
各々の詳細は、helpの後に参照したいコマンドや量子ゲートの記号を入れると表示されます。

    >> help X
    == X gate ==
    [description]
      X gate is 1-qubit gate called 'pauli X gate'.
      - matrix expression:
        | 0 1 |
        | 1 0 |
    [usage]
      >> x <qubit_id>

以上
