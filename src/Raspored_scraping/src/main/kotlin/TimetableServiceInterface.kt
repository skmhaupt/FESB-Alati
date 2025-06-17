
import NetworkServiceResult

interface TimetableServiceInterface {

    suspend fun fetchTimeTable(
        params: HashMap<String, String>
    ): NetworkServiceResult.TimeTableResult

}
