#include <iostream>
#include <pthread.h>

#include "hdp.h"

struct CounterData
{
	int counter;
	int turn;
	pthread_mutex_t mutex;
	pthread_cond_t condition;
};

struct ThreadData
{
	CounterData *counterData;
	int id;
};

void *decrementCounter(void *argument)
{
	ThreadData *threadData = static_cast<ThreadData *>(argument);
	CounterData *data = threadData->counterData;

	while (true)
	{
		NZ(pthread_mutex_lock(&data->mutex));

		while (data->counter > 1 && data->turn != threadData->id)
		{
			NZ(pthread_cond_wait(&data->condition, &data->mutex));
		}

		if (data->counter == 1)
		{
			NZ(pthread_cond_broadcast(&data->condition));
			NZ(pthread_mutex_unlock(&data->mutex));
			return NULL;
		}

		--data->counter;
		std::cout << "TID " << pthread_self() << ": " << data->counter << '\n';
		data->turn = 1 - threadData->id;

		NZ(pthread_cond_broadcast(&data->condition));
		NZ(pthread_mutex_unlock(&data->mutex));
	}
}

int main()
{
	CounterData data{};

	std::cout << "Enter counter value (10 to 20): ";
	while (!(std::cin >> data.counter) || data.counter < 10 || data.counter > 20)
	{
		std::cout << "Invalid value. Enter counter value (10 to 20): ";
		std::cin.clear();
		std::cin.ignore(10000, '\n');
	}

	data.turn = 0;
	NZ(pthread_mutex_init(&data.mutex, NULL));
	NZ(pthread_cond_init(&data.condition, NULL));

	pthread_t childThreads[2];
	ThreadData threadData[2] = {{&data, 0}, {&data, 1}};

	for (int i = 0; i < 2; ++i)
	{
		NZ(pthread_create(&childThreads[i], NULL, decrementCounter, &threadData[i]));
	}

	for (int i = 0; i < 2; ++i)
	{
		NZ(pthread_join(childThreads[i], NULL));
	}

	NZ(pthread_cond_destroy(&data.condition));
	NZ(pthread_mutex_destroy(&data.mutex));

	return 0;
}
