#include "stock.h"
#include <iostream>
#include <fstream>
#include <ctime>

// log function
void log_message(const std::string& message) {
    std::ofstream logfile("cout.log", std::ios::app);
    if (logfile.is_open()) {
        time_t now = time(0);
        char* dt = ctime(&now);
        dt[strlen(dt) - 1] = '\0'; // remove newline
        logfile << "[" << dt << "] " << message << std::endl;
        logfile.close();
    }
}

stock::stock() : company("No Name"), shares(0), share_val(0.0), total_val(0.0) {}
stock::stock(const std::string& co, long n, double pr) : company(co) {
    acquire(co, n, pr);
}
stock::~stock() {}

void stock::acquire(const std::string& co, long n, double pr) {
    company = co;
    if (n < 0) {
        try {
            throw "Error: Negative value";
        }
        catch (const char* msg) {
            log_message(msg);
        }
		shares = 0;
    }
    else {
        shares = n;
        share_val = pr;
        set_tot();
    }
}

void stock::buy(double price, long num) {
    if (num < 0) {
        try {
            throw "Error: Negative value";
        }
        catch (const char* msg) {
            log_message(msg);
        }
    }
    else {
        shares += num;
        share_val = price;
        set_tot();
    }
}

void stock::sell(double price, long num) { 
    if (num < 0) {
        try {
            throw "Error: Negative value";
        }
        catch (const char* msg) {
            log_message(msg);
        }
    }
    else if (num > shares) {
        try {
            throw "Error: Not enough shares";
        }
        catch (const char* msg) {
            log_message(msg);
        }
    }
    else {
        shares -= num;
        share_val = price;
        set_tot();
    }
}

void stock::update(double price) {
    share_val = price;
    set_tot();
}

void stock::show() const {
    std::cout << "Company: " << company
        << " Shares: " << shares
        << " Share Price: $" << share_val
        << " Total Worth: $" << total_val << std::endl;
}