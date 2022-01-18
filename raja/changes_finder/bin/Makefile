output: dh.o ./utils/array.o ./utils/inputs.o
	gcc -g -O2 -ggdb3 dh.o ./utils/array.o ./utils/inputs.o -o dh_lin.exe

dh.o: dh.c
	gcc -c -ggdb3 dh.c

./utils/array.o: ./utils/array.c ./utils/array.h
	gcc -c -ggdb3 ./utils/array.c -o ./utils/array.o

./utils/inputs.o: ./utils/inputs.c ./utils/inputs.h
	gcc -c -ggdb3 ./utils/inputs.c -o ./utils/inputs.o

clean:
	rm *.o ./utils/*.o dh_lin.exe