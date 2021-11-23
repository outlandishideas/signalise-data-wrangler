from src.workers.Worker import Worker


class ExampleWorker(Worker):
    @property
    def name(self):
        return "CreateCalendarFromConfirmedMonday"

    def find_candidates(self):
        # todo

        return [{"a": 1}, {"b": 42}]

    def work(self, candidate):
        # todo save the event in the target calendar
        print(candidate)


if __name__ == "__main__":
    worker = ExampleWorker()
    worker.do_all_work()
