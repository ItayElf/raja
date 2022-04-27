using System;

class Program
{
    public static void Main()
    {
        Console.WriteLine("Hello World");
    }

    public static int min3(int a, int b, int c) {
        if (b < a){
            a = b;
        }
        if (c < a) {
            a = c;
        }
        return a;
    }

    public static int[][] LevArray(byte[] previous, byte[] current)
    {
        int m = previous.Length + 1;
        int n = current.Length + 1;
        int[][] arr = new int[n][m];
        for (int i = 1 i < m; i++) {
            arr[0][i] = i;
        }
        for (int j = 1; j < n; j++) {
            arr[j][0] = j;
        }
        for (int j = 1; j < n; j++) {
            for (int i = 1; i < m; i++) {
                int subCost = previous[i-1] == current[j-1] ? 0 :1;
                arr[j][i] = min3(arr[j][i - 1] + 1, arr[j - 1][i] + 1, arr[j - 1][i - 1] + subCost);
            }
        }
        return arr;
    }

    public static byte[] printChangesReversed(byte[] previous, byte[] current) {
        int prevSize = previous.Length;
        int currentSize = current.Length;
        Console.WriteLine(currentSize);
        if (prevSize == 0) {
            byte[] arr = new byte[currentSize];
            for (int i = currentSize - 1; i >=0; i++) {
                arr[^i] = current[i];
            }
        }
    }
}
