import pandas as pd
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox

from Package.charts.tables import A2, D3, D4, A3, B3, B4, d2
import numpy as np
import statistics
from math import gamma

def CpCpkDisplay(USL, LSL, Data, Sample_Size):
    SubGroupList = [ ]
    RList = [ ]

    if len(Data) != 0 and len(Data) >= Sample_Size:
        try:
            R = int(len(Data) / Sample_Size)
            No = 0
            while len(SubGroupList) != R and len(SubGroupList) <= R:
                Reading = [ ]
                for i in range(Sample_Size):
                    Reading.append(Data[ No ])
                    No += 1
                SubGroupList.append(np.average(Reading))
                RList.append(max(Reading) - min(Reading))

            stdWi = np.average(RList) / d2[ Sample_Size ]
            m = np.average(SubGroupList)
            Cp = (USL - LSL) / (6 * stdWi)
            CPU = (m - LSL) / (3 * stdWi)
            CPL = (USL - m) / (3 * stdWi)
            Cpk = min(CPL, CPU)
            z = min((USL - m) / stdWi, (m - LSL) / stdWi)

            ReadingsArrary = np.array(Data)
            Pp = (USL - LSL) / (6 * statistics.stdev(Data))
            Ppu = (USL - ReadingsArrary.mean()) / (3 * statistics.stdev(Data))
            Ppl = (ReadingsArrary.mean() - LSL) / (3 * statistics.stdev(Data))
            Ppk = min(Ppl, Ppu)

            num_samples = len(ReadingsArrary)
            sample_mean = np.mean(SubGroupList)
            sample_std_within = stdWi
            sample_std_overall = ReadingsArrary.std()

            Cpcpk = {"Cp": round(Cp, 4), "Cpl": round(CPL, 4), "Cpu": round(CPU, 4), "Cpk": round(Cpk, 4),
                     "Std": round(sample_std_within, 4)}

            PpPpk = {"Pp": round(Pp, 4), "Ppl": round(Ppl, 4), "Ppu": round(Ppu, 4), "Ppk": round(Ppk, 4),
                     "Std": round(sample_std_overall, 4)}

            return [ Cpcpk, PpPpk ]

        except ZeroDivisionError:
            print("CpCpkDisplay ERROR * There is insufficient variation. No calculations can be done.")

        except Exception as Error:
            print(__file__, "Cp_Cpk_Chart :", Error)

def CpCpk(USL, LSL, Data, Sample_Size):  # return (Cpcpk, PpPpk, statistics, Performance)

    SubGroupList = [ ]
    RList = [ ]
    if len(Data) != 0 and len(Data) >= Sample_Size:
        try:
            R = int(len(Data) / Sample_Size)
            No = 0
            while len(SubGroupList) != R and len(SubGroupList) <= R:
                Reading = [ ]
                for i in range(Sample_Size):
                    Reading.append(Data[ No ])
                    No += 1
                SubGroupList.append(np.average(Reading))
                RList.append(max(Reading) - min(Reading))

            stdWi = np.average(RList) / d2[ Sample_Size ]
            print(stdWi)
            m = np.average(SubGroupList)
            Cp = (USL - LSL) / (6 * stdWi)
            CPU = (m - LSL) / (3 * stdWi)
            CPL = (USL - m) / (3 * stdWi)
            Cpk = min(CPL, CPU)
            z = min((USL - m) / stdWi, (m - LSL) / stdWi)

            ReadingsArrary = np.array(Data)
            Pp = (USL - LSL) / (6 * statistics.stdev(Data))
            Ppu = (USL - ReadingsArrary.mean()) / (3 * statistics.stdev(Data))
            Ppl = (ReadingsArrary.mean() - LSL) / (3 * statistics.stdev(Data))
            Ppk = min(Ppl, Ppu)

            num_samples = len(ReadingsArrary)
            sample_mean = np.mean(SubGroupList)
            sample_std_within = stdWi
            sample_std_overall = ReadingsArrary.std()
            sample_max = max(Data)
            sample_min = min(Data)
            sample_median = np.median(ReadingsArrary)

            ReadingsAvg_Arrary = np.array(SubGroupList)

            ov_pct_below_LSL = len(ReadingsArrary[ ReadingsArrary < LSL ]) / len(ReadingsArrary) * 1000000
            ov_pct_below_LSL_Def = len(ReadingsArrary[ ReadingsArrary < LSL ]) / len(ReadingsArrary) * 100
            ov_pct_above_USL = len(ReadingsArrary[ ReadingsArrary > USL ]) / len(ReadingsArrary) * 1000000
            ov_pct_above_USL_Def = len(ReadingsArrary[ ReadingsArrary > USL ]) / len(ReadingsArrary) * 100
            ov_total = ov_pct_below_LSL + ov_pct_above_USL

            wi_ppm_below_LSL = len(ReadingsAvg_Arrary[ ReadingsAvg_Arrary < LSL ]) / len(ReadingsAvg_Arrary) * 1000000
            wi_ppm_below_LSL_Def = len(ReadingsAvg_Arrary[ ReadingsAvg_Arrary < LSL ]) / len(ReadingsAvg_Arrary) * 100
            wi_ppm_above_USL = len(ReadingsAvg_Arrary[ ReadingsAvg_Arrary > USL ]) / len(ReadingsAvg_Arrary) * 1000000
            wi_ppm_above_USL_Def = len(ReadingsAvg_Arrary[ ReadingsAvg_Arrary > USL ]) / len(ReadingsAvg_Arrary) * 100
            wi_total = wi_ppm_below_LSL + wi_ppm_above_USL

            Cpcpk = {"Std": sample_std_within, "Mean": sample_mean, "Cp": round(Cp, 3), "Cpl": round(CPL, 3),
                     "Cpu": round(CPU, 3), "Cpk": round(Cpk, 3), "Z": round(z, 3)}

            PpPpk = {"Std": sample_std_overall, "Pp": round(Pp, 3), "Ppl": round(Ppl, 3), "Ppu": round(Ppu, 3),
                     "Ppk": round(Ppk, 3)}

            statistics = {"Sample": num_samples, "Mean": sample_mean, "Std Within": sample_std_within,
                          "Std Overall": sample_std_overall, "Max": sample_max, "Min": sample_min,
                          "Median": sample_median}

            Performance = {"PPM > LSL": [ ov_pct_below_LSL, wi_ppm_below_LSL ],
                           "PPM > USL": [ ov_pct_above_USL, wi_ppm_above_USL ], "TOTAl PPM": [ wi_total, ov_total ]}

            return (Cpcpk, PpPpk, statistics, Performance)

        except ZeroDivisionError:
            showDialog('* ERROR * There is insufficient variation.\n No calculations can be done.')

            print("* ERROR * There is insufficient variation. No calculations can be done.")

        except Exception as Error:
            print(__file__, "Cp_Cpk_Chart :", Error)

def CpCpkForGraph(USL, LSL, Data, Sample_Size):  # return (Cpcpk, PpPpk, statistics, Performance)

    SubGroupList = [ ]
    RList = [ ]
    if len(Data) != 0 and len(Data) >= Sample_Size:
        try:
            R = int(len(Data) / Sample_Size)
            No = 0
            while len(SubGroupList) != R and len(SubGroupList) <= R:
                Reading = [ ]
                for i in range(Sample_Size):
                    Reading.append(Data[ No ])
                    No += 1
                SubGroupList.append(np.average(Reading))
                RList.append(max(Reading) - min(Reading))

            stdWi = np.average(RList) / d2[ Sample_Size ]
            m = np.average(SubGroupList)
            Cp = (USL - LSL) / (6 * stdWi)
            CPU = (USL - m) / (3 * stdWi)
            CPL = (m - LSL) / (3 * stdWi)
            Cpk = min(CPL, CPU)
            z = min((USL - m) / stdWi, (m - LSL) / stdWi)

            ReadingsArrary = np.array(Data)
            Pp = (USL - LSL) / (6 * statistics.stdev(Data))
            Ppu = (USL - ReadingsArrary.mean()) / (3 * statistics.stdev(Data))
            Ppl = (ReadingsArrary.mean() - LSL) / (3 * statistics.stdev(Data))
            Ppk = min(Ppl, Ppu)

            num_samples = len(ReadingsArrary)
            sample_mean = np.mean(SubGroupList)
            sample_std_within = stdWi
            sample_std_overall = ReadingsArrary.std()
            sample_max = max(Data)
            sample_min = min(Data)
            sample_median = np.median(ReadingsArrary)

            ReadingsAvg_Arrary = np.array(SubGroupList)

            ov_pct_below_LSL = len(ReadingsArrary[ ReadingsArrary < LSL ]) / len(ReadingsArrary) * 1000000
            ov_pct_below_LSL_Def = len(ReadingsArrary[ ReadingsArrary < LSL ]) / len(ReadingsArrary) * 100
            ov_pct_above_USL = len(ReadingsArrary[ ReadingsArrary > USL ]) / len(ReadingsArrary) * 1000000
            ov_pct_above_USL_Def = len(ReadingsArrary[ ReadingsArrary > USL ]) / len(ReadingsArrary) * 100
            ov_total = ov_pct_below_LSL + ov_pct_above_USL

            wi_ppm_below_LSL = len(ReadingsAvg_Arrary[ ReadingsAvg_Arrary < LSL ]) / len(ReadingsAvg_Arrary) * 1000000
            wi_ppm_below_LSL_Def = len(ReadingsAvg_Arrary[ ReadingsAvg_Arrary < LSL ]) / len(ReadingsAvg_Arrary) * 100
            wi_ppm_above_USL = len(ReadingsAvg_Arrary[ ReadingsAvg_Arrary > USL ]) / len(ReadingsAvg_Arrary) * 1000000
            wi_ppm_above_USL_Def = len(ReadingsAvg_Arrary[ ReadingsAvg_Arrary > USL ]) / len(ReadingsAvg_Arrary) * 100
            wi_total = wi_ppm_below_LSL + wi_ppm_above_USL

            Cpcpk = {"Cp": round(Cp, 3), "Pp": round(Pp, 3), "Cpl": round(CPL, 3), "Ppl": round(Ppl, 3),
                     "Cpu": round(CPU, 3), "Ppu": round(Ppu, 3), "Cpk": round(Cpk, 3), "Ppk": round(Ppk, 3),
                     "Std Within": round(sample_std_within, 4), "Std Overall": round(sample_std_overall, 4),
                     "Sample": num_samples, "Z": round(z, 3), "Median": round(sample_median, 3),
                     "Sample Mean": round(sample_mean, 4), "Max": sample_max, "Min": sample_min,
                     "PPM > LSL": round(ov_pct_below_LSL, 6), "PPM > USL": round(ov_pct_above_USL, 6),
                     "Total Overall PPM": round(ov_total, 6), "Total Within PPM": round(wi_total, 6)}

            return Cpcpk

        except ZeroDivisionError:
            showDialog('* ERROR * There is insufficient variation.\n No calculations can be done.')

            print("* ERROR * There is insufficient variation. No calculations can be done.")

        except Exception as Error:
            print(__file__, "Cp_Cpk_Chart :", Error)

def XBarR_plot(Data, Sample_Size):
    if len(Data) != 0 and len(Data) >= Sample_Size:
        try:

            SubGroupList = [ ]
            RList, XList = [ ], [ ]  # values

            R = int(len(Data) / Sample_Size)
            No = 0
            while len(SubGroupList) != R and len(SubGroupList) <= R:
                Reading = [ ]
                for i in range(Sample_Size):
                    Reading.append(Data[ No ])
                    No += 1
                SubGroupList.append(np.average(Reading))
                RList.append(max(Reading) - min(Reading))
                XList.append(np.mean(Reading))

            Rbar = np.mean(RList)  # center
            Xbar = np.mean(XList)

            lcl = Xbar - A2[ Sample_Size ] * Rbar
            ucl = Xbar + A2[ Sample_Size ] * Rbar

            _title = "Xbar-R Chart"

            return {"Data": XList, "Mean": Xbar, "LCL": lcl, "UCL": ucl, "title": [ _title, "UCL", "Xbar", "LCL" ]}

        except ZeroDivisionError:
            showDialog('* ERROR * There is insufficient variation.\n No calculations can be done.')

            print("* ERROR * There is insufficient variation. No calculations can be done.")

        except Exception as Error:
            print(__file__, "XBarR_plot :", Error)

def RChart_plot(Data, Sample_Size):
    if len(Data) != 0 and len(Data) >= Sample_Size:
        try:
            SubGroupList = [ ]
            RbarList = [ ]  # values
            R = int(len(Data) / Sample_Size)
            No = 0
            while len(SubGroupList) != R and len(SubGroupList) <= R:
                Reading = [ ]
                for i in range(Sample_Size):
                    Reading.append(Data[ No ])
                    No += 1
                SubGroupList.append(np.average(Reading))
                RbarList.append(max(Reading) - min(Reading))

            Rbar = np.mean(RbarList)  # center
            lcl = D3[ Sample_Size ] * Rbar
            ucl = D4[ Sample_Size ] * Rbar

            _title = "R Chart"

            return {"Data": RbarList, "Mean": Rbar, "LCL": lcl, "UCL": ucl,
                    "title": [ _title, "UCL", "Rbar", "LCL" ]}


        except ZeroDivisionError:
            showDialog('* ERROR * There is insufficient variation.\n No calculations can be done.')

            print("* ERROR * There is insufficient variation. No calculations can be done.")

        except Exception as Error:
            print(__file__, "R Chart :", Error)

def XBarS_plot(Data, Sample_Size):
    if len(Data) != 0 and len(Data) >= Sample_Size:
        try:
            SubGroupList = [ ]
            SList, XList = [ ], [ ]  # values

            R = int(len(Data) / Sample_Size)
            No = 0
            while len(SubGroupList) != R and len(SubGroupList) <= R:
                Reading = [ ]
                for i in range(Sample_Size):
                    Reading.append(Data[ No ])
                    No += 1
                SubGroupList.append(np.average(Reading))
                SList.append(np.std(Reading, ddof=1))
                XList.append(np.mean(Reading))

            sbar = np.mean(SList)  # center
            Xbar = np.mean(XList)
            lclx = Xbar - A3[ Sample_Size ] * sbar
            uclx = Xbar + A3[ Sample_Size ] * sbar
            _title = "Xbar-S Chart"

            return {"Data": XList, "Mean": Xbar, "LCL": lclx, "UCL": uclx,
                    "title": [ _title, "UCLX", "xbar", "LCLX" ]}

        except ZeroDivisionError:
            showDialog('* ERROR * There is insufficient variation.\n No calculations can be done.')

            print("* ERROR * There is insufficient variation. No calculations can be done.")

        except Exception as Error:
            print(__file__, "Xbar-S Chart :", Error)

def SChart_plot(Data, Sample_Size):
    if len(Data) != 0 and len(Data) >= Sample_Size:
        try:

            SubGroupList = [ ]
            SList = [ ]  # values
            R = int(len(Data) / Sample_Size)
            No = 0
            while len(SubGroupList) != R and len(SubGroupList) <= R:
                Reading = [ ]
                for i in range(Sample_Size):
                    Reading.append(Data[ No ])
                    No += 1
                SList.append(np.std(Reading, ddof=1))
                SubGroupList.append(np.std(Reading, ddof=1))

            sbar = np.mean(SList)
            lcls = B3[ Sample_Size ] * sbar
            ucls = B4[ Sample_Size ] * sbar
            _title = "Standard Deviation Chart"

            return {"Data": SList, "Mean": sbar, "LCL": lcls, "UCL": ucls,
                    "title": [ _title, "UCLS", "Sbar", "LCLS" ]}


        except ZeroDivisionError:
            showDialog('* ERROR * There is insufficient variation.\n No calculations can be done.')

            print("* ERROR * There is insufficient variation. No calculations can be done.")

        except Exception as Error:
            print(__file__, "SChart_plot :", Error)

def MR_plot(Data, Sample_Size):
    if len(Data) != 0 and len(Data) >= Sample_Size:
        try:

            R = np.array([ np.nan ] + [ abs(Data[ i ] - Data[ i + 1 ]) for i in range(len(Data) - 1) ])

            Rbar = np.nanmean(R)

            lclr = D3[ 2 ] * Rbar
            uclr = D4[ 2 ] * Rbar

            _title = "MR - Moving Range Chart"

            return {"Data": R, "Mean": Rbar, "LCL": lclr, "UCL": uclr, "title": [ _title, "UCLR", "Rbar", "LCLR" ]}


        except ZeroDivisionError:
            showDialog('* ERROR * There is insufficient variation.\n No calculations can be done.')

            print("* ERROR * There is insufficient variation. No calculations can be done.")

        except Exception as Error:
            print(__file__, "MR_plot :", Error)

def MRXchart_plot(Data, Sample_Size):
    if len(Data) != 0 and len(Data) >= Sample_Size:
        try:
            R = np.array([ np.nan ] + [ abs(Data[ i ] - Data[ i + 1 ]) for i in range(len(Data) - 1) ])
            Rbar = np.nanmean(R)
            Xbar = np.mean(Data)
            lclx = Xbar - 3 * (Rbar / d2[ 2 ])
            uclx = Xbar + 3 * (Rbar / d2[ 2 ])
            _title = "X chart"

            return {"Data": Data, "Mean": Xbar, "LCL": lclx, "UCL": uclx, "title": [ _title, "UCLX", "Xbar", "LCLx" ]}

        except ZeroDivisionError:
            showDialog('* ERROR * There is insufficient variation.\n No calculations can be done.')
            print("* ERROR * There is insufficient variation. No calculations can be done.")

        except Exception as Error:
            print(__file__, "Cp_Cpk_Chart :", Error)

# -------------------------------------not use---------------------------------------------------------------------------------

def Cchart_plot(data, size):
    cbar = np.mean(data)

    lcl = cbar - 3 * np.sqrt(cbar)
    ucl = cbar + 3 * np.sqrt(cbar)

    _title = "C chart"

    return (data, cbar, lcl, ucl, _title)


def U_Chartplot(data, size):
    SampleData = np.array(data)
    ubar = np.sum(size) / np.sum(SampleData)

    data2 = [ ]
    for data, size in zip(SampleData, size):
        data2_v = size / SampleData
        data2.append(data2_v)

    lcl, ucl = [ ], [ ]
    for i in data:
        lcl.append(ubar - 3 * np.sqrt(ubar / i))
        ucl.append(ubar + 3 * np.sqrt(ubar / i))

    _title = "U Chart"

    return (data2, ubar, lcl, ucl, _title)


def NPChart_plot(data, size):
    p = np.mean([ float(d) / size for d in data ])
    pbar = np.mean(data)

    lcl = pbar - 3 * np.sqrt(pbar * (1 - p))
    ucl = pbar + 3 * np.sqrt(pbar * (1 - p))

    _title = "NP Chart"

    return (data, pbar, lcl, ucl, _title)


def PChart_plot(data, sizes):
    SampleData = np.array(data)
    data2 = [ ]
    for data, size in zip(SampleData, sizes):
        data2_v = size / SampleData
        data2.append(data2_v)

    pbar = np.mean(data2)

    lcl, ucl = [ ], [ ]
    for size in sizes:
        lcl.append(pbar - 3 * np.sqrt((pbar * (1 - pbar)) / size))
        ucl.append(pbar + 3 * np.sqrt((pbar * (1 - pbar)) / size))

    _title = "P Chart"

    return (data2, pbar, lcl, ucl, _title)


def showDialog(msg):
    pass

    # msgBox = QMessageBox()  # msgBox.setIcon(QMessageBox.Question)  # msgBox.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)  #  # msgBox.setText(msg)  # msgBox.setStyleSheet('''QMessageBox {  #                                       background-color: #F2F2F2;  #                                       background-color:rgb(29,32,34);  #  #                                       border: 1px solid rgb(255, 250, 250);  #                                       border-radius: 10px;  #                                       }  #                                       QMessageBox QLabel#qt_msgbox_label {  #                                       color: #298DFF;  #                                       background-color: transparent;  #                                       min-width: 300px;  #                                       min-height: 80px;  #                                       font:14pt;  #                                       }  #                                       QMessageBox QLabel#qt_msgboxex_icon_label {  #                                       width: 50px;  #                                       height: 40px;  #                                       }  #  #                                       QMessageBox QPushButton {  #                                       border: 1px solid #298DFF;  #                                       border-radius: 3px;  #                                       background-color: #F2F2F2;  #                                       background-color:rgb(29,32,34);  #                                       color: #298DFF;  #                                       font: 14pt;  #                                       min-width: 90px;  #                                       min-height: 30px;  #                                       }  #                                       QMessageBox QPushButton:hover {  #                                       background-color: #298DFF;  #                                       color: #F2F2F2;  #                                       }  #                                       QMessageBox QPushButton:pressed {  #                                       background-color: #257FE6;  #                                       }  #                                       QMessageBox QDialogButtonBox#qt_msgbox_buttonbox {  #                                       button-layout: 0;  #                                       }''')  # msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)  # # msgBox.buttonClicked.connect(msgButtonClick)  # returnValue = msgBox.exec()
