#include "./array.h"

#include <stdio.h>
#include <stdlib.h>

int** create_2d_array(int rows, int cols) {
    int** arr = malloc(rows * sizeof(int*));
    for (int i = 0; i < rows; i++) {
        arr[i] = calloc(cols, sizeof(int));
        for (int j = 0; j < cols; j++) {
            arr[i][j] = 0;
        }
    }
    return arr;
}

void print_2d_array(int** arr, int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%d ", arr[i][j]);
        }
        printf("\n");
    }
}

void destroy_array(int** arr) {
    free(*arr);
    free(arr);
}