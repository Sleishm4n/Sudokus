CC = gcc
CXX = g++
CFLAGS = -Wall -Wextra -std=c11 -O2
CXXFLAGS = -Wall -Wextra -std=c++17 -O2

%: %.c
	$(CC) $(CFLAGS) $< -o $@

%: %.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

clean:
	rm -f $(basename $(wildcard *.c *.cpp))