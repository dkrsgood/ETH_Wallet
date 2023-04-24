import datetime
import os
import time
import tkinter as tk
import warnings
from datetime import datetime
from tkinter import messagebox

import mnemonic as m
import qrcode
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Spacer
from reportlab.platypus import SimpleDocTemplate, Table
from web3 import Web3, HTTPProvider
from web3.exceptions import TransactionNotFound

warnings.filterwarnings("default")


class BlockchainWallet:
    """
    钱包主界面
    """

    def __init__(self, master):
        """
        登录以太坊账户界面初始化
        :param master:
        """
        self.web3 = Web3(HTTPProvider('https://goerli.infura.io/v3/<your API key>'))  # 输入自己的APIkey,可以自己选择连接到主网或者测试网
        self.master = master
        self.master.title("以太坊钱包")
        image = Image.open("Wallet1.PNG")
        photo = ImageTk.PhotoImage(image)
        window_width = 1250
        window_height = 900
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x_pos = int((screen_width - window_width) / 2)
        y_pos = int((screen_height - window_height) / 2)
        self.master.geometry("{}x{}+{}+{}".format(window_width, window_height, x_pos, y_pos))
        self.master.minsize(window_width, window_height)
        self.master.maxsize(window_width, window_height)
        self.outputimage = tk.Label(self.master)
        self.outputimage.place(x=0, y=0)
        self.outputimage.configure(image=photo)
        self.outputimage.image = photo
        # 添加控件
        self.label_title = tk.Label(self.master)
        self.label_title.grid(row=0, column=1, columnspan=2, padx=0, pady=0)
        self.label_title.configure(bg="white")
        self.label_address = tk.Label(self.master, text="账户地址：", font=("Arial", 20))
        self.label_address.configure(bg="white")
        self.label_address.grid(row=1, column=0, sticky="e", padx=20, pady=60)
        self.entry_address = tk.Entry(self.master, width=50, font=("Arial", 20), highlightthickness=1,
                                      highlightbackground="black")
        self.entry_address.grid(row=1, column=1, sticky="", padx=20, pady=10)
        self.label_PriKey = tk.Label(self.master, text="私钥：", font=("Arial", 20))
        self.label_PriKey.grid(row=2, column=0, sticky="e", padx=20, pady=20)
        self.label_PriKey.configure(bg="white")
        self.entry_PriKey = tk.Entry(self.master, width=50, show="*", font=("Arial", 20), highlightthickness=1,
                                     highlightbackground="black")
        self.entry_PriKey.grid(row=2, column=1, sticky="", padx=20, pady=20)
        self.button_create = tk.Button(self.master, text="没有账户？创建账户", font=("Arial", 20),
                                       command=self.goto_CreatWallet, bg='#F8EFEF', width=20, height=1)
        self.button_create.grid(row=6, column=1, sticky="", padx=20, pady=20)

        self.button_enter = tk.Button(self.master, text="进入钱包", font=("Arial", 20), command=self.goto_Wallet,
                                      bg='#F8EFEF', width=20, height=1)
        self.button_enter.grid(row=5, column=1, sticky="", padx=20, pady=20)

        self.button_create = tk.Button(self.master, text="退出钱包", font=("Arial", 20),
                                       command=self.exit_app, bg='#F8EFEF', width=20, height=1)
        self.button_create.grid(row=7, column=1, sticky="", padx=20, pady=20)

    def goto_CreatWallet(self):
        """
        进入以太坊账户创建界面
        """
        self.master.withdraw()  # 隐藏主页窗口
        page1 = tk.Toplevel()  # 进入以太坊账户创建界面
        CreateWalletWindow(page1)

    def goto_Wallet(self):
        """
        以太坊账户登录界面
        """
        if not self.web3.is_connected():  # 判断网络是否连接正常
            messagebox.showerror("网络异常", "网络连接异常，请检查网络连接!")
            return None

        try:
            account = self.web3.eth.account.from_key(self.entry_PriKey.get())  # 从用户输入的私钥中获得以太坊账户，包括公钥和账户地址
            """
            判断用户输入的账户地址格式是否正确，以及用户输入的账户地址和私钥是否匹配
            """
            if self.web3.to_checksum_address(account.address) == self.web3.to_checksum_address(
                    self.entry_address.get()):
                # 验证成功，进入账户详细界面
                key = self.entry_PriKey.get()
                addr = self.entry_address.get()
                self.master.withdraw()  # 隐藏主页窗口
                page2 = tk.Toplevel()  # 创建账户详细窗口
                TransactionWindow(page2, addr, key)  # 将用户输入的账户地址和私钥参数传递给账户详细界面

            else:
                # 验证失败，错误提示
                messagebox.showerror("错误", "账户或私钥错误，请重新输入！")
        except:
            messagebox.showerror("错误", "账户或私钥错误，请重新输入！")

    def exit_app(self):
        """
        退出钱包应用界面
        """
        result = messagebox.askyesno("退出", "确定要退出钱包应用吗？")  # 弹窗提示，确认用户是否确定退出钱包应用
        if result:
            self.master.destroy()  # 销毁界面


class CreateWalletWindow:
    """
    以太坊账户创建界面
    """

    def __init__(self, master):
        """
        界面初始化
        :param master:
        """
        self.web3 = Web3(HTTPProvider('https://goerli.infura.io/v3/<your API key>'))
        self.master = master
        self.master.title("以太坊钱包")
        window_width = 1250
        window_height = 900
        image = Image.open("Wallet2.PNG")
        photo = ImageTk.PhotoImage(image)
        self.label = tk.Label(self.master, image=photo)
        self.label.place(x=0, y=0)
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x_pos = int((screen_width - window_width) / 2)
        y_pos = int((screen_height - window_height) / 2)
        self.master.geometry("{}x{}+{}+{}".format(window_width, window_height, x_pos, y_pos))
        self.master.minsize(window_width, window_height)
        self.master.maxsize(window_width, window_height)
        self.label_address = tk.Label(self.master, text="账户地址：", font=("Arial", 20))
        self.label_address.grid(row=1, column=0, sticky="", padx=20, pady=20)
        self.label_address.configure(bg='white')
        self.entry_address = tk.Entry(self.master, width=45, font=("Arial", 20), highlightthickness=1,
                                      highlightbackground="black")
        self.entry_address.grid(row=1, column=1, sticky="", padx=20, pady=20)

        self.button_create = tk.Button(self.master, text="创建账户", font=("Arial", 20), command=self.qr_generate,
                                       bg='#F8EFEF')
        self.button_create.grid(row=2, column=0, sticky="W", padx=20, pady=20)
        self.qr_output = tk.Label(self.master)
        self.qr_output.grid(row=3, column=0, columnspan=2)
        self.qr_output.configure(bg="white")
        self.button_create = tk.Button(self.master, text="返回", font=("Arial", 20), command=self.goto_main,
                                       bg='#F8EFEF')
        self.button_create.place(x=1160, y=825)
        root.mainloop()

    def goto_main(self):
        """
        退出创建以太坊账户界面
        :return:None
        """
        result = messagebox.askyesno("退出", "确定要退出账户创建吗？")  # 确认用户是否退出账户创建
        if result:
            self.master.destroy()  # 销毁账户创建界面
            main_page.master.deiconify()  # 显示主页窗口

    def qr_generate(self):
        """
        生成账户地址私钥和助记词函数，并将私钥和助记词写入到二维码中
        :return:None
        """

        new_account = self.web3.eth.account.create()  # 创建一个以太坊账户，包含公私钥对
        new_address = new_account.address  # 获取账户地址
        new_private_key = new_account._private_key  # 获取私钥
        mnemonic = m.Mnemonic('english', ).to_mnemonic(new_private_key)  # 通过私钥生成助记词
        self.entry_address.insert(0, new_address)

        data = "私钥:" + new_private_key.hex()[2:] + '\n' + "助记词：" + mnemonic  # 编码的信息
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=2)
        qr.add_data(data)  # 将编码的私钥和助记词写入到二维码中
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")  # 生成二维码图片
        tk_image = ImageTk.PhotoImage(img)
        # 在组件中输出二维码图片
        self.qr_output.configure(image=tk_image)
        self.qr_output.image = tk_image
        self.label_title = tk.Label(self.master,
                                    text="账户创建成功!请扫描二维码获取私钥和助记词！",
                                    font=("Arial", 28))
        self.label_title.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=20, pady=20)
        self.label_title.configure(bg="white")
        self.button_create = tk.Button(self.master, text="再次创建账户", font=("Arial", 20), command=self.qr_generate,
                                       bg='#F8EFEF')
        self.button_create.grid(row=2, column=0, sticky="W", padx=20, pady=20)


class TransactionWindow:
    """
    以太坊账户地址详细界面
    """

    def __init__(self, master, addr, key):
        """
        账户界面初始化
        :param master:
        :param addr: 账户地址
        :param key: 私钥
        """

        self.web3 = Web3(HTTPProvider('https://goerli.infura.io/v3/<your API key>'))
        self.master = master
        self.address = addr
        self.priviateKey = key
        self.balance_var = tk.StringVar()
        self.master.title("账户信息")
        window_width = 1250
        window_height = 900
        image = Image.open("Wallet3.PNG")
        photo = ImageTk.PhotoImage(image)
        self.label = tk.Label(self.master, image=photo)
        self.label.place(x=0, y=0)
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x_pos = int((screen_width - window_width) / 2)
        y_pos = int((screen_height - window_height) / 2)
        self.master.geometry("{}x{}+{}+{}".format(window_width, window_height, x_pos, y_pos))
        self.master.minsize(window_width, window_height)
        self.master.maxsize(window_width, window_height)
        self.label_address = tk.Label(self.master, text="地址：" + str(self.address), font=("Arial", 20))
        self.label_address.grid(row=0, column=1, sticky="W", padx=20, pady=20)
        self.label_address.configure(bg='white')
        self.label_balance = tk.Label(self.master, text="余额：" + str(self.get_balance(self.address)) + " ether",
                                      font=("Arial", 20))
        self.label_balance.grid(row=1, column=1, sticky="W", padx=20, pady=20)
        self.label_balance.configure(bg='white')
        self.label_network = tk.Label(self.master, text="网络：Goerli测试网络", font=("Arial", 20))
        self.label_network.grid(row=2, column=1, sticky="W", padx=20, pady=20)
        self.label_network.configure(bg='white')

        self.label_receiveAddr = tk.Label(self.master, text="To", font=("Arial", 18))
        self.label_receiveAddr.grid(row=3, column=1, sticky="W", padx=20, pady=18)
        self.label_receiveAddr.configure(bg='white')
        self.entry_receiveAddr = tk.Entry(self.master, width=30, font=("Arial", 18), highlightthickness=1,
                                          highlightbackground="black")
        self.entry_receiveAddr.grid(row=3, column=1, sticky="", padx=20, pady=18)
        self.label_amount = tk.Label(self.master, text="金额(ETH)", font=("Arial", 18))
        self.label_amount.grid(row=4, column=1, sticky="W", padx=20, pady=18)
        self.label_amount.configure(bg='white')
        self.entry_amount = tk.Entry(self.master, width=30, font=("Arial", 18), highlightthickness=1,
                                     highlightbackground="black")
        self.entry_amount.grid(row=4, column=1, sticky="", padx=20, pady=18)
        self.label_data = tk.Label(self.master, text="Data", font=("Arial", 18))
        self.label_data.grid(row=5, column=1, sticky="W", padx=20, pady=18)
        self.label_data.configure(bg='white')
        self.entry_data = tk.Entry(self.master, width=30, font=("Arial", 18), highlightthickness=1,
                                   highlightbackground="black")
        self.entry_data.grid(row=5, column=1, sticky="", padx=20, pady=18)
        self.button_tranfer = tk.Button(self.master, text="转账", font=("Arial", 20), command=self.send_transaction,
                                        bg='#F8EFEF')
        self.button_tranfer.grid(row=6, column=0, columnspan=2, sticky="", padx=20, pady=20)
        self.transation_text = tk.Text(self.master, font=("Arial", 18), width=100, height=50)
        self.transation_text.grid(row=7, column=0, columnspan=2, sticky="nsew", padx=20, pady=20)

        # 创建垂直滚动条
        self.scrollbar = tk.Scrollbar(self.master, command=self.transation_text.yview)
        self.scrollbar.grid(row=7, column=2, sticky="ns")

        # 将滚动条与文本框关联
        self.transation_text.config(yscrollcommand=self.scrollbar.set)

        # 设置文本框的网格行和列的拉伸权重
        self.master.grid_rowconfigure(7, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # 设置网格行和列的伸缩性
        self.master.rowconfigure(7, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.button_back = tk.Button(self.master, text="退出", font=("Arial", 20), command=self.goto_main, bg='#F8EFEF')
        self.button_back.grid(row=8, column=1, sticky="SE", padx=20, pady=20)
        self.button_export = tk.Button(self.master, text="导出交易", font=("Arial", 20), command=self.export_receipt,
                                       bg='#F8EFEF')
        self.button_export.grid(row=8, column=0, sticky="SW", padx=20, pady=20)
        root.mainloop()

    def goto_main(self):
        """
        返回钱包主界面
        :return:
        """
        result = messagebox.askyesno("退出", "确定要退出您的钱包账户吗？")  # 确认用户是否要退出账户界面，返回钱包主界面
        if result:
            self.master.destroy()  # 销毁账户界面
            main_page.master.deiconify()  # 显示钱包主界面窗口

    def send_transaction(self):
        """
        生成并发送交易
        :return:
        """
        result = messagebox.askyesno("交易确认",
                                     "确定要给 " + self.entry_receiveAddr.get() + " 账户转帐 "
                                     + self.entry_amount.get() + "ether吗?")  # 确认用户是否要发送交易
        if result:
            # 发送交易
            try:
                sender_private_key = bytes.fromhex(self.priviateKey)  # 获取发送方私钥，并将十六进制私钥转换为字节串
                # web3.to_checksum_address()会将输入的地址进行大小写混合，并将其转换为以"0x"开头的42个字符的字符串。
                # 其中包含了大小写的混合以及校验和相关的字符。如果输入的地址不是一个有效的以太坊地址，该函数将会抛出异常。
                sender_address = self.web3.to_checksum_address(self.address)  # 获取发送方账户地址，同时会校验和验证账户地址格式是否正确，
                receiver_address = self.web3.to_checksum_address(self.entry_receiveAddr.get())  # 从用户输入框获得交易接收方地址
                data = self.entry_data.get()  # 从用户输入框获取交易中附加的data数据，默认data字段为空，这里的data仅支持16进制字符
                amount = self.entry_amount.get()  # 从用户输入框获取交易金额，单位为ETH
                nonce = self.web3.eth.get_transaction_count(sender_address)  # 获取当前交易的nonce值
                gas_price = self.web3.eth.gas_price * 1.5  # 获取gas费，这里为了提高交易被打包上链的速度，将gas费提高了50%，可以选择自己合适的gasprice
                # 估计这笔交易所需要的汽油单位个数
                gas = self.web3.eth.estimate_gas({
                    'from': sender_address,
                    'to': receiver_address,
                    'value': self.web3.to_wei(amount, 'ether'),
                    'data': data
                })
                gas *= 1.2  # 为防止汽油单位估计不准确，导致实际交易给的汽油单位不足，交易失败，设置缓冲，将给的汽油单位提高20%
                # 创建一个交易对象，包含交易的所有必要细节，如接收地址、要发送的ETH,gas数量,gas价格，以及要包含在交易中的数据（如果有）
                transaction = {
                    'nonce': nonce,
                    'from': sender_address,
                    'to': receiver_address,
                    'value': self.web3.to_wei(amount, 'ether'),
                    'gas': int(gas),
                    'gasPrice': int(gas_price),
                    'data': data
                }
                # 对这笔交易用交易发送方的私钥签名，得到已签名的交易对象 signed_tx
                signed_tx = self.web3.eth.account.sign_transaction(transaction, sender_private_key)
                timestamp = time.time()
                # 将时间戳格式化为日期和时间字符串，获取发起交易时的时间戳
                submit_transaction_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

                # signed_tx.rawTransaction是获取已签名的交易的二进制编码，
                # send_raw_transaction()代表将已签名的交易广播到区块链网络中

                tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
                # 自定义的交易头信息
                transaction_info = "=====================Initiate transaction time:" + submit_transaction_time + \
                                   "=====================" + '\n'



            except Exception as e:
                # 交易对象创建失败，弹出交易异常提示框
                messagebox.showerror("交易异常", "交易异常，请重新发起交易！" + "异常信息：" + str(e))
                return None
            receipt = self.update_receipt(tx_hash)  # 调用update_receipt函数，不断在区块链网络上查询这笔交易是否已经上链，上链则返回交易收据
            block_number = receipt['blockNumber']  # 获取交易上链后，交易所在的区块高度
            timestamp = self.web3.eth.get_block(block_number)['timestamp']  # 获取交易被打包上链时的时间戳
            gas_used = receipt['gasUsed']  # 获取交易的gas消耗量
            gas_price = self.web3.eth.get_transaction(tx_hash).gasPrice  # 获取这笔交易实际的gas价格
            percentage_used = "{:.2%}".format(gas_used / gas)  # 计算gas消耗百分比
            transaction_fee = gas_used * gas_price  # 交易费=gas消耗量*单位gas价格
            timestamp_common = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')  # 将时间戳从UTC时间转化为本地时间
            # 下面是交易信息汇总
            transaction_info += "Transaction Hash: " + str(
                tx_hash.hex()) + '\n' + "Status: success" + '\n' + "Block number: " \
                                + str(block_number) + '\n' + "Timestamp: " + str(timestamp_common) + '\n' + "From: " + \
                                self.address + '\n' + "To: " + str(self.entry_receiveAddr.get()) + '\n' + "Value: " \
                                + str(self.entry_amount.get()) + '\n' + "Transaction Fee: " + str(
                self.web3.from_wei(transaction_fee, 'ether')) + "ETH" + '\n' + \
                                "Gas Price: " + str(self.web3.from_wei(gas_price, 'gwei')) + "Gwei" + '\n' \
                                + "Gas Limit & Usage by Txn: " + str(int(gas)) + " | " \
                                + str(gas_used) + "(" + str(percentage_used) + ")" + '\n' + "Input Data: " + \
                                str(self.entry_data.get()) + '\n\n'

            self.transation_text.insert(tk.END, transaction_info)

        self.label_balance = tk.Label(self.master, text="余额：" + str(self.get_balance(self.address)) + " ether",
                                      font=("Arial", 20))  # 更新交易成功后账户余额
        self.label_balance.grid(row=1, column=1, sticky="W", padx=20, pady=20)
        self.label_balance.configure(bg='white')

    def get_balance(self, address):
        """
        获取以太坊账户余额
        :param address: 账户地址
        :return:余额
        """
        balance_wei = self.web3.eth.get_balance(address)
        balance = self.web3.from_wei(balance_wei, 'ether')
        return balance

    def export_receipt(self):
        """
        导出交易收据,每次最多能导出4笔交易
        :return:None
        """

        result = messagebox.askyesno("导出交易", "确定要导出您当前的交易记录吗？")
        if result:
            try:
                timestamp = time.time()
                receipt_info = self.transation_text.get("1.0", tk.END)
                file_name = str(datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d-%H-%M-%S")) + "receipt.pdf"
                folder_path = "transaction_history"
                file_path = os.path.join(folder_path, file_name)
                # 确保文件夹路径存在，并具有写入权限
                if not os.path.exists(folder_path):  # 没有这个文件夹则自动创建，用于保存交易历史收据
                    os.makedirs(folder_path)
                receipt_pdf = SimpleDocTemplate(file_path, pagesize=A4, topMargin=20)
                elements = []
                title_style = ParagraphStyle(
                    "Title",
                    fontSize=20,
                    leading=10,
                    alignment=1,  # 居中对齐
                    fontName="Times-Bold",
                )
                title = Paragraph("transaction history", title_style)
                elements.append(title)
                elements.append(Spacer(1, 30))
                elements.append(
                    Table([[receipt_info]], colWidths=receipt_pdf.width, rowHeights=[None]))
                receipt_pdf.build(elements)
            except Exception as e:
                # 导出异常，弹出异常提示框
                messagebox.showerror("失败", "交易导出失败，请重试！" + " 异常信息:" + str(e))
                return None
            messagebox.showinfo("导出成功", "交易导出成功！交易已导入到 " + file_path + " 文件中！")  # 导出成功

    def update_receipt(self, tx_hash, interval=3):
        """
        更新交易收据，直到交易上链为止
        :param tx_hash: 交易哈希
        :param interval: 查询时间间隔，默认为3秒
        :return: 交易收据
        """

        receipt = None

        while receipt is None:
            try:
                receipt = self.web3.eth.get_transaction_receipt(tx_hash)  # 通过交易哈希去区块链网络上查询交易是否上链，如果上链则返回交易收据receipt
                if receipt is not None and receipt['status']:  # receipt不为空且'status'为0表示交易成功上链
                    return receipt  # 返回交易收据
            except TransactionNotFound:

                pass
            time.sleep(interval)


if __name__ == "__main__":
    root = tk.Tk()
    main_page = BlockchainWallet(root)
    root.mainloop()
