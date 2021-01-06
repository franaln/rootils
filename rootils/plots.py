import ROOT
import numpy as np
import pandas as pd

import rootils.utils as ut

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)


def lines(data=None,
          x=[],
          y=[],
          colors=[],
          labels=[],
          xtitle='',
          ytitle='',
          xlog=False,
          ylog=False,
          xlimits=(),
          ylimits=(),
          mstyle=[],
          lstyle=[],
          legend=False,
          legend_pos='top_right',
          save=None):

    """
    Input:
    - data: pandas.DataFrame, x: list of columns or column, y: list of columns
    - data: None, x: list of array, y: list of arrays
    - data: list of TGraph, x/y: None
    - tree
    """

    graphs = []

    if isinstance(data, pd.DataFrame):
        #data = daxta.copy(deep=True)

        if not isinstance(y, list):
            y = [y,]

        n_lines = len(y)

        if not x:
            y = 'x'
            data[x] = [ float(i+1) for i in range(len(data)) ]

        for i in range(n_lines):
            g = ut.array_to_graph(data[x].values, data[y[i]].values)
            graphs.append(g)

    elif isinstance(data, list):
        pass

    elif data is None and isinstance(y, list):
        n_lines = len(y)
        for i in range(n_lines):
            if isinstance(x, list) and isinstance(x[0], list):
                g = ut.array_to_graph(x[i], y[i])
            else:
                g = ut.array_to_graph(x, y[i])
            graphs.append(g)


    # Plot
    canvas = ut.create_canvas()

    ut.set_style_all(graphs, colors, mstyle, lstyle)

    ut.set_titles_labels(graphs, xtitle, ytitle)

    for i in range(n_lines):
        if i == 0:
            graphs[i].Draw('pla')
        else:
            graphs[i].Draw('pl')

    ut.set_axis_limits(graphs)

    leg = ut.legend(graphs, labels, pos=legend_pos)
    leg.Draw()

    ut.footer(canvas, save)

    return canvas


def hists(data,
          x=[],
          bins=True,
          # norm_hist=False,
          logx=False,
          logy=False,
          xtitle='',
          ytitle='',
          labels=[],
          drawopts='hist',
          colors=[],
          mstyle=[],
          lstyle=[],
          text=None,
          legend=True,
          legend_pos='top_right',
          grid=False,
          save=False):

    """
    Input:
    - data: pandas.DataFrame, x: list of columns or column
    - data: numpy array
    - data: list of TH1, x: None
    - data: tree or list of trees, x: list of branch name
    """

    hists = []
    if isinstance(data, pd.DataFrame):
        pass


    elif isinstance(data, ROOT.TTree):
        pass
    elif isinstance(data, list):
        hists = data

    # if bins:
    #     if isinstance(x, list) is False:
    #         bins = int(len(data[x].unique()) / 10) + 5
    #     else:
    #         bins = 10

    # # if dropna is True:
    # #     data = data[data[x].isna() == False]

    # if isinstance(x, list) is False:
    #     x = [x]

    # n_colors = len(x)

    # PLOT
    canvas = ut.create_canvas(logy=logy, logx=logx, grid=grid)

    ut.set_style_all(hists, colors, mstyle, lstyle)

    ut.set_titles_labels(hists, xtitle, ytitle)

    ut.set_axis_limits(hists, logx, logy)
    for hist in hists:
        hist.Draw(drawopts+'same')


    ut.set_axis_limits(hists, logx, logy)

    if legend:
        leg = ut.legend(hists, labels, pos=legend_pos)
        leg.Draw()

    if text is not None:
        ut.draw_text(text, legend_pos)

    ut.footer(canvas, save)

    return canvas


def hists_ratio(data,
                x=[],
                bins=True,
                # norm_hist=False,
                logx=False,
                logy=False,
                xtitle='',
                ytitle='',
                labels=[],
                drawopts='hist',
                colors=[],
                mstyle=[],
                lstyle=[],
                text=None,
                legend=True,
                legend_pos='top_right',
                save=False):

    """
    Input:
    - data: pandas.DataFrame, x: list of columns or column
    - data: numpy array
    - data: list of TH1, x: None
    - data: tree or list of trees, x: list of branch name
    """

    hists = []
    if isinstance(data, pd.DataFrame):
        pass


    elif isinstance(data, ROOT.TTree):
        pass
    elif isinstance(data, list):
        hists = data

    # if bins:
    #     if isinstance(x, list) is False:
    #         bins = int(len(data[x].unique()) / 10) + 5
    #     else:
    #         bins = 10

    # # if dropna is True:
    # #     data = data[data[x].isna() == False]

    # if isinstance(x, list) is False:
    #     x = [x]

    # n_colors = len(x)

    # PLOT
    canvas, cup, cdn = ut.create_canvas_with_ratio(logy=logy, logx=logx)

    ut.set_style_all(hists, colors, mstyle, lstyle)

    ut.set_titles_labels(hists, xtitle, ytitle)

    ut.set_axis_limits(hists, logx, logy)

    cup.cd()
    for hist in hists:
        hist.Draw(drawopts+'same')

    ut.set_axis_limits(hists, logx, logy)

    if legend:
        leg = ut.legend(hists, labels, pos=legend_pos)
        leg.Draw()

    if text is not None:
        ut.draw_text(text, legend_pos)

    # Ratios
    ratios = []
    for hist in hists[1:]:
        ratio = hist.Clone(hist.GetName()+'_ratio')
        ratio.Divide(hists[0])
        ratios.append(ratio)

    cdn.cd()
    ut.set_ratio_axis_limits(ratios, logx, logy)

    ratios[0].GetXaxis().SetLabelSize(0.1)
    ratios[0].GetYaxis().SetLabelSize(0.1)
    for ratio in ratios:
        ratio.Draw(drawopts+'same')


    ut.footer(canvas, save)

    return canvas


def corr(data,
         corr_method='spearman',
         annot=False,
         save=False):

    # Compute correlation
    corr_matrix = data.corr(method=corr_method).to_numpy()

    columns = data.columns

    hist = ut.matrix_to_th2(corr_matrix)

    # PLOT
    ut.default_style()

    canvas = ut.create_canvas(800, 800, True, True)

    ax = hist.GetXaxis()
    ay = hist.GetYaxis()

    nx = hist.GetNbinsX()

    if True:
        for i in range(nx):
            ax.SetBinLabel(i+1, columns[i])

        for i in range(nx):
            ay.SetBinLabel(i+1, columns[i])

    else:
        for i in range(1, nx+1):
            ax.SetBinLabel(i, str(i))

        for i in range(1, ny+1):
            ay.SetBinLabel(i, str(i))

    hist.SetContour(999)
    hist.GetZaxis().SetRangeUser(-1, 1)

    hist.SetStats(0)
    hist.SetTitle('')

    if annot:
        hist.Draw('colz text')
    else:
        hist.Draw('colz')

    ut.footer(canvas, save)

    return canvas


def heatmap():

    #
    hist = ut.create_TH2(neta, 0, neta, nphi, 0, nphi)

    idx = 0
    for x in range(neta):
        for y in range(nphi):
            hist.SetBinContent(x+1, y+1, data[idx])
            idx += 1

    ax = hist.GetXaxis()
    ay = hist.GetYaxis()

    nx = hist.GetNbinsX()
    ny = hist.GetNbinsY()

    for i in range(1, nx+1):
        ax.SetBinLabel(i, str(i))

    for i in range(1, ny+1):
        ay.SetBinLabel(i, str(i))

    ay.SetTitle(ytitle)
    ax.SetTitle(xtitle)

    hist.SetContour(999)
    # h.GetZaxis().SetRangeUser(0, zmax)

    canvas = ut.create_canvas(grid=True)


    hist.Draw('colz')

    ut.footer(canvas, save)

    return canvas


def confusion_matrix(tp, tn, fp, fn, norm=False, save=False):

    hist = ut.create_TH2(2, 0, 2, 2, 0, 2)

    if norm:
        total = tp+tn+fp+fn
        tp /= total
        tn /= total
        fp /= total
        fn /= total

    hist.SetBinContent(1, 1, tp)
    hist.SetBinContent(1, 2, fn)
    hist.SetBinContent(2, 1, fp)
    hist.SetBinContent(2, 2, tn)

    ax = hist.GetXaxis()
    ay = hist.GetYaxis()

    ax.SetBinLabel(1, 'P')
    ax.SetBinLabel(2, 'N')
    ay.SetBinLabel(1, 'P')
    ay.SetBinLabel(2, 'N')

    ay.SetTitle('Truth')
    ax.SetTitle('Prediction')
    ax.CenterTitle()
    ay.CenterTitle()

    hist.SetContour(999)
    if norm:
        hist.GetZaxis().SetRangeUser(0, 1)

    ut.default_style()

    canvas = ut.create_canvas(800, 800, True, True)

    hist.Draw('colz text')

    ut.footer(canvas, save)

    return canvas
