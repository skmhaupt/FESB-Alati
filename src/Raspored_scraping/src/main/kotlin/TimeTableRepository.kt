import java.time.LocalDate
import java.time.format.DateTimeFormatter


class TimeTableRepository(
    private val timetableService: TimetableServiceInterface
) : TimeTableRepositoryInterface {


    override suspend fun fetchTimetable(
        user: String,
        startDate: LocalDate,
        endDate: LocalDate
    ): List<Event> {
        val params: HashMap<String, String> = hashMapOf(
            "DataType" to "User",
            "DataId" to user,
            "MinDate" to startDate.format(DateTimeFormatter.ofPattern("MM-dd-yyyy")),
            "MaxDate" to endDate.format(DateTimeFormatter.ofPattern("MM-dd-yyyy"))
        )

        when (val result = timetableService.fetchTimeTable(params = params)) {
            is NetworkServiceResult.TimeTableResult.Success -> {
                val events = parseTimetable(result.data)
                return events
            }
            is NetworkServiceResult.TimeTableResult.Failure -> {
                throw Exception("Timetable fetching error")
            }
        }
    }

    companion object {
        private val TAG = this.javaClass.canonicalName
    }

}