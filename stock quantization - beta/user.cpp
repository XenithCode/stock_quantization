#include "user.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <functional>
#include <ctime>

// password hashing function
std::string hash_password(const std::string& password) {
    std::hash<std::string> hasher;
    return std::to_string(hasher(password));
}

// primary key generator
int generate_primary_key() {
    std::ifstream infile("user.sq");
    int last_key = 0;
    std::string line;
    while (std::getline(infile, line)) {
        std::istringstream iss(line);
        int key;
        iss >> key;
        if (key > last_key) last_key = key;
    }
    return last_key + 1;
}

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

// registration function
int user::Register() {
    std::cin>>user_name>>user_password>>user_email>>user_phone_number;
    int primary_key = generate_primary_key();
    std::ofstream outfile{ "user.sq", std::ios::app };
    if (!outfile) {
        log_message("Error: cannot open file for registration");
        return -1;
    }
    outfile << primary_key << " " << user_name << " "
        << hash_password(user_password) << " "
        << user_email << " " << user_phone_number << std::endl;
    if (!outfile) {
        log_message("Error: failed to write to file during registration");
        return -1;
    }
    outfile.close();
    return 0;
}

// login function
int user::Login(const std::string& username, const std::string& user_password) {
    std::ifstream infile{ "user.sq" };
    if (!infile) {
        log_message("Error: cannot open file");
        return -1;
    }
    std::string line;
    std::string hashed_input = hash_password(user_password);
    while (std::getline(infile, line)) {
        std::istringstream iss(line);
        int primary_key;
        std::string name, password, email;
        long long phone_number;
        iss >> primary_key >> name >> password >> email >> phone_number;
        if (username == name && password == hashed_input) {
            infile.close();
            return 0;
        }
    }
    infile.close();
    return -1;
}

int user::login()
{
    int check;
    std::string username, user_password;
    std::cin >> username >> user_password;
    check = Login(username, user_password);
    if (check == 0) {
        return 0;
    }
    else {
        log_message("Login failed for user: " + username);
        return -1;
    }
}