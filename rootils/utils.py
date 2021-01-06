import sys
import ROOT
import math
import numpy as np
from array import array

is_py3 = (sys.version_info > (3, 0))

if not is_py3:
    range = xrange

colourdict = {
    'orange':      '#E24A33',
    'purple':      '#7A68A6',
    'blue':        '#348ABD',
    'lblue':       '#68add5',
    'turquoise':   '#188487',
    'red':         '#A60628',
    'pink':        '#CF4457',
    'green':       '#32b43c',
    'lgreen':      '#88de8f',
    'yellow':      '#e2a233',
    'lyellow':     '#f7fab3',
    'grey':        '#838283',
    'gray':        '#838283',
}

def get_color(c):

    if not isinstance(c, str):
        return c

    if c.startswith('#'):
        colour = ROOT.TColor.GetColor(c)
    else:
        try:
            colour = ROOT.TColor.GetColor(colourdict[c])
        except KeyError:
            if '+' in c:
                col, n = c.split('+')
                colour = getattr(ROOT, col)
                colour += int(n)
            elif '-' in c:
                col, n = c.split('-')
                colour = getattr(ROOT, col)
                colour -= int(n)
            else:
                colour = getattr(ROOT, c)

    return colour


def set_color(obj, color, fill=False, alpha=None):
    color = get_color(color)
    obj.SetLineColor(color)
    obj.SetMarkerColor(color)
    if fill:
        if alpha is not None:
            obj.SetFillColorAlpha(color, alpha)
        else:
            obj.SetFillColor(color)

def set_palette(name='reds'):

    if name == 'reds':
        stops = array('d', [0.0000, 0.1250, 0.2500, 0.3750, 0.5000, 0.6250, 0.7500, 0.8750, 1.0000])
        r = array('d', [ 37./255., 102./255., 157./255., 188./255., 196./255., 214./255., 223./255., 235./255., 251./255.])
        g = array('d', [ 37./255.,  29./255.,  25./255.,  37./255.,  67./255.,  91./255., 132./255., 185./255., 251./255.])
        b = array('d', [ 37./255.,  32./255.,  33./255.,  45./255.,  66./255.,  98./255., 137./255., 187./255., 251./255.])
    elif name == 'blues':
        stops = array('d', [0.0000, 0.1250, 0.2500, 0.3750, 0.5000, 0.6250, 0.7500, 0.8750, 1.0000])
        r = array('d', [ 37./255.,  32./255.,  33./255.,  45./255.,  66./255.,  98./255., 137./255., 187./255., 251./255.])
        g = array('d', [ 37./255.,  29./255.,  25./255.,  37./255.,  67./255.,  91./255., 132./255., 185./255., 251./255.])
        b = array('d', [ 37./255., 102./255., 157./255., 188./255., 196./255., 214./255., 223./255., 235./255., 251./255.])

    ROOT.TColor.CreateGradientColorTable(len(stops), stops, r, g, b, 999)
    ROOT.gStyle.SetNumberContours(999)
    ROOT.TColor.InvertPalette()


def default_style():

    ROOT.gStyle.SetOptStat(0)

    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)
    ROOT.gStyle.SetFrameFillColor(0)
    ROOT.gStyle.SetFrameBorderSize(0)
    ROOT.gStyle.SetFrameBorderMode(0)
    ROOT.gStyle.SetCanvasColor(0)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetTitleBorderSize(0)
    ROOT.gStyle.SetTitleFillColor(0)
    ROOT.gStyle.SetTextFont(132)
    ROOT.gStyle.SetLegendFont(132)
    ROOT.gStyle.SetLabelFont(132, "XYZ")
    ROOT.gStyle.SetTitleFont(132, "XYZ")
    ROOT.gStyle.SetEndErrorSize(0)

    # use plain black on white colors
    icol = 0
    ROOT.gStyle.SetFrameBorderMode(icol)
    ROOT.gStyle.SetFrameFillColor(icol)
    ROOT.gStyle.SetCanvasBorderMode(icol)
    ROOT.gStyle.SetCanvasColor(icol)
    ROOT.gStyle.SetPadBorderMode(icol)
    ROOT.gStyle.SetPadColor(icol)
    ROOT.gStyle.SetStatColor(icol)

    # set the paper & margin sizes
    ROOT.gStyle.SetPaperSize(20,26)

    # set margin sizes
    ROOT.gStyle.SetPadTopMargin(0.05)
    ROOT.gStyle.SetPadRightMargin(0.05)
    ROOT.gStyle.SetPadBottomMargin(0.16)
    ROOT.gStyle.SetPadLeftMargin(0.16)

    # set title offsets (for axis label)
    ROOT.gStyle.SetTitleXOffset(1.4)
    ROOT.gStyle.SetTitleYOffset(1.4)

    # use large fonts
    font = 42 # Helvetica
    tsize = 0.05
    ROOT.gStyle.SetTextFont(font)
    ROOT.gStyle.SetTextSize(tsize)

    ROOT.gStyle.SetLabelFont(font, "x")
    ROOT.gStyle.SetTitleFont(font, "x")
    ROOT.gStyle.SetLabelFont(font, "y")
    ROOT.gStyle.SetTitleFont(font, "y")
    ROOT.gStyle.SetLabelFont(font, "z")
    ROOT.gStyle.SetTitleFont(font, "z")

    ROOT.gStyle.SetLabelSize(tsize, "x")
    ROOT.gStyle.SetTitleSize(tsize, "x")
    ROOT.gStyle.SetLabelSize(tsize, "y")
    ROOT.gStyle.SetTitleSize(tsize, "y")
    ROOT.gStyle.SetLabelSize(tsize, "z")
    ROOT.gStyle.SetTitleSize(tsize, "z")

    # use bold lines and markers
    ROOT.gStyle.SetMarkerStyle(20)
    ROOT.gStyle.SetMarkerSize(1.2)
    ROOT.gStyle.SetHistLineWidth(2)
    ROOT.gStyle.SetLineStyleString(2, "[12 12]")
    ROOT.gStyle.SetEndErrorSize(0.)

    # do not display any of the standard histogram decorations
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptFit(0)

    set_palette()


def set_style(obj, **kwargs):

    is_hist = obj.InheritsFrom('TH1')

    color = kwargs.get('color', ROOT.kBlack)
    alpha = kwargs.get('alpha', None)

    mstyle = kwargs.get('mstyle', 20)
    fstyle = kwargs.get('fstyle', None)
    lstyle = kwargs.get('lstyle',None)

    msize  = kwargs.get('msize', 0.8)
    lwidth = kwargs.get('lwidth', 2)

    fill = (kwargs.get('fill', False) or fstyle is not None)

    # xtitle = kwargs.get('xtitle', None)
    # ytitle = kwargs.get('ytitle', None)

    # xmin = kwargs.get('xmin', None)
    # xmax = kwargs.get('xmax', None)
    # ymin = kwargs.get('ymin', None)
    # ymax = kwargs.get('ymax', None)

    # default
    obj.SetTitle('')
    if is_hist:
        obj.SetStats(0)

    # color
    set_color(obj, color, fill, alpha)

    # marker
    obj.SetMarkerStyle(mstyle)
    obj.SetMarkerSize(msize)

    # line
    obj.SetLineWidth(lwidth)
    if lstyle is not None:
        obj.SetLineStyle(lstyle)

    # fill
    if fstyle is not None:
        obj.SetFillStyle(fstyle)

    # # axis titles
    # if xtitle is not None:
    #     obj.GetXaxis().SetTitle(xtitle)
    # if ytitle is not None:
    #     obj.GetYaxis().SetTitle(ytitle)

    # if xmin is not None and xmax is not None:
    #     obj.GetXaxis().SetRangeUser(xmin, xmax)
    # if ymin is not None and ymax is not None:
    #     obj.GetYaxis().SetRangeUser(ymin, ymax)


def create_canvas(w=800, h=600, rightaxis=False, grid=False, logx=False, logy=False):
    canvas = ROOT.TCanvas("canvas", "", w, h)
    ROOT.SetOwnership(canvas, False)

    canvas.SetLeftMargin(0.12)
    canvas.SetBottomMargin(0.12)
    canvas.SetTopMargin(0.02)
    if rightaxis:
        canvas.SetRightMargin(0.12)
    else:
        canvas.SetRightMargin(0.02)
    canvas.SetTicks()
    if grid:
        canvas.SetGrid()
    if logy:
        canvas.SetLogy()
    if logx:
        canvas.SetLogx()

    return canvas

def create_canvas_with_ratio(w=800, h=600, rightaxis=False, grid=False, logx=False, logy=False):
    # TODO

    canvas = ROOT.TCanvas("canvas", "", w, h)
    ROOT.SetOwnership(canvas, False)

    cup   = ROOT.TPad("u", "u", 0., 0.305, 0.99, 1)
    cdn  = ROOT.TPad("d", "d", 0., 0.01, 0.99, 0.295)
    cup.SetRightMargin(0.05)
    cup.SetBottomMargin(0.005)

    cup.SetTickx()
    cup.SetTicky()
    cdn.SetTickx()
    cdn.SetTicky()
    cdn.SetRightMargin(0.05)
    cdn.SetBottomMargin(0.25)
    cdn.SetTopMargin(0.0054)
    cdn.SetFillColor(ROOT.kWhite)

    if logy:
        cup.SetLogy()
    if logx:
        cup.SetLogx()

    cdn.SetGridy()

    cup.Draw()
    cdn.Draw()

    # cup.SetLogy()
    # cup.SetTopMargin(0.08)
    # cdown.SetBottomMargin(0.4)

    return canvas, cup, cdn

def legend(objs, labels, pos='top_right', ncols=1):

    # find the best place
    if pos == 'tr' or pos == 'top_right':
        legend = ROOT.TLegend(0.65, 0.84, 0.94, 0.94)
    elif pos == 'bl'or pos == 'bottom_left':
        legend = ROOT.TLegend(0.15, 0.15, 0.45, 0.45)

    legend.SetFillColor(0)
    legend.SetBorderSize(0)
    legend.SetNColumns(ncols)

    for i in range(len(objs)):
        legend.AddEntry(objs[i], labels[i])

    return legend


def footer(canvas, save=False):
    canvas.RedrawAxis()
    if save:
        canvas.SaveAs(save)


def set_axis_limits(objs, logx=False, logy=False):

    # check if graphs or hists
    if objs[0].InheritsFrom('TGraph'):
        xmin = min([ min(o.GetX()) for o in objs ])
        ymin = min([ min(o.GetY()) for o in objs ])

        xmax = max([ max(o.GetX()) for o in objs ])
        ymax = max([ max(o.GetY()) for o in objs ])
    else:
        xmin = min([ o.GetXaxis().GetXmin() for o in objs ])
        xmax = max([ o.GetXaxis().GetXmax() for o in objs ])

        ymin = min([ o.GetMinimum() for o in objs ])
        ymax = max([ o.GetMaximum() for o in objs ])

    if logy:
        if ymin < 0.001:
            ymin = 0.001
        ymin *= 0.5
        ymax *= 5

    else:
        ymin *= 0.9
        ymax *= 1.1

        # # ymin_hist = 0.5*ymin_hist if is_logy else 0.8*ymin_hist
    # # ymax_hist = 5*ymax_hist if is_logy else 1.2*ymax_hist

    # # if ymin_hist < 0.1 and is_logy:
    # #     ymin_hist = 0.1

    objs[0].GetXaxis().SetRangeUser(xmin, xmax)
    objs[0].GetYaxis().SetRangeUser(ymin, ymax)


def set_ratio_axis_limits(objs, logx=False, logy=False):

    # check if graphs or hists
    if objs[0].InheritsFrom('TGraph'):
        xmin = min([ min(o.GetX()) for o in objs ])
        ymin = min([ min(o.GetY()) for o in objs ])

        xmax = max([ max(o.GetX()) for o in objs ])
        ymax = max([ max(o.GetY()) for o in objs ])
    else:
        xmin = min([ o.GetXaxis().GetXmin() for o in objs ])
        xmax = max([ o.GetXaxis().GetXmax() for o in objs ])

        ymin = min([ o.GetMinimum() for o in objs ])
        ymax = max([ o.GetMaximum() for o in objs ])

    # if logy:
    #     if ymin < 0.001:
    #         ymin = 0.001
    #     ymin *= 0.5
    #     ymax *= 5

    # else:
    #     ymin *= 0.9
    #     ymax *= 1.1

        # # ymin_hist = 0.5*ymin_hist if is_logy else 0.8*ymin_hist
    # # ymax_hist = 5*ymax_hist if is_logy else 1.2*ymax_hist

    # # if ymin_hist < 0.1 and is_logy:
    # #     ymin_hist = 0.1

    objs[0].GetXaxis().SetRangeUser(xmin, xmax)
    objs[0].GetYaxis().SetRangeUser(ymin, ymax)


def set_default_hist_style(hist):
    hist.SetStats(0)
    hist.SetTitle('')

_default_colors = [
    # ROOT.kBlack,
    'red',
    'blue',
    'orange',
    'pink',
    'lblue',
    'purple',
    'gray',
    'green',
    'yellow',
    'turquoise',
    'lgreen',
    'lyellow',
    ROOT.kBlack,
    ROOT.kMagenta,
    ROOT.kSpring,
    ROOT.kRed-4,
    ROOT.kBlue-4,
]

def set_style_all(objs, colors=[], mstyle=[], lstyle=[]):
    for i in range(len(objs)):
        c = colors[i] if colors else _default_colors[i]
        ls = lstyle[i] if lstyle else None
        set_style(objs[i], color=c, lstyle=ls)



def set_titles_labels(objs, xtitle, ytitle):
    objs[0].GetXaxis().SetTitle(xtitle)
    objs[0].GetYaxis().SetTitle(ytitle)


def sort_graph(g, sort_x=True):

    ax = array('f', [])
    ay = array('f', [])

    d = dict()
    for i in range(g.GetN()):

        xtmp = ROOT.Double(0)
        ytmp = ROOT.Double(0)

        g.GetPoint(i, xtmp, ytmp)
        d[xtmp] = ytmp

    if sort_x:
        for x, y in sorted(d.items()):
            ax.append(x)
            ay.append(y)
    else:
        for x, y in sorted(d, key=d.get):
            ax.append(x)
            ay.append(y)

    return ROOT.TGraph(g.GetN(), ax, ay)


def draw_text(text, pos='top_right', size=0.03, ndc=True):

    if pos == 'top_right':
        x, y = 0.65, 0.75

    l = ROOT.TLatex(x, y, text)
    ROOT.SetOwnership(l, False)
    l.SetTextFont(42)

    if ndc:
        l.SetNDC()

    if size is not None:
        l.SetTextSize(size)

    l.Draw()


def draw_horizontal_line(y): # FIX

    l = ROOT.TLine(0, 220, 200, 220)
    l.SetLineStyle(2)
    l.SetLineColor(ROOT.kGray+1)
    l.Draw()


def draw_ratio_lines(ratio):

    firstbin = ratio.GetXaxis().GetFirst()
    lastbin  = ratio.GetXaxis().GetLast()
    xmax     = ratio.GetXaxis().GetBinUpEdge(lastbin)
    xmin     = ratio.GetXaxis().GetBinLowEdge(firstbin)

    lines = [None, None, None,]
    lines[0] = ROOT.TLine(xmin, 1., xmax, 1.)
    lines[1] = ROOT.TLine(xmin, 0.5,xmax, 0.5)
    lines[2] = ROOT.TLine(xmin, 1.5,xmax, 1.5)

    lines[0].SetLineWidth(1)
    lines[0].SetLineStyle(2)
    lines[1].SetLineStyle(3)
    lines[2].SetLineStyle(3)

    for line in lines:
        line.AppendPad()
        line.Draw()


def set_default_graph_style(g):
    g.SetTitle('')
    g.SetLineColor(ROOT.kAzure-2)
    g.SetMarkerColor(ROOT.kAzure-2)
    g.SetMarkerStyle(20)


def set_default_hist_style(h):
    h.SetTitle('')
    h.SetStats(0)
    h.SetLineColor(ROOT.kAzure-2)
    h.SetMarkerColor(ROOT.kAzure-2)
    h.SetMarkerStyle(20)


def create_TGraph(x, y):
    g = ROOT.TGraph(len(x), x, y)
    ROOT.SetOwnership(g, False)
    set_default_graph_style(g)
    return g

def create_TH1(nx=None, xmin=None, xmax=None, xbins=None):
    name = 'h1'
    if xbins:
        hist = ROOT.TH1F(name, name, len(xbins)-1, array('d', xbins))
    elif nx is not None and xmin is not None and xmax is not None:
        hist = ROOT.TH1F(name, name, nx, xmin, xmax)

    hist.SetDirectory(0)
    ROOT.SetOwnership(hist, False)

    hist.Sumw2()
    hist.SetStats(0)
    hist.SetTitle('')
    set_default_hist_style(hist)

    return hist

def create_TH2(nx, xmin, xmax, ny, ymin, ymax, xbins=None, ybins=None):
    name = 'h2'
    if xbins is not None and ybins is not None:
        hist = ROOT.TH2F(name, name, len(xbins)-1, array('d', xbins), len(ybins)-1, array('d', ybins))
    else:
        hist = ROOT.TH2F(name, name, nx, xmin, xmax, ny, ymin, ymax)
    ROOT.SetOwnership(hist, False)
    hist.SetDirectory(0)
    hist.SetStats(0)
    set_default_hist_style(hist)

    return hist

def array_to_graph(x, y=None):
    if y is None:
        ax = np.asarray([ z[0] for z in x ], 'float64')
        ay = np.asarray([ z[1] for z in x ], 'float64')
    else:
        ax = np.asarray(x, 'float64')
        ay = np.asarray(y, 'float64')

    return create_TGraph(ax[:], ay[:])


def guess_binning(array):
    xmin = round(np.min(array), 0)
    xmax = round(np.max(array), 0)
    return (100, xmin, xmax)


def array_to_hist(array, nx=100, xmin=None, xmax=None, xbins=None, w=None):

    hist = create_TH1(nx, xmin, xmax, xbins)
    if w is not None:
        for x, w in zip(array, w):
            hist.Fill(x, w)
    else:
        for x in array:
            hist.Fill(x)

    return hist


def array_to_hist2d(array):

    nx, ny = array.shape

    hist = create_TH2(nx, 0, ny, nx, 0, ny)

    for x in range(nx):
        for y in range(ny):
            hist.SetBinContent(x+1, y+1, array[x,y])

    return hist
