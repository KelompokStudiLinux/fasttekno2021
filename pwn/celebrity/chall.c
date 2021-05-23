#include <stdio.h>
#include <stdlib.h>

int mishell(){
  char prm[0x10] = "/bin/sh";

  system(&prm);
  return 0;
}

void initialization()
{
	setvbuf(stdin,0,2,0);
	setvbuf(stdout,0,2,0);
	setvbuf(stderr,0,2,0);
}

int main(){
  initialization();
  char buf[0x20];
  gets(buf);

  return 0;
}
