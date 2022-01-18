#include "inputs.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* read_file(char* filename) {
    FILE* f = fopen(filename, "rb");
    if (!f) {
        printf("Couldn't open file named %s.\n", filename);
        return malloc(sizeof(char));
    }
    fseek(f, 0, SEEK_END);
    size_t len = (size_t)ftell(f);
    fseek(f, 0, SEEK_SET);
    char* str = malloc(sizeof(char) * (len + 1));
    fread(str, len, 1, f);
    // unsigned long new_len = len;
    // while (new_len > 0 && new_len <= len) {
    //     char temp[255];
    //     fgets(temp, 255, f);
    //     strcat(str, temp);
    //     new_len = len - strlen(str);
    // }
    fclose(f);
    str[len] = '\0';
    return str;
}

// char* read_str_with_len() {
//     int str_len;
//     scanf("%d\n", &str_len);
//     char* str = (char*)(malloc(sizeof(char) * (str_len + 1)));
//     for (int i = 0; i < str_len; i++) {
//         str[i] = 0;
//     }
//     if (str_len != 0) {
//         char temp;
//         int i;
//         for (i = 0; i < str_len; i++) {
//             temp = getchar();
//             str[i] = temp;
//         }
//         str[i] = '\0';
//     }
//     return str;
// }

char* read_str_with_len() {
    size_t str_len;
    scanf("%ld\n", &str_len);
    char* str = malloc(sizeof(char) * (str_len + 1));
    // for (int i = 0; i < str_len; i++) {
    //     str[i] = 0;
    // }
    if (str_len != 0) {
        fread(str, str_len, 1, stdin);
    }
    str[str_len] = '\0';
    return str;
}