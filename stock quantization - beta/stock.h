#pragma once
#ifndef STOCK_H_
#define STOCK_H_

#include<string>

class stock 
{
	private:
		std::string company;
		long shares;
		double share_val;
		double total_val;
		inline void set_tot() {
			total_val = shares * share_val;
		}
	public:
		stock();
		stock(const std::string& co, long n = 0, double pr = 0.0);
        ~stock();
		void acquire(const std::string& co, long n, double pr);
        void buy(double price, long num);
        void sell(double price, long num);
        void update(double price);
        void show() const;
		const stock & topval(const stock & s) const {
			return (s.total_val > total_val) ? s : *this;
		}
};

#endif