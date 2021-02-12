import copy
import networkx as nx

from qlazypy import QComp, Backend
from qlazypy.tools.Register import CreateRegister, InitRegister

class QComp_SurfaceCode(QComp):

    def __init__(self, qubit_num=0, qid=None, backend=None):

        cmem_num = qubit_num
        super().__init__(qubit_num=qubit_num, cmem_num=cmem_num, backend=backend)
        self.qid = qid
        self.cid = copy.deepcopy(qid)
        self.lattice = self.__make_lattice(qid)
        xstab_id, zstab_id = self.__make_stab_id(qid)
        self.xstab_id = xstab_id
        self.zstab_id = zstab_id
        self.Lx_chain = []
        self.Lz_chain = []
        self.Lx_ancilla = 0
        self.Lz_ancilla = 0

    def run(self, reset_qubits=False, reset_cmem=False, reset_qcirc=True, shots=1):
        """ 量子回路を実行
            (default: 実行後、量子回路はリセットするが、量子状態と古典メモリはリセットしない) 
        """
        return super().run(reset_qubits=reset_qubits, reset_cmem=reset_cmem,
                           reset_qcirc=reset_qcirc, shots=shots)

    def initialize(self):
        """ 符号空間を初期化(真空状態を作成) """

        for i in range(len(self.xstab_id)):
            for j in range(len(self.xstab_id[0])):
                self.__xstab_meas(i, j)

    def set_logical_plus(self):
        """ 論理|+>状態を準備 """

        rows = [6, 5, 4, 3, 2]
        cols = [4, 4, 4, 4, 4]
        self.__move_defect_p(rows, cols)

        for i, (row, col) in enumerate(zip(rows, cols)):
            if i > 0:
                q = self.__get_common(self.zstab_id[row_pre][col_pre], self.zstab_id[row][col])
                self.Lx_chain.append(q)
            row_pre, col_pre = row, col
            
        self.Lz_chain = list(nx.neighbors(self.lattice, self.zstab_id[6][4]))
        self.Lz_ancilla = self.zstab_id[6][4]
        self.Lx_ancilla = self.xstab_id[0][0]

    def operate_Lx(self):
        """ 論理パウリX演算 """
        [self.x(n) for n in self.Lx_chain]
        self.run()

    def measure_Lx(self, shots=1):
        """ 論理パウリX演算子の測定 """

        ancilla = self.Lx_ancilla
        self.h(ancilla)
        [self.cx(ancilla, n) for n in self.Lx_chain]
        self.h(ancilla).measure(qid=[ancilla], cid=[ancilla])
        result = self.run(shots=shots)
        if self.cmem[ancilla] == 1: self.x(ancilla).run()
        return result

    def measure_Lz(self, shots=1):
        """ 論理パウリZ演算子の測定 """

        ancilla = self.Lz_ancilla
        [self.cx(n, ancilla) for n in self.Lz_chain]
        self.measure(qid=[ancilla], cid=[ancilla])
        result = self.run(shots=shots)
        if self.cmem[ancilla] == 1: self.x(ancilla).run()
        return result

    def operate_Lh(self):
        """ 論理アダマール演算 """

        # 周りにお掘りをつくって欠陥対を孤立させる
        rows = [1,1,1,1,1,1,1, 1,2,3,4,5,6,7, 8,8,8,8,8,8,8, 8,7,6,5,4,3,2, 1]
        cols = [1,2,3,4,5,6,7, 8,8,8,8,8,8,8, 8,7,6,5,4,3,2, 1,1,1,1,1,1,1, 1]
        chain = self.__get_chain(rows, cols, stab_kind='X')
        [self.__z_meas(q) for q in chain]
        
        # お掘りの中(下半分)のqubitのZ測定値が1となる数をカウント
        meas_one_count = 0
        rows = [5,6,7,8, 8,8,8,8,8,8,8, 7,6,5]
        cols = [1,1,1,1, 2,3,4,5,6,7,8, 8,8,8]
        chain = self.__get_chain(rows, cols, stab_kind='X')
        meas_one_count = sum([self.cmem[q] for q in chain])
        
        # 島の下半分のZスタビライザの測定値が1となる数をカウント(ただし、欠陥部分(面座標(6,4)は除く)
        for i in [5,6,7]:
            for j in [1,2,3,4,5,6,7]:
                if i != 6 or j != 4:
                    q = self.zstab_id[i][j]
                    if self.cmem[q] == 1: meas_one_count += 1
        if meas_one_count % 2 == 1: self.operate_Lx()

        # 欠陥を含まない小さい島を作るため、残したい島以外の量子ビットをZ測定する
        # ただし、上下の辺はX boundaryにするためX測定する

        # 外側の周(Z測定)
        rows = [1,1,1,1,1,1, 1,2,3,4,5,6, 7,7,7,7,7,7, 7,6,5,4,3,2, 1]
        cols = [1,2,3,4,5,6, 7,7,7,7,7,7, 7,6,5,4,3,2, 1,1,1,1,1,1, 1]
        chain = self.__get_chain(rows, cols, stab_kind='Z')
        [self.__z_meas(q) for q in chain]

        # 内側の周(Z測定)
        rows = [2,2,2,2,2, 2,3,4,5,6, 7,7,7,7,7, 7,6,5,4,3, 2]
        cols = [2,3,4,5,6, 7,7,7,7,7, 7,6,5,4,3, 2,2,2,2,2, 2]
        chain = self.__get_chain(rows, cols, stab_kind='Z')
        [self.__z_meas(q) for q in chain]
        
        # もうひとつ内側の縦ライン(Z測定)
        rows = [2,3,4,5,6]
        cols = [2,2,2,2,2]
        chain = self.__get_chain(rows, cols, stab_kind='Z')
        [self.__z_meas(q) for q in chain]
        
        # さらにもうひとつ内側の縦ライン(Z測定)
        rows = [2,3,4,5,6,7]
        cols = [3,3,3,3,3,3]
        chain = self.__get_chain(rows, cols, stab_kind='X')
        [self.__z_meas(q) for q in chain]
        
        # 上辺(X測定)
        rows = [2,2,2,2]
        cols = [3,4,5,6]
        chain = self.__get_chain(rows, cols, stab_kind='Z')
        [self.__x_meas(q) for q in chain]

        # 下辺(X測定)
        rows = [6,6,6,6]
        cols = [3,4,5,6]
        chain = self.__get_chain(rows, cols, stab_kind='Z')
        [self.__x_meas(q) for q in chain]

        # 島を構成するすべての量子ビットにアダマール演算
        # - 量子ビット座標(6,5)~(12,13)の中に含まれるデータ量子ビット座標リストを取得しながらアダマール演算
        d_positions = []  # data qubits
        q_positions = []  # all qubits
        for i in [5,6,7,8,9,10,11,12,13]:
            for j in [7,8,9,10,11,12,13]:
                q_positions.append((i, j))
                if (i%2 == 0 and j%2 == 1) or (i%2 == 1 and j%2 == 0):
                    d_positions.append((i,j))
                    self.h(self.qid[i][j]).run()

        # スワップ
        # - データ量子ビットとその上の測定量子ビットをスワップ
        for (i, j) in d_positions:
            if (i <= 5 or i >= 13) or (j <= 6 or j >= 14): continue
            d_0, d_1 = self.qid[i][j], self.qid[i-1][j]
            self.cx(d_0, d_1).cx(d_1, d_0).cx(d_0, d_1).run()

        # - 測定量子ビットとその左の測定量子ビットをスワップ
        for (i, j) in d_positions:
            if (i <= 5 or i >= 13) or (j <= 6 or j >= 14): continue
            d_0, d_1 = self.qid[i-1][j], self.qid[i-1][j-1]
            self.cx(d_0, d_1).cx(d_1, d_0).cx(d_0, d_1).run()

        # - 補助量子ビットに対応した古典レジスタを左斜め上に移動
        for (i, j) in q_positions:
            if (i <= 5 or i >= 13) or (j <= 6 or j >= 14): continue
            a_0, a_1 = self.cid[i][j], self.cid[i-1][j-1]
            self.cmem[a_1] = self.cmem[a_0]
    
        # 島を拡張
        [self.__xstab_meas(2, j) for j in [2,3,4,5,6,7]]
        [self.__xstab_meas(3, j) for j in [2,3,4,5,6,7]]
        [self.__xstab_meas(4, j) for j in [2,3,4,5,6,7]]
        [self.__xstab_meas(5, j) for j in [2,3,4,5,6,7]]
        [self.__xstab_meas(6, j) for j in [2,3,4,5,6,7]]
        [self.__xstab_meas(7, j) for j in [2,3,4,5,6,7]]
        [self.__zstab_meas(1, j) for j in [1,2,3,4,5,6,7]]
        [self.__zstab_meas(2, j) for j in [1,2,3,4,5,6,7]]
        [self.__zstab_meas(3, j) for j in [1,2,3,4,5,6,7]]
        [self.__zstab_meas(4, j) for j in [1,3,4,5,7]]      # 座標(4,2),(4,6)は欠陥
        [self.__zstab_meas(5, j) for j in [1,2,3,4,5,6,7]]
        [self.__zstab_meas(6, j) for j in [1,2,3,4,5,6,7]]
        [self.__zstab_meas(7, j) for j in [1,2,3,4,5,6,7]]

        # 論理Z演算子を上下方向に拡張
        self.Lx_chain = [177, 179, 181, 183]
        col = 4
        for i, row in enumerate([1,2,3,4,5,6,7,8]):
            if i == 1 or i == 6 or i == 7:
                q = self.__get_common(self.xstab_id[row_pre][col], self.xstab_id[row][col])
                if self.cmem[q] == 1: self.operate_Lx()
            row_pre = row
        
        # お掘りの中のqubitのZ測定しながら測定値が1となる数をカウント
        rows = [1,1,1,1, 1,2,3,4,5,6,7, 8,8,8,8,8]
        cols = [4,5,6,7, 8,8,8,8,8,8,8, 8,7,6,5,4]
        chain = self.__get_chain(rows, cols, stab_kind='X')
        [self.__z_meas(q) for q in chain]
        meas_one_count = sum([self.cmem[q] for q in chain])
        
        # 島の右半分のZスタビライザを測定しながら測定値が1となる数をカウント
        # (ただし、欠陥を作りたい部分(面座標(4,6)は除く)
        for i in [1,2,3,4,5,6,7]:
            for j in [4,5,6,7]:
                if i != 4 or j != 6:
                    self.__zstab_meas(i,j)
                    q = self.zstab_id[i][j]
                    if self.cmem[q] == 1: meas_one_count += 1
        if meas_one_count % 2 == 1: self.operate_Lx()
        
        # 周りのお掘りを埋め戻す
        rows = [1,1,1,1,1,1,1, 1,2,3,4,5,6,7, 8,8,8,8,8,8,8, 8,7,6,5,4,3,2]
        cols = [1,2,3,4,5,6,7, 8,8,8,8,8,8,8, 8,7,6,5,4,3,2, 1,1,1,1,1,1,1]
        for i, (row, col) in enumerate(zip(rows, cols)): self.__zstab_meas(row, col)

        self.Lz_chain = list(nx.neighbors(self.lattice, self.zstab_id[4][6]))
        self.Lz_ancilla = self.zstab_id[4][6]
    
    def __get_common(self, q0, q1):
        """ q0の隣接量子ビットとq1の隣接量子ビットに共通している一つの量子ビット番号を取得 """

        list_0 = list(nx.neighbors(self.lattice, q0))
        list_1 = list(nx.neighbors(self.lattice, q1))
        common = list(set(list_0) & set(list_1))
        if len(common) == 0: return None
        return common[0]
        
    def __get_chain(self, rows, cols, stab_kind):
        """ スタビライザー座標のリストからデータ量子ビット番号のチェーンを取得 
            (スタビライザー座標のリストは順に隣接している必要があります)

        """
        chain = []
        for i, (row, col) in enumerate(zip(rows, cols)):
            if i > 0:
                if stab_kind == 'X':
                    q = self.__get_common(self.xstab_id[row_pre][col_pre], self.xstab_id[row][col])
                elif stab_kind == 'Z':
                    q = self.__get_common(self.zstab_id[row_pre][col_pre], self.zstab_id[row][col])
                chain.append(q)
            row_pre, col_pre = row, col
        return chain

    def __make_lattice(self, qid):
        """ 格子をnetworkxのグラフとして作成(nodeは量子ビット番号) """

        row_length = len(qid)
        col_length = len(qid[0])
        lattice = nx.Graph()
        pos = {}
        for i in range(row_length):
            for j in range(col_length):
                lattice.add_node(qid[i][j])
                if i+1 < row_length: lattice.add_edge(qid[i][j], qid[i+1][j])
                if j+1 < col_length: lattice.add_edge(qid[i][j], qid[i][j+1])
        return lattice

    def __make_stab_id(self, qid):
        """ XスタビライザとZスタビライザの位置座標と対応した補助量子ビット番号を結びつける
            - Xスタビライザの位置座標 = 頂点の位置を表す２次元座標
            - Zスタビライザの位置座標 = 面の位置を表す２次元座標
        """

        xid_row_length = (len(qid) + 1) // 2
        xid_col_length = (len(qid[0]) + 1) // 2
        xid = [[0]*xid_col_length for _ in range(xid_row_length)]

        zid_row_length = (len(qid) - 1) // 2
        zid_col_length = (len(qid[0]) - 1) // 2
        zid = [[0]*zid_col_length for _ in range(zid_row_length)]

        for i in range(len(qid)):
            for j in range(len(qid[0])):
                if i%2 == 1 and j%2 == 1: zid[i//2][j//2] = qid[i][j]
                elif i%2 == 0 and j%2 == 0: xid[i//2][j//2] = qid[i][j]
        return xid, zid

    def __xstab_meas(self, i, j, shots=1):
        """ 頂点(i,j)に対応したXスタビライザを測定 """

        ancilla = self.xstab_id[i][j]
        neighbors = list(nx.neighbors(self.lattice, ancilla))
        self.h(ancilla)
        [self.cx(ancilla, n) for n in neighbors]
        self.h(ancilla)
        self.measure(qid=[ancilla], cid=[ancilla])
        result = self.run()
        if self.cmem[ancilla] == 1: self.x(ancilla).run()
        return result

    def __zstab_meas(self, i, j, shots=1):
        """ 面(i,j)に対応したZスタビライザを測定 """

        ancilla = self.zstab_id[i][j]
        neighbors = list(nx.neighbors(self.lattice, ancilla))
        [self.cx(n, ancilla) for n in neighbors]
        self.measure(qid=[ancilla], cid=[ancilla])
        result = self.run(shots=shots)
        if self.cmem[ancilla] == 1: self.x(ancilla).run()
        return result

    def __x_meas(self, q):
        """ q番目の量子ビットをX基底で測定 """

        self.h(q).measure(qid=[q], cid=[q])
        result = self.run()
        self.h(q).run()
        return result

    def __z_meas(self, q):
        """ q番目の量子ビットをZ基底で測定 """

        self.measure(qid=[q], cid=[q])
        result = self.run()
        return result

    def __move_defect_p(self, rows, cols):
        """ p型欠陥を移動
            - 座標(rows[0],cols[0])と座標(rows[1],cols[1])の位置にある欠陥対A,Bのうち、
            - Bを座標(rows[2],cols[2])->(rows[2],cols[2])->...->(rows[N-1],cols[N-1])に移動

        """
        chain = []
        for i, (row, col) in enumerate(zip(rows, cols)):
            if i > 0:
                q = self.__get_common(self.zstab_id[row_pre][col_pre], self.zstab_id[row][col])
                self.__x_meas(q)
                if self.cmem[q] == 1:
                    [self.z(n) for n in list(nx.neighbors(self.lattice, self.zstab_id[rows[0]][cols[0]]))]
                    self.run()
                if i > 1:
                    self.__zstab_meas(row_pre, col_pre)
                    if self.cmem[self.zstab_id[row_pre][col_pre]] == 1:
                        [self.x(n) for n in chain]
                        self.run()
                chain.append(q)
            row_pre, col_pre = row, col

def main():

    row_length = 19
    col_length = 19
    qid = CreateRegister(row_length, col_length)  # 量子ビットは2次元配列(格子)に置く
    qubit_num = InitRegister(qid)
    
    bk = Backend(name='qlazy_stabilizer_simulator')
    qc = QComp_SurfaceCode(qubit_num=qubit_num, qid=qid, backend=bk)

    qc.initialize()        # 真空状態を作成
    qc.set_logical_plus()  # 論理|+>状態を準備
    qc.operate_Lh()        # 論理アダマール演算
    # qc.operate_Lx()        # 論理パウリX演算

    result = qc.measure_Lz(shots=100)  # 論理パウリZ演算子を測定
    # result = qc.measure_Lx(shots=100)  # 論理パウリX演算子を測定
    print("frequency =", result['frequency'])

    qc.free()

if __name__ == '__main__':
    main()
