#include <stdio.h>
#include <string.h>

int main(){
    char f[29] = "Pk}~^ouxy\x85t\x7f}^i~|>m=iw=ir=r=\x87";    // geser 10
    // int k[4] = {1,2,3,4};
    char inp[29];

    printf("%s","Input: ");
    scanf("%s",inp);

    for(int i=0;i<29;i++){
        f[i] = (char) ((int) f[i] - 10);
    }
    
    if(!strncmp(f,inp,29)){
        printf("%s\n","BANG!!");
    }
    else{
        printf("%s\n","Whoosh...");
    }
}