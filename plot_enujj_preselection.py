import os , math, copy
import ROOT as r
from numpy import array

def setStyle ( plot, color, style, width ) :
    plot.SetLineColor( color ) 
    plot.SetFillColor( color ) 
    plot.SetFillStyle( style ) 
    plot.SetLineWidth( width )
    return

def rebin ( plot, bins ) :
    n_bins    = len ( bins ) - 1
    bin_array = array ( bins, dtype=float ) 
    new_name  = plot.GetName() + "_rebin"
    new_plot  = plot.Rebin ( n_bins, new_name, bin_array ) 
    return new_plot

def makeSafe ( plot ) :
    n_bins = plot.GetNbinsX()
    for i in range ( 1, n_bins + 1 ):
        old_content = plot.GetBinContent(i)
        if old_content > 0. and old_content < 0.0001:
            plot.SetBinContent(i, 0. )
            plot.SetBinError  (i, 0. )
    

masses = [ 450, 650 ]
mass_colors = [ 28, 38 ]

vars     = [ 
    "sT_PAS",
    "Mej_PAS"
] 

x_labels = [ 
    "S_{T}^{e #nu j j} [GeV]",
    "M^{e j} [GeV]"
]

x_bins = [ 
    [300, 330, 370, 420, 480, 550, 630, 720, 820, 930, 1050, 1180, 1320, 1470, 1630, 1800, 1980, 2170, 2370, 2580, 2800, 3000],
    [0, 25, 55, 90, 130, 175, 225, 280, 340, 405, 475, 550, 630, 715, 805, 900, 1000, 1105, 1215, 1330, 1450, 1575, 1705, 1840, 1980]
]

r.gROOT.SetStyle('Plain')
r.gStyle.SetTextFont ( 42 );
r.gStyle.SetTitleFont ( 42, "XYZ" );
r.gStyle.SetLabelFont ( 42, "XYZ" );
r.gStyle.SetOptTitle(0);
r.gStyle.SetOptStat(0);

r.gStyle.SetPadTopMargin(0.1);
r.gStyle.SetPadBottomMargin(0.16);
r.gStyle.SetPadLeftMargin(0.12);
r.gStyle.SetPadRightMargin(0.1);

mass1 = 450
mass2 = 650

bkgd_file = r.TFile(os.environ["LQDATA"] + "/enujj_analysis/enujj/scaled_output_cutTable_lq_enujj_MT/analysisClass_lq_enujj_MT_plots.root" )
qcd_file  = r.TFile(os.environ["LQDATA"] + "/enujj_analysis/enujj_qcd/output_cutTable_lq_enujj_MT/analysisClass_lq_enujj_MT_QCD_plots.root")

for i_var, var in enumerate(vars):

    wjets_hist = bkgd_file.Get( "histo1D__WJet_Madgraph__"     + var  )
    ttbar_hist = bkgd_file.Get( "histo1D__TTbar_Madgraph__"    + var  )
    other_hist = bkgd_file.Get( "histo1D__OTHERBKG__"          + var  )
    qcd_hist   = qcd_file .Get( "histo1D__DATA__"              + var  )
    data_hist  = bkgd_file.Get( "histo1D__DATA__"              + var  )
    sig1_hist  = bkgd_file.Get( "histo1D__LQ_M"+str(mass1)+"__" + var )
    sig2_hist  = bkgd_file.Get( "histo1D__LQ_M"+str(mass2)+"__" + var )

    wjets_hist = rebin ( wjets_hist, x_bins[i_var] )
    ttbar_hist = rebin ( ttbar_hist, x_bins[i_var] )
    other_hist = rebin ( other_hist, x_bins[i_var] )
    qcd_hist   = rebin ( qcd_hist  , x_bins[i_var] )
    data_hist  = rebin ( data_hist , x_bins[i_var] )
    sig1_hist  = rebin ( sig1_hist  , x_bins[i_var] )
    sig2_hist  = rebin ( sig2_hist  , x_bins[i_var] )

    setStyle (wjets_hist, 6 , 3007, 2)
    setStyle (ttbar_hist, 4 , 3005, 2)
    setStyle (other_hist, 3 , 3006, 2)
    setStyle (qcd_hist  , 7 , 3004, 2)
    setStyle (sig1_hist , 28,    0, 3)
    setStyle (sig2_hist , 38,    0, 3)
    setStyle (data_hist , 1 ,    0, 1)

    data_hist.SetMarkerStyle(20)
    data_hist.SetMarkerSize (0.7)
    
    stack = r.THStack ("stack", "stack")
    stack.Add ( qcd_hist   );
    stack.Add ( other_hist );
    stack.Add ( ttbar_hist );
    stack.Add ( wjets_hist );
    stack.Draw();
    stack.SetMaximum(20000000);
    stack.SetMinimum(0.1);

    stack.GetXaxis().SetTitle( x_labels [i_var] )
    stack.GetYaxis().SetTitle( "Events/Bin" )
    stack.GetXaxis().CenterTitle()
    stack.GetYaxis().CenterTitle()

    stack.GetHistogram().GetXaxis().SetLabelOffset(0.007)
    stack.GetHistogram().GetYaxis().SetLabelOffset(0.007)
    stack.GetHistogram().GetXaxis().SetLabelSize(0.05)
    stack.GetHistogram().GetYaxis().SetLabelSize(0.05)
    
    stack.GetHistogram().GetXaxis().SetTitleOffset(0.92)
    stack.GetHistogram().GetYaxis().SetTitleOffset(0.92)
    stack.GetHistogram().GetXaxis().SetTitleSize(0.06)
    stack.GetHistogram().GetYaxis().SetTitleSize(0.06)
    stack.GetHistogram().GetXaxis().CenterTitle(1)
    stack.GetHistogram().GetYaxis().CenterTitle(1)
    
    leg = r.TLegend(0.43,0.52,0.89,0.88,"","brNDC");
    leg.SetTextFont(42);
    leg.SetFillColor(0);
    leg.SetBorderSize(0);
    leg.SetTextSize(.05)
    leg.AddEntry(data_hist ,"Data");
    leg.AddEntry(wjets_hist,"W + jets");
    leg.AddEntry(ttbar_hist,"t #bar{t} + jets");
    leg.AddEntry(other_hist,"Other background");
    leg.AddEntry(qcd_hist  ,"QCD");
    leg.AddEntry(sig1_hist  ,"LQ, M = "+str(mass1)+" GeV, #beta = 0.5");
    leg.AddEntry(sig2_hist  ,"LQ, M = "+str(mass2)+" GeV, #beta = 0.5");
    
    sqrts = "#sqrt{s} = 8 TeV";
    l1 = r.TLatex()
    l1.SetTextAlign(12)
    l1.SetTextFont(42)
    l1.SetNDC()
    l1.SetTextSize(0.06)
    
    canv_name = var + "_canv"
    pad_name  = var + "_pad"
    save_name = var + "_enujj.pdf"
    save_name = save_name.replace("PAS","preselection")

    canvas = r.TCanvas(canv_name,canv_name,800,550)
    canvas.cd()
    pad1   = r.TPad( pad_name, pad_name , 0.0, 0.0, 1.0, 1.0 )
    canvas.SetLogy()

    stack.Draw("HIST");
    sig1_hist.Draw("HIST SAME");
    sig2_hist.Draw("HIST SAME");
    data_hist.Draw("SAME");
    leg.Draw()
    l1.DrawLatex(0.18,0.94,"CMS #it{Preliminary}      "+sqrts+", 19.7 fb^{  -1}")
    
    canvas.SaveAs(save_name)

