#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstdlib>
#include <vector>
#include <algorithm>

using namespace std;

struct nyc {
    vector<vector<unsigned> > m_count;
    
    nyc() {
        m_count.resize(100);
        for(auto &i : m_count) {
            i.resize(100);
        }
    }
    
    void print() {
        for(auto &i : m_count) {
            for(auto &j : i) {
                cout << j << "\t";
            }
            cout << endl;
        }
    }
    
    void fprint(string file) {
        ofstream fout;
        fout.open(file);
        for(auto &i : m_count) {
            for(auto &j : i) {
                fout << j << "\t";
            }
            fout << endl;
        }
    }
    
};

vector<nyc> mapByHours;

void fileParse(const string dataset) {
    ifstream instream;
    instream.open(dataset.c_str());
    if(!instream.is_open()) {
        throw std::runtime_error(string("Could not open file ") + dataset);
    }
    
    string line;
    
    nyc* iterator = new nyc;
    double lat, lon;
    char pipe;
    while(getline(instream, line)) {
    
        if(line.find("rows") == string::npos){
            if (line.find("--") != string::npos || line.find("pick") != string::npos) continue;
            
            stringstream ss(line);
            ss >> lat >> pipe >> lon;
            
            unsigned y_index = ((lat - 40.484496) / 0.004356);
            unsigned x_index = ((lon + 74.268148) / 0.005822);
            
            iterator->m_count.at(x_index).at(y_index) += 1;
        }
        else{
            //iterator->print();
            mapByHours.push_back(*iterator);
            iterator = new nyc;
        }
    }
    
    for(auto &i : mapByHours) {
        string file = "map_hour_";
        for (int j = 0; j < mapByHours.size(); j++)
            i.fprint(file + to_string(j));
    }
}


int main(int argc, char * argv[]) {
    
    string dataset = argv[1];
    
    fileParse(dataset);
    
    return 0;
}