if __name__ == "__main__":
    from _config import get_settings_config
    from csvmanager import CSVManager
else:
    from .csvmanager import CSVManager
    from ._config import get_settings_config

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class BarGraphManager:
    def __init__(self):
        csvmanager = CSVManager()
        dataset = csvmanager.list_od_from_csv()
        self.ages = []
        self.dataset = dataset
        for entry in dataset:
            self.ages.append(int(entry["AGE"]))
        self.fig = self.bar_graph_age_vs_Case()
        self.fig1 = self.bar_graph_case_gender_wise()
        self.layout = [
            [
                sg.TabGroup(
                    [
                        [
                            sg.Tab(
                                "Age vs Case",
                                self.bar_graph_age_vs_Case,
                                element_justification="center",
                                key="age-vs-case",
                            ),
                            sg.Tab(
                                "Case vs Gender",
                                self.layout_bar_graph_case_gender_wise,
                                element_justification="center",
                                key="case-vs-gender",
                            ),
                        ]
                    ],
                    enable_events=True,
                    key="bargraph_tab",
                )
            ]
        ]

    def draw_figure(self, canvas, figure, loc=(0, 0)):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=False)
        return figure_canvas_agg

    def bar_graph_age_vs_Case(self):
        v1, v2, v3, v4, v5 = 0, 0, 0, 0, 0
        for i in range(len(self.ages)):
            a = self.ages[i]
            if a >= 1 and a <= 20:
                v1 += 1
            elif a >= 21 and a <= 40:
                v2 += 1
            elif a >= 41 and a <= 60:
                v3 += 1
            elif a >= 61 and a <= 80:
                v4 += 1
            elif a >= 81:
                v5 += 1
        values_to_plot = (v1, v2, v3, v4, v5)
        ind = np.arange(len(values_to_plot))
        width = 0.4

        p1 = plt.bar(ind, values_to_plot, width)

        plt.ylabel("NO.OF.CASES")
        plt.title("AGE VS CASES")
        plt.xticks(ind, ("1-20", "21-40", "41-60", "61-80", "81-100"))
        plt.yticks(np.arange(0, 31, 5))
        plt.legend((p1[0],), ("AGE LIMIT",))

        fig = plt.gcf()
        
        figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds

        self.bar_graph_age_vs_Case = [
            [sg.Text("Age vs Case", font="serif " + get_settings_config()["fontsize"])],
            [sg.Canvas(size=(figure_w, figure_h), key="-CANVAS-")],
        ]
        return fig

    def bar_graph_case_gender_wise(self):
        dataset = self.dataset
        m1, m2, m3, m4, m5 = 0, 0, 0, 0, 0
        f1, f2, f3, f4, f5 = 0, 0, 0, 0, 0
        for i in range(len(dataset)):
            if dataset[i]["GENDER"] == "MALE":
                a = int(dataset[i]["AGE"])
                if a >= 1 and a <= 20:
                    m1 += 1
                elif a >= 21 and a <= 40:
                    m2 += 1
                elif a >= 41 and a <= 60:
                    m3 += 1
                elif a >= 61 and a <= 80:
                    m4 += 1
                elif a >= 81:
                    m5 += 1
            else:
                a = int(dataset[i]["AGE"])
                if a >= 1 and a <= 20:
                    f1 += 1
                elif a >= 21 and a <= 40:
                    f2 += 1
                elif a >= 41 and a <= 60:
                    f3 += 1
                elif a >= 61 and a <= 80:
                    f4 += 1
                elif a >= 81:
                    f5 += 1
        barWidth = 0.25
        bars1 = [m1, m2, m3, m4, m5]
        bars2 = [f1, f2, f3, f4, f5]
        r1 = np.arange(len(bars1))
        r2 = [x + barWidth for x in r1]
        p1 = plt.bar(
            r1, bars1, color="#7f6d5f", width=barWidth, edgecolor="white", label="MALE"
        )
        p2 = plt.bar(
            r2,
            bars2,
            color="#557f2d",
            width=barWidth,
            edgecolor="white",
            label="FEMALE",
        )
        plt.xlabel("AGE", fontweight="bold")
        plt.xticks(
            [r + barWidth for r in range(len(bars1))],
            ["1-20", "21-40", "41-60", "61-80", "81-100"],
        )
        plt.legend([p1[0], p2[0]], ("Males", "Female"))
        fig = plt.gcf()
        #plt.show()
        figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds

        self.layout_bar_graph_case_gender_wise = [
            [
                sg.Text(
                    "Case Gender Wise", font="serif" + get_settings_config()["fontsize"]
                )
            ],
            [sg.Canvas(size=(figure_w, figure_h), key="-GENDER_CANVAS-")],
        ]
        return fig


if __name__ == "__main__":
    a = BarGraphManager()
    window = sg.Window(
        "Demo Application - Embedding Matplotlib In PySimpleGUI",
        a.layout,
        force_toplevel=True,
        finalize=True,
    )
    fig_photo = a.draw_figure(window["-CANVAS-"].TKCanvas, a.fig)
    event, values = window.read()
    window.close()
