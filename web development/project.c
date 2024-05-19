// C program for the above approach
#include <conio.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Defining Structure
typedef struct details {
	char name[20];
	char gen[6];
	int age;
	char email[100];
	char mobile[10];
	char password[100];
	struct mynode* link;
} Node;

struct details s[100];
Node* start = NULL;

void details(int);
int seat(int);
int cal(int, int, int);
int bill(int, int);
void add_node(char lol[20], char der[6], int b);
// Function to get the
// input for new account.
void signup();

// Function to check whether
// the account is already
// existed or not
void account_check();

// Function to validate
// all the input fields.
int validate();
void login();
// Global variables
int flag=1, count = 0, caps = 0;
int small = 0, special = 0, numbers = 0;
int success = 0;
char source[20], des[20], train[40];
char station[40], cla[40];
int time1, time2, a[55], choice, x, i,j=0;
char pass_name[100], pass_password1[100];
char pass_password2[100], pass_email[100];
char pass_mobile[100];
int pass_age, search_choice, confirm;
int main(){
    
    while (1) {
		printf(""
			"\n\nWelcome to Food ");
		printf("Ordering System\n\n1)SIGNUP\n");
		printf("2)LOGIN\n3)EXIT\n\n");
		printf("Enter your choice\t");
		scanf("%d", &choice);
		switch (choice) {
		case 1: {
			signup();
			break;
		}
		case 2: {
			login();
			break;
		}
		case 3: {
			// exit(1);
			return 0;
		}
		default: {
			printf("\nPlease Enter the ");
			printf("valid choice\n");
			break;
		}
		}
	}
}
// Function to create a new
// user for the Food ordering
// system
void signup()
{
	printf("Enter Your name\t");
	scanf("%s", pass_name);

	printf("Enter Your Age\t");
	scanf("%d", &pass_age);

	printf("Enter Your Email\t");
	scanf("%s", pass_email);

	printf("Enter Password\t");
	scanf("%s", pass_password1);

	printf("Confirm Password\t");
	scanf("%s", pass_password2);

	printf("Enter Your Mobile Number\t");
	scanf("%s", pass_mobile);

	// Function Call to validate
	// the user creation
	x = validate();
	if (x == 1)
		account_check();
}

// Function to validate the user
// for signup process
int validate()
{
	// Validate the name
	for (i = 0; pass_name[i] != '\0'; i++) {
		if (!((pass_name[i] >= 'a' && pass_name[i] <= 'z')
			|| (pass_name[i] >= 'A'
				&& pass_name[i] <= 'Z'))) {
			printf("\nPlease Enter the");
			printf("valid Name\n");
			flag = 0;
			break;
		}
	}
	if (flag == 1) {
		count = 0;

		// Validate the Email ID
		for (i = 0;
			pass_email[i] != '\0'; i++) {
			if (pass_email[i] == '@'
				|| pass_email[i] == '.')
				count++;
		}
		if (count >= 2
			&& strlen(pass_email) >= 5) {
			// Validating the Password and
			// Check whether it matches
			// with Conform Password
			if (!strcmp(pass_password1,
						pass_password2)) {
				if (strlen(pass_password1) >= 8
					&& strlen(pass_password1) <= 12) {
					caps = 0;
					small = 0;
					numbers = 0;
					special = 0;
					for (i = 0; pass_password1[i] != '\0';
						i++) {
						if (pass_password1[i] >= 'A'
							&& pass_password1[i] <= 'Z')
							caps++;
						else if (pass_password1[i] >= 'a'
								&& pass_password1[i]
										<= 'z')
							small++;
						else if (pass_password1[i] >= '0'
								&& pass_password1[i]
										<= '9')
							numbers++;
						else if (pass_password1[i] == '@'
								|| pass_password1[i] == '&'
								|| pass_password1[i] == '#'
								|| pass_password1[i]
										== '*')
							special++;
					}
					if (caps >= 1 && small >= 1
						&& numbers >= 1 && special >= 1) {
						// Validating the Input age
						if (pass_age != 0 && pass_age > 0) {
							// Validating the Input mobile
							// number
							if (strlen(pass_mobile) == 10) {
								for (i = 0; i < 10; i++) {
									if (pass_mobile[i]
											>= '0'
										&& pass_mobile[i]
											<= '9') {
										success = 1;
									}
									else {
										printf("\n\nPlease");
										printf("Enter Valid ");
										printf("Mobile "
											"Number\n\n");
										return 0;
										break;
									}
								}

								// Success is assigned with
								// value 1, Once every
								// inputs are correct.
								if (success == 1)
									return 1;
							}
							else {
								printf("\n\nPlease Enter the");
								printf("10 digit mobile");
								printf("number\n\n");
								return 0;
							}
						}
						else {
							printf("\n\nPlease Enter ");
							printf("the valid age\n\n");
							return 0;
						}
					}
					else {
						printf("\n\nPlease Enter the");
						printf("strong password, Your ");
						printf("password must contain ");
						printf("atleast one uppercase, ");
						printf("Lowercase, Number and ");
						printf("special character\n\n");
						return 0;
					}
				}
				else {
					printf("\nYour Password is very");
					printf("short\nLength must ");
					printf("between 8 to 12\n\n");
					return 0;
				}
			}
			else {
				printf("\nPassword Mismatch\n\n");
				return 0;
			}
		}
		else {
			printf("\nPlease Enter"
				" Valid E-Mail\n\n");
			return 0;
		}
	}
}

// Function to check if the account
// already exists or not
void account_check()
{
	for (i = 0; i < 100; i++) {
		// Check whether the email
		// and password are already
		// matched with existed account
		if (!(strcmp(pass_email, s[i].email)
			&& strcmp(pass_password1,
						s[i].password))) {
			printf("\n\nAccount Already");
			printf("Existed. Please Login !!\n\n");
			main();
			break;
		}
	}
	// if account does not already
	// existed, it creates a new
	// one with new inputs
	if (i == 100) {
		strcpy(s[j].name, pass_name);
		s[j].age = pass_age;
		strcpy(s[j].password, pass_password1);
		strcpy(s[j].email, pass_email);
		strcpy(s[j].mobile, pass_mobile);
		j++;
		printf("\n\n\nAccount Successfully");
		printf("Created!!\n\n");
	}
}

// Function to Login the users
void login()
{
	printf("\n\nLOGIN\n\n");
	printf("\nEnter Your Email\t");
	scanf("%s", pass_email);
	printf("Enter Your Password\t");
	scanf("%s", pass_password1);
	for (i = 0; i < 100; i++) {
		// Check whether the input
		// email is already existed or not
		if (!strcmp(s[i].email, pass_email)) {
			// Check whether the password
			// is matched with the email or not
			if (!strcmp(s[i].password, pass_password1)) {
				printf("\n\nWelcome %s, ", s[i].name);
				printf("Your are successfully ");
				printf("logged in\n\nWe Provide ");
				printf("two ways of search\n1) ");
				printf("Search By sleeper seat\n2) ");
				printf("Search by AC seat\n3) ");
				printf("Exit\n\nPlease Enter");
				printf("your choice\t");
				scanf("%d", &search_choice);

				// Getting the input whether
				// the user are going to search
				// /Order by hotels or search/
				// order by food.
				switch (search_choice) {
				case 1: {
					seat();
					break;
				}
				case 2: {
					seat();
					break;
				}
				case 3: {
					// exit(1);
					return;
				}
				default: {
					printf("Please Enter ");
					printf("the valid choice\n\n");
					break;
				}
				}
				break;
			}
			else {
				printf("\n\nInvalid Password! ");
				printf("Please Enter the ");
				printf("correct password\n\n");
				main();
				break;
			}
		}
		else {
			printf("\n\nAccount doesn't ");
			printf("exist, Please signup!!\n\n");
			main();
			break;
		}
	}
}
