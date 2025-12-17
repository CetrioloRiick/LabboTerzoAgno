double pippo(double *v, double *par) {
    double x = v[0];
    double iconzero = par[0];
    double etavuti  = par[1];
    return iconzero * (exp(x / etavuti) - 1.0);
}

void fitCaratteristica() {
    std::ifstream file("datiCaratteristicaSilicio2.csv");
    if(!file.is_open()) {
        std::cerr << "Errore apertura file" << std::endl;
        return;
    }

    std::string header;
    std::getline(file, header);  // skip header

    vector<float> vx, vy, sx, sy;

    double V, I, eV, eI;
    char comma;

    while(file >> V >> comma >> eV >> comma >> I >> comma >> eI) {
        vx.push_back(V);
        vy.push_back(I);
        sx.push_back(eV);
        sy.push_back(eI);
    }


    int N = vx.size();
    TGraphErrors *graf = new TGraphErrors(N, vx.data(), vy.data(), sx.data(), sy.data());

 

    // Fit function reinterpreted as a 2D function

    //TF1 *fit = new TF1("f", "[0] * (exp(x/[1]) - 1.0)", 0, 11);
    TF1 *f = new TF1("f", [](Double_t *x, Double_t *par){
                         Double_t xx = x[0];
                         double iconzero = par[0];
                         double etavuti  = par[1];
                         return iconzero * (exp(xx / etavuti) - 1.0);
                     },0, 250, 2);

    f->SetParameter(0, 1.0);  // iconzero
    f->SetParameter(1, 60.0); // etavuti

    // Perform full Minuit fit
    graf->Fit(f);

    double iconzero_fit = f->GetParameter(0);
    double etavuti_fit  = f->GetParameter(1);
    double err_iconzero = f->GetParError(0);
    double err_etavuti  = f->GetParError(1);

    std::cout << "\n--- Risultati fit ---\n";
    std::cout << "iconzero = " << iconzero_fit 
              << " +/- " << err_iconzero << std::endl;
    std::cout << "etavuti  = " << etavuti_fit
              << " +/- " << err_etavuti << std::endl;

    // Plot
    TCanvas *c1 = new TCanvas("c1", "Fit I-V", 900, 600);
    graf->Draw();
    f->SetLineColor(kRed);
    f->Draw("same");
}
