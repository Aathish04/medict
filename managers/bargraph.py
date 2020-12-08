import tkinter as Tk

import matplotlib as mpl
import matplotlib.backends.tkagg as tkagg
import numpy as np
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

if __name__ == "__main__":
    from _config import get_settings_config
    from csvmanager import CSVManager
else:
    from ._config import get_settings_config
    from .csvmanager import CSVManager


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
        """Draw a matplotlib figure onto a Tk canvas

        loc: location of top-left corner of figure on canvas in pixels.

        """
        canvas.pack()
        figure_canvas_agg = FigureCanvasTkAgg(figure, master=canvas)
        figure_canvas_agg.draw()
        figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
        figure_w, figure_h = int(figure_w), int(figure_h)
        photo = Tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)
        canvas.create_image(loc[0] + figure_w / 2, loc[1] + figure_h / 2, image=photo)
        tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)
        # Return a handle which contains a reference to the photo object
        # which must be kept live or else the picture disappears
        return photo

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
        width = 0.5
        fig = mpl.figure.Figure()
        subplt = fig.add_subplot(1, 1, 1)
        p1 = subplt.bar(ind, values_to_plot, width)
        subplt.set_title(
            "Age vs Case", fontdict={"fontsize": get_settings_config()["fontsize"]}
        )
        subplt.set_ylabel("NO.OF.CASES")
        subplt.set_xlabel("AGE")
        subplt.set_xticks(ind)
        subplt.set_xticklabels(("1-20", "21-40", "41-60", "61-80", "81-100"))
        subplt.set_yticks(np.arange(0, 31, 5))
        subplt.legend((p1[0],), ("AGE LIMIT",))
        fig.align_labels(subplt)
        figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds
        self.bar_graph_age_vs_Case = [
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
        fig = mpl.figure.Figure()
        plt = fig.add_subplot(1, 1, 1)
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
        plt.set_title(
            "AGE vs Gender", fontdict={"fontsize": get_settings_config()["fontsize"]}
        )
        plt.set_xlabel("AGE")
        plt.set_xticks([r + barWidth for r in range(len(bars1))])
        plt.set_xticklabels(["1-20", "21-40", "41-60", "61-80", "81-100"])
        plt.legend([p1[0], p2[0]], ("Males", "Female"))

        figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds

        self.layout_bar_graph_case_gender_wise = [
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
