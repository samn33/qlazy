スタビライザー(Stabilizerクラス)
================================

## スタビライザーの操作

パウリ群の部分群S=<g_1,g_2,..,g_n>の要素g_iを作用させてもある状態が不
変になるとき、Sをスタビライザー群と言い、不変になる状態をスタビライザー
状態と言います。通常、状態の変化はヒルベルト空間上のベクトルに施される
ユニタリ変換'U |psi>'として表されますが、スタビライザーg_iに対するユニ
タリ変換'U g_i U+'で表すこともできます。Gottesmann-Knillの定理によると、
Uをクリフォード演算(X,Y,Z,H,S,S+,CX,CY,CZ)に限定すれば、スタビライザー
による表現方法(スタビライザー形式)によって、量子状態の変化は古典計算機
で効率良くシミュレーションできます。

qlazyには、スタビライザーを作成してクリフォード演算による状態変化や測
定をシミュレートする機能があります。

### 生成・初期化　

Stabilizerクラスがスタビライザーを表します。使用例を以下に示します。

    from qlazy import Stabilizer
    sb = Stabilizer(qubit_num=3)

これで量子ビット数3の状態を特定するためのスタビライザーsbを生成します。
show()メソッドでスタビライザーを確認することができます。

    sb.show()
    >>> g[0]:  III
    >>> g[1]:  III
    >>> g[3]:  III

3量子ビットの状態をユニークに決めるためにはスタビライザー演算子は量子
ビットと同じ数3つ必要になりますので、g[0],g[1],g[2]という3つの演算子
(生成元と呼ばれています)を用意しています。最初はすべてがI(恒等演算子)
に設定されていますので、これでは状態はユニークに決まりません。そのため、
まず初期生成元の設定が必要です。例えば、すべての量子ビットを|0>に初期
化するためには、生成元は各々、

    >>> g[0]:  ZII
    >>> g[1]:  IZI
    >>> g[2]:  IIZ

になっている必要があります。set_allメソッドを呼び出すことで、この状態
にすることができます。以下のようにします。

    sb.set_all('Z')
	sb.show()
    >>> g[0]:  ZII
    >>> g[1]:  IZI
    >>> g[2]:  IIZ

また、すべての量子ビットを|+>に初期化したい場合には、

    sb.set_all('X')
	sb.show()
    >>> g[0]:  XII
    >>> g[1]:  IXI
    >>> g[2]:  IIX

とします。初期演算子を任意に設定することもできます。set_pauli_opメソッ
ドを使います。例えば、

    sb.set_pauli_op(0, 0, 'X')
    sb.set_pauli_op(0, 1, 'X')
    sb.set_pauli_op(1, 1, 'Z')
    sb.set_pauli_op(1, 2, 'Z')
    sb.set_pauli_op(2, 0, 'X')
	sb.show()
    >>> g[0]:  XXI
    >>> g[1]:  IZZ
    >>> g[2]:  XII

とします。set_pauli_opの第1引数は生成元番号を表し、第2引数は量子ビット
番号を表し、第3引数は設定するパウリ演算子('X','Y','Z','I')を指定します。
また、各生成元に4つの符号(+1,-1,+i,-i)をつけることもできます。
set_pauli_facメソッドを使います。例えば、

    sb.set_pauli_fac(1, '-i')
	sb.show()
    >>> g[0]:  XXI
    >>> g[1]:-iIZZ
    >>> g[2]:  XII

とします。set_pauli_facの第1引数は生成元の番具で、第2引数は指定したい
符号(4つのうちのどれか)を文字列で指定します。

パウリ積のリストをStabilizerの引数に与えてインスタンスを生成することも
できます。

    str_list = ["IIIXXXX", "IXXIIXX", "XIXIXIX", "IIIZZZZ", "IZZIIZZ", "ZIZIZIZ"]
    pp_list = [PauliProduct(pauli_str=pp_str) for pp_str in str_list]
    sb = Stabilizer(pp_list=gene_list)
	sb.show()
    >>> g[0]:  IIIXXXX
    >>> g[1]:  IXXIIXX
    >>> g[2]:  XIXIXIX
    >>> g[3]:  IIIZZZZ
    >>> g[4]:  IZZIIZZ
    >>> g[5]:  ZIZIZIZ

### ゲート演算

スタビライザーに対してゲート演算を実行することができます。ただし、クリ
フォード演算に限定されます。つまり、対応しているゲート演算は
X,Y,Z,H,S,S+,CX,CY,CZのみです。Tゲートや回転ゲートは非クリフォード演算
なので実行できません。書式はQStateクラスやDensOpクラスの場合と同様です。

    sb.h(0).cx(0,1)
    ...
	
という具合に実行します。

#### 量子ビット数の制限

制限はありません。メモリが許す限り量子ビット数を設定できます。

#### 量子ビット数と生成元の数が異なる場合

以下のようにスタビライザーを生成してゲート演算を実行することができます。
独立な生成元の個数が量子ビット数と同じであれば測定もできます（状態がユ
ニークに決まるので）。が、そうでない場合測定はできません（エラーを返し
ます）。

    sb = Stabilizer(gene_num=4, qubit_num=3)
    sb.set_all('Z')
    sb.h(0).cx(0,1).cx(0,2)
    ...

#### カスタム・ゲートの追加

Stabilizerクラスを継承することで、自分専用の量子ゲートを簡単に作成・追
加することができます。ベル状態を作成する回路をbellメソッドとして、
Stabilizerを継承したMyStabilizerクラスに追加する例を示します。

    class MyStabilizer(Stabilizer):

        def bell(self, q0, q1):
            self.h(q0).cx(q0,q1)
            return self

    sb = MyStabilizer(qubit_num=2).set_all('Z')
	sb.bell(0,1)
    ...

これは非常に簡単な例なのであまりご利益を感じないかもしれませんが、大規
模な量子回路を作成したい場合など、便利に使える場面は多いと思います。


### パウリ積の演算

パウリ演算子X,Y,Zのテンソル積を定義してスタビライザー状態に演算することができま
す。パウリ積を扱うために、まず、

    from qlazy import Stabilizer, PauliProduct
	
のようにPauliProductクラスをimportする必要があります。例えば、3量子ビッ
トのスタビライザー状態sbに対して、X2 Y0 Z1というパウリ積を演算したい場合、

	pp = PauliProduct(pauli_str="XYZ", qid=[2,0,1])
	sb.operate(pp=pp)
	
のようにoperateメソッドのppオプションにPauliProductのインスタンスを指
定します。制御化されたパウリ積はoperateメソッドのctrlオプションに制御
量子ビット番号を指定することで実現できます。以下のようにします。

	pp = PauliProduct(pauli_str="XYZ", qid=[2,0,1])
	sb.operate(pp=pp, ctlr=3)

### 測定

QStateクラスと同様にmメソッドで測定データ(MDataStabilizerクラス)を取得
して適当な変数に格納します。頻度や最後の測定結果はfrequencyプロパティ
(pythonのCounter形式)とlastプロパティ(文字列)で取得することができます。

    md = sb.m(qid=[0,1,2], shots=100)
    print(md.frequency)
    print(md.last)
    >>> Counter({'000':58,'111':42})
    >>> 111

### 一回限りの測定（もう一つの方法）

計算基底で単純に１回だけ測定してその測定値を得たい場合、measureメソッ
ドを使うこともできます。

	sb = Stabilizer(qubit=2).set_all('Z').h(0).cx(0,1)
	mval = sb.measure(qid=[0,1])
	print(mval)
	sb.show()

とやればmvalに文字列'00'または'11'が格納されます。スタビライザー状態は測定後の状
態になります（例えば以下のように）。

	>> 11
	>> g[0]: -ZI
	>> g[1]:  ZZ


### メモリ解放

スタビライザーインスタンスのメモリは使用されなくなったら自動的に解放されますが、
明示的に解放したい場合、

    del sb
	
とすれば好きなタイミングで解放することができます。
	
クラス・メソッド'del_all'を使えば複数のスタビライザーのインスタンスを一気に
解放することができます。

    Stabilizer.del_all(sb_0, sb_1, sb_2)

このとき、引数に指定するのはスタビライザーのリストやタプルであっても良
いですし、それらの入れ子でもOKです。例えば、

    sb_A = [sb_1, sb_2]
    Stabilizer.del_all(sb_0, sb_A)

    sb_B = [sb_3, [sb_4, sb_5]]
    Stabilizer.del_all(sb_B)

という指定の仕方でも大丈夫です。

### 複製

スタビライザーを複製することができます。以下のようにcloneメソッドを呼
び出します。

    sb_clone = sb.clone()

### リセット

すでに生成済みのスタビライザーを破棄することなく、再度初期化して使いた
い場合は、reset()メソッドを使います。

    sb.reset()

とすれば、すべての演算子を恒等演算子Iにリセットすることができます。

### スタビライザーの表示

Stabilizerクラスのshowメソッドを使います。使用例を以下に示します。

    sb.show()

例えば、以下のように各生成元に含まれるパウリ演算子が表示されます。

    g[0]:  XXI
    g[1]:-iIZZ
    g[2]:  XII
	
### 要素の取得

get_pauli_opメソッドget_pauli_facメソッドで取得できます。

    sb.show()
    >>> g[0]:  XXI
    >>> g[1]:-iIZZ
    >>> g[2]:  XII

    print(sb.get_pauli_op(1,2))
	>>> Z
    print(sb.get_pauli_fac(1))
	>>> (0-1j)
    

以上
