import tkinter as tk
from tkinter import messagebox, filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import random, json, os
from PIL import Image, ImageTk

class QuizApp:
    def __init__(self, root, questions):
        self.root = root
        root.title("金工实习刷题 · 卡片版")
        root.geometry("700x500")          # 初始大小
        root.minsize(600, 450)
        root.place_window_center()        # ttkbootstrap 内置居中
        self.style = ttk.Style("superhero")  # 青蓝暗黑主题

        # 数据
        random.shuffle(questions)
        self.questions = questions
        self.idx = 0
        self.score = 0
        self.wrong = []

        # 顶层进度
        self.pb = ttk.Progressbar(root, length=300, mode='determinate', bootstyle=SUCCESS)
        self.pb.pack(pady=8)
        self.update_pb()

        # 卡片区域
        self.card = ttk.Labelframe(root, text="题目", padding=15)
        self.card.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        self.qlabel = ttk.Label(self.card, font=("Microsoft YaHei", 15), wraplength=620, justify=LEFT)
        self.qlabel.pack(anchor=NW)

        self.var = tk.StringVar()
        self.radio_fr = ttk.Frame(self.card)
        self.radio_fr.pack(pady=15)

        # 底部按钮
        btn_fr = ttk.Frame(root)
        btn_fr.pack(pady=10)
        ttk.Button(btn_fr, text="提交", command=self.submit_answer, bootstyle=SUCCESS, width=10).pack(side=LEFT, padx=5)
        ttk.Button(btn_fr, text="交卷", command=self.wrap_up, bootstyle=WARNING, width=10).pack(side=LEFT, padx=5)
        self.score_lbl = ttk.Label(btn_fr, text="得分: 0", font=("", 12))
        self.score_lbl.pack(side=LEFT, padx=20)

        self.build_options()
        self.show()

    # --------------- 内部方法 ---------------
    def update_pb(self):
        self.pb["value"] = (self.idx + 1) / len(self.questions) * 100

    def build_options(self):
        self.radios = []
        for i in range(4):          # 最多 4 选项
            r = ttk.Radiobutton(self.radio_fr, text="", variable=self.var, value=str(i),
                               bootstyle=INFO, width=50)
            r.grid(row=i, sticky=W, pady=4)
            self.radios.append(r)

    def show(self):
        q = self.questions[self.idx]
        self.qlabel["text"] = f"{self.idx + 1}. {q['question']}"
        opts = q["options"]
        for r, opt in zip(self.radios, opts):
            r["text"] = opt
            r.grid()
        for r in self.radios[len(opts):]:
            r.grid_remove()
        self.var.set(-1)

    def submit_answer(self):
        """提交后显示正误，并出现【下一题】按钮"""
        if not self.var.get():
            messagebox.showwarning("提示", "请先选择答案！")
            return

        q = self.questions[self.idx]
        user_ans = self.var.get()          # 字母  A/B/C
        right_ans = q["answer"]            # 字母  A/B/C
        if user_ans == right_ans:
            self.score += 1
            self.animate(True)
        else:
            self.wrong.append(q)
            self.animate(False)

        self.score_label.config(text=f"得分: {self.score}")
        self.submit_button.config(state="disabled")      # 禁用提交
        self.next_button.grid()                          # 显示下一题
        # 显示正确答案
        idx_right = ord(right_ans) - ord("A")
        self.options[idx_right].config(fg=self.success, font=self.font_opt + ("bold",))

    def animate(self, ok: bool):
        bg = "success" if ok else "danger"
        self.style.configure("anim.TLabel", background=self.style.colors.get(bg))
        pop = ttk.Label(self.root, text="✓" if ok else "✗", style="anim.TLabel",
                       font=("", 60, "bold"), anchor=CENTER)
        pop.place(relx=.5, rely=.4, anchor=CENTER)
        pop.after(400, pop.destroy)

    def wrap_up(self):
        t = f"总得分：{self.score}/{len(self.questions)}\n"
        if self.wrong:
            t += f"错题 {len(self.wrong)} 道，是否导出？"
            if messagebox.askyesno("交卷", t):
                self.export_wrong()
        else:
            t += "全部正确，太棒了！"
            messagebox.showinfo("交卷", t)
        self.root.quit()

    def export_wrong(self):
        path = filedialog.asksaveasfilename(defaultextension=".json",
                                          filetypes=[("JSON", "*.json")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.wrong, f, ensure_ascii=False, indent=2)
            os.startfile(os.path.dirname(path))

# ------------------ 主程序 ------------------
if __name__ == "__main__":
    questions = [
    {"question": "12. 在型芯内放置型芯骨的作用是：", "options": ['A. 加强型芯的强度', 'B. 加强型芯的透气性', 'C. 加强型芯的耐火性'], "answer": 'A'},
    {"question": "13. 铸件上的外形尺寸与模型上的对应尺寸相比哪个大？", "options": ['A. 铸件大', 'B. 模型大', 'C. 一样大'], "answer": 'B'},
    {"question": "14. 大批量生产皮带轮毛坯应选用的工艺方法是：", "options": ['A. 焊接', 'B. 铸造', 'C. 热处理'], "answer": 'B'},
    {"question": "15. 刮砂造型适用于哪种场合？", "options": ['A. 单件生产', 'B. 中批生产', 'C. 大批生产'], "answer": 'A'},
    {"question": "16. 大型锻件必须采用自由锻的方式生产。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'A'},
    {"question": "17. 板料拉伸时，拉伸系数越小变形越容易。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "18. 空气锤的公称规格是指其锤杆加锤头的质量而言。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'A'},
    {"question": "19. 过烧的锻件还可通过热处理的方法进行挽救。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "20. 胎模锻是在自由锻的设备上进行的。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'A'},
    {"question": "21. 锻压的金属材料应具备的性能是：", "options": ['A. 硬度高', 'B. 塑性高', 'C. 强度高'], "answer": 'B'},
    {"question": "22. 模锻适合于：", "options": ['A. 大批量生产', 'B. 小批量生产', 'C. 与生产批量无关'], "answer": 'A'},
    {"question": "23. 大批量生产的垫圈最好采用：", "options": ['A. 简单冲模', 'B. 复合冲模', 'C. 连续冲模'], "answer": 'C'},
    {"question": "24. 镦粗时，还料的高径比应小于：", "options": ['A. 2.5', 'B. 4.5', 'C. 5.5'], "answer": 'A'},
    {"question": "25. 轴类零件自由锻的基本工序为：", "options": ['A. 拔长、切肩、拔长', 'B. 镦粗、冲孔、滚圆', 'C. 拔长、镦粗、弯曲'], "answer": 'A'},
    {"question": "26. 设交流电弧焊机的空载电压是多少伏？", "options": ['A. 60~70', 'B. 50~60', 'C. 80~90'], "answer": 'A'},
    {"question": "27. 埋弧自动焊的特点是：", "options": ['A. 适应性好，特别宜焊垂直焊缝', 'B. 焊接质量好，且一次焊透深度较大', 'C. 很适合单件小批量焊各种位置的焊缝'], "answer": 'A'},
    {"question": "28. 用直流反接时，焊条应接什么极？", "options": ['A. 正极', 'B. 负极', 'C. 正负均可'], "answer": 'A'},
    {"question": "29. 焊接电弧的绝对温度可达多少度？", "options": ['A. 6000℃', 'B. 5000℃', 'C. 4000℃'], "answer": 'A'},
    {"question": "30. 用电弧焊焊薄板是宜用何种方法？", "options": ['A. 交流弧焊', 'B. 直流弧焊正接', 'C. 直流弧焊反接'], "answer": 'C'},
    {"question": "31. 气焊炬关闭的顺序：", "options": ['A. 先关氧气后关乙炔', 'B. 先关乙炔后关氧气', 'C. 乙炔与氧气同时关闭'], "answer": 'B'},
    {"question": "32. 焊接结构中，最宜多采用哪种接头形式？", "options": ['A. 对接', 'B. 角接', 'C. 搭接'], "answer": 'A'},
    {"question": "33. 为防爆炸，乙炔发生器应配备什么装置？", "options": ['A. 回火保险器', 'B. 乙炔钢瓶', 'C. 减压器'], "answer": 'A'},
    {"question": "34. 结构钢焊条的选择主要原则是焊缝与母材在下列哪一方面应相等：", "options": ['A. 化学成分', 'B. 强度等级', 'C. 结晶组织'], "answer": 'A'},
    {"question": "35. 酸性焊条用得比较广泛的原因之一是：", "options": ['A. 焊接质量好', 'B. 焊缝抗裂性好', 'C. 焊接工艺性能好'], "answer": 'C'},
    {"question": "36. 碱性焊条常用直流焊机原因是：", "options": ['A. 减少焊件的热变形', 'B. 电弧燃烧稳定', 'C. 减少焊缝的含氢量'], "answer": 'B'},
    {"question": "37. 埋弧自动焊生产效率较高的主要原因是：", "options": ['A. 焊缝表面盖了一层焊剂', 'B. 电弧电压较高', 'C. 可用较大的焊接电流'], "answer": 'C'},
    {"question": "38. 用手工电弧焊焊小于6mm厚的焊件时，焊条直径的选用主要依据是：", "options": ['A. 焊接电流', 'B. 被焊工件的厚度', 'C. 坡口的形式'], "answer": 'B'},
    {"question": "39. 气焊中最常用的氧乙炔焰是：", "options": ['A. 碳化焰', 'B. 中性焰', 'C. 氧化焰'], "answer": 'B'},
    {"question": "40. 焊条药皮的作用是：", "options": ['A. 稳定电弧', 'B. 增加焊接温度', 'C. 增加焊接电流'], "answer": 'A'},
    {"question": "41. 随着碳含量的增加，钢的强度和硬度不断增加。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'A'},
    {"question": "42. T10钢的平均含碳量为0.1%。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "43. 可锻铸铁可以锻造成型的。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "44. 钢材随着冷变形量的增加，强度、硬度会增加，而塑性、韧性降低。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'A'},
    {"question": "45. 调质处理就是淬火加中温回火。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "46. 在车床上钻孔时，工件作旋转运动，钻头作直线进给运动。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'A'},
    {"question": "47. 车削外圆时，车刀的主切削刃与车刀前进方向的夹角称为副偏角。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "48. 刀具前角是前刀面与基面间的夹角，在正交平面上测量。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'A'},
    {"question": "49. 车床上横走刀是指与床身平行的方向走刀。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "50. 碳化硅砂轮可用来刃磨高速钢车刀。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "51. 车床主轴箱用于车削不同种类的螺纹。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "52. 车床的操纵杆可以控制车床主轴正转及反转，但不能控制停车。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "53. 刀具材料在高温下仍保持原有硬度的性能叫高速切削性。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "54. 车外圆时，车刀的主切削刃与车刀前进方向的夹角称为：", "options": ['A. 前角', 'B. 主偏角', 'C. 副偏角'], "answer": 'B'},
    {"question": "55. 车外圆时，切削主运动是指：", "options": ['A. 刀架的横向运动', 'B. 工件的转动', 'C. 刀架的纵向运动'], "answer": 'B'},
    {"question": "56. 车外圆时的切削深度是指：", "options": ['A. 待加工表面与已加工表面的直径差', 'B. 切出的切屑厚度', 'C. 待加工表面与已加工表面的直径差的一半'], "answer": 'C'},
    {"question": "57. 车刀的前刀面与主后刀面的交线称为：", "options": ['A. 副切削刃', 'B. 主切削刃', 'C. 刀尖'], "answer": 'B'},
    {"question": "58. C6140车床能加工的最大工件直径为：", "options": ['A. 20MM', 'B. 40MM', 'C. 400MM'], "answer": 'C'},
    {"question": "59. 250转/分的转速，车削ΦD60mm的外圆和用400转/分的转速车削ΦD30mm的外圆，切削速度高的是：", "options": ['A. 前者', 'B. 后者', 'C. 都不是'], "answer": 'A'},
    {"question": "60. 安装车刀时，刀尖应装得与工件中心：", "options": ['A. 等高', 'B. 比工件中心稍高', 'C. 比工件中心稍低'], "answer": 'A'},
    {"question": "61. 车刀刃倾角是主切削刃与基面间的夹角，在哪内测量？", "options": ['A. 正交平面', 'B. 切削平面', 'C. 基面'], "answer": 'B'},
    {"question": "62. 车削工件时切屑流过的表面为：", "options": ['A. 主后刀面', 'B. 副后刀面', 'C. 前刀面'], "answer": 'C'},
    {"question": "63. 不能戴下列哪些物品开车床？", "options": ['A. 帽', 'B. 手套', 'C. 眼镜'], "answer": 'B'},
    {"question": "64. 卧式铣床的主轴是设置：", "options": ['A. 水平', 'B. 与水平成45°', 'C. 垂直'], "answer": 'A'},
    {"question": "65. 刨床的主运动是：", "options": ['A. 工作台带工件的前后运动', 'B. 滑枕带刀具的左右运动', 'C. 刀架带刨刀的上下运动'], "answer": 'B'},
    {"question": "66. 卧式铣床选用：", "options": ['A. 带孔的铣刀', 'B. 带孔且有键槽的铣刀', 'C. 带直柄的铣刀'], "answer": 'B'},
    {"question": "67. 铣床不能加工：", "options": ['A. 斜面', 'B. 燕尾槽', 'C. 外圆柱面'], "answer": 'C'},
    {"question": "68. 工作表面有硬皮时，应采用：", "options": ['A. 顺铣', 'B. 端铣', 'C. 逆铣'], "answer": 'C'},
    {"question": "69. 顺铣时会引起打刀现象，这是由于什么造成？", "options": ['A. 进给机构的齿轮齿条有间隙', 'B. 进给机机构的蜗杆蜗轮有间隙', 'C. 进给机构的丝杆与螺母有间隙'], "answer": 'C'},
    {"question": "70. 砂轮具有自锐性。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'A'},
    {"question": "71. 下面的哪个不是铣床附件。", "options": ['A. 分度头', 'B. 平口钳', 'C. 跟刀架'], "answer": 'C'},
    {"question": "72. 组成砂轮的三个基本要素是：", "options": ['A. 磨料、粒度、结合剂', 'B. 磨料硬度、形状尺寸、结合剂强度', 'C. 磨料、结合剂、孔隙'], "answer": 'C'},
    {"question": "73. 在铣床上加工30个齿的齿轮，采用分度头直接分度时，手柄应转转。", "options": ['A. 2', 'B. 3', 'C. 4'], "answer": 'B'},
    {"question": "74. 砂轮的硬度是指：", "options": ['A. 砂轮磨料的硬度', 'B. 砂轮磨粒的脱落难易程度', 'C. 使用结合剂的强度'], "answer": 'B'},
    {"question": "75. 这次实习时使用的平面磨床是", "options": ['A. 园台周磨', 'B. 园台端磨', 'C. 矩台周磨'], "answer": 'AC'},
    {"question": "76. 手锯条用什么材料制成？", "options": ['A. 碳素工具钢', 'B. 碳素结构钢', 'C. 高速钢'], "answer": 'A'},
    {"question": "77. 为什么锯齿按波形排列？", "options": ['A. 减少摩擦', 'B. 容易散热', 'C. 加强锯条钢性'], "answer": 'B'},
    {"question": "78. 锯条装得太松会怎样？", "options": ['A. 锯缝会不直', 'B. 锯条易折断', 'C. 锯起来费力'], "answer": 'B'},
    {"question": "79. 锯片安装时应", "options": ['A. 锯齿向前', 'B. 锯齿向后', 'C. 锯齿方向无要求'], "answer": 'A'},
    {"question": "80. 锉齿的粗细怎么划分？", "options": ['A. 按每10mm长的齿数', 'B. 按锉齿的高低', 'C. 按锉齿的宽窄'], "answer": 'A'},
    {"question": "81. 钳工在圆杆上加工出外螺纹，应用哪种工具？", "options": ['A. 板牙', 'B. 丝锥', 'C. 锉刀'], "answer": 'A'},
    {"question": "82. 攻丝前钻孔的直径应", "options": ['A. 等于螺孔的内径尺寸', 'B. 应大于螺孔的内径尺寸', 'C. 应小于螺孔的内径尺寸'], "answer": 'A'},
    {"question": "83. 孔快钻通时应注意什么？", "options": ['A. 保持原来的进给速度不变', 'B. 加快进给速度', 'C. 减慢进给速度'], "answer": 'C'},
    {"question": "84. 检查工件形状和位置误差可使用下列哪些量具？", "options": ['A. 百分尺', 'B. 百分表', 'C. 卡尺'], "answer": 'B'},
    {"question": "85. 工件装配时可用铁捶直接敲击工件表面直到压入。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "1. 铸件整个都在同一砂箱内，好吗？", "options": ['A. 好', 'B. 不好', 'C. 看情况而定'], "answer": 'A'},
    {"question": "2. 下面三种说法，哪种才对？", "options": ['A. 为了保证型砂紧实，应用大力将型砂椿得越紧越好。', 'B. 椿砂要做到砂型各处的紧实程度都一致。', 'C. 椿砂应均匀的按一定的路线进行，注意不要椿撞到木模上。'], "answer": 'C'},
    {"question": "3. 制模型时，在要铸出孔的地方，应加什么？", "options": ['A. 收缩量', 'B. 型芯头', 'C. 加工余量'], "answer": 'B'},
    {"question": "4. 有时型砂中加入少量煤粉，其主要目的是：", "options": ['A. 提高型砂的透气性', 'B. 提高型砂的强度', 'C. 减少粘砂的倾向'], "answer": 'A'},
    {"question": "5. 内浇口最好开设在铸件的重要部位，对吗？", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "6. 铸件的分模面即分型面，对吗？", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "7. 通气孔必须扎到与型腔相通， 对吗？", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "8. 型砂的耐火性不足会产生什么缺陷？", "options": ['A. 气孔', 'B. 粘砂', 'C. 裂纹'], "answer": 'B'},
    {"question": "9. 浇不足缺陷产生的主要原因是：", "options": ['A. 液体金属的收缩量太大', 'B. 型砂的退让性差', 'C. 液体金属的流动性差或液体金属的量不够'], "answer": 'C'},
    {"question": "10. 铸件上的拔模斜度应加在哪些面上为好？", "options": ['A. 各个面上', 'B. 与分型面平行的平面', 'C. 与分型面垂直的平面'], "answer": 'C'},
    {"question": "11. 浇注系统中，冒口的主要作用是：", "options": ['A. 排气', 'B. 挡渣', 'C. 补缩'], "answer": 'C'},
    {"question": "12. 最常用的铸造合金是什么？", "options": ['A. 铸钢', 'B. 灰口铸铁', 'C. 铸造铝合金'], "answer": 'B'},
    {"question": "13. 型芯的主要作用是：", "options": ['A. 增加铸件的强度', 'B. 增加铸件的透气性', 'C. 形成铸件的内腔'], "answer": 'C'},
    {"question": "14. 三箱造型适用于哪种场合？", "options": ['A. 单件生产', 'B. 中批生产', 'C. 大批生产'], "answer": 'A'},
    {"question": "15. 大批量生产小型铝合金喇叭外壳零件，最适合的铸造方法是：", "options": ['A. 砂型铸造', 'B. 熔模铸造', 'C. 压力铸造'], "answer": 'C'},
    {"question": "16. 空气锤的公称规格，是指其最大打击力而言。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "17. 承受动载荷的工件通常需要锻压制坏。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'A'},
    {"question": "18. 模锻适合大批量生产。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'A'},
    {"question": "19. 板料弯曲时，其纤维方向应与弯曲轴线方向平行。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "20. 锻造加热的目的是为了提高锻件的塑性。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'A'},
    {"question": "21. 自由锻适合于：", "options": ['A. 单件、小批生产', 'B. 成批生产', 'C. 大量生产'], "answer": 'A'},
    {"question": "22. 在板料冲孔工序中，废料应是：", "options": ['A. 冲落部分', 'B. 剩余部分', 'C. 不一定'], "answer": 'A'},
    {"question": "23. 锻造时，使坏料的截面积增大，高度减小的工序为：", "options": ['A. 拔长', 'B. 错移', 'C. 镦粗'], "answer": 'C'},
    {"question": "24. 将45钢加热至始锻温度（1150℃），保温时间过长时，会产生的缺陷：", "options": ['A. 过烧', 'B. 过热', 'C. 变形, 裂纹'], "answer": 'B'},
    {"question": "25. 大批量生产的发动机曲轴，应采用的锻造方法是：", "options": ['A. 自由锻', 'B. 模锻', 'C. 胎模锻'], "answer": 'B'},
    {"question": "26. 电阻焊的特点之一是：", "options": ['A. 低电压, 大电流', 'B. 高电压, 大电流', 'C. 高电压, 低电流'], "answer": 'A'},
    {"question": "27. 焊条药皮的作用之一是：", "options": ['A. 向焊缝加有用合金元素', 'B. 增加焊接温度', 'C. 增加焊接电流'], "answer": 'A'},
    {"question": "28. 气割时要求被割金属应具备的性质之一是：", "options": ['A. 金属的燃点应高于其熔点', 'B. 金属的燃点应低于其熔点', 'C. 与金属的燃点无关只与熔点有关'], "answer": 'B'},
    {"question": "29. 埋弧自动焊的主要特点之一是：", "options": ['A. 电弧电压较高', 'B. 焊接工艺性能好', 'C. 一般只适合于平直焊缝的焊接'], "answer": 'C'},
    {"question": "30. 选用酸性焊条的主要原因是：", "options": ['A. 焊缝的抗裂性能好', 'B. 焊接工艺性能好，成本低', 'C. 焊缝塑性高'], "answer": 'B'},
    {"question": "31. 钨极氩弧焊的特点之一是：", "options": ['A. 可使用大电流，焊接生产率高', 'B. 特别适用于高合金钢和有色金属的焊接', 'C. 可适用于各种材料焊接，应用广泛'], "answer": 'B'},
    {"question": "32. 手弧焊时，焊接电流确定的主要依据是：", "options": ['A. 焊丝的直径', 'B. 焊逢的宽度', 'C. 焊接位置'], "answer": 'A'},
    {"question": "33. 焊接电弧的实质是：", "options": ['A. 电流流过两个电极时产生的高温', 'B. 电极间气体电离导电产生的高温', 'C. 药皮溶化燃烧时产生的高温'], "answer": 'B'},
    {"question": "34. 用直流电弧焊正接法施焊时，焊条应接什么极：", "options": ['A. 正极', 'B. 正负极均可', 'C. 负极'], "answer": 'C'},
    {"question": "35. 气焊炬关闭的顺序：", "options": ['A. 先关乙炔，后关氧气', 'B. 先关氧气，后关乙炔', 'C. 乙炔和氧气同时关'], "answer": 'A'},
    {"question": "36. 气焊时，把氧气引出使用时要连接：", "options": ['A. 回火保险器', 'B. 氧气发生器', 'C. 减压器'], "answer": 'C'},
    {"question": "37. 焊接结构中，最宜多用的是哪种接头：", "options": ['A. 角接', 'B. 对接', 'C. 搭接'], "answer": 'B'},
    {"question": "38. 手工电弧焊常用的点火方法是：", "options": ['A. 短路法', 'B. 高压电压法', 'C. 火源点火法'], "answer": 'A'},
    {"question": "39. 用手工电弧焊焊小于6mm厚的焊件时，焊条直径的选用主要依据是：", "options": ['A. 被焊工件的厚度', 'B. 坡口的形式', 'C. 焊接电流'], "answer": 'A'},
    {"question": "40. 最适合于焊接的钢材是：", "options": ['A. 高碳钢', 'B. 低碳钢', 'C. 高合金钢'], "answer": 'B'},
    {"question": "41. 中碳钢的热处理工艺通常采用调质处理获得良好的综合机械性能。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'A'},
    {"question": "42. 退火条件下T12钢的强度和硬度都高于60钢。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "43. T8钢和80钢的含碳量都是0.8%。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'A'},
    {"question": "44. 弹簧钢的最终热处理工艺通常采用淬火加低温回火，获得回火马氏体组织。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "45. 20钢采用正火预先热处理可以提高钢的硬度，提高切削加工性能。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'A'},
    {"question": "46. 计算车外圆的切削速度时，应按照已加工表面的直径数值，而不是按照待加工表面直径的数值进行计算。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "47. 车削外圆时，七也可以通过丝杠传动实现纵向自动走刀。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "48. 车刀上切屑流过的刀面叫后刀面，", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "49. 车螺纹时必须用丝杠带动刀架进给，其目的是为了获得准确的螺距。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'A'},
    {"question": "50. 溜板箱的作用是实现车螺纹和锥度。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "51. 车床变速箱的功用是用来改变进给量的。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "52. 在车床上切断钢件时须加切削液，但切铸铁时一般不加切削液。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'A'},
    {"question": "53. 车削工件时，车刀的运动是辅助运动。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "54. 车削加工时，工件有多种转速，这是因为：", "options": ['A. 电机可变多种转速', 'B. 有变速手柄', 'C. 床头箱内有变速机构'], "answer": 'C'},
    {"question": "55. 可作车刀的材料是：", "options": ['A. 铸铁', 'B. 碳素结构钢', 'C. 高速钢'], "answer": 'C'},
    {"question": "56. 车刀主偏角是主切削刃在基面上的投影与进给方向的夹角，在", "options": ['A. 正交平面', 'B. 基面', 'C. 切削平面'], "answer": 'B'},
    {"question": "57. 切削普通螺纹时，车刀的刀尖角应等于：", "options": ['A. 30°', 'B. 29°', 'C. 60°'], "answer": 'C'},
    {"question": "58. 为了确定和测量车刀的几何角度，需要选取三个辅助平面作为基准，这三个辅助平面是基面、正交平面和：", "options": ['A. 加工平面', 'B. 主剖面', 'C. 切削平面'], "answer": 'C'},
    {"question": "59. 车床上何处用到齿条齿轮机构？", "options": ['A. 进给箱', 'B. 溜板箱', 'C. 主轴箱'], "answer": 'B'},
    {"question": "60. 在车削工件时，常用百分尺测量工件外径，其准确度为：", "options": ['A. 0.1', 'B. 0.01', 'C. 0.001'], "answer": 'B'},
    {"question": "61. 车床通用夹具中，能自动定心的是：", "options": ['A. 四爪卡盘', 'B. 三爪卡盘', 'C. 花盘'], "answer": 'B'},
    {"question": "62. 车端面时车不完整，中心总是留有一小凸台，何故？", "options": ['A. 刀尖低于工件中心', 'B. 刀尖磨钝了', 'C. 刀尖低于车床主轴中心'], "answer": 'A'},
    {"question": "63. 车削钢件时铁屑缠绕挡住了视线，想看清车刀和工件，应该怎么做？", "options": ['A. 停车把切屑除去', 'B. 不停车戴上手套后将铁屑除去', 'C. 不停车用铁钩将铁屑除去'], "answer": 'A'},
    {"question": "64. 适合车床上加工的平面是什么样的平面？", "options": ['A. 回转面', 'B. 轴上和圆盘上的端面', 'C. 一般平面'], "answer": 'B'},
    {"question": "65. 车外圆时的切削深度是指：", "options": ['A. 待加工表面与已加工表面的直径差', 'B. 切出的切屑厚度', 'C. 待加工表面与已加工表面的直径差的一半'], "answer": 'C'},
    {"question": "66. 顺铣时会引起打刀现象，这是出于，造成。", "options": ['A. 进给机构的蜗杆蜗轮有间隙', 'B. 进给机构的齿轮副有间隙', 'C. 进给机构的丝杆螺母有间隙'], "answer": 'C'},
    {"question": "67. 铣床的主运动是：", "options": ['A. 铣刀的旋转运动', 'B. 工作台的左右运动', 'C. 工作台的前后运动'], "answer": 'A'},
    {"question": "68. 下面的不是铣床附件。", "options": ['A. 跟刀架', 'B. 平口钳', 'C. 分度头'], "answer": 'A'},
    {"question": "69. 刨床不能加工：", "options": ['A. 斜面', 'B. 外园柱面', 'C. 燕尾槽'], "answer": 'C'},
    {"question": "70. 工件表面如有硬皮时，应采用：", "options": ['A. 周铣', 'B. 顺铣', 'C. 逆铣'], "answer": 'C'},
    {"question": "71. 在铣床上加工30个齿的齿轮，采用分度头直接分度时，手柄应转", "options": ['A. 1/30', 'B. 1/60', 'C. 1/90', 'D. 1/120'], "answer": 'B'},
    {"question": "72. 牛头刨床刨削时的主运动是：", "options": ['A. 工作台间歇进给', 'B. 工作台上下移动', 'C. 滑枕往复移动'], "answer": 'C'},
    {"question": "73. 砂轮的硬度是指：", "options": ['A. 砂轮磨粒的硬度', 'B. 砂轮磨粒的脱落难易程度', 'C. 使用的结合剂的强度'], "answer": 'B'},
    {"question": "74. 内园磨床的主运动是：", "options": ['A. 工件的旋转运动', 'B. 工件的左右水平运动', 'C. 砂轮的旋转运动'], "answer": 'C'},
    {"question": "75. 组成砂轮的三个基本要素是：", "options": ['A. 磨料、粒度、砂轮硬度', 'B. 磨料、结合剂、孔隙', 'C. 磨料、粒度、结合剂强度'], "answer": 'B'},
    {"question": "76. 锉刀往后返回时应注意什么？", "options": ['A. 提起锤刀', 'B. 和前进时一样均匀加压', 'C. 不紧压工件'], "answer": 'A'},
    {"question": "77. 用手锯锯钢管时应选用哪种锯条？", "options": ['A. 粗齿', 'B. 中齿', 'C. 细齿'], "answer": 'C'},
    {"question": "78. 钳工的划线基准通常与设计基准一致", "options": ['A. 对', 'B. 不对', 'C. 有时对'], "answer": 'A'},
    {"question": "79. 手锯条用什么材料制成？", "options": ['A. 碳素工具钢', 'B. 碳素结构钢', 'C. 高速钢'], "answer": 'A'},
    {"question": "80. 锉齿的粗细怎么划分？", "options": ['A. 按锉齿的高低', 'B. 按每10mm长的齿数', 'C. 按锉齿的宽窄'], "answer": 'B'},
    {"question": "81. 为什么锯齿按波形排列？", "options": ['A. 减少摩擦', 'B. 容易散热', 'C. 加强锯条钢性'], "answer": 'A'},
    {"question": "82. 锯片的安装采用：", "options": ['A. 锯齿向前', 'B. 锯齿向后', 'C. 锯齿方向无要求'], "answer": 'A'},
    {"question": "83. 攻丝前钻孔的直径", "options": ['A. 应等于螺孔的内径尺寸', 'B. 应大于螺孔的内径尺寸', 'C. 应小于螺孔的内径尺寸'], "answer": 'C'},
    {"question": "84. 实习中使用的游标卡尺的测量精度为：", "options": ['A. 0.01mm', 'B. 0.02mm', 'C. 0.1mm'], "answer": 'B'},
    {"question": "85. 轴承如果采用较大的过盈配合，可采用加工后趁热装入。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'A'},
    {"question": "1. 铸件的分模面即分型面，对吗？", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'B'},
    {"question": "2. 铸件上重要加工面在铸型中最好应处于什么样的浇注位置？", "options": ['A. 最上部', 'B. 最上部或侧面', 'C. 侧面或底面'], "answer": 'C'},
    {"question": "3. 为了得到质量好的铸件，浇注温度越高越好，对吗？", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "4. 最常用的铸造合金是什么？", "options": ['A. 铸钢', 'B. 铸铝', 'C. 灰口铸铁'], "answer": 'C'},
    {"question": "5. 适用于整模造型的零件， 其最大截面一般在哪里？", "options": ['A. 端部', 'B. 中部', 'C. 近底部'], "answer": 'A'},
    {"question": "6. 铸型中除了上砂箱、下砂箱和型芯外，还有一个主要部分是什么？", "options": ['A. 通气孔', 'B. 分型面', 'C. 浇注系统'], "answer": 'C'},
    {"question": "7. 型砂的主要成分是什么？", "options": ['A. 砂、粘土、水与附加物', 'B. 砂、成型剂与水'], "answer": 'A'},
    {"question": "8. 型砂的退让性不足会产生什么缺陷？", "options": ['A. 气孔', 'B. 夹砂', 'C. 裂纹'], "answer": 'C'},
    {"question": "9. 生产中，车床床身毛坯的加工方法是：", "options": ['A. 焊接', 'B. 锻造', 'C. 铸造'], "answer": 'C'},
    {"question": "10. 挖砂造型适用于哪种场合？", "options": ['A. 单件生产', 'B. 中批生产', 'C. 大批生产'], "answer": 'A'},
    {"question": "11. 铸件的形状和模型的形状相似，对吗？", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'B'},
    {"question": "12. 桩砂用的平椿，在未用到时，应怎样放置？", "options": ['A. 垂直放', 'B. 横放', 'C. 随便放'], "answer": 'B'},
    {"question": "13. 什么是错箱？", "options": ['A. 砂箱尺寸选错了', 'B. 放错了另一个上箱', 'C. 寿件上、下面部分在分型面处错开'], "answer": 'C'},
    {"question": "14. 型腔中跌落了一些松砂，应怎么办？", "options": ['A. 用嘴吹', 'B. 用砂椿椿平', 'C. 用皮老虎吹走或用毛笔水带走'], "answer": 'C'},
    {"question": "15. 铸件上的拔模斜度应加在哪些面上最好？", "options": ['A. 各个面上', 'B. 与分型面平行的平面', 'C. 与分型面垂直的平面'], "answer": 'C'},
    {"question": "16. 可锻铸铁可以锻造成型的。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "17. 弹簧钢的最终热处理工艺通常采用淬火加低温回火，获得回火马氏体组织。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "18. 20钢采用正火预先热处理可以提高钢的硬度，提高切削加工性能。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'A'},
    {"question": "19. 钢材随着冷变形量的增加：强度、硬度会增加，而塑性、韧性降低。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'A'},
    {"question": "20. 调质处理就是淬火加中温回火", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "21. 车削时的主运动是工件的旋转运动，进给运动是刀具移动。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'A'},
    {"question": "22. 车刀常用材料的有高速钢和硬质合金。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'A'},
    {"question": "23. 常用于刃磨高速钢车刀的砂轮是：", "options": ['A. 氧化铝砂轮', 'B. 碳化硅砂轮', 'C. 氧化锆砂轮'], "answer": 'A'},
    {"question": "24. 切削三要素是指切削速度、进给量和切削宽度。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "25. 车外圆时的切削深度是指：", "options": ['A. 待加工表面与已加工表面的直径差', 'B. 切出切削厚度', 'C. 待加工表面与已加工表面的直径差的一半'], "answer": 'C'},
    {"question": "26. 端面时车不完整，中心总是留有一小凸台：何故？", "options": ['A. 尖低于工件中心', 'B. 尖磨钝了', 'C. 尖低于车床主轴中心'], "answer": 'A'},
    {"question": "27. 车刀主偏角选取值一般为：", "options": ['A. 10~20°', 'B. 20° ~ 30°', 'C. 30°~90°'], "answer": 'C'},
    {"question": "28. 车床通用夹具中，能自动定心的是：", "options": ['A. 四爪卡盘', 'B. 三爪卡盘', 'C. 花盘'], "answer": 'B'},
    {"question": "29. 车刀的前刀面与主后刀面的交线称为：", "options": ['A. 副切削刃', 'B. 主切削刃', 'C. 刀尖'], "answer": 'B'},
    {"question": "30. 不能戴下列哪些物品开车床？", "options": ['A. 帽', 'B. 手套', 'C. 眼镜'], "answer": 'B'},
    {"question": "31. 车床主轴箱用于车削不同种类的螺纹。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "32. 车外圆时，车刀的主切削刃与车刀前进方向的夹角称为：", "options": ['A. 前角', 'B. 主偏角', 'C. 副偏角'], "answer": 'B'},
    {"question": "33. 安装车刀时，刀尖应装得与工件中心：", "options": ['A. 等高', 'B. 比工件中心稍高', 'C. 比工件中心稍低'], "answer": 'A'},
    {"question": "34. 车削钢件时铁屑缠绕挡住了视线，想看清车刀和工件，应该怎么做？", "options": ['A. 停车把切屑除去', 'B. 不停车戴上手套后将铁屑除去', 'C. 不停车用铁钩将铁屑除去'], "answer": 'A'},
    {"question": "35. 适合车床上加工的平面是什么样的平面？", "options": ['A. 回转面', 'B. 轴上和圆盘上的端面', 'C. 一般平面'], "answer": 'B'},
    {"question": "36. 车刀刃倾角选取值一般为：", "options": ['A. 5°~10°', 'B. -10°~5°', 'C. 15°~20°'], "answer": 'B'},
    {"question": "37. 可作车刀的材料是：", "options": ['A. 铸铁', 'B. 碳素结构钢', 'C. 高速钢'], "answer": 'C'},
    {"question": "38. 用手锯锯钢管时应选用哪种锯条？", "options": ['A. 粗齿', 'B. 中齿', 'C. 细齿'], "answer": 'C'},
    {"question": "39. 某一同学在攻丝时，攻了一段时间发现全无螺纹，但丝锥已深入工件内，原因是：", "options": ['A. 丝锥与工件不垂直，攻丝时摇晃造成', 'B. 孔径与丝锥外径一样大', 'C. 丝锥选错了'], "answer": 'B'},
    {"question": "40. 钳工在圆杆上加工出外螺纹，应用哪种工具？", "options": ['A. 丝锥', 'B. 板牙', 'C. 子'], "answer": 'B'},
    {"question": "41. 锯条的锯齿为什么按波形排列？", "options": ['A. 减少摩擦', 'B. 容易散热', 'C. 加强锯条钢性'], "answer": 'A'},
    {"question": "42. 孔快钻通时应注意什么：", "options": ['A. 保持原来的进给速度不变', 'B. 加快进给速度', 'C. 减慢进给速度'], "answer": 'C'},
    {"question": "43. 锯条装得太松会怎样？", "options": ['A. 锯条易折断', 'B. 锯缝会不直', 'C. 锯起来费力'], "answer": 'A'},
    {"question": "44. 锯片的安装应：", "options": ['A. 锯齿向前', 'B. 锯齿向后', 'C. 锯齿方向无要求'], "answer": 'A'},
    {"question": "45. 工件装配时可用铁捶直接敲击工件表面直到压入。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "1. 锻造加热时，时间越长越好。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "2. 钢和铸铁都能进行压力加工。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "3. 冲压工序中的落料，被冲落下的部分为工件。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'A'},
    {"question": "4. 冷冲压的汽车外壳钢板，最好选用：", "options": ['A. 低碳钢板', 'B. 中碳钢板', 'C. 高碳钢板'], "answer": 'A'},
    {"question": "5. 锻造时，使坏料的长度增加，直径减小的工序为：", "options": ['A. 镦粗', 'B. 拔长', 'C. 错移'], "answer": 'B'},
    {"question": "6. 钢在加热时温度过高，使其晶粒边界熔化，这一缺陷称为：", "options": ['A. 过热', 'B. 氧化/脱碳', 'C. 过烧'], "answer": 'C'},
    {"question": "7. 在一个冲程内，在不同部位完成两道以上工序的冲模为：", "options": ['A. 简单冲模', 'B. 连续冲模', 'C. 复合冲模'], "answer": 'C'},
    {"question": "8. 下列工件中，适合锻造制坏的是：", "options": ['A. 变速箱箱体', 'B. 起重机吊钩', 'C. 车床床身'], "answer": 'B'},
    {"question": "9. 锻造加热的目的是：", "options": ['A. 提高塑性', 'B. 提高强度', 'C. 提高韧性'], "answer": 'A'},
    {"question": "10. 钢材随着冷变形量的增加，强度、硬度会增加，而塑性、韧性降低。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'A'},
    {"question": "11. 气焊时气焊炬关闭的顺序：", "options": ['A. 先关氧气，后关乙炔', 'B. 先关乙炔，后关氧气', 'C. 乙炔和氧气同时关'], "answer": 'B'},
    {"question": "12. 用直流电弧焊正接法施焊时，焊条应接什么极？", "options": ['A. 正极', 'B. 负极', 'C. 正负极均可'], "answer": 'B'},
    {"question": "13. 手工电弧焊的热源是：", "options": ['A. 电弧产生的热', 'B. 药皮燃烧产生的热', 'C. 电源电流产生的热'], "answer": 'C'},
    {"question": "14. 埋弧自动焊的优点是：", "options": ['A. 适应性好，特别宜焊垂直焊缝', 'B. 可用更大的电流，一次焊透深度较大', 'C. 很适合单件小批量焊各种位置的焊缝'], "answer": 'B'},
    {"question": "15. 焊接电弧的实质是：", "options": ['A. 电流流过两个电极时产生的高温', 'B. 药皮溶化燃烧时产生的高温', 'C. 电极间气体电离导电产生的高温'], "answer": 'C'},
    {"question": "16. 选用碱性焊条的主要原因是：", "options": ['A. 焊缝的抗裂性能好', 'B. 焊接工艺性能好', 'C. 可以使用廉价的交流焊机'], "answer": 'A'},
    {"question": "17. 焊条药皮的作用之一是：", "options": ['A. 增加焊接电流', 'B. 对焊逢起保护作用', 'C. 增加焊接温度'], "answer": 'B'},
    {"question": "18. 气割时要求被割金属应具备的性质之一是：", "options": ['A. 金属氧化物的熔点应低于金属的熔点', 'B. 金属氧化物的熔点应低于金属的燃点', 'C. 金属氧化物的熔点应等于金属的熔点'], "answer": 'A'},
    {"question": "19. 手弧焊时，焊接电流确定的主要依据是：", "options": ['A. 焊逢的宽度', 'B. 焊丝的直径', 'C. 焊接位置'], "answer": 'B'},
    {"question": "20. 手弧焊焊大于6mm厚的焊件时，应采取什么样的措施保证质量：", "options": ['A. 使用大于6mm直径的焊丝', 'B. 焊件接头处开坡口', 'C. 采用更大的电流'], "answer": 'B'},
    {"question": "21. 刨床的主运动是：", "options": ['A. 工作台带工件的前后运动', 'B. 滑枕带刀具的左右运动', 'C. 刀架带刨刀的上下运动'], "answer": 'B'},
    {"question": "22. 刨床不能加工下列的：", "options": ['A. 斜面', 'B. 燕尾槽', 'C. 外园柱面'], "answer": 'C'},
    {"question": "23. 下面的不是铣床附件。", "options": ['A. 平口钳', 'B. 中心架', 'C. 分度头'], "answer": 'B'},
    {"question": "24. 在铣床上加工30个齿的齿轮，来采用分度头直接分度时，手柄应转：", "options": ['A. 1! 转', 'B. 3 转', 'C. 12 转'], "answer": 'B'},
    {"question": "25. 铣床的主运动是：", "options": ['A. 工作台带工件的左右运动', 'B. 工作台带工件的前后运动', 'C. 铣刀的旋转运动'], "answer": 'C'},
    {"question": "26. 工件表面有硬皮时，应采用：", "options": ['A. 周铣', 'B. 逆铣', 'C. 顺铣'], "answer": 'B'},
    {"question": "27. 卧式铣床一般选用：", "options": ['A. 带孔的铣刀', 'B. 带锥柄的铣刀', 'C. 带直柄的铣刀'], "answer": 'A'},
    {"question": "28. 顺铣时会引起打刀现象，这是由于以下哪种原因造成的：", "options": ['A. 进给机构的齿轮副有间隙', 'B. 进给机构的丝杆与螺母有间隙', 'C. 进给机构的蜗杆蜗轮有间隙'], "answer": 'B'},
    {"question": "29. 外园磨床的主运动是", "options": ['A. 工件的旋转运动', 'B. 工件的左右水平运动', 'C. 砂轮的旋转运动'], "answer": 'C'},
    {"question": "30. 砂轮的硬度是指：", "options": ['A. 砂轮磨粒的硬度', 'B. 砂轮磨粒的脱落难易程度', 'C. 使用的结合剂的强度'], "answer": 'B'},
    {"question": "31. 组成砂轮的三个基本要素是：", "options": ['A. 磨料粒度、砂轮硬度、形状尺寸', 'B. 磨料、结合剂、孔隙', 'C. 磨料、粒度、结合剂强度'], "answer": 'B'},
    {"question": "32. 这次实习时使用的平面磨床是", "options": ['A. 园台周磨', 'B. 园台端磨', 'C. 矩台周磨'], "answer": 'C'},
    {"question": "33. 检查工件形状和位置误差可使用下列哪些量具？", "options": ['A. 百分尺', 'B. 百分表', 'C. 卡尺'], "answer": 'B'},
    {"question": "34. 实习中使用的游标卡尺的测量精度为：", "options": ['A. 0.01mm', 'B. 0.02mm', 'C. 0.1mm'], "answer": 'B'},
    {"question": "35. 工件加工表面质量的主要指标是表面粗糙度。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'A'},
    {"question": "36. 游标卡尺不能测量深度方向的尺寸。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "37. 表面粗糙度越小，零件表面越光。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'A'},
    {"question": "38. 数控机床由机床主体和数控系统两部分组成。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "39. 数控机床的进给运动是由伺服系统完成。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'A'},
    {"question": "40. 数控车床也有主轴箱和溜板箱。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'C'},
    {"question": "41. “G00X25Z71”表示定位到X25Z71的位置。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'A'},
    {"question": "42. 指令“G02X50Z30”将完成以下操作：", "options": ['A. 直线插补', 'B. 顺时针圆弧插补', 'C. 逆时针圆弧插补'], "answer": 'B'},
    {"question": "43. 按照绝对坐标进行数控编程是用移动的终点坐标的坐标值进行编程。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'A'},
    {"question": "44. 数控代码“S800”表示：", "options": ['A. 进给速度为800毫米/分', 'B. 转速为800转/分', 'C. 其他含义'], "answer": 'B'},
    {"question": "45. 在数控加工中可自动进行刀具半径的补偿。", "options": ['A. 对', 'B. 有时对', 'C. 不对'], "answer": 'A'},
{
        "question": "247. 在车床上用切断刀切断工件时，切断速度是始终不变的。",
        "options": [
            "A. 对",
            "B. 不对"
        ],
        "answer": "B"
    },
    {
        "question": "248. 车床主轴的反转是通过电动机反转实现的。",
        "options": [
            "A. 对",
            "B. 不对"
        ],
        "answer": "A"
    },
    {
        "question": "249. 直头车刀的形状简单，主要用来粗车外圆。",
        "options": [
            "A. 对",
            "B. 不对"
        ],
        "answer": "A"
    },
    {
        "question": "250. 三爪卡盘的个爪可以单独移动吗？",
        "options": [
            "A. 可以",
            "B. 不可以"
        ],
        "answer": "B"
    },
    {
        "question": "251. 车外圆时带动溜板箱作进给运动的是：",
        "options": [
            "A. 光杠",
            "B. 丝杠",
            "C. 螺杠"
        ],
        "answer": "A"
    },
    {
        "question": "252. 车床的主运动和进给运动是由两台电动机分别带动的。",
        "options": [
            "A. 对",
            "B. 不对"
        ],
        "answer": "B"
    },
    {
        "question": "253. 车床夹具中能自动定心的是四爪卡盘。",
        "options": [
            "A. 对",
            "B. 不对"
        ],
        "answer": "B"
    },
    {
        "question": "254. 刀具后角是主后刀面与基面间的夹角，在正交面上测量。",
        "options": [
            "A. 对",
            "B. 不对"
        ],
        "answer": "A"
    },
    {
        "question": "255. 主偏刀是指主偏角大于或等于90°的车刀。",
        "options": [
            "A. 对",
            "B. 不对"
        ],
        "answer": "A"
    },
    {
        "question": "256. 车外圆时的切削深度是指：",
        "options": [
            "A. 待加工表面与已加工表面的直径差",
            "B. 切出切削厚度",
            "C. 待加工表面与已加工表面的直径差的一半"
        ],
        "answer": "C"
    },
    {
        "question": "257. 氧化铝砂轮可以用来刃磨硬质合金车刀。",
        "options": [
            "A. 对",
            "B. 不对"
        ],
        "answer": "B"
    },
    {
        "question": "258. 车刀的前刀面与主后刀面的交线称为：",
        "options": [
            "A. 副切削刃",
            "B. 主切削刃",
            "C. 刀尖"
        ],
        "answer": "B"
    },
    {
        "question": "259. 不能戴下列哪些物品开车床？",
        "options": [
            "A. 帽",
            "B. 手套",
            "C. 眼镜"
        ],
        "answer": "B"
    },
    {
        "question": "260. 车削工件时，切屑流过的表面是：",
        "options": [
            "A. 主后刀面",
            "B. 副后刀面",
            "C. 前刀面"
        ],
        "answer": "C"
    },
    {
        "question": "261. 车削较短圆锥时，如锥角为α，则车刀切削刃与主轴轴线的夹角就为：",
        "options": [
            "A. α",
            "B. α/2",
            "C. α/3"
        ],
        "answer": "B"
    },
    {
        "question": "262. 尾座只能用于安装后顶尖以支持工件，而不能安装钻头。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "263. 车削钢件时铁屑缠绕挡住了视线，想看清车刀和工件，应该怎么做？",
        "options": [
            "A. 停车把切屑除去",
            "B. 不停车戴上手套后将铁屑除去",
            "C. 不停车用铁钩将铁屑除去"
        ],
        "answer": "A"
    },
    {
        "question": "264. 适合车床上加工的平面是什么样的平面？",
        "options": [
            "A. 回转面",
            "B. 轴上和圆盘上的端面",
            "C. 一般平面"
        ],
        "answer": "B"
    },
    {
        "question": "265. 车刀刃倾角选取值一般为：",
        "options": [
            "A. 5°~10°",
            "B. -10°~5°",
            "C. 15°~20°"
        ],
        "answer": "B"
    },
    {
        "question": "266. 可作车刀的材料是：",
        "options": [
            "A. 铸铁",
            "B. 碳素结构钢",
            "C. 高速钢"
        ],
        "answer": "C"
    },
    {
        "question": "267. 手锯条用什么材料制成？",
        "options": [
            "A. 碳素结构钢",
            "B. 碳素工具钢",
            "C. 高速钢"
        ],
        "answer": "B"
    },
    {
        "question": "268. 锉刀往后返回时应注意什么？",
        "options": [
            "A. 提起锉刀",
            "B. 和前进时一样均匀加压",
            "C. 不紧压工件"
        ],
        "answer": "A"
    },
    {
        "question": "269. 孔快要钻穿时，进给速度应怎样控制？",
        "options": [
            "A. 保持匀速",
            "B. 减慢",
            "C. 加快"
        ],
        "answer": "B"
    },
    {
        "question": "270. 锉削铜，铝等软金属宜用哪种锉刀？",
        "options": [
            "A. 细齿锉",
            "B. 粗齿锉",
            "C. 中齿锉"
        ],
        "answer": "B"
    },
    {
        "question": "271. 锯片的安装应：",
        "options": [
            "A. 锯齿向前",
            "B. 锯齿向后",
            "C. 锯齿方向无要求"
        ],
        "answer": "A"
    },
    {
        "question": "272. 钳工在圆杆上加工出外螺纹，应用哪种工具？",
        "options": [
            "A. 板牙",
            "B. 丝锥"
        ],
        "answer": "A"
    },
    {
        "question": "273. 如何才能锉出平整表面？",
        "options": [
            "A. 锉削时两手施于锉刀的力应保持锉刀在水平面上运动",
            "B. 两手施于锉刀的力应始终不变",
            "C. 右手握柄施力，左手压锉不能用力"
        ],
        "answer": "A"
    },
    {
        "question": "274. 钳工的划线基准通常与设计基准一致。",
        "options": [
            "A. 对",
            "B. 不对",
            "C. 有时对"
        ],
        "answer": "A"
    },
    {
        "question": "275. 某一同学在攻丝时，攻了一段时间发现全无螺纹，但丝锥已深入工件内，什么原因？",
        "options": [
            "A. 丝锥与工件不垂直，攻丝时摇晃造成",
            "B. 孔径与丝锥外径一样大"
        ],
        "answer": "B"
    },
    {
        "question": "276. 交流电弧焊机实质上是一种什么变压器？",
        "options": [
            "A. 降压变压器",
            "B. 升压变压器",
            "C. 特殊的降压变压器"
        ],
        "answer": "C"
    },
    {
        "question": "277. 碱性焊条焊接时应使用哪种电焊机？",
        "options": [
            "A. 交流电焊机",
            "B. 交流和直流焊机都可使用",
            "C. 直流电焊机"
        ],
        "answer": "C"
    },
    {
        "question": "278. 气焊炬开放气体和调节火焰的顺序：",
        "options": [
            "A. 先开乙炔一一点火一开氧气一调节火焰",
            "B. 先微开氧气一开乙炔一一点火一调节火焰",
            "C. 先开乙炔一开氧气一一点火一调节火焰"
        ],
        "answer": "B"
    },
    {
        "question": "279. 焊条药皮的作用之一是：",
        "options": [
            "A. 增加焊接电流",
            "B. 脱去有害杂质",
            "C. 增加焊接温度"
        ],
        "answer": "B"
    },
    {
        "question": "280. 为防爆炸，乙炔发生器应配备什么装置？",
        "options": [
            "A. 乙炔钢瓶",
            "B. 减压器",
            "C. 回火保险器"
        ],
        "answer": "C"
    },
    {
        "question": "281. 用直流电弧焊反接法施焊时，焊条应接哪一极？",
        "options": [
            "A. 正极",
            "B. 负极",
            "C. 正负极均可"
        ],
        "answer": "A"
    },
    {
        "question": "282. 气体保护焊的热源是：",
        "options": [
            "A. 气体",
            "B. 电弧",
            "C. 电阻"
        ],
        "answer": "B"
    },
    {
        "question": "283. 气焊可用来切割吗？",
        "options": [
            "A. 可以",
            "B. 不可以"
        ],
        "answer": "B"
    },
    {
        "question": "284. 气焊中较少使用的氧乙炔焰是：",
        "options": [
            "A. 碳化焰",
            "B. 中性焰",
            "C. 氧化焰"
        ],
        "answer": "C"
    },
    {
        "question": "285. 焊条直径是指哪一部分的直径？",
        "options": [
            "A. 焊条外径",
            "B. 焊芯直径",
            "C. 最大处直径"
        ],
        "answer": "B"
    },
    {
        "question": "286. 数控机床的进给运动是由伺服系统完成。",
        "options": [
            "A. 对",
            "B. 不对"
        ],
        "answer": "A"
    },
    {
        "question": "287. “G00X25Z71”表示定位到X25Z71的位置。",
        "options": [
            "A. 对",
            "B. 不对"
        ],
        "answer": "B"
    },
    {
        "question": "288. 指令“G02X50Z30”将完成以下操作：",
        "options": [
            "A. 直线插补",
            "B. 顺时针圆弧插补",
            "C. 逆时针圆弧插补"
        ],
        "answer": "B"
    },
    {
        "question": "289. 按照相对坐标进行数控编程是用实际移动量进行编程。",
        "options": [
            "A. 对",
            "B. 不对"
        ],
        "answer": "A"
    },
    {
        "question": "290. 数控代码“G98F100”表示：",
        "options": [
            "A. 进给速度为100毫米/分",
            "B. 转速为100转/分",
            "C. 其他含义"
        ],
        "answer": "A"
    },
    {
        "question": "291. T10钢的平均含碳量为0.1%",
        "options": [
            "A. 对",
            "B. 不对"
        ],
        "answer": "B"
    },
    {
        "question": "292. 可锻铸铁可以锻造成型的。",
        "options": [
            "A. 对",
            "B. 不对"
        ],
        "answer": "B"
    },
    {
        "question": "293. 调质处理就是淬火加中温回火。",
        "options": [
            "A. 对",
            "B. 不对"
        ],
        "answer": "B"
    },
    {
        "question": "294. 中碳钢的热处理工艺通常采用调质处理获得良好的综合机械性能。",
        "options": [
            "A. 对",
            "B. 不对"
        ],
        "answer": "A"
    },
    {
        "question": "295. 钢材随着冷变形量的增加，强度、硬度会增加，而塑性、韧性降低。",
        "options": [
            "A. 对",
            "B. 不对"
        ],
        "answer": "A"
    },
    {
        "question": "296. 大批量生产手轮毛坏应选用的工艺方法是：",
        "options": [
            "A. 锻造",
            "B. 铸造",
            "C. 焊接"
        ],
        "answer": "B"
    },
    {
        "question": "297. 制模型时，在要铸出孔的地方，应加什么？",
        "options": [
            "A. 收缩量",
            "B. 型芯头",
            "C. 加工余量"
        ],
        "answer": "B"
    },
    {
        "question": "298. 有时型砂中加入少量煤粉，其主要目的是：",
        "options": [
            "A. 提高型砂的透气性",
            "B. 提高型砂的强度",
            "C. 减少粘砂的倾向"
        ],
        "answer": "A"
    },
    {
        "question": "299. 铸件的形状和模型的形状相似，对吗？",
        "options": [
            "A. 对",
            "B. 不对"
        ],
        "answer": "A"
    },
    {
        "question": "300. 什么是错箱？",
        "options": [
            "A. 砂箱尺寸选错了",
            "B. 放错了另一个上箱",
            "C. 铸件上、下面部分在分型面处错开"
        ],
        "answer": "C"
    },
    {
        "question": "301. 铸件上的拔模斜度应加在哪些面上最好？",
        "options": [
            "A. 各个面上",
            "B. 与分型面平行的平面",
            "C. 与分型面垂直的平面"
        ],
        "answer": "C"
    },
    {
        "question": "302. 铸件表面上有局部凹陷的地方，这是什么原因造成的？",
        "options": [
            "A. 浇不足",
            "B. 收缩",
            "C. 铸型开裂"
        ],
        "answer": "B"
    },
    {
        "question": "303. 型砂的强度不足会产生什么缺陷？",
        "options": [
            "A. 气孔",
            "B. 夹砂",
            "C. 裂纹"
        ],
        "answer": "B"
    },
    {
        "question": "304. 浇注系统中内浇口主要作用是：",
        "options": [
            "A. 缓冲",
            "B. 挡渣",
            "C. 控制液体金属流速和流向"
        ],
        "answer": "C"
    },
    {
        "question": "305. 用什么方法可把三箱造型改为两箱造型？",
        "options": [
            "A. 加外型芯",
            "B. 加高下箱",
            "C. 修改浇注系统"
        ],
        "answer": "A"
    },
    {
        "question": "306. 桩砂用的平椿，在未用到时，应怎样放置？",
        "options": [
            "A. 垂直放",
            "B. 横放",
            "C. 随便放"
        ],
        "answer": "B"
    },
    {
        "question": "307. 型芯的主要作用是：",
        "options": [
            "A. 增加铸件的强度",
            "B. 增加铸件的透气性",
            "C. 形成铸件的内腔"
        ],
        "answer": "C"
    },
    {
        "question": "308. 通气孔必须扎到与型腔相通，对吗？",
        "options": [
            "A. 对",
            "B. 不对"
        ],
        "answer": "B"
    },
    {
        "question": "309. 型腔中跌落了一些松砂，应怎么办？",
        "options": [
            "A. 用嘴吹",
            "B. 用砂椿椿平",
            "C. 用皮老虎吹走或用毛笔蘸水带走"
        ],
        "answer": "C"
    },
    {
        "question": "310. 铸件整个都在同一砂箱内，好吗？",
        "options": [
            "A. 好",
            "B. 不好",
            "C. 看情况而定"
        ],
        "answer": "C"
    },
    {
        "question": "311. 下列工件中，适合锻造制坏的是：",
        "options": [
            "A. 变速箱箱体",
            "B. 起重机吊钩",
            "C. 车床床身"
        ],
        "answer": "B"
    },
    {
        "question": "312. 锻造加热的目的是：",
        "options": [
            "A. 提高塑性",
            "B. 提高强度",
            "C. 提高韧性"
        ],
        "answer": "A"
    },
    {
        "question": "313. 水轮机主轴应采取的锻造方法是：",
        "options": [
            "A. 模锻",
            "B. 自由锻",
            "C. 胎模锻"
        ],
        "answer": "B"
    },
    {
        "question": "314. 锻造加热时，使工件内部晶粒粗化，塑性下降，这一缺陷称为：",
        "options": [
            "A. 过热",
            "B. 过烧",
            "C. 脱碳"
        ],
        "answer": "A"
    },
    {
        "question": "315. 内孔和外缘同轴度要求较高的冲压件，最好采用：",
        "options": [
            "A. 简单冲模",
            "B. 连续冲模",
            "C. 复合冲模"
        ],
        "answer": "C"
    },
    {
        "question": "316. 冷变形（再结晶温度T以下）会产生加工硬化组织。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "A"
    },
    {
        "question": "317. 水压机的公称规格是以产生的最大压力来定义。",
        "options": [
            "A. 对",
            "B. 不对"
        ],
        "answer": "A"
    },
    {
        "question": "318. 锻造加热时，温度越高越好。",
        "options": [
            "A. 对",
            "B. 不对"
        ],
        "answer": "B"
    },
    {
        "question": "319. 模锻件一般不超过150Kg。",
        "options": [
            "A. 对",
            "B. 不对"
        ],
        "answer": "A"
    },
    {
        "question": "320. 冲压工序中的冲孔，被冲落下的部分为工件。",
        "options": [
            "A. 对",
            "B. 不对"
        ],
        "answer": "A"
    },
    {
        "question": "321. 下面的不是铣床附件。",
        "options": [
            "A. 中心架",
            "B. 平口钳",
            "C. 分度头"
        ],
        "answer": "A"
    },
    {
        "question": "322. 铣床的主运动是：",
        "options": [
            "A. 铣刀的旋转运动",
            "B. 工作台带工件的上下运动",
            "C. 工作台带工件的前后运动"
        ],
        "answer": "A"
    },
    {
        "question": "323. 铣床不能加工：",
        "options": [
            "A. 燕尾槽",
            "B. 斜面",
            "C. 外圆柱面"
        ],
        "answer": "C"
    },
    {
        "question": "324. 工件表面有硬皮时，应采用：",
        "options": [
            "A. 端铣",
            "B. 顺铣",
            "C. 逆铣"
        ],
        "answer": "C"
    },
    {
        "question": "325. 顺铣时会引起打刀现象，这是由于，造成。",
        "options": [
            "A. 进给机构的齿轮副有间隙",
            "B. 进给机构的丝杆与螺母有间隙",
            "C. 进给机构的蜗杆蜗轮有间隙"
        ],
        "answer": "B"
    },
    {
        "question": "326. 在牛头刨床进行刨削的主运动是：",
        "options": [
            "A. 工作台的间歇进给",
            "B. 滑枕的往复移动",
            "C. 工作台的上下移动"
        ],
        "answer": "B"
    },
    {
        "question": "327. 砂轮的硬度是指：",
        "options": [
            "A. 砂轮磨料的硬度",
            "B. 砂轮磨粒的脱落难易程度",
            "C. 结合剂的强度"
        ],
        "answer": "B"
    },
    {
        "question": "328. 组成砂轮的三个基本要素是：",
        "options": [
            "A. 磨料、结合剂、孔隙",
            "B. 磨料粒度、砂轮硬度、形状尺寸",
            "C. 磨料硬度、结合剂硬度、砂轮硬度"
        ],
        "answer": "A"
    },
    {
        "question": "329. 实习中使用的游标卡尺的测量精度为：",
        "options": [
            "A. 0.01mm",
            "B. 0.02mm",
            "C. 0.1mm"
        ],
        "answer": "B"
    },
    {
        "question": "330. 工件加工表面质量的主要指标是表面粗糙度。",
        "options": [
            "A. 对",
            "B. 不对"
        ],
        "answer": "A"
    },
    {
        "question": "331. 检查工件形状和位置误差可使用下列哪些量具？",
        "options": [
            "A. 百分尺",
            "B. 百分表",
            "C. 卡尺"
        ],
        "answer": "B"
    },
    {
        "question": "332. 齿轮和轴的联接方式通常采用：",
        "options": [
            "A. 键联接",
            "B. 销联接",
            "C. 螺纹联接"
        ],
        "answer": "A"
    },
    {
        "question": "333. 工件装配时可用铁捶直接敲击工件表面直到压入。",
        "options": [
            "A. 对",
            "B. 不对"
        ],
        "answer": "B"
    },
    {
        "question": "334. 轴承如果采用较大的过盈配合，可采用加工后趁热装入。",
        "options": [
            "A. 对",
            "B. 不对"
        ],
        "answer": "A"
    },
    {
        "question": "335. 铸件的形状和模型的形状相似，对吗？",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "A"
    },
    {
        "question": "336. 什么是错箱？",
        "options": [
            "A. 砂箱尺寸选错了",
            "B. 放错了另一个上箱",
            "C. 铸件上、下面部分在分型面处错开"
        ],
        "answer": "B"
    },
    {
        "question": "337. 桩砂用的平椿，在未用到时，应怎样放置？",
        "options": [
            "A. 垂直放",
            "B. 横放",
            "C. 随便放"
        ],
        "answer": "B"
    },
    {
        "question": "338. 型腔中跌落了些松砂，应怎么办？",
        "options": [
            "A. 用嘴吹",
            "B. 用砂椿椿平",
            "C. 用皮老虎吹走或用毛笔蘸水带走"
        ],
        "answer": "C"
    },
    {
        "question": "339. 铸件整个都在同一砂箱内，好吗？",
        "options": [
            "A. 好",
            "B. 不好",
            "C. 看情况而定"
        ],
        "answer": "A"
    },
    {
        "question": "340. 铸件上的拔模斜度应加在哪些面上最好？",
        "options": [
            "A. 各个面上",
            "B. 与分型面平行的平面",
            "C. 与分型面垂直的平面"
        ],
        "answer": "C"
    },
    {
        "question": "341. 铸件表面上有局部凹陷的地方，这是什么原因造成的？",
        "options": [
            "A. 浇不足",
            "B. 收缩",
            "C. 铸型开裂"
        ],
        "answer": "A"
    },
    {
        "question": "342. 型砂的强度不足会产生什么缺陷？",
        "options": [
            "A. 气孔",
            "B. 夹砂",
            "C. 裂纹"
        ],
        "answer": "B"
    },
    {
        "question": "343. 型芯的主要作用是：",
        "options": [
            "A. 增加铸件的强度",
            "B. 增加铸件的透气性",
            "C. 形成铸件的内腔"
        ],
        "answer": "C"
    },
    {
        "question": "344. 通气孔必须扎到与型腔相通，对吗？",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "345. 本实习中心铸造车间用什么熔炉？",
        "options": [
            "A. 冲天炉",
            "B. 坩埚炉",
            "C. 平炉"
        ],
        "answer": "B"
    },
    {
        "question": "346. 活块造型适用于哪种场合？",
        "options": [
            "A. 单件生产",
            "B. 中批生产",
            "C. 大批生产"
        ],
        "answer": "A"
    },
    {
        "question": "347. 浇注系统中内浇口主要作用是：",
        "options": [
            "A. 缓冲",
            "B. 挡渣",
            "C. 控制液体金属流速和流向"
        ],
        "answer": "C"
    },
    {
        "question": "348. 用什么方法可把三箱造型改为两箱造型？",
        "options": [
            "A. 加外型芯",
            "B. 加高下箱",
            "C. 修改浇注系统"
        ],
        "answer": "A"
    },
    {
        "question": "349. 大批量生产手轮毛坏应选用的工艺方法是：",
        "options": [
            "A. 锻造",
            "B. 铸造",
            "C. 焊接"
        ],
        "answer": "A"
    },
    {
        "question": "350. 冷变形（再结晶温度T以下）会产生加工硬化组织。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "A"
    },
    {
        "question": "351. 水压机的公称规格是以产生的最大压力来定义。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "A"
    },
    {
        "question": "352. 锻造加热时，温度越高越好。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "353. 模锻件一般不超过150Kg。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "A"
    },
    {
        "question": "354. 冲压工序中的冲孔，被冲落下的部分为工件。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "355. 下列工件中，适合锻造制坏的是：",
        "options": [
            "A. 变速箱箱体",
            "B. 起重机吊钩",
            "C. 车床床身"
        ],
        "answer": "B"
    },
    {
        "question": "356. 锻造加热的目的是：",
        "options": [
            "A. 提高塑性",
            "B. 提高强度",
            "C. 提高韧性"
        ],
        "answer": "A"
    },
    {
        "question": "357. 水轮机主轴应采取的锻造方法是：",
        "options": [
            "A. 模锻",
            "B. 自由锻",
            "C. 胎模锻"
        ],
        "answer": "B"
    },
    {
        "question": "358. 锻造加热时，使工件内部晶粒粗化，塑性下降，这一缺陷称为：",
        "options": [
            "A. 过热",
            "B. 过烧",
            "C. 脱碳"
        ],
        "answer": "A"
    },
    {
        "question": "359. 内孔和外缘同轴度要求较高的冲压件，最好采用：",
        "options": [
            "A. 简单冲模",
            "B. 连续冲模",
            "C. 复合冲模"
        ],
        "answer": "C"
    },
    {
        "question": "360. 用直流电弧焊反接法施焊时，焊条应接哪一极？",
        "options": [
            "A. 正极",
            "B. 负极",
            "C. 正负极均可"
        ],
        "answer": "A"
    },
    {
        "question": "361. 气体保护焊的热源是：",
        "options": [
            "A. 气体",
            "B. 电弧",
            "C. 电阻"
        ],
        "answer": "B"
    },
    {
        "question": "362. 气焊可用来切割吗？",
        "options": [
            "A. 可以",
            "B. 不可以",
            "C. 有时可以"
        ],
        "answer": "C"
    },
    {
        "question": "363. 普通焊接结构最常用哪种材料？",
        "options": [
            "A. 高碳钢",
            "B. 中碳钢",
            "C. 低碳钢"
        ],
        "answer": "C"
    },
    {
        "question": "364. 焊条直径是指哪部分的直径？",
        "options": [
            "A. 焊条外径",
            "B. 焊芯直径",
            "C. 最大处直径"
        ],
        "answer": "B"
    },
    {
        "question": "365. 交流电弧焊机实质上是一个什么变压器？",
        "options": [
            "A. 降压变压器",
            "B. 升压变压器",
            "C. 特殊的降压变压器"
        ],
        "answer": "C"
    },
    {
        "question": "366. 碱性焊条焊接时应使用那种电焊机？",
        "options": [
            "A. 交流电焊机",
            "B. 交流和直流焊机都可使用",
            "C. 直流电焊机"
        ],
        "answer": "C"
    },
    {
        "question": "367. 气焊炬开放气体和调节火焰的顺序：",
        "options": [
            "A. 先开乙炔一点火—开氧气—调节火焰",
            "B. 先微开氧气—开乙炔一点火—调节火焰",
            "C. 先开乙炔—开氧气一点火—调节火焰"
        ],
        "answer": "B"
    },
    {
        "question": "368. 电阻焊的特点之一是：",
        "options": [
            "A. 焊接时加压、加热同时进行",
            "B. 焊接时先加热，后加压",
            "C. 焊接时先加压，到加热时去除压力"
        ],
        "answer": "A"
    },
    {
        "question": "369. 焊条药皮的作用之一是：",
        "options": [
            "A. 增加焊接电流",
            "B. 脱去有害杂质",
            "C. 增加焊接温度"
        ],
        "answer": "B"
    },
    {
        "question": "370. 埋弧自动焊的主要特点之一是：",
        "options": [
            "A. 焊缝保护好，焊接质量高",
            "B. 焊接工艺性能好，适应面广",
            "C. 焊缝含氢量少，又称低氢焊接"
        ],
        "answer": "A"
    },
    {
        "question": "371. 用手工电弧焊焊小于6mm厚的焊件时，焊条直径的选用主要依据是：",
        "options": [
            "A. 焊接电流",
            "B. 坡口的形式",
            "C. 被焊工件的厚度"
        ],
        "answer": "C"
    },
    {
        "question": "372. “结423”焊条中尾3的含义是：",
        "options": [
            "A. 碱性焊条",
            "B. 酸性焊条",
            "C. 塑性约等于3%"
        ],
        "answer": "B"
    },
    {
        "question": "373. 为防爆炸，乙炔发生器应配备什么装置？",
        "options": [
            "A. 乙炔钢瓶",
            "B. 减压器",
            "C. 回火保险器"
        ],
        "answer": "C"
    },
    {
        "question": "374. 气焊中较少使用的氧乙炔焰是：",
        "options": [
            "A. 碳化焰",
            "B. 中性焰",
            "C. 氧化焰"
        ],
        "answer": "C"
    },
    {
        "question": "375. T10钢的平均含碳量为0.1%。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "376. 可锻铸铁可以锻造成型的。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "377. 奥氏体的塑性高于珠光体，所以钢要加热到奥氏体后进行锻造成型。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "378. 钢材随着冷变形量的增加，强度、硬度会增加，而塑性、韧性降低。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "A"
    },
    {
        "question": "379. 调质处理就是淬火加中温回火。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "380. 车床的主运动和进给运动是由两台电动机分别带动的。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "381. 车床夹具中能自动定心的是四爪卡盘。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "382. 刀具后角是主后刀面与基面间的夹角，在正交面上测量，",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "383. 主偏刀是指主偏角大于或等于90°的车刀。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "A"
    },
    {
        "question": "384. 氧化铝砂轮可以用来刃磨硬质合金车刀。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "385. 在车床上用切断刀切断工件时，切断速度是始终不变的。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "386. 车床主轴的反转是通过电动机反转实现的。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "A"
    },
    {
        "question": "387. 直头车刀的形状简单，主要用来粗车外圆。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "388. 三爪卡盘的个爪可以单独移动吗？",
        "options": [
            "A. 可以",
            "B. 不可以",
            "C. 有时可以"
        ],
        "answer": "B"
    },
    {
        "question": "389. 车外圆时带动溜板箱作进给运动的是：",
        "options": [
            "A. 光杠",
            "B. 丝杠",
            "C. 螺杠"
        ],
        "answer": "A"
    },
    {
        "question": "390. 车削钢件时铁屑缠绕挡住了视线，想看清车刀和工件，应该怎么做？",
        "options": [
            "A. 停车把切屑除去",
            "B. 不停车戴上手套后将铁屑除去",
            "C. 不停车用铁钩将铁屑除去"
        ],
        "answer": "C"
    },
    {
        "question": "391. 适合车床上加工的平面是什么样的平面？",
        "options": [
            "A. 回转面",
            "B. 轴上和圆盘上的端面",
            "C. 一般平面"
        ],
        "answer": "A"
    },
    {
        "question": "392. 车刀刃倾角选取值一般为：",
        "options": [
            "A. 5°~10°",
            "B. 10°~5°",
            "C. 15°~20°"
        ],
        "answer": "B"
    },
    {
        "question": "393. 高速钢车刀的红硬性温度为：",
        "options": [
            "A. 300°~400°C",
            "B. 500°~600°C",
            "C. 800°~1000°C"
        ],
        "answer": "B"
    },
    {
        "question": "394. 车外圆时的切削深度是指：",
        "options": [
            "A. 待加工表面与已加工表面的直径差",
            "B. 切出切削厚度",
            "C. 待加工表面与已加工表面的直径差的一半"
        ],
        "answer": "C"
    },
    {
        "question": "395. 车刀的前刀面与主后刀面的交线称为：",
        "options": [
            "A. 副切削刃",
            "B. 主切削刃",
            "C. 刀尖"
        ],
        "answer": "B"
    },
    {
        "question": "396. 不能戴下列哪些物品开车床？",
        "options": [
            "A. 帽",
            "B. 手套",
            "C. 眼镜"
        ],
        "answer": "B"
    },
    {
        "question": "397. 车削工件时，切屑流过的表面是：",
        "options": [
            "A. 主后刀面",
            "B. 副后刀面",
            "C. 前刀面"
        ],
        "answer": "C"
    },
    {
        "question": "398. 车削较短圆锥时，如锥角为α，则车刀切削刃与主轴轴线的夹角就为：",
        "options": [
            "A. α",
            "B. α/2",
            "C. α/3"
        ],
        "answer": "B"
    },
    {
        "question": "399. 尾座只能用于安装后顶尖以支持工件，而不能安装钻头。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "400. 卧式铣床的主轴是如何设置的？",
        "options": [
            "A. 垂直",
            "B. 水平",
            "C. 与水平成45°"
        ],
        "answer": "B"
    },
    {
        "question": "401. 铣床的主运动是：",
        "options": [
            "A. 铣刀的旋转运动",
            "B. 工作台带工件的上下运动",
            "C. 工作台带工件的前后运动"
        ],
        "answer": "A"
    },
    {
        "question": "402. 卧式铣床选用：",
        "options": [
            "A. 带直柄的铣刀",
            "B. 带孔的铣刀",
            "C. 带锥柄的铣刀"
        ],
        "answer": "B"
    },
    {
        "question": "403. 铣床不能加工：",
        "options": [
            "A. 燕尾槽",
            "B. 斜面",
            "C. 外圆柱面"
        ],
        "answer": "C"
    },
    {
        "question": "404. 工件表面有硬皮时，应采用：",
        "options": [
            "A. 端铣",
            "B. 顺铣",
            "C. 逆铣"
        ],
        "answer": "C"
    },
    {
        "question": "405. 顺铣时会引起打刀现象，这是由于___造成。",
        "options": [
            "A. 进给机构的齿轮副有间隙",
            "B. 进给机构的丝杆与螺母有间隙",
            "C. 进给机构的蜗杆蜗轮有间隙"
        ],
        "answer": "B"
    },
    {
        "question": "406. 在牛头创床进行刨削的主运动是：",
        "options": [
            "A. 工作台的间歇进给",
            "B. 滑枕的往复移动",
            "C. 工作台的上下移动"
        ],
        "answer": "B"
    },
    {
        "question": "407. 砂轮的硬度是指：",
        "options": [
            "A. 砂轮磨料的硬度",
            "B. 砂轮磨粒的脱落难易程度",
            "C. 结合剂的强度"
        ],
        "answer": "B"
    },
    {
        "question": "408. 下面的___不是铣床附件。",
        "options": [
            "A. 中心架",
            "B. 平口钳",
            "C. 分度头"
        ],
        "answer": "A"
    },
    {
        "question": "409. 组成砂轮的三个基本要素是：",
        "options": [
            "A. 磨料、结合剂、孔隙",
            "B. 磨料粒度、砂轮硬度、形状尺寸",
            "C. 磨料硬度、结合剂硬度、砂轮硬度"
        ],
        "answer": "A"
    },
    {
        "question": "410. 手锯条用什么材料制成？",
        "options": [
            "A. 碳素结构钢",
            "B. 碳素工具钢",
            "C. 高速钢"
        ],
        "answer": "B"
    },
    {
        "question": "411. 锉刀往后返回时应注意什么？",
        "options": [
            "A. 提起锉刀",
            "B. 和前进时一样均匀加压",
            "C. 不紧压工件"
        ],
        "answer": "A"
    },
    {
        "question": "412. 孔快要钻穿时，进给速度应怎样控制？",
        "options": [
            "A. 保持匀速",
            "B. 减慢",
            "C. 加快"
        ],
        "answer": "B"
    },
    {
        "question": "413. 锉削铜，铝等软金属宜用哪种锉刀？",
        "options": [
            "A. 细齿锉",
            "B. 粗齿锉",
            "C. 中齿锉"
        ],
        "answer": "B"
    },
    {
        "question": "414. 锯片的安装锯齿向前，锯齿向后，锯齿方向无要求",
        "options": [
            "A. 锯齿向前",
            "B. 锯齿向后",
            "C. 锯齿方向无要求"
        ],
        "answer": "A"
    },
    {
        "question": "415. 钳工在圆杆上加工出外螺纹，应用哪种方法？",
        "options": [
            "A. 板牙",
            "B. 丝锥",
            "C. 外螺纹刀"
        ],
        "answer": "A"
    },
    {
        "question": "416. 如何才能锉出平整表面？",
        "options": [
            "A. 锉削时两手施于锉刀的力应保持锉刀在水平面上运动",
            "B. 两手施于锉刀的力应始终不变",
            "C. 右手握柄施力，左手压锉不能用力"
        ],
        "answer": "A"
    },
    {
        "question": "417. 实习中使用的游标卡尺的测量精度为：",
        "options": [
            "A. 0.01mm",
            "B. 0.02mm",
            "C. 0.1mm"
        ],
        "answer": "B"
    },
    {
        "question": "418. 齿轮和轴的联接方式通常采用：",
        "options": [
            "A. 键联接",
            "B. 销联接",
            "C. 螺纹联接"
        ],
        "answer": "A"
    },
    {
        "question": "419. 下列造型方法中，适合于机器造型的是：",
        "options": [
            "A. 二箱造型",
            "B. 三箱造型",
            "C. 挖砂造型"
        ],
        "answer": "A"
    },
    {
        "question": "420. 如果铸件形状比较复杂，不宜用分模造型，而应用整模造型，对吗？",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "421. 铸件上重要加工面在铸型中最好应处于什么样的浇注位置？",
        "options": [
            "A. 最上部",
            "B. 最上部或侧面",
            "C. 侧面或底面"
        ],
        "answer": "B"
    },
    {
        "question": "422. 型砂的透气性不足会产生什么缺陷？",
        "options": [
            "A. 气孔",
            "B. 夹砂",
            "C. 裂纹"
        ],
        "answer": "A"
    },
    {
        "question": "423. 制模型时，在要铸出孔的地方，应加什么？",
        "options": [
            "A. 收缩量",
            "B. 型芯头",
            "C. 加工余量"
        ],
        "answer": "B"
    },
    {
        "question": "424. 铸件的分模面即分型面，对吗？",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "B"
    },
    {
        "question": "425. 通气孔必须扎到与型腔相通，对吗？",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "426. 浇不足缺陷产生的主要原因是：",
        "options": [
            "A. 液体金属的收缩量太大",
            "B. 型砂的退让性差",
            "C. 液体金属的流动性差或液体金属的量不够"
        ],
        "answer": "C"
    },
    {
        "question": "427. 铸铝的浇注温度是：",
        "options": [
            "A. 500多度",
            "B. 700多度",
            "C. 900多度"
        ],
        "answer": "C"
    },
    {
        "question": "428. 最常用的铸造合金是什么？",
        "options": [
            "A. 铸钢",
            "B. 铸铝",
            "C. 灰口铸铁"
        ],
        "answer": "C"
    },
    {
        "question": "429. 型腔中跌落了一些松砂，应怎么办？",
        "options": [
            "A. 用嘴吹",
            "B. 用砂椿楠纸",
            "C. 用毛笔蘸水带走"
        ],
        "answer": "C"
    },
    {
        "question": "430. 什么是错箱？",
        "options": [
            "A. 砂箱尺寸选错了",
            "B. 放错了另一个上箱",
            "C. 铸件上、下面部分在分型面处错开"
        ],
        "answer": "C"
    },
    {
        "question": "431. 铸件的形状和模型的形状相似，对吗？",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "A"
    },
    {
        "question": "432. 有时型砂中加入少量煤粉，其主要目的是：",
        "options": [
            "A. 提高型砂的透气性",
            "B. 提高型砂的强度",
            "C. 减少粘砂的倾向"
        ],
        "answer": "C"
    },
    {
        "question": "433. 大批量生产手轮毛坏应选用的工艺方法是：",
        "options": [
            "A. 锻造",
            "B. 铸造",
            "C. 焊接"
        ],
        "answer": "B"
    },
    {
        "question": "434. 制模型时，在要铸出孔的地方，应加什么？",
        "options": [
            "A. 收缩量",
            "B. 型芯头",
            "C. 加工余量"
        ],
        "answer": "B"
    },
    {
        "question": "435. 桩砂用的平椿，在未用到时，应怎样放置？",
        "options": [
            "A. 垂直放",
            "B. 横放",
            "C. 随便放"
        ],
        "answer": "A"
    },
    {
        "question": "436. 型芯的主要作用是：",
        "options": [
            "A. 增加铸件的强度",
            "B. 增加铸件的透气性",
            "C. 形成铸件的内腔"
        ],
        "answer": "C"
    },
    {
        "question": "437. 通气孔必须扎到与型腔相通，对吗？",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "438. 铸件整个都在同一砂箱内，好吗？",
        "options": [
            "A. 好",
            "B. 不好",
            "C. 看情况而定"
        ],
        "answer": "A"
    },
    {
        "question": "439. 铸件上的拔模斜度应加在哪些面上最好？",
        "options": [
            "A. 各个面上",
            "B. 与分型面平行的平面",
            "C. 与分型面垂直的平面"
        ],
        "answer": "C"
    },
    {
        "question": "440. 铸件表面上有局部凹陷的地方，这是什么原因造成的？",
        "options": [
            "A. 浇不足",
            "B. 收缩",
            "C. 铸型开裂"
        ],
        "answer": "B"
    },
    {
        "question": "441. 用什么方法可把三箱造型改为两箱造型？",
        "options": [
            "A. 加外型芯",
            "B. 加高下箱",
            "C. 修改浇注系统"
        ],
        "answer": "A"
    },
    {
        "question": "442. 内浇口最好开设在铸件的重要部位，对吗？",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "443. 通气孔必须扎到与型腔相通，对吗？",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "444. 型砂的耐火性不足会产生什么缺陷？",
        "options": [
            "A. 气孔",
            "B. 粘砂",
            "C. 裂纹"
        ],
        "answer": "B"
    },
    {
        "question": "445. 空气锤的公称规格，是指其最大打击力而言。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "446. 承受动载荷的工件通常需要锻压制坏。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "A"
    },
    {
        "question": "447. 锻造加热时，温度越高越好。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "448. 过烧的锻件还可通过热处理的方法进行挽救。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "449. 胎模锻是在自出锻的设备上进行的。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "A"
    },
    {
        "question": "450. 下列工件中，适合锻造制坏的是：",
        "options": [
            "A. 变速箱箱体",
            "B. 起重机吊钩",
            "C. 车床床身"
        ],
        "answer": "B"
    },
    {
        "question": "451. 锻造加热的目的是：",
        "options": [
            "A. 提高塑性",
            "B. 提高强度",
            "C. 提高韧性"
        ],
        "answer": "A"
    },
    {
        "question": "452. 水轮机主轴应采取的锻造方法是：",
        "options": [
            "A. 模锻",
            "B. 自由锻",
            "C. 胎模锻"
        ],
        "answer": "B"
    },
    {
        "question": "453. 锻造加热时，使工件内部晶粒粗化，塑性下降，这一缺陷称为：",
        "options": [
            "A. 过热",
            "B. 过烧",
            "C. 脱碳"
        ],
        "answer": "A"
    },
    {
        "question": "454. 内孔和外缘同轴度要求较高的冲压件，最好采用：",
        "options": [
            "A. 复合冲模",
            "B. 简单冲模",
            "C. 连续冲模"
        ],
        "answer": "C"
    },
    {
        "question": "455. 电阻焊的特点之一是：",
        "options": [
            "A. 低电压, 大电流",
            "B. 高电压, 大电流",
            "C. 高电压, 低电流"
        ],
        "answer": "A"
    },
    {
        "question": "456. 焊条药皮的作用之一是：",
        "options": [
            "A. 向焊缝加有用合金元素",
            "B. 增加焊接温度",
            "C. 增加焊接电流"
        ],
        "answer": "A"
    },
    {
        "question": "457. 埋弧自动焊的主要特点之一是：",
        "options": [
            "A. 电弧电压较高",
            "B. 焊接工艺性能好",
            "C. 一般只适合于平直焊缝的焊接"
        ],
        "answer": "C"
    },
    {
        "question": "458. 手弧焊时，焊接电流确定的主要依据是：",
        "options": [
            "A. 焊丝的直径",
            "B. 焊逢的宽度",
            "C. 焊接位置"
        ],
        "answer": "A"
    },
    {
        "question": "459. 焊接电弧的实质是：",
        "options": [
            "A. 电流流过两个电极时产生的高温",
            "B. 电极间气体电离导电产生的高温",
            "C. 药皮溶化燃烧时产生的高温"
        ],
        "answer": "B"
    },
    {
        "question": "460. 用直流电弧焊正接法施焊时，焊条应接什么极：",
        "options": [
            "A. 正极",
            "B. 正负极均可",
            "C. 负极"
        ],
        "answer": "C"
    },
    {
        "question": "461. 气焊炬关闭的顺序：",
        "options": [
            "A. 先关乙炔，后关氧气",
            "B. 先关氧气，后关乙炔",
            "C. 乙炔和氧气同时关"
        ],
        "answer": "A"
    },
    {
        "question": "462. 气焊时，把氧气引出使用时要连接：",
        "options": [
            "A. 回火保险器",
            "B. 氧气发生器",
            "C. 减压器"
        ],
        "answer": "C"
    },
    {
        "question": "463. 焊接结构中，最宜多用的是哪种接头：",
        "options": [
            "A. 角接",
            "B. 对接",
            "C. 搭接"
        ],
        "answer": "B"
    },
    {
        "question": "464. 最适合于焊接的钢材是：",
        "options": [
            "A. 高碳钢",
            "B. 低碳钢",
            "C. 高合金钢"
        ],
        "answer": "B"
    },
    {
        "question": "465. T10钢的平均含碳量为0.1%：",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "466. 可锻铸铁可以锻造成型的。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "467. 调质处理就是淬火加中温回火，",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "468. 中碳钢的热处理工艺通常采用调质处理获得良好的综合机械性能。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "A"
    },
    {
        "question": "469. 钢材随着冷变形量的增加，强度、硬度会增加，而塑性、韧性降低。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "A"
    },
    {
        "question": "470. 在车床上用切断刀切断工件时，切断速度是始终不变的。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "471. 车床主轴的反转是通过电动机反转实现的。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "B"
    },
    {
        "question": "472. 直头车刀的形状简单，主要用来粗车外圆。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "B"
    },
    {
        "question": "473. 三爪卡盘的一个爪可以单独移动吗？",
        "options": [
            "A. 可以",
            "B. 不可以",
            "C. 有时可以"
        ],
        "answer": "B"
    },
    {
        "question": "474. 车外圆时带动溜板箱作进给运动的是：",
        "options": [
            "A. 光杠",
            "B. 丝杠",
            "C. 螺杠"
        ],
        "answer": "A"
    },
    {
        "question": "475. 车床的主运动和进给运动是由两台电动机分别带动的。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "476. 车床夹具中能自动定心的是四爪卡盘。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "477. 刀具后角是主后刀面与基面间的夹角，在正交面上测量。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "478. 主偏刀是指主偏角大于或等于90°的车刀。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "A"
    },
    {
        "question": "479. 氧化铝砂轮可以用来刃磨硬质合金车刀。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "480. 车外圆时的切削深度是指：",
        "options": [
            "A. 待加工表面与已加工表面的直径差",
            "B. 切出切削厚度",
            "C. 待加工表面与已加工表面的直径差的一半"
        ],
        "answer": "C"
    },
    {
        "question": "481. 车刀的前刀面与主后刀面的交线称为：",
        "options": [
            "A. 副切削刃",
            "B. 主切削刃",
            "C. 刀尖"
        ],
        "answer": "B"
    },
    {
        "question": "482. 不能戴下列哪些物品开车床？",
        "options": [
            "A. 帽",
            "B. 手套",
            "C. 眼镜"
        ],
        "answer": "B"
    },
    {
        "question": "483. 车削工件时，切屑流过的表面是：",
        "options": [
            "A. 主后刀面",
            "B. 副后刀面",
            "C. 前刀面"
        ],
        "answer": "C"
    },
    {
        "question": "484. 车削较短圆锥时，如锥角为α，则车刀切削刃与主轴轴线的夹角就为：",
        "options": [
            "A. α",
            "B. α/2",
            "C. α/3"
        ],
        "answer": "A"
    },
    {
        "question": "485. 尾座只能用于安装后顶尖以支持工件，而不能安装钻头。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    },
    {
        "question": "486. 车削钢件时铁屑缠绕挡住了视线，想看清车刀和工件，应该怎么做？",
        "options": [
            "A. 停车把切屑除去",
            "B. 不停车戴上手套后将铁屑除去",
            "C. 不停车用铁钩将铁屑除去"
        ],
        "answer": "A"
    },
    {
        "question": "487. 适合车床上加工的平面是什么样的平面？",
        "options": [
            "A. 回转面",
            "B. 轴上和圆盘上的端面",
            "C. 一般平面"
        ],
        "answer": "B"
    },
    {
        "question": "488. 车刀刃倾角选取值一般为：",
        "options": [
            "A. 5°~10°",
            "B. -10°~5°",
            "C. 15°~20°"
        ],
        "answer": "B"
    },
    {
        "question": "489. 可作车刀的材料是：",
        "options": [
            "A. 铸铁",
            "B. 碳素结构钢",
            "C. 高速钢"
        ],
        "answer": "C"
    },
    {
        "question": "490. 下面的不是铣床附件。",
        "options": [
            "A. 中心架",
            "B. 平口钳",
            "C. 分度头"
        ],
        "answer": "A"
    },
    {
        "question": "491. 铣床的主运动是：",
        "options": [
            "A. 铣刀的旋转运动",
            "B. 工作台带工件的上下运动",
            "C. 工作台带工件的前后运动"
        ],
        "answer": "A"
    },
    {
        "question": "492. 卧式铣床选用：",
        "options": [
            "A. 带直柄的铣刀",
            "B. 带孔的铣刀",
            "C. 带锥柄的铣刀"
        ],
        "answer": "B"
    },
    {
        "question": "493. 铣床不能加工：",
        "options": [
            "A. 燕尾槽",
            "B. 斜面",
            "C. 外圆柱面"
        ],
        "answer": "C"
    },
    {
        "question": "494. 工件表面有硬皮时，应采用：",
        "options": [
            "A. 端铣",
            "B. 顺铣",
            "C. 逆铣"
        ],
        "answer": "C"
    },
    {
        "question": "495. 顺铣时会引起打刀现象，这是由于造成。",
        "options": [
            "A. 进给机构的齿轮副有间隙",
            "B. 进给机构的丝杆与螺母有间隙",
            "C. 进给机构的蜗杆蜗轮有间隙"
        ],
        "answer": "B"
    },
    {
        "question": "496. 在牛头刨床进行刨削的主运动是：",
        "options": [
            "A. 工作台的间歇进给",
            "B. 滑枕的往复移动",
            "C. 工作台的上下移动"
        ],
        "answer": "B"
    },
    {
        "question": "497. 砂轮的硬度是指：",
        "options": [
            "A. 砂轮磨料的硬度",
            "B. 砂轮磨粒的脱落难易程度",
            "C. 结合剂的强度"
        ],
        "answer": "B"
    },
    {
        "question": "498. 组成砂轮的三个基本要素是：",
        "options": [
            "A. 磨料、结合剂、孔隙",
            "B. 磨料粒度、砂轮硬度、形状尺寸",
            "C. 磨料硬度、结合剂硬度、砂轮硬度"
        ],
        "answer": "A"
    },
    {
        "question": "499. 手锯条用什么材料制成？",
        "options": [
            "A. 碳素结构钢",
            "B. 碳素工具钢",
            "C. 高速钢"
        ],
        "answer": "B"
    },
    {
        "question": "500. 锉刀往后返回时应注意什么？",
        "options": [
            "A. 提起锉刀",
            "B. 和前稚时一样均匀加压",
            "C. 不紧压工件"
        ],
        "answer": "C"
    },
    {
        "question": "501. 孔快要钻穿时，进给速度应怎样控制？",
        "options": [
            "A. 保持匀速",
            "B. 减慢",
            "C. 加快"
        ],
        "answer": "B"
    },
    {
        "question": "502. 钳工的划线基准通常与设计基准一致",
        "options": [
            "A. 对",
            "B. 不对",
            "C. 有时对"
        ],
        "answer": "A"
    },
    {
        "question": "503. 某一同学在攻丝时，攻了一段时间发现全无螺纹，但丝锥已深入工件内，什么原因？",
        "options": [
            "A. 丝锥与工件不垂直，攻丝时摇晃造成",
            "B. 孔径与丝锥外径一样大",
            "C. 丝锥没有润滑"
        ],
        "answer": "B"
    },
    {
        "question": "504. 手锯条用什么材料制成？",
        "options": [
            "A. 碳素结构钢",
            "B. 碳素工具钢",
            "C. 高速钢"
        ],
        "answer": "B"
    },
    {
        "question": "505. 锉刀往后返回时应注意什么？",
        "options": [
            "A. 提起锉刀",
            "B. 和前稚时一样均匀加压",
            "C. 不紧压工件"
        ],
        "answer": "C"
    },
    {
        "question": "506. 孔快要钻穿时，进给速度应怎样控制？",
        "options": [
            "A. 保持匀速",
            "B. 减慢",
            "C. 加快"
        ],
        "answer": "B"
    },
    {
        "question": "507. 如何才能锉出平整表面？",
        "options": [
            "A. 锉削时两手施于锉刀的力应保持锉刀在水平面上运动",
            "B. 两手施于锉刀的力应始终不变",
            "C. 右手握柄施力，左手压锉不能用力"
        ],
        "answer": "A"
    },
    {
        "question": "508. 实习中使用的游标卡尺的测量精度为：",
        "options": [
            "A. 0.01mm",
            "B. 0.02mm",
            "C. 0.1mm"
        ],
        "answer": "B"
    },
    {
        "question": "509. 工件加工表面质量的主要指标是表面粗糙度。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "A"
    },
    {
        "question": "510. 检查工件形状和位置误差可使用下列哪些量具？",
        "options": [
            "A. 百分尺",
            "B. 百分表",
            "C. 卡尺"
        ],
        "answer": "B"
    },
    {
        "question": "511. 齿轮和轴的联接方式通常采用：",
        "options": [
            "A. 键联接",
            "B. 销联接",
            "C. 螺纹联接"
        ],
        "answer": "A"
    },
    {
        "question": "512. 工件装配时可用铁捶直接敲击工件表面直到压入。",
        "options": [
            "A. 对",
            "B. 有时对",
            "C. 不对"
        ],
        "answer": "C"
    }

]

root = ttk.Window()
QuizApp(root, questions)
root.mainloop()
