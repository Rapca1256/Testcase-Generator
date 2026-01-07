import random
import string


class Integers:
    """
    整数列を生成し、書き込む
    """
    def __init__(self, f, N, mini, maxi, duplication=True):
        """
        :param f: 書き込むファイルのパス
        :param N: 生成する整数の個数
        :param mini: 生成される整数の最小値
        :param maxi: 生成される整数の最大値
        :param duplication: 重複して良いか
        """
        self.f = f
        self.N = N
        self.mini = mini
        self.maxi = maxi
        self.duplication = duplication

        if not N > 0 :
            raise ValueError("Nの値は正の整数である必要があります。")
        if not mini <= maxi:
            raise ValueError("要素として使用できる値は最低1つ必要です。")

        self._generate()
    
    def _generate(self):
        sample = list(range(self.mini, self.maxi+1))
        
        if self.duplication:
            print(*random.choices(sample, k=self.N), file=self.f)
            return
        
        if self.N > self.maxi - self.mini + 1:
            raise ValueError("種類数以上の要素数からなる重複しないリストを生成することはできません。")
        
        print(*random.sample(sample, self.N), file=self.f)
        return

class Strings:
    """
    文字列を生成し、書き込む
    """
    def __init__(self, f, N, length, add=[], allow_lower=True, allow_upper=False, duplication=True):
        """
        :param f: 書き込むファイルのパス
        :param N: 生成する整数の個数
        :param length: 生成される文字列の長さ
        :param alphabets: アルファベットを入れるか(記号のみ、一部のアルファベットのみなどの場合はFalse)
        :add: 追加で入れる記号
        :param duplication: 重複して良いか
        """
        self.f = f
        self.N = N
        self.length = length
        self.add = add
        self.duplication = duplication

        if not N > 0 :
            raise ValueError("Nの値を確認してください。")

        self.characters = [] # 使える文字
        if allow_lower:
            self.characters.extend(list(string.ascii_lowercase))
        if allow_upper:
            self.characters.extend(list(string.ascii_uppercase))
        self.characters.extend(add)

        if not self.characters:
            raise ValueError("使用可能な文字は最低一種類以上必要です。")

        self._generate()
    
    def _generate(self):
        if self.duplication:
            s = ''
            for _ in range(self.N):
                for _ in range(self.length):
                    s += random.choice(self.characters)
                s += ' '
            
            print(s[0:-1], file=self.f)
            return
        generated = set([''])

        s = ''
        t = ''
        for _ in range(self.N):
            while t in generated:
                t = ''
                for _ in range(self.length):
                    t += random.choice(self.characters)
            generated.add(t)
            s += t
            s += ' '
            
        print(s[0:-1], file=self.f)

class Case:
    """
    条件に従い、テストケースを一つ作成する
    """
    def __init__(self, f, queries):
        """
        :param queries:
            ケース生成に用いる各種パラメータのリスト。

            ① ケース生成に直接関与しない値
                形式:
                    (min, max, None)
                説明:
                    値の範囲のみを指定し、後続のケース生成には影響しません。

            ② 後続の「整数値」ケース生成に関与する値（type="int"）
                形式:
                    (min, max, "int", data_min, data_max, duplication)
                説明:
                    指定された範囲内の整数値を生成するためのパラメータです。

                各要素の意味:
                    min, max        : この値自体の範囲
                    data_min        : 生成される整数の最小値
                    data_max        : 生成される整数の最大値
                    duplication    : 重複を許可するかどうか（bool）

            ③ 後続の「文字列」ケース生成に関与する値（type="str"）
                形式:
                    (min, max, "str", length_min, length_max,
                    allow_lower, allow_upper, duplication, add)
                説明:
                    指定された条件に基づいて文字列を生成するためのパラメータです。

                各要素の意味:
                    min, max        : この値自体の範囲
                    length_min     : 文字列の最小長
                    length_max     : 文字列の最大長
                    allow_lower    : 小文字を許可するかどうか（bool）
                    allow_upper    : 大文字を許可するかどうか（bool）
                    duplication    : 文字の重複を許可するかどうか（bool）
                    add            : 追加で使用可能な文字集合
        """
        self.queries = queries
        self.f = f

        if not queries:
            raise ValueError("条件値が設定されていません。")
        self._generate()
    
    def _generate(self):
        generated = []
        tasks = []

        for query in self.queries:
            if not query[2]:
                generated.append(random.randint(query[0], query[1]))
                continue

            n = random.randint(query[0], query[1])
            generated.append(n)

            if query[2] == "int":
                tasks.append((Integers, self.f, n, *query[3:]))
                continue

            elif query[2] == "str":
                length = random.randint(query[3], query[4]) # 文字列の長さ
                generated.append(length)
                if len(query) == 8:
                    tasks.append((Strings, self.f, n, length, [], query[5], query[6], query[7]))
                    continue
                tasks.append((Strings, self.f, n, length, query[8:], query[5], query[6], query[7]))
                continue
            else:
                raise ValueError("3つ目の引数'type'が正しく設定されていません。")
        
        print(*generated, file=self.f)
        
        for task in tasks:
            c, args = task[0], task[1:]
            c(*args)

class TestCase:
    def __init__(self, f, T_min, T_max, queries):
        self.f = f
        self.T_min = T_min
        self.T_max = T_max
        self.queries = queries
        self._generate()
    
    def _generate(self):
        T = random.randint(self.T_min, self.T_max)
        print(T, file=self.f)
        for _ in range(T):
            Case(f=self.f, queries=self.queries)


if __name__ == '__main__':
    PATH = r".\Generated\test.txt"
    with open(PATH, "w") as f:
        TestCase(f=f, T_min=3, T_max=5, queries=[(2, 5, "int", 30, 100, True), (2, 4, "str", 3, 5, True, False, True)])