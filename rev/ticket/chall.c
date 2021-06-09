#include <stdio.h>
#include <string.h>

int check(char* serial){
    // m = [5,11,17,23]
    int score = 0;
    if(strlen(serial) == 31){
        score++;
    }
    if((int)(serial[5]) == 45 && (int)(serial[11]) == 45 && (int)(serial[17]) == 45 && (int)(serial[23]) == 45){
        score++;
    }
    if((int)(serial[0]) * (int)(serial[15]) - (int)(serial[1]) == 6132){
        score++;
    }
    if((int)(serial[3]) + 1220 == 1337){
        score++;
    }
    if((int)(serial[4]) - (int)(serial[15]) == 20){
        score++;
    }
    if(((int)(serial[6]) ^ (int)(serial[7])) == 35){
        score++;
    }
    if((int)(serial[7]) * (int)(serial[0]) - (int)(serial[13]) == 7424){
        score++;
    }
    if((int)(serial[8]) == 114){
        score++;
    }
    if((int)(serial[9]) * (int)(serial[9]) + (int)(serial[24]) == 13761){
        score++;
    }
    if((int)(serial[10]) * (int)(serial[12]) - (int)(serial[10]) == 4182){
        score++;
    }
    if(((int)(serial[12]) ^ ((int)(serial[30])) + (int)(serial[20])) == 231){
        score++;
    }
    if((((int)(serial[16]) ^ (int)(serial[0])) ^ (int)(serial[13])) == 10){
        score++;
    }
    if((int)(serial[18]) + (int)(serial[20]) - (int)(serial[22]) == (int)(serial[6])){
        score++;
    }
    if((int)(serial[19]) - (int)(serial[10]) == (int)(serial[29]) - 9){
        score++;
    }
    if(((int)(serial[21]) & (int)(serial[25])) == 68){
        score++;
    }
    if((int)(serial[26]) + (int)(serial[27]) == 162){
        score++;
    }
    if(((int)(serial[28]) ^ 13) == 84){
        score++;
    }
    if((int)(serial[29]) - (int)(serial[30]) + 81 == 69){
        score++;
    }
    if((int)(serial[0]) * 2 + 2 == 180){
        score++;
    }
    if((int)(serial[2]) * (int)(serial[13]) + (int)(serial[23]) == 3945){
        score++;
    }
    if((int)(serial[10]) + (int)(serial[12]) == 134){
        score++;
    }
    if((int)(serial[9]) + (int)(serial[9]) == 234){
        score++;
    }
    if((int)(serial[19]) + (int)(serial[9]) << 3 == 1792){
        score++;
    }
    if((int)(serial[18]) + 33 == (int)(serial[8])){
        score++;
    }
    if((int)(serial[26]) == 83){
        score++;
    }
    if(((int)(serial[22]) ^ (int)(serial[25])) == 4){
        score++;
    }
    if((int)(serial[2]) == 75){
        score++;
    }
    if((int)(serial[21]) == 102){
        score++;
    }
    if((int)(serial[14]) == (int)(serial[21]) - 2){
        score++;
    }
    if((int)(serial[15]) == 70){
        score++;
    }

    if(score == 30){
        return 1;
    }
    else{
        return 0;
    }
}

int main(){
    char serial[31];
    puts("Welcome, kind stranger..");
    puts("Just give me your ticket, and i'll let you pass...");
    printf("%s","Ticket: ");
    scanf("%s",serial);
    
    // YbKuZ-wTru3-S4dFg-QkgfA-HESOYAM
    if(check(serial)){
        printf("Here is your flag: FastTekno{%s}\n",serial);
    }
    else{
        puts("YOU SHALL NOT PASS!!!!!!!");
    }
}