output: dh.o ./utils/array.o
	gcc -g dh.o ./utils/array.o -o dh_lin.exe

dh.o: dh.c
	gcc -c dh.c

./utils/array.o: utils/array.c ./utils/array.h
	gcc -c ./utils/array.c -o ./utils/array.o

clean:
	rm *.o ./utils/*.o dh_lin.exe