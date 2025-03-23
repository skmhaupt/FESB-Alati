import java.time.LocalDate

interface TimeTableRepositoryInterface {

    suspend fun fetchTimetable(user: String, startDate: LocalDate, endDate: LocalDate): List<Event>

}
