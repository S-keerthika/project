#include<stdio.h>
int main(){
      int number1, number2, sum;
    
    printf("Enter first integers: ");
    scanf("%d", &number1);
    printf("Enter second integers: ");
    scanf("%d", &number2);
    // calculating sum
    sum = number1 + number2;      
    
    printf(" sum of %d + %d = %d", number1, number2, sum);
    return 0;
}
