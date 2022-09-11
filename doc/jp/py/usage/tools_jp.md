便利なツール
============

## レジスタ関連ツール

大規模な量子回路を相手に量子プログラミングしたい場合、レジスタ関連ツー
ルを使うと便利です。

まず、

    >>> from qlazy.tools.Register import CreateRegister,InitRegister

という具合に、CreateRegister関数とInitRegister関数をインポートします。
典型的な使い方は以下の通りです。

    >>> dat = CreateRegister(3)
    >>> anc = CreateRegister(2)
    >>> qubit_num = InitRegister(dat, anc)

これは、3つのデータ量子ビットと2つの補助量子ビットを用意する例です。

    >>> print(dat)
    [0,1,2]
	>>> print(anc)
    [3,4]
    >>> print(qubit_num)
    5

という具合にdatやancに量子ビット番号が順番に重ならないようにリストとし
て設定され、InitRegister関数の結果、合計のビット数がリターンされます。
レジスタを1次元配列としてではなく、多次元配列にして管理したい場合もあ
るかと思います。その場合は、

    >>> qid = CreateRegister(3,3)
	>>> qubit_num = InitRegister(qid)

とすると、3X3の2次元配列として、

    >>> print(qid)
    [[0,1,2],[3,4,5],[6,7,8]]
    >>> print(qubit_num)
    9

のようにレジスタがセットされます。3次元以上の配列も同じように、

    >>> qid = CreateRegister(2,3,4)
    >>> qubit_num = InitRegister(qid)
    >>> print(qid)
    [[[0,1,2,3],[4,5,6,7],[8,9,10,11]],[[12,13,14,15],[16,17,18,19],[20,21,22,23]]]
    >>> print(qubit_num)
    24

とできます。量子レジスタと古典レジスタの両方をセットする場合は、

    >>> # 量子レジスタ
    >>> qid = CreateRegister(2)
    >>> qubit_num = InitRegister(qid)
	>>> 
    >>> # 古典レジスタ
    >>> cid = CreateRegister(2)
    >>> cmem_num = InitRegister(cid)
	>>> 
    >>> # 量子コンピュータ(バックエンド)の用意
    >>> bk = Backend('qlazy_stabilizer_simulator')
	>>> 
    >>> # 量子回路の設定と実行
    >>> qc = QCirc().h(qid[0]).cx(qid[0],qid[1]).measure(qid=qid[0], cid=cid[0])
    >>> ...
    >>> result = bk.run(qcirc=qc, shots=10)
    >>> ...

とします。量子レジスタと古典レジスタの番号は別々に割り振りたいので、各々
でCreateRegisterとInitRegisterを実行しています。

## 確率分布関連ツール

量子回路を実行すると結果は量子状態に対応した頻度分布として得られます。例えば、

    >>> from qlazy import QCirc, Backend
	>>> bk = Backend()
	>>> qc = QCirc().h(0).cx(0, 1).measure(qid=[0, 1], cid=[0, 1])
	>>> result = bk.run(qcirc=qc, shots=100)
	>>> print(result.frequency)
	Counter({'00': 52, '11': 48})

という具合です。いろんな量子計算をするとそれらの結果を比較評価したくなる場合があります。
そんなときお使いいただけるツールとして確率分布関連ツールがあります。
まず、以下のようにツール（関数）をインポートします。

    >>> from qlazy.tools.Probability import freq2prob, entropy, kl_divergence, cross_entropy

頻度分布(freq = Counter({{'00': 52, '11': 48}}))を確率分布に変換する場合、
以下のようにすると、総和が1.0になる確率系列が辞書データとして得られます。

    >>> prob = freq2prob(freq)
	>>> print(prob)
	{'00': 0.52, '11': 0.48}

確率分布に対してエントロピーを知りたい場合は、entropy関数を使います。

    >>> ent = entropy(prob)
	>>> print(ent)
    0.9988455359952018
	
2つの確率分布(prob_0とprob_1)のKLダイバージェンスを知りたい場合は、

	>>> kl_div = kl_divergence(prob_0, prob_1)

とします。クロスエントロピー（交差エントロピー）は、

	>>> c_ent = cross_entropy(prob_0, prob_1)

で求めることができます。


以上
