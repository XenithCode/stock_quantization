#pragma once
#include <string>
#include <iostream>

#ifndef USER_H
#define USER_H

class user
{
private:
    int id;
    std::string user_name;
    std::string user_password;
    std::string user_email;
    long long user_phone_number;
    double balance;
public:
    user(int id, const std::string& user_name, const std::string& user_password,
        const std::string& user_email, long long user_phone_number, double balance)
        : id(id), user_name(user_name), user_password(user_password),
        user_email(user_email), user_phone_number(user_phone_number), balance(balance) {
    }
   ~user() {}

    int Register();
    int Login(const std::string& username, const std::string& user_password);
    int login();
    std::string GetUserName() const { return user_name; }
    std::string GetUserPassword() const { return user_password; }
};

#endif