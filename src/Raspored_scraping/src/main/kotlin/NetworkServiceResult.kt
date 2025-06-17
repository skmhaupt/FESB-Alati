
sealed class NetworkServiceResult {
    sealed class TimeTableResult: NetworkServiceResult(){
        data class Success(val data: String) : TimeTableResult()
        class Failure(val throwable: Throwable) : TimeTableResult()
    }
}
