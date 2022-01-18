#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "./utils/array.h"
#include "./utils/inputs.h"

int min_3(int a, int b, int c) {
    if (b < a)
        a = b;
    if (c < a)
        a = c;
    return a;
}

int** lev_array(char* previous, char* current, size_t previous_size, size_t current_size) {
    int m = previous_size + 1;
    int n = current_size + 1;
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
    size_t previous_size = strlen(previous);
    size_t current_size = strlen(current);
    printf("%ld\n", current_size);
    if (previous_size == 0) {
        for (int i = current_size - 1; i >= 0; i--) {
            printf("A%c%d", current[i], i);
        }
        return;
    } else if (current_size == 0) {
        for (int i = previous_size - 1; i >= 0; i--) {
            printf("S%c%d", previous[i], 0);
        }
        return;
    }
    int** arr = lev_array(previous, current, previous_size, current_size);
    int i = previous_size;
    int j = current_size;
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
    destroy_array(arr, current_size + 1);
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
