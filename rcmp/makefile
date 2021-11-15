# builds the C++ scripts with this dir

CXX = g++

output: main.o sender.o
	$(CXX) main.o sender.o -o output

main.o: main.cpp
	$(CXX) -c main.cpp

sender.o: sender.cpp sender.h
	$(CXX) -c sender.cpp

clean:
	rm *.o output