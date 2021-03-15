#include <stdio.h>
#include <stdlib.h>

char *chunks[12];
unsigned int sizes[12];

void init(){
  setvbuf(stdin, 0, 2 ,0);
  setvbuf(stdout, 0, 2 ,0);
  setvbuf(stderr, 0, 2 ,0);
}

int get_int(){
  char buf[16];
  return atoi(fgets(buf, 16, stdin));
}

void create(){
  printf("Index: ");
  int idx = get_int();
  if(idx < 0 || idx > 12) puts("Invalid index");
  else if(chunks[idx]) puts("Index already allocated");
  else{
    printf("Size: ");
    if((sizes[idx] = (unsigned int)get_int()) > 0x100) puts("Invalid size");
    else{
      chunks[idx] = (char *)malloc(sizes[idx]);
      printf("Fill the chunk: ");
      chunks[idx][read(0, chunks[idx], sizes[idx])] = 0;
      puts("Chunk created");
    }
  }
}

void delete(){
  printf("Index: ");
  int idx = get_int();
  if(idx < 0 || idx > 12) puts("Invalid index");
  else if(!chunks[idx]) puts("Index is not allocated");
  else{
    free(chunks[idx]);
    puts("Chunk deleted");
  }
}

void show(){
  printf("Index: ");
  int idx = get_int();
  if(idx < 0 || idx > 12) puts("Invalid index");
  else if(!chunks[idx]) puts("Index is not allocated");
  else printf("Content: %.*s\n", sizes[idx], chunks[idx]);
}

void edit(){
  printf("Index: ");
  int idx = get_int();
  if(idx < 0 || idx > 12) puts("Invalid index");
  else if(!chunks[idx]) puts("Index is not allocated");
  else {
    printf("Edit the chunk: ");
    chunks[idx][read(0, chunks[idx], sizes[idx])] = 0;
    puts("Chunk edited");
  }
}

void menu(){
  puts("This is a heap challenge");
  puts("1. Alloc");
  puts("2. Edit");
  puts("3. Free");
  puts("4. Print");
  puts("5. Exit");
}

int main(){
  int choice;
  init();
  menu();
  while(1){
    printf(">> ");
    switch(choice = get_int()){
      case 1:
        create();
        break;
      case 2:
        edit();
        break;
      case 3:
        delete();
        break;
      case 4:
        show();
        break;
      default:
        puts("Invalid choice!");
        break;
    }
  }
}