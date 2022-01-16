#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "./utils/array.h"

int min_3(int a, int b, int c) {
    if (b < a)
        a = b;
    if (c < a)
        a = c;
    return a;
}

int** lev_array(char* previous, char* current) {
    int m = strlen(previous) + 1;
    int n = strlen(current) + 1;
    int** arr = create_2d_array(n, m);
    for (int i = 1; i < m; i++) {
        arr[0][i] = i;
    }
    for (int j = 1; j < n; j++) {
        arr[j][0] = j;
    }
    for (int j = 1; j < n; j++) {
        for (int i = 1; i < m; i++) {
            int sub_cost = 1;
            if (previous[i - 1] == current[j - 1]) {
                sub_cost = 0;
            }
            arr[j][i] = min_3(arr[j][i - 1] + 1, arr[j - 1][i] + 1, arr[j - 1][i - 1] + sub_cost);
        }
    }
    return arr;
}

void print_changes_reversed(char* previous, char* current) {
    if (strlen(previous) == 0) {
        for (int i = strlen(current) - 1; i >= 0; i--) {
            printf("A%c%d", current[i], i);
        }
        return;
    } else if (strlen(current) == 0) {
        for (int i = strlen(previous) - 1; i >= 0; i--) {
            printf("S%c%d", previous[i], 0);
        }
        return;
    }
    int** arr = lev_array(previous, current);
    int i = strlen(previous);
    int j = strlen(current);
    int corner, top, left;

    while (i >= 0 && j >= 0 && i + j > 0) {
        corner = i * j != 0 ? arr[j - 1][i - 1] : INT_MAX;
        top = j != 0 ? arr[j - 1][i] : INT_MAX;
        left = i != 0 ? arr[j][i - 1] : INT_MAX;

        int min = min_3(corner, top, left);
        if (min == corner) {
            if (previous[i - 1] != current[j - 1]) {
                printf("R%c%c%d", current[j - 1], previous[i - 1], i - 1);
            }
            i--;
            j--;
        } else if (min == top) {
            printf("A%c%d", current[j - 1], i);
            j--;
        } else if (min == left) {
            printf("S%c%d", previous[i - 1], i - 1);
            i--;
        }
    }
    printf("\n");
    destroy_array(arr);
}

char* read_str_with_len() {
    int str_len;
    scanf("%d\n", &str_len);
    char* str = (char*)(malloc(sizeof(char) * (str_len + 1)));
    for (int i = 0; i < str_len; i++) {
        str[i] = 0;
    }
    if (str_len != 0) {
        char temp;
        int i;
        for (i = 0; i < str_len; i++) {
            temp = getchar();
            str[i] = temp;
        }
        str[i] = '\0';
    }
    return str;
}

char* read_file(char* filename) {
    FILE* f = fopen(filename, "rb");
    if (!f) {
        printf("Couldn't open file named %s.\n", filename);
        return malloc(sizeof(char));
    }
    fseek(f, 0, SEEK_END);
    unsigned long len = (unsigned long)ftell(f);
    fclose(f);
    f = fopen(filename, "rb");
    char* str = malloc(sizeof(char) * len);
    unsigned long new_len = len;
    while (new_len > 0 && new_len <= len) {
        char temp[255];
        fgets(temp, 255, f);
        strcat(str, temp);
        new_len = len - strlen(str);
    }
    fclose(f);
    return str;
}

void handle_cli(int argc, char** args) {
    if (argc == 3) {
        char* prev = read_file(args[1]);
        char* curr = read_file(args[2]);
        print_changes_reversed(prev, curr);
        free(prev);
        free(curr);
    } else if (argc == 2) {
        char* prev = read_str_with_len();
        char* curr = read_file(args[1]);
        print_changes_reversed(prev, curr);
        free(prev);
        free(curr);
    } else {
        char* prev = read_str_with_len();
        char* curr = read_str_with_len();
        print_changes_reversed(prev, curr);
        free(prev);
        free(curr);
    }
}

int main(int argc, char** args) {
    handle_cli(argc, args);
    return 0;
}
