import okhttp3.HttpUrl.Companion.toHttpUrl
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response

class TimetableService(private val client: OkHttpClient) : TimetableServiceInterface {

    private val baseURL = "https://raspored.fesb.unist.hr"

    override suspend fun fetchTimeTable(params: HashMap<String, String>): NetworkServiceResult.TimeTableResult {
        val endpointUrl  = "$baseURL/part/raspored/kalendar"
        val urlBuilder = endpointUrl
            .toHttpUrl()
            .newBuilder()

        for ((key, value) in params) {
            urlBuilder.addQueryParameter(key, value)
        }

        val request = Request.Builder()
            .url(urlBuilder.build())
            .build()

        val response: Response = client.newCall(request).execute()
        val value = response.body?.string()
        val success = response.isSuccessful

        response.close()

        if (!success || value.isNullOrEmpty()) {
            return NetworkServiceResult.TimeTableResult.Failure(Throwable("Failed to fetch schedule"))
        }

        return NetworkServiceResult.TimeTableResult.Success(value)
    }

}
