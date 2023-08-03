import os, json

import tkinter as tk
import tkinter.ttk as ttk
import ttkbootstrap as ttkbs


class Enchanting:
    def __init__(self):
        self.data, self.error = self.get_enchant_list()
        self.root = tk.Tk()
        self.root.title("附魔顺序计算器")
        # 禁止改变窗口大小
        self.root.resizable(0, 0)
        # 设置窗口风格
        self.style = ttkbs.Style(theme="minty")
        # 设置全局字体
        self.style.configure("TLabel", font=10)
        # 下拉菜单
        self.cb = ttkbs.Combobox(
            self.root,
            width=20,
            state="readonly",
            justify="center",
            bootstyle=("success"),
        )
        self.cb_list = ()
        for i in self.data:
            self.cb_list += (i,)
        self.cb["values"] = self.cb_list
        self.cb.current(0)
        self.cb.grid(row=0, column=0, padx=10, pady=10)
        self.cb.bind(
            "<<ComboboxSelected>>",
            lambda event: self.update(
                self.root, self.cb, self.get_enchant(self.data, self.cb.get()), self.old_enchant
            ),
        )
        # 显示可用附魔
        self.label = tk.Label(self.root, text="可用附魔：")
        self.label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        # 显示可用附魔按钮
        self.old_enchant = self.get_enchant(self.data, self.cb.get())
        self.update_button(self.root, self.cb, self.old_enchant, [])
        # 显示已选附魔
        self.label2 = tk.Label(self.root, text="已选附魔：")
        self.label2.grid(row=0, column=1, sticky="w")
        # 显示列表
        rowspan = len(self.old_enchant) + 1
        self.listbox = tk.Listbox(self.root, width=20, height=20, justify="center")
        self.listbox.grid(row=1, column=1, rowspan=rowspan, padx=10, pady=0, sticky="W")
        self.listbox.bind("<Double-Button-1>", lambda event: self.delenchant())
        self.chosen_enchant = []
        self.error_enchant = []
        # 显示提示
        self.label3 = tk.Label(self.root, text="双击删除附魔")
        self.label3.grid(row=rowspan + 1, column=1, padx=0, pady=10, sticky="N")

    # 将点击的附魔加入列表
    def addenchant(self, enchant):
        self.is_error(enchant)
        self.update_button_state()
        # 加入列表
        self.chosen_enchant.append(enchant)
        self.listbox.insert("end", enchant[1])

    # 判断是否有冲突
    def is_error(self, enchant):
        for i in self.error:
            if enchant[2][0] in i:
                for j in i:
                    self.error_enchant.append(j)
                self.error_enchant.remove(enchant[2][0])

    # 更新按钮状态
    def update_button_state(self):
        # 解除禁用
        for i in self.old_enchant:
            for j in i:
                exec(f"self.{j[0]}.config(state='normal')")
        # 禁用冲突附魔
        for i in self.old_enchant:
            for j in i:
                if j[2][0] in self.error_enchant:
                    exec(f"self.{j[0]}.config(state='disabled')")
                else:
                    break

    # 更新
    def update(self, gui, cb, enchant_list, old_enchant_list):
        self.chosen_enchant = []
        self.error_enchant = []
        self.listbox.delete(0, "end")
        self.update_button(gui, cb, enchant_list, old_enchant_list)
        self.label3.destroy()

    # 更新按钮
    def update_button(self, gui, cb, enchant_list, old_enchant_list):
        # 清空按钮
        try:
            num = 0
            for i in old_enchant_list:
                num += 1
                exec(f"self.fm{num}.destroy()")
            self.okbutton.destroy()
        except:
            pass
        # 重新创建按钮
        enchant_list = self.get_enchant(self.data, cb.get())
        row = 2
        num = 0
        for i in enchant_list:
            num += 1
            exec(f"self.fm{num} = tk.Frame(self.root)")
            exec(f'self.fm{num}.grid(row=row, column=0, padx=10, pady=0, sticky="w")')
            for j in i:
                exec(f"self.{j[0]}= ttkbs.Button(self.fm{num}, text=j[1])")
                getattr(self, j[0]).pack(side="left", padx=2, pady=2)
                getattr(self, j[0]).config(command=lambda arg=j: self.addenchant(arg))
            row += 1
        self.old_enchant = enchant_list
        # 显示确认按钮
        self.okbutton = ttkbs.Button(self.root, text="开始计算", bootstyle=("outline"))
        self.okbutton.grid(row=row, column=0, padx=10, pady=10)
        self.okbutton.bind("<Button-1>", lambda event: self.ok())

    # 删除附魔
    def delenchant(self):
        try:
            num = self.listbox.curselection()[0]
            self.listbox.delete(num)
            self.chosen_enchant.pop(num)
            self.error_enchant = []
            for i in self.chosen_enchant:
                self.is_error(i)
            self.update_button_state()
        except:
            pass

    # 读取附魔表
    def get_enchant_list(self):
        failname = os.getcwd() + "\\附魔对照表.json"
        with open(failname, "r", encoding="utf-8") as f:
            Enchanting = json.load(f)
        data = {}
        error = []
        for i in Enchanting:
            if i == "冲突附魔":
                error = Enchanting[i]
            else:
                for j in Enchanting[i]["适用装备"]:
                    if j not in data:
                        data[j] = []
                    data[j].append(
                        [Enchanting[i]["魔咒"], Enchanting[i]["最高等级"], Enchanting[i]["权重"]]
                    )
        return data, error

    # 获取可用附魔
    def get_enchant(self, data, equip):
        enchant_list = []
        num = 0
        for enchant in data[equip]:
            num += 1
            if enchant[1] == "1":
                enchant_list.append(
                    [[f"enchant{num}", enchant[0], [enchant[0], 1, int(enchant[2])]]]
                )
            else:
                enchant_lists = []
                for i in range(int(enchant[1])):
                    enchant_lists.append(
                        [
                            f"enchant{num}{i+1}",
                            f"{enchant[0]}{i+1}",
                            [enchant[0], i + 1, int(enchant[2])],
                        ]
                    )
                enchant_list.append(enchant_lists)
        return enchant_list

    # 计算
    def ok(self):
        try:
            self.label3.destroy()
        except:
            pass
        equip = self.cb.get()
        enchant = self.chosen_enchant
        list = []
        for i in range(len(enchant)):
            list.append([enchant[i][2][0], int(enchant[i][2][1]) * int(enchant[i][2][2])])
        list = sorted(list, key=lambda x: x[1], reverse=True)

        data = []
        for i in range(len(list)):
            data.append([str(i) + list[i][0], list[i][1], 0])  # 附魔,等级,次数
        count = 0  # 附魔次数+1
        equip_ = [0, 0]  # 次数,总等级
        step = []
        while data != []:
            if equip_[0] == count:
                txt = f"【{data[0][1]+2**equip_[0]-1+2**data[0][2]-1}级】{equip} + {data[0][0]} = {equip}"
                step.append(txt)
                equip_[1] += data[0][1] + 2 ** equip_[0] - 1 + 2 ** data[0][2] - 1
                equip_[0] += 1
                data.pop(0)
                step.append("-" * 20)
            else:
                data_ = data
                data = []
                while data_ != []:
                    if len(data_) == 1:
                        data.append([f"{data_[0][0]}", data_[0][1], data_[0][2]])
                        data_.pop(0)
                    else:
                        txt = f"【{data_[-1][1]+2**data_[0][2]-1+2**data_[-1][2]-1}级】{data_[0][0]} + {data_[-1][0]} = {data_[0][0]}"
                        step.append(txt)
                        data.append([f"{data_[0][0]}", data_[0][1] + data_[-1][1], 1 + data_[0][2]])
                        equip_[1] += data_[-1][1] + 2 ** data_[0][2] - 1 + 2 ** data_[-1][2] - 1
                        data_.pop(0)
                        data_.pop(-1)
                count += 1
        txt = ""
        for i in step:
            txt += i + "\n"
        txt += f"共计花费{equip_[1]}级经验"
        self.label3 = tk.Label(self.root, text=txt, justify="left")
        self.label3.grid(row=0, column=2, rowspan=20, padx=10, pady=10, sticky="w")

    # 启动
    def run(self):
        self.root.mainloop()


Enchanting().run()
