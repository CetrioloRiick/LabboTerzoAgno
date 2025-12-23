struct diegoData{
    vector<float> vx, vy, sx, sy;
};
diegoData getData(string nomeFile){
    std::ifstream file(nomeFile);
    if(!file.is_open()) {
        std::cerr << "Errore apertura file" << std::endl;
    }

    std::string header;
    std::getline(file, header);  // skip header

    diegoData pippo;
    
    double V, I, eV, eI;
    char comma;

    while(file >> V >> comma >> eV >> comma >> I >> comma >> eI) {
        pippo.vx.push_back(V);
        pippo.vy.push_back(I);
        pippo.sx.push_back(eV);
        pippo.sy.push_back(eI);
    }
    return pippo;
}
void fitog() {
    gStyle->SetOptStat(0);
gStyle->SetOptFit(0);
gStyle->SetTitleFont(42, "XYZ");
gStyle->SetLabelFont(42, "XYZ");
gStyle->SetTitleSize(0.05, "XYZ");
gStyle->SetLabelSize(0.045, "XYZ");
gStyle->SetPadGridX(true);
gStyle->SetPadGridY(true);
gStyle->SetGridStyle(3);

TCanvas *c1 = new TCanvas("c1","IV characteristics",2400,1800);
c1->SetLeftMargin(0.12);
c1->SetBottomMargin(0.12);
c1->SetRightMargin(0.05);
c1->SetTopMargin(0.08);
c1->SetLogy();


    diegoData SIL{getData("datiSnoZeros.csv")};
    diegoData GER{getData("datiGnoZeros.csv")};


    TGraphErrors *Sgraf = new TGraphErrors(SIL.vx.size(), SIL.vx.data(), SIL.vy.data(), SIL.sx.data(), SIL.sy.data());
    Sgraf->SetMarkerStyle(20);
    Sgraf->SetMarkerColor(kRed);
    Sgraf->SetLineColor(kRed);

    TF1 *Sf = new TF1("Sf", [](Double_t *x, Double_t *par){
                         Double_t xx = x[0];
                         double iconzero = par[0];
                         double etavuti  = par[1];
                         return iconzero * (exp(xx / etavuti) - 1.0);
                     },0, 250, 2);
    Sf->SetParameter(0, 1.0);  // iconzero
    Sf->SetParameter(1, 60.0); // etavuti
    Sf->SetLineColor(kPink-4);
    Sf->SetLineWidth(3);
    

    TGraphErrors *Ggraf = new TGraphErrors(GER.vx.size(), GER.vx.data(), GER.vy.data(), GER.sx.data(), GER.sy.data());
    Ggraf->SetMarkerStyle(21);
    Ggraf->SetMarkerColor(kBlue);
    Ggraf->SetLineColor(kBlue);
    TF1 *Gf = new TF1("Gf", [](Double_t *x, Double_t *par){
                         Double_t xx = x[0];
                         double iconzero = par[0];
                         double etavuti  = par[1];
                         return iconzero * (exp(xx / etavuti) - 1.0);
                     },0, 250, 2);
    Gf->SetParameter(0, 1.0);  // iconzero
    Gf->SetParameter(1, 60.0); // etavuti
    Gf->SetLineColor(kAzure-4);
    Gf->SetLineWidth(3);



    TMultiGraph *mg = new TMultiGraph();
    mg->Add(Sgraf);
    mg->Add(Ggraf);

    mg->SetTitle(";V [mV];I [100#muA]");
 mg->SetMinimum(1e-3);   // oppure 1e-6, dipende dalla scala dei dati
    mg->Draw("AP");

    mg->GetXaxis()->CenterTitle();
mg->GetYaxis()->CenterTitle();

mg->GetXaxis()->SetTitleOffset(1.1);
mg->GetYaxis()->SetTitleOffset(1.2);

mg->SetMinimum(0);

Sgraf->SetMarkerSize(1.2);
Sgraf->SetLineWidth(2);

Ggraf->SetMarkerSize(1.2);
Ggraf->SetLineWidth(2);
    Sgraf->Fit(Sf);

    double iconzero_fit = Sf->GetParameter(0);
    double etavuti_fit  = Sf->GetParameter(1);
    double err_iconzero = Sf->GetParError(0);
    double err_etavuti  = Sf->GetParError(1);

    std::cout << "\n--- Risultati fit ---\n";
    std::cout << "iconzero = " << iconzero_fit 
              << " +/- " << err_iconzero << std::endl;
    std::cout << "etavuti  = " << etavuti_fit
              << " +/- " << err_etavuti << std::endl;


    Ggraf->Fit(Gf);
    iconzero_fit = Gf->GetParameter(0);
    etavuti_fit  = Gf->GetParameter(1);
    err_iconzero = Gf->GetParError(0);
    err_etavuti  = Gf->GetParError(1);

    std::cout << "\n--- Risultati fit ---\n";
    std::cout << "iconzero = " << iconzero_fit 
              << " +/- " << err_iconzero << std::endl;
    std::cout << "etavuti  = " << etavuti_fit
              << " +/- " << err_etavuti << std::endl;
  
            gSystem->Setenv("ROOT_USE_CAIRO","1");
c1->Print("plot.pdf");
            }
