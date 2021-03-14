#include <stdio.h>

int main(){
  int fd1 = open("flag.txt", 0, 0);
  char buf[0x20];

  read(3, buf, 0x20);
  printf("%s\n", buf);
  printf("%d\n", fd1);
  return 0;
}