CXX = g++
CXXFLAGS = -Wall -ggdb -pthread -I../support
LDFLAGS = -L../support -lsupport -pthread -lm

TARGETS = fork1 fork2 fork3 fork4 child

.PHONY:	all clean cleanall

all: $(TARGETS)

$(TARGETS):	%: %.o 
		g++ -o $@ $^ $(LDFLAGS)

clean:
	rm -f *.o

cleanall:	clean
	rm -f $(TARGETS) 
