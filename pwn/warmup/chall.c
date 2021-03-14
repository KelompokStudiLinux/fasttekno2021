#include <stdio.h>
#include <stdlib.h>

int init(){
  setvbuf(stdin,0,2,0);
	setvbuf(stdout,0,2,0);
	setvbuf(stderr,0,2,0);
	alarm(30);
}

int main(){
  char buf[0x48];
  init();
  read(0, buf, 0xa);
  printf(buf);
  for(int i = 0; i < 2; i ++){
    read(0, buf, 0x48);
    printf("Echo: ");
    printf(buf);
  }

  return 0;
}