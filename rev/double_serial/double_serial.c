#include <stdio.h>
#include <string.h>
#include "b64.h"    // https://github.com/littlstar/b64.c

int flag_enc[72] = {35, 82, 26, 88, 3, 121, 31, 7, 6, 95, 88, 47, 14, 44, 58, 15, 49, 102, 104, 35, 60, 14, 100, 80, 63, 12, 42, 28, 4, 1, 84, 44, 38, 1, 0, 4, 50, 102, 108, 44, 18, 103, 9, 88, 63, 13, 42, 17, 6, 41, 35, 54, 38, 103, 81, 15, 37, 88, 119, 103, 63, 85, 18, 73, 61, 85, 20, 90, 1, 60, 80, 100};

int check(char p1[20], char p2[20]){
    int x;
    int res;

    if(strlen(p1) != 20 || strlen(p2) != 20){
        return 0;
    }
    if((int)p1[7] != 45 || (int)p1[12] != 45 || (int)p1[16] != 45){
        return 0;
    }

    if((int)p1[0] != 74){
        return 0;
    }
    if((int)p1[1] != 111){
        return 0;
    }
    if((int)p1[2] != 104){
        return 0;
    }
    if((int)p1[3] != 110){
        return 0;
    }
    if((int)p1[4] != 68){
        return 0;
    }
    if((int)p1[5] != (int)p1[1]){
        return 0;
    }
    if((int)p1[6] != (int)p1[3] - 9){
        return 0;
    }
    if((int)p1[8] != (int)p1[7] + 4){
        return 0;
    }
    if((int)p1[9] != (int)p1[8] + 2){
        return 0;
    }
    if((int)p1[10] != (int)p1[9]){
        return 0;
    }
    if((int)p1[11] != (int)p1[9] + 4){
        return 0;
    }
    if((int)p1[13] != (int)p1[8] + 3){
        return 0;
    }
    if((int)p1[14] != (int)p1[8] + 1){
        return 0;
    }
    if((int)p1[15] != (int)p1[8] - 1){
        return 0;
    }

    if((int)p2[17] != 116){
        return 0;
    }
    if((int)p2[18] != (int)p2[17] + 3){
        return 0;
    }
    if((int)p2[19] != 60){
        return 0;
    }

    for(int i = 0; i < strlen(p1); i++){
        x = (int)p2[i];
        res = (32*(x-17)) % 127;
        if(res != (int)p1[i]){
            return 0;
        }
    }
    return 1;
}

void get_flag(char p1[20], char p2[20]){
    char key[20];
    char result[72];

    for(int i = 0; i < 20; i++){
        key[i] = (int)p1[i] ^ (int)p2[i];
    }

    for(int i = 0; i < 72; i++){
        result[i] = (char)(flag_enc[i] ^ key[i%20]);
    }

    char *dec = b64_decode(result, 72);
    printf("%s\n", dec);
}

int main(void){
    char p1[20];
    char p2[20];
    printf("%s","Serial #1: ");
    scanf("%s",p1);
    printf("%s","Serial #2: ");
    scanf("%s",p2);
    int res = check(p1,p2);
    if(res){
        printf("%s","Welcome, here is your flag: ");
        get_flag(p1,p2);
    }
    else{
        puts("YOU SHALL NOT PASS!!!");
    }
}