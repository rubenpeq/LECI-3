#include <iostream>
#include <pthread.h>

#include "hdp.h"

struct CounterData
{
	int counter;
	int maximum;
};

void *incrementCounter(void *argument)
{
	CounterData *data = static_cast<CounterData *>(argument);

	std::cout << "Enter N2 (10 to 20): ";
	while (!(std::cin >> data->maximum) || data->maximum < 10 || data->maximum > 20)
	{
		std::cout << "Invalid value. Enter N2 (10 to 20): ";
		std::cin.clear();
		std::cin.ignore(10000, '\n');
	}

	std::cout << "Child Thread: " << data->counter << ' ';

	while (data->counter < data->maximum)
	{
		std::cout << ++data->counter << ' ';
	}

	return NULL;
}

int main()
{
	CounterData data{};

	std::cout << "Enter N1 (1 to 9): ";
	while (!(std::cin >> data.counter) || data.counter < 1 || data.counter > 9)
	{
		std::cout << "Invalid value. Enter N1 (1 to 9): ";
		std::cin.clear();
		std::cin.ignore(10000, '\n');
	}

	pthread_t childThread;
	NZ(pthread_create(&childThread, NULL, incrementCounter, &data));
	NZ(pthread_join(childThread, NULL));

	std::cout << "\nMain Thread: ";

	while (data.counter > 1)
	{
		--data.counter;
		std::cout << data.counter << ' ';
	}
	std::cout << '\n';

	return 0;
}
