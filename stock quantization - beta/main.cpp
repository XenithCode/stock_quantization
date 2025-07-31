#include"stock.h"
#include"user.h"

int main()
{
    user current_user(-1,"name" , "password" , "email" , 1234567890 , 0.0);
	while (true)
	{
		int choice;
        std::cout << "1. Login" << std::endl;
        std::cout << "2. Register" << std::endl;
		std::cout << "3. Exit" << std::endl;
        std::cout << "Enter your choice: ";
        std::cin >> choice;

        switch (choice)
        {
        case 1:
            current_user.login();
            break;
        case 2:
            current_user.Register();
            break;
        case 3:
            return 0;
        default:
            std::cout << "Invalid choice. Please try again." << std::endl;
        }
	}
	return 0;
}