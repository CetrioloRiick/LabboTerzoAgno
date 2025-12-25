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
void calibration(){
    gStyle->SetPadGridX(true);
    gStyle->SetPadGridY(true);
    gStyle->SetGridStyle(3);
    diegoData CAL{getData("datiCalibrazione.csv")};
    TGraphErrors *g = new TGraphErrors(CAL.sx.size(), CAL.vx.data(), CAL.vy.data(), CAL.sx.data(), CAL.sy.data());
    g->SetMarkerStyle(20);
    g->SetMarkerColor(kGreen+1);
    g->SetLineColor(kGreen+1);

    
    TF1 *f = new TF1("f", "[0]+[1]*x", 0, 600);
    f->SetLineColor(kGreen-4);
    f->SetLineWidth(3);

    g->SetTitle(";V (mv);V (mv)");
    g->Draw("AP");
    g->Fit(f);
}