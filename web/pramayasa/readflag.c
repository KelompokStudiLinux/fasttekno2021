#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>

int main() {
  char f = open("./flag.txt", 0);

  setuid(getuid());

  char *args[] = {"sh", 0};
  execvp("/bin/sh", args);
  return 0;
}
