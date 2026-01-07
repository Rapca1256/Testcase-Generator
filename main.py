from tkinter import *
from tkinter import ttk, filedialog, messagebox
from in_generate import TestCase, Case
from out_generate import Output
import tempfile
import zipfile
import os

"""
テストケースの情報をtkinterで受け取り、それを用いてテストケースを生成するクラス
"""
class TestCaseGenerator:
    def __init__(self, master):
        def toggle_button():
            if self.include_desc_var.get():
                self.testcase_num_lower_label.grid(row=2, column=0, sticky=W)
                self.testcase_num_lower_entry.grid(row=2, column=1, sticky=(W, E))
                self.testcase_num_upper_label.grid(row=3, column=0, sticky=W)
                self.testcase_num_upper_entry.grid(row=3, column=1, sticky=(W, E))
            else:
                self.testcase_num_lower_label.grid_forget()
                self.testcase_num_lower_entry.grid_forget()
                self.testcase_num_upper_label.grid_forget()
                self.testcase_num_upper_entry.grid_forget()
        self.master = master
        self.master.title("Test Case Generator")
        self.master.resizable(False, False)

        # フレームの作成
        self.frame = ttk.Frame(master, padding="10")
        self.frame.grid(row=0, column=0, sticky=(N, W, E, S))

        # ファイル数
        self.desc_label = ttk.Label(self.frame, text="生成するファイル数:")
        self.desc_label.grid(row=0, column=0, sticky=W)
        self.desc_entry = ttk.Entry(self.frame, width=30)
        self.desc_entry.insert(0, "20")  # デフォルト値
        self.desc_entry.grid(row=0, column=1, sticky=(W, E))

        # 生成ボタン
        self.include_desc_var = BooleanVar(value=False)
        self.include_desc_check = ttk.Checkbutton(self.frame,
                                                   text="一つのファイルにつき複数のテストケースでテスト",
                                                   variable=self.include_desc_var,
                                                   command=toggle_button)
        self.include_desc_check.grid(row=1, column=0, sticky=W)

        # テストケースの個数の上下限
        self.testcase_num_lower_label = ttk.Label(self.frame, text="1ファイル当たりのテストケースの個数の下限:")
        self.testcase_num_lower_entry = ttk.Entry(self.frame, width=30)
        self.testcase_num_lower_entry.insert(0, "1")  # デフォルト値
        
        self.testcase_num_upper_label = ttk.Label(self.frame, text="1ファイル当たりのテストケースの個数の上限:")
        self.testcase_num_upper_entry = ttk.Entry(self.frame, width=30)
        self.testcase_num_upper_entry.insert(0, "10")  # デフォルト値

        # 区切り線
        separator = ttk.Separator(self.frame, orient='horizontal')
        separator.grid(row=4, column=0, columnspan=2, pady=10, sticky=(W, E))

        # 各種パラメータ入力フィールド
        self.num_min_label = ttk.Label(self.frame, text="値の最小値:")
        self.num_min_label.grid(row=5, column=0, sticky=W)
        self.num_min_entry = ttk.Entry(self.frame, width=30)
        self.num_min_entry.insert(0, "1")  # デフォルト値
        self.num_min_entry.grid(row=5, column=1, sticky=(W, E))

        self.num_max_label = ttk.Label(self.frame, text="値の最大値:")
        self.num_max_label.grid(row=6, column=0, sticky=W)
        self.num_max_entry = ttk.Entry(self.frame, width=30)
        self.num_max_entry.insert(0, "100")  # デフォルト値
        self.num_max_entry.grid(row=6, column=1, sticky=(W, E))

        self.data_type_label = ttk.Label(self.frame, text="データタイプ:")
        self.data_type_label.grid(row=7, column=0, sticky=W)
        self.data_type = ttk.Combobox(self.frame, values=["None", "Integer", "String"], state="readonly")
        self.data_type.current(0)
        self.data_type.grid(row=7, column=1, sticky=(W, E))

        # 整数生成時に表示（初期は非表示）
        self.type_label_min = ttk.Label(self.frame, text="")
        self.type_label_max = ttk.Label(self.frame, text="")
        self.data_min_entry = ttk.Entry(self.frame, width=30)
        self.data_min_entry.insert(0, "1")  # デフォルト値
        self.data_max_entry = ttk.Entry(self.frame, width=30)
        self.data_max_entry.insert(0, "100")  # デフォルト値
        self.duplication_var = BooleanVar(value=True)
        self.duplication_check = ttk.Checkbutton(self.frame,
                                                   text="重複を許容する",
                                                   variable=self.duplication_var)
        
        # 文字列生成時に表示（初期は非表示）
        self.length_min_label = ttk.Label(self.frame, text="文字列の最小長:")
        self.length_min_entry = ttk.Entry(self.frame, width=30)
        self.length_min_entry.insert(0, "1")  # デフォルト値
        

        self.length_max_label = ttk.Label(self.frame, text="文字列の最大長:")
        self.length_max_entry = ttk.Entry(self.frame, width=30)
        self.length_max_entry.insert(0, "10")  # デフォルト値

        
        self.lower_var = BooleanVar(value=True)
        self.lower_check = ttk.Checkbutton(self.frame,
                                                   text="小文字を許容する",
                                                   variable=self.lower_var)
        self.upper_var = BooleanVar(value=False)
        self.upper_check = ttk.Checkbutton(self.frame,
                                                   text="大文字を許容する",
                                                   variable=self.upper_var)

        self.add_label = ttk.Label(self.frame, text="追加で使用する記号:")
        self.add_entry = ttk.Entry(self.frame, width=30)
        self.add_entry.insert(0, "")  # デフォルト値

        # 追加ボタン
        self.add_button = ttk.Button(self.frame, text="数値を追加", command=self.add_test_case)
        self.add_button.grid(row=9, column=0, columnspan=2, sticky=(W, E))

        # 区切り線
        separator2 = ttk.Separator(self.frame, orient='horizontal')
        separator2.grid(row=8, column=0, columnspan=2, pady=10, sticky=(W, E))

        self.source_path_label = ttk.Label(
            self.frame,
            text="解答のソースコード: 選択されていません",
            width=80
        )
        self.source_path_label.grid(
            row=10, column=0, columnspan=2,
            sticky="w", padx=5, pady=5
        )

        self.get_source_button = ttk.Button(
            self.frame,
            text="選択",
            command=self.get_source
        )
        self.get_source_button.grid(
            row=10, column=1,
            sticky="e", padx=5, pady=5
        )

        # 区切り線
        separator3 = ttk.Separator(self.frame, orient='horizontal')

        # 結果表示用テキストエリア
        self.result_text = Text(self.frame, height=11, width=50, state="disabled")
        self.result_text.grid(row=12, column=0, columnspan=2)
        # 生成ボタン
        self.generate_button = ttk.Button(self.frame, text="生成", command=self.generate_cases)
        self.generate_button.grid(row=13, column=0, columnspan=2, sticky=(W, E))

        self.queries = []
        
        # Combobox の選択変更時にラベル表示と下のウィジェットをずらす処理
        def on_data_type_change(event=None):
            val = self.data_type.get()
            if val == "Integer":
                # string 用のウィジェットを隠す
                self.length_min_label.grid_forget()
                self.length_min_entry.grid_forget()
                self.length_max_label.grid_forget()
                self.length_max_entry.grid_forget()
                self.lower_check.grid_forget()
                self.upper_check.grid_forget()
                self.add_label.grid_forget()
                self.add_entry.grid_forget()


                separator2.grid(row=8, column=0, columnspan=2, pady=10, sticky=(W, E))
                self.type_label_min.config(text="データの最小値")
                self.type_label_min.grid(row=9, column=0, sticky=W)
                self.data_min_entry.grid(row=9, column=1, sticky=(W, E))

                self.type_label_max.config(text="データの最大値")
                self.type_label_max.grid(row=10, column=0, sticky=W)
                self.data_max_entry.grid(row=10, column=1, sticky=(W, E))

                self.duplication_check.grid(row=11, column=0, sticky=W)

                gen_row = 13
                text_row = 15
            elif val == "String":
                # integer 用のウィジェットを隠す
                self.type_label_min.grid_forget()
                self.type_label_max.grid_forget()
                self.data_min_entry.grid_forget()
                self.data_max_entry.grid_forget()
                self.duplication_check.grid_forget()

                separator2.grid(row=8, column=0, columnspan=2, pady=10, sticky=(W, E))
                
                self.length_min_label.grid(row=9, column=0, sticky=W)
                self.length_min_entry.grid(row=9, column=1, sticky=(W, E))

                self.length_max_label.grid(row=10, column=0, sticky=W)
                self.length_max_entry.grid(row=10, column=1, sticky=(W, E))

                self.add_label.grid(row=11, column=0, sticky=W)
                self.add_entry.grid(row=11, column=1, sticky=(W, E))

                self.lower_check.grid(row=12, column=0, sticky=W)
                self.upper_check.grid(row=13, column=0, sticky=W)   
                self.duplication_check.grid(row=14, column=0, sticky=W)

                gen_row = 16
                text_row = 18
            else:
                # None の場合はラベルを隠し、ウィジェットを上に戻す
                try:
                    self.type_label_min.grid_forget()
                    self.type_label_max.grid_forget()
                    self.data_min_entry.grid_forget()
                    self.data_max_entry.grid_forget()
                    self.duplication_check.grid_forget()
                    self.length_min_label.grid_forget()
                    self.length_min_entry.grid_forget()
                    self.length_max_label.grid_forget()
                    self.length_max_entry.grid_forget()
                    self.lower_check.grid_forget()
                    self.upper_check.grid_forget()
                    self.add_label.grid_forget()
                    self.add_entry.grid_forget()
                    separator3.grid_forget()
                except Exception:
                    pass
                gen_row = 11
                text_row = 12

            # ボタンとテキストエリアを新しい行に再配置
            self.source_path_label.grid_configure(row=gen_row-1, column=0, columnspan=2, sticky="w", padx=5, pady=5)
            self.get_source_button.grid_configure(row=gen_row-1, column=1, sticky="w")
            self.add_button.grid_configure(row=gen_row, column=0, columnspan=2, sticky=(W, E))
            if val != "None":
                separator3.grid(row=text_row-1, column=0, columnspan=2, pady=10, sticky=(W, E))
            self.result_text.grid_configure(row=text_row, column=0, columnspan=2)
            self.generate_button.grid_configure(row=text_row+1, column=0, columnspan=2)

        self.data_type.bind("<<ComboboxSelected>>", on_data_type_change)
    
    def get_source(self):
        file_path = filedialog.askopenfilename(
            title="ファイルを選択してください",
            filetypes=[
                ("Python files", "*.py"),
                ("C++ files", "*.cpp"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.source_path_label.config(text= "解答のソースコード: " + file_path)

    def add_test_case(self):
        # ここで各種パラメータを取得し、テストケースを生成する処理を実装
        if self.data_type.get() == "Integer":
            query = (int(self.num_min_entry.get()), int(self.num_max_entry.get()), "int",
                     int(self.data_min_entry.get()), int(self.data_max_entry.get()),
                     self.duplication_var.get())
        elif self.data_type.get() == "String":
            query = (int(self.num_min_entry.get()), int(self.num_max_entry.get()), "str",
                     int(self.length_min_entry.get()), int(self.length_max_entry.get()),
                     self.lower_var.get(), self.upper_var.get(),
                     self.duplication_var.get(), list(self.add_entry.get()))
        else:

            query = (int(self.num_min_entry.get()), int(self.num_max_entry.get()), None)

        self.queries.append(query)

        test_case = str(query)
        self.result_text.config(state="normal")
        self.result_text.insert(END, test_case + "\n")
        self.result_text.config(state="disabled")
    
    def generate_cases(self):
        if not self.queries:
            return

        with tempfile.TemporaryDirectory() as temp_dir:
            generated_dir = os.path.join(temp_dir, "Generated")
            os.mkdir(generated_dir)

            if self.include_desc_var.get():
                testcase_num_lower = int(self.testcase_num_lower_entry.get())
                testcase_num_upper = int(self.testcase_num_upper_entry.get())

                for i in range(int(self.desc_entry.get())):
                    path = os.path.join(generated_dir, f"{i}.in")
                    with open(path, "w", encoding="utf-8") as f:
                        TestCase(
                            f=f,
                            T_min=testcase_num_lower,
                            T_max=testcase_num_upper,
                            queries=self.queries
                        )
                    
                    Output(
                        source=self.source_path_label.cget("text")[11:],
                        input_filepath=path,
                        output_filepath=os.path.join(generated_dir, f"{i}.out"),
                        timeout=5
                    )
                    
            else:
                for i in range(int(self.desc_entry.get())):
                    path = os.path.join(generated_dir, f"{i}.in")
                    with open(path, "w", encoding="utf-8") as f:
                        Case(f=f, queries=self.queries)
                    
                    Output(
                        source=self.source_path_label.cget("text")[11:],
                        input_filepath=path,
                        output_filepath=os.path.join(generated_dir, f"{i}.out"),
                        timeout=5
                    )

            # zip にまとめる（Generated の中身だけ）
            zip_path = "testcase.zip"   # ← 保存先（temp_dir の外！）
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
                for filename in os.listdir(generated_dir):
                    full_path = os.path.join(generated_dir, filename)
                    z.write(full_path, arcname=filename)

            generated_fill_path = os.path.join(generated_dir, zip_path)
            messagebox.showinfo("完了", f"テストケースの生成が完了しました。\n{generated_fill_path} に保存されました。")
            # ← ここで Generated フォルダは自動削除


if __name__ == '__main__':
    # 起動！
    a = TestCaseGenerator(Tk())
    a.master.mainloop()
