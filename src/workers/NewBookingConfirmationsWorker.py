from src.workers.Worker import Worker


class NewBookingConfirmationsWorker(Worker):
    @property
    def name(self):
        return "CreateCalendarFromConfirmedMonday"

    def find_candidates(self):
        # todo
        q = """
        SELECT * FROM monday.hr_tmp_booking mb 
        LEFT JOIN gsuite.events ge ON description ~* ('BREF:' || mb.bookingref)
        WHERE mb.status = 'booking' 
        """
        return [1, 2]

    def work(self, candidate):
        # todo save the event in the target calendar
        print(candidate)


if __name__ == "__main__":
    worker = NewBookingConfirmationsWorker()
    worker.do_all_work()
