from src.workers.Worker import Worker


class CreateCalendarFromConfirmedMondayWorker(Worker):
    @property
    def name(self):
        return "CreateCalendarFromConfirmedMonday"

    def find_candidates(self):
        # todo
        q = """
        SELECT * FROM monday.bookings mb 
        LEFT JOIN gsuite.events ge ON description ~* ('BREF:' || mb.bookingref)
        WHERE mb.status = 'done' 
        """
        return [1, 2]

    def work(self, candidate):
        # todo save the event in the target calendar
        print(candidate)


if __name__ == "__main__":
    worker = CreateCalendarFromConfirmedMondayWorker()
    worker.do_all_work()
