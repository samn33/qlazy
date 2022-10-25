オブザーバブル(Obserbableクラス)
================================

量子力学においては、ハミルトニアンをはじめとする観測可能な物理量のこと
を「オブザーバブル(observable)」と言います。古典力学と違い、それらオブ
ザーバブルは複素ベクトルから複素ベクトルにマッピングする演算子（or 複
素行列）として表現されます。実際の測定器で測定される値は、そのオペレー
タの固有値とみなされます。固有値は実数値なので（測定値が複素数なんてお
かしいですよね..）、オブザーバブルはエルミート演算子でなければなりませ
ん。このあたりの詳細については適当な量子力学の教科書を参照してください。


量子力学や量子情報理論でよくお目にかかるオブザーバブルはパウリ演算子
X,Y,Zの積和で表現されたものです。スピンの集まりや量子ビットの集まりの
ような２準位の量子多体系で何らかの物理量をエルミート演算子として表そう
とすると、こういう表現が自然に出てくる場合が多いのだと思います。

qlazyでは、このようなパウリ演算子の積和で表現された
オブザーバブルにまつわるいくつかの計算を実行することができます。具体的
には、QStateクラスの量子状態に対して、

- オブザーバブルの期待値
- 量子状態の時間発展(オブザーバブルをハミルトニアンとする量子系の時間発展)

MPStateクラスの行列積状態に対して、

- オブザーバブルの期待値

を計算できます。その使い方についてはQStateクラスおよびMPStateクラスの
ドキュメントを参照いただくとして、ここではオブザーバブルを記述する
Observableクラスを使って、どのようにオブザーバブルを作成するかを説明し
ます。また、作成したオブザーバブルに対して実行できる演算がいくつかある
ので、それについても説明します。


## オブザーバブルの作成

まず、

    >>> from qlazy import Observable
    >>> from qlazy.Observable import X,Y,Z

のようにObservableクラスおよび関連した関数X,Y,Zをimportします。オブザー
バブルの作成には以下３通りのやり方があります。

- 文字列指定による方法
- 重み付きパウリ積を順次追加する方法
- X,Y,Zの加減乗除で指定する方法

以下の節で順に説明します。

### 文字列指定による方法

例えば、3.0 Z(0) Z(1) + 4.0 X(2) X(3) - 2.0というオブザーバブルは、以
下のようにして作成できます。

    >>> ob = Observable("3.0*Z_0*Z_1+4.0*X_2*X_3+5*Y_4-2.0")

'+','-'や'*'の前後にスペースがあっても良いですし、X,Y,Zは小文字でも良いです。

    >>> ob = Observable("3.0 * z_0 * z_1 + 4.0 * x_2 * x_3 + 5 * y_4 - 2.0")

print文を使って指定したオブザーバブルを確認することができます。

    >>> print(ob)
	3.0 Z(0) Z(1) + 4.0 X(2) X(3) + 5.0 Y(4) - 2.0

ここで、１点注意事項があります。上の例の最後の項は-2.0になっていますが、
これは恒等演算子Iに-2.0がかかったものと考えてください。qlazyでは恒等演
算子を明示的に記載せずにオブザーバブルを指定する仕様としています。もち
ろん、内部的には恒等演算子が存在するものとして各種処理がなされます。

### 重み付きパウリ積を順次追加する方法

前節と同じオブザーバブルは、以下のようにして作成することも可能です。
まず、空のオブザーバブルを作成します。

    >>> ob = Observable()

そして、作成したインスタンスに対してadd_wppメソッド(add weighted pauli
product method)を適用することで、パウリ積とそれに対する係数（重み）を
追加していきます。

    >>> ob.add_wpp(weight=3.0, pp=PauliProduct('ZZ', [0,1]))
    >>> ob.add_wpp(weight=4.0, pp=PauliProduct('XX', [2,3]))
    >>> ob.add_wpp(weight=5.0, pp=PauliProduct('Y', [4]))
    >>> ob.add_wpp(weight=-2.0)
    >>> print(ob)
	3.0 Z(0) Z(1) + 4.0 X(2) X(3) + 5.0 Y(4) - 2.0

### X,Y,Zの加減乗除で指定する方法

この方法で作成する場合、X,Y,Z関数がimportされている必要があります。

    >>> from qlazy.Qbservable import X, Y, Z

その上で、前節までのオブザーバブルは、以下のように作成することができます。

    >>> ob = 3.0 * Z(0) * Z(1) + 4.0 * X(2) * X(3) + 5.0 * Y(4) - 2.0
    >>> print(ob)
    3.0 Z(0) Z(1) + 4.0 X(2) X(3) + 5.0 Y(4) - 2.0


## オブザーバブルに関する演算

上記のように作成された複数のオブザーバブルのインスタンスに対して、加減
乗除やべき乗および比較演算を実行することができます。

### 加算

'+'演算子を使って、２つのオブザーバブルの加算を実行することができます。

    >>> ob_1 = 3.0 * Z(0) * Z(1) + 4.0 * X(2) * X(3) + 5.0 * Y(4) - 2.0
    >>> ob_2 = -3.0 * Z(0) * Z(1) - 2.0 * X(2) * X(3) + X(1) * X(2) + 2.0
    >>> ob_3 = ob_1 + ob_2
    >>> print(ob_3)
    2.0 X(2) X(3) + 5.0 Y(4) + X(1) X(2)

また、'+='演算子を使って、インクリメンタルな加算も実行できます。

    >>> ob_1 = -2.0 + 3.0 * Z(0) * Z(1) + 4.0 * X(2) * X(3) + 5.0 * Y(4)
    >>> ob_2 = 2.0 - 3.0 * Z(0) * Z(1) - 2.0 * X(2) * X(3) + X(1) * X(2)
    >>> ob_1 += ob_2
    >>> print(ob_1)
    2.0 X(2) X(3) + 5.0 Y(4) + X(1) X(2)

### 減算

'-'演算子を使って、２つのオブザーバブルの減算を実行することができます。

    >>> ob_1 = 3.0 * Z(0) * Z(1) + 4.0 * X(2) * X(3) + 5.0 * Y(4) - 2.0
    >>> ob_2 = -3.0 * Z(0) * Z(1) - 2.0 * X(2) * X(3) + X(1) * X(2) + 2.0
    >>> ob_3 = ob_1 - ob_2
    >>> print(ob_3)
    6.0 Z(0) Z(1) + 6.0 X(2) X(3) + 5.0 Y(4) - 4.0 - X(1) X(2)

また、'-='演算子を使って、インクリメンタルな減算も実行できます。

    ob_1 = 3.0 * Z(0) * Z(1) + 4.0 * X(2) * X(3) + 5.0 * Y(4) - 2.0
    ob_2 = -3.0 * Z(0) * Z(1) - 2.0 * X(2) * X(3) + X(1) * X(2) + 2.0
    ob_1 -= ob_2
    print(ob_1)
    6.0 Z(0) Z(1) + 6.0 X(2) X(3) + 5.0 Y(4) - 4.0 - X(1) X(2)

### 乗算

'*'演算子を使って、オブザーバブルの実数倍を得ることができます。

    >>> ob_1 = Z(0) + 2.0 * Z(1)
    >>> ob_2 = ob_1 * 3.0
    >>> print(ob_2)
    3.0 Z(0) + 6.0 Z(1)

２つのオブザーバブルの乗算も実行できます。

    >>> ob_1 = Z(0) + 2.0 * Z(1)
    >>> ob_2 = 3.0 * Z(0) + 4.0 * Z(1)
    >>> ob_3 = ob_1 * ob_2
    >>> print(ob_3)
    11.0 + 10.0 Z(0) Z(1)

'*='演算子を使って、それらをインクリメンタルに実行することもできます。

    >>> ob_1 = Z(0) + 2.0 * Z(1)
    >>> ob_1 *= 3.0
    >>> print(ob_1)
    3.0 Z(0) + 6.0 Z(1)

    >>> ob_1 = Z(0) + 2.0 * Z(1)
    >>> ob_2 = 3.0 * Z(0) + 4.0 * Z(1)
    >>> ob_1 *= ob_2
    >>> print(ob_1)
    11.0 + 10.0 Z(0) Z(1)

### 除算

'/'演算子を使って、オブザーバブルを実数値で割る除算を実行すること
ができます。

    >>> ob_1 = Z(0) + 2.0 * Z(1)
    >>> ob_2 = ob_1 / 2.0
    >>> print(ob_2)
    0.5 Z(0) + Z(1)

また、'/='演算子を使って、インクリメンタルな除算も実行できます。

    >>> ob_1 = Z(0) + 2.0 * Z(1)
    >>> ob_1 /= 2.0
    >>> print(ob_1)
    0.5 Z(0) + Z(1)

オブザーバブルをオブザーバブルで割る除算はサポートされていません。

### べき乗

'**'演算子を使って、オブザーバブルのべき乗を実行することができます。

    >>> ob_1 = Z(0) + 2.0 * Z(1)
    >>> ob_2 = ob_1 ** 2
    >>> print(ob_2)
    5.0 + 4.0 Z(0) Z(1)
    >>> ob_3 = ob_1 ** 3
    >>> print(ob_3)
    13.0 Z(0) + 14.0 Z(1)

### 比較

２つのオブザーバブルが等しいかどうかを"==","!="演算子で確認することができます。

    >>> ob_1 = Z(0) + 2.0 * Z(1)
    >>> ob_2 = 2.0 * Z(1) + Z(0)
    >>> print(ob_1 == ob_2)
	True
    >>> print(ob_1 != ob_2)
	False

### 非エルミートなオブザーバブルに関する注意事項

上記の演算を行うと結果としてエルミートでないオブザーバブルが出来上がる
ことがあります。例えば、

    >>> ob_1 = Z(0) * X(0)

とすると、ZX = iYなのでob_1はエルミートではなくなります。本来エルミー
トでなければならないオブザーバブルなのですがqlazyの仕様ではこれは許さ
れます。しかし、このオブザーバブルをprint文で表示したり、何らかの量子
状態のもとでこの期待値を計算しようとすると「エルミートではない」という
意味のエラーが出ます。

    >>> print(ob_1)  # --> error
	>>> expect_value = qs.expect(observable=ob_1)  # --> error

これは許されません。が、上のob_1に対して何らかの演算をすることはできます。
例えば、

    >>> ob_2 = ob_1 * X(0)

という演算は問題なく実行できます。結果、ZXX = Zなのでこれはエルミートです。
なので、print文で、

    >>> print(ob_2)
	Z(0)

と問題なく表示できますし、

    >>> qs.expect(observable=ob_2)
	
も問題なく計算できます。

オブザーバブルがエルミートかどうかはis_hermitianメソッドで取得できます。

    >>> ob_1 = Z(0) X(0)
	>>> print(ob_1.is_hermitian())
	False
    >>> ob_2 = ob_1 * X(0)
	>>> print(ob_2.is_hermitian())
	True


以上